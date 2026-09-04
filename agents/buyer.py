"""
Hermes Buyer Agent
==================
The star of the show. This agent:
1. Parses natural language shopping requests
2. Discovers and queries multiple merchants
3. Negotiates deals with each merchant
4. Compares offers and picks the best combination
5. Executes payments through Razorpay
6. Handles failures gracefully
7. Produces a full audit trail
"""

import asyncio
import math
from datetime import datetime
from typing import Optional

from protocol.spec import (
    ProtocolMessage, MessageType, AgentRole,
    OrderSummary, TransactionReport
)
from merchants.sdk import MerchantAgent
from payments.razorpay_client import RazorpayPaymentClient
from agents.llm import (
    llm_reason, PARSE_REQUEST_PROMPT, NEGOTIATION_PROMPT,
    COMPARE_DEALS_PROMPT, FAILURE_ANALYSIS_PROMPT
)


class BuyerAgent:
    """
    AI-powered buyer agent that shops across multiple merchants.
    """
    
    def __init__(self):
        self.merchants: dict[str, MerchantAgent] = {}
        self.payment_client = RazorpayPaymentClient()
        self.event_log: list[dict] = []  # Full audit trail
        self.current_report: Optional[TransactionReport] = None
    
    def register_merchant(self, merchant: MerchantAgent):
        """Register a merchant that this buyer can transact with."""
        self.merchants[merchant.info.id] = merchant
        self._log("discovery", f"Registered merchant: {merchant.info.name} ({merchant.info.id})")
    
    def _log(self, event_type: str, message: str, data: dict = None):
        """Add an event to the audit trail."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "event": event_type,
            "message": message,
        }
        if data:
            entry["data"] = data
        self.event_log.append(entry)
    
    @staticmethod
    def _json_safe(value):
        """Recursively replace non-JSON-compliant floats (e.g. the budget=inf a chat
        checkout passes for "no hard cap") so protocol message payloads always serialize."""
        if isinstance(value, float) and not math.isfinite(value):
            return None
        if isinstance(value, dict):
            return {k: BuyerAgent._json_safe(v) for k, v in value.items()}
        if isinstance(value, list):
            return [BuyerAgent._json_safe(v) for v in value]
        return value

    @staticmethod
    def _summarize_negotiation_response(response: ProtocolMessage, current_offer: float) -> str:
        """Human-readable summary of a seller's negotiation response for the protocol
        feed. Prefers the seller's own "message" field — both the rule-based merchant
        and LLMMerchantAgent set this (the LLM seller's message_to_buyer lands here),
        so this is also how the seller's in-character reply surfaces in the UI."""
        p = response.payload
        if p.get("message"):
            return p["message"]
        if response.type == MessageType.NEGOTIATE_ACCEPT:
            return f"Accepted ₹{p.get('accepted_total', current_offer):,.0f}"
        if response.type == MessageType.NEGOTIATE_COUNTER:
            return f"Countered with ₹{p.get('counter_total', 0):,.0f}"
        if response.type == MessageType.NEGOTIATE_REJECT:
            return f"Rejected — {p.get('reason', 'terms not acceptable')}"
        return response.type.value

    @staticmethod
    def _log_protocol_message(log: list, sender: str, receiver: str, msg_type: str,
                               summary: str, details: dict) -> None:
        log.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "sender": sender,
            "receiver": receiver,
            "type": msg_type,
            "summary": summary,
            "details": BuyerAgent._json_safe(details),
        })

    async def process_request(self, user_request: str, callback=None) -> TransactionReport:
        """
        Main entry point. Takes a natural language request and handles everything.
        
        Args:
            user_request: Natural language shopping request
            callback: Optional async function called with (event_type, data) for live updates
        
        Returns:
            TransactionReport with full details
        """
        report = TransactionReport(user_request=user_request)
        self.current_report = report
        
        async def notify(event_type: str, data: dict):
            self._log(event_type, data.get("message", ""), data)
            if callback:
                await callback(event_type, data)
        
        # Step 1: Parse the request using AI
        await notify("parsing", {"message": f"Understanding your request: '{user_request}'"})
        
        parsed = await self._parse_request(user_request)
        if "error" in parsed:
            await notify("error", {"message": f"Failed to parse request: {parsed['error']}"})
            return report
        
        report.budget = parsed.get("budget", 0)
        await notify("parsed", {
            "message": f"Got it! Planning for {parsed.get('event_name', 'your event')} "
                       f"with budget ₹{report.budget:,.0f}",
            "parsed": parsed,
        })
        
        # Step 2: Discover merchants and get catalogs
        await notify("discovery", {
            "message": f"Checking {len(self.merchants)} merchants..."
        })
        
        requested_categories = [r.get("category") for r in parsed.get("requirements", []) if r.get("category")]
        wanted_categories = {c.lower() for c in requested_categories}

        merchant_catalogs = {}
        for mid, merchant in self.merchants.items():
            catalog_msg = merchant.handle_message(ProtocolMessage(
                type=MessageType.CATALOG_REQUEST,
                sender=AgentRole.BUYER,
                receiver=AgentRole.SELLER,
                merchant_id=mid,
                payload={}
            ))
            merchant_catalogs[mid] = {
                "name": merchant.info.name,
                "catalog": catalog_msg.payload,
                "summary": merchant.get_catalog_summary(categories=requested_categories, limit=15),
                "relevant": not wanted_categories or any(c.lower() in wanted_categories for c in merchant.info.categories),
            }
            report.merchants_contacted += 1

            await notify("catalog_received", {
                "message": f"Got catalog from {merchant.info.name} — "
                           f"{catalog_msg.payload['total_results']} products",
                "merchant": merchant.info.name,
                "products": catalog_msg.payload["total_results"],
            })

        # Step 3: Use AI to decide what to buy from whom.
        # Only send the LLM catalogs from merchants relevant to the parsed categories —
        # with hundreds of products per store across 6 merchants, including everyone
        # blows straight through Groq's per-minute token limit regardless of per-merchant caps.
        relevant_catalogs = {mid: c for mid, c in merchant_catalogs.items() if c["relevant"]}
        catalogs_for_llm = relevant_catalogs if relevant_catalogs else merchant_catalogs

        await notify("analyzing", {
            "message": f"Comparing options across {len(catalogs_for_llm)} relevant merchant(s)..."
        })

        shopping_plan = await self._plan_shopping(parsed, catalogs_for_llm)
        
        if "error" in shopping_plan:
            await notify("error", {"message": f"Planning failed: {shopping_plan['error']}"})
            return report
        
        # Step 4: Negotiate with each merchant
        negotiations_results = {}
        for order_plan in shopping_plan.get("selected_orders", []):
            merchant_id = order_plan["merchant_id"]
            merchant_name = order_plan["merchant_name"]
            merchant = self.merchants.get(merchant_id)
            
            if not merchant:
                await notify("error", {"message": f"Merchant {merchant_name} not found"})
                continue
            
            await notify("negotiating", {
                "message": f"Negotiating with {merchant_name}...",
                "merchant": merchant_name,
            })
            
            neg_result = await self.negotiate_with_merchant(
                merchant, order_plan, parsed.get("budget", 0), notify
            )
            negotiations_results[merchant_id] = neg_result
            report.negotiations_completed += 1
        
        # Step 5: Process payments for accepted deals
        for merchant_id, neg_result in negotiations_results.items():
            if neg_result["status"] != "accepted":
                await notify("skipped", {
                    "message": f"Skipping {neg_result['merchant_name']} — negotiation {neg_result['status']}",
                })
                continue
            
            merchant_name = neg_result["merchant_name"]
            amount = neg_result["final_amount"]
            items = neg_result["items"]
            
            await notify("payment_processing", {
                "message": f"Processing payment of ₹{amount:,.0f} to {merchant_name}...",
                "merchant": merchant_name,
                "amount": amount,
            })
            
            items_summary = ", ".join(
                f"{it.get('name', it.get('product_id'))} x{it['quantity']}" 
                for it in items
            )
            
            payment_result = await self.payment_client.create_order_with_retry(
                amount=amount,
                merchant_name=merchant_name,
                items_summary=items_summary,
            )
            
            # Build order summary
            order = OrderSummary(
                order_id=payment_result.order_id or f"FAILED_{merchant_id}",
                merchant_id=merchant_id,
                merchant_name=merchant_name,
                items=items,
                subtotal=neg_result.get("original_total", amount),
                discount_applied=neg_result.get("savings", 0),
                final_amount=amount,
                razorpay_order_id=payment_result.order_id,
                razorpay_payment_id=payment_result.payment_id,
                payment_status="success" if payment_result.success else "failed",
                negotiation_rounds=neg_result.get("rounds", 0),
                negotiation_savings=neg_result.get("savings", 0),
            )
            
            order.add_audit("order_created", f"Order placed with {merchant_name}")
            order.add_audit("payment_attempted", 
                          f"Payment {'succeeded' if payment_result.success else 'failed'} "
                          f"after {payment_result.attempts} attempt(s)")
            
            if payment_result.success:
                await notify("payment_success", {
                    "message": f"✓ Paid ₹{amount:,.0f} to {merchant_name} "
                               f"(Order: {payment_result.order_id})",
                    "order_id": payment_result.order_id,
                    "merchant": merchant_name,
                    "amount": amount,
                })
            else:
                # Handle payment failure
                await notify("payment_failed", {
                    "message": f"✗ Payment to {merchant_name} failed: {payment_result.error}",
                    "merchant": merchant_name,
                    "error": payment_result.error,
                })
                
                failure_analysis = await self._handle_failure(
                    "payment", merchant_name, payment_result.error
                )
                report.failures.append({
                    "type": "payment",
                    "merchant": merchant_name,
                    "error": payment_result.error,
                    "recovery": failure_analysis,
                })
                
                order.add_audit("failure_handled", 
                              f"Recovery action: {failure_analysis.get('recovery_action', 'none')}")
            
            report.orders.append(order)
        
        # Step 6: Finalize report
        report.finalize()
        report.total_saved = sum(o.negotiation_savings for o in report.orders)
        
        await notify("complete", {
            "message": f"Done! Spent ₹{report.total_spent:,.0f} of ₹{report.budget:,.0f} budget. "
                       f"Saved ₹{report.total_saved:,.0f} through negotiation.",
            "report": {
                "total_spent": report.total_spent,
                "budget_remaining": report.budget_remaining,
                "total_saved": report.total_saved,
                "orders": report.payments_successful,
                "failures": report.payments_failed,
            }
        })
        
        return report
    
    async def _parse_request(self, request: str) -> dict:
        """Use AI to parse natural language request into structured requirements."""
        try:
            return await llm_reason(PARSE_REQUEST_PROMPT, request)
        except Exception as e:
            self._log("error", f"LLM parsing failed: {e}")
            return {"error": str(e)}
    
    async def _plan_shopping(self, requirements: dict, catalogs: dict) -> dict:
        """Use AI to decide what to buy from which merchant."""
        context = f"""
Budget: ₹{requirements.get('budget', 0):,.0f}
Event: {requirements.get('event_name', 'Event')} for {requirements.get('event_size', 'unknown')} people

Requirements:
{self._format_requirements(requirements.get('requirements', []))}

Available Merchants:
{self._format_catalogs(catalogs)}
"""
        try:
            return await llm_reason(COMPARE_DEALS_PROMPT, context)
        except Exception as e:
            self._log("error", f"LLM planning failed: {e}")
            return {"error": str(e)}
    
    async def negotiate_with_merchant(self, merchant: MerchantAgent, order_plan: dict,
                                        budget: float, notify, protocol_log: Optional[list] = None) -> dict:
        """Run negotiation rounds with a merchant.

        If protocol_log is given, the real ProtocolMessage exchanged each round
        (buyer's offer and the merchant's response) is recorded into it as
        {timestamp, sender, receiver, type, summary, details} — used to drive the
        agent-network visualization in the dashboard.
        """
        items = order_plan.get("items", [])
        merchant_name = order_plan["merchant_name"]
        
        # Calculate original total from catalog prices
        original_total = 0
        for item in items:
            product = merchant.products.get(item["product_id"])
            if product:
                original_total += product.get_total_for_quantity(item["quantity"])
        
        # Start negotiation: offer 15% below catalog price
        current_offer = round(original_total * 0.85, 2)
        
        for round_num in range(1, 4):  # Max 3 rounds
            # Send offer to merchant
            offer_msg = ProtocolMessage(
                type=MessageType.NEGOTIATE_OFFER,
                sender=AgentRole.BUYER,
                receiver=AgentRole.SELLER,
                merchant_id=merchant.info.id,
                payload={
                    "items": items,
                    "offered_total": current_offer,
                    "budget": budget,
                }
            )
            
            response = await merchant.handle_message_async(offer_msg)

            if protocol_log is not None:
                self._log_protocol_message(protocol_log, "Buyer Agent", merchant_name,
                    offer_msg.type.value,
                    f"Offering ₹{current_offer:,.0f} for {sum(i['quantity'] for i in items)} unit(s)",
                    offer_msg.payload)

                self._log_protocol_message(protocol_log, merchant_name, "Buyer Agent",
                    response.type.value, self._summarize_negotiation_response(response, current_offer),
                    response.payload)

            await notify("negotiation_round", {
                "message": f"Round {round_num} with {merchant_name}: "
                           f"Offered ₹{current_offer:,.0f}",
                "round": round_num,
                "merchant": merchant_name,
                "offer": current_offer,
                "response_type": response.type.value,
            })
            
            if response.type == MessageType.NEGOTIATE_ACCEPT:
                accepted_total = response.payload.get("accepted_total", current_offer)
                savings = round(original_total - accepted_total, 2)
                
                await notify("negotiation_accepted", {
                    "message": f"Deal! {merchant_name} accepted ₹{accepted_total:,.0f} "
                               f"(saved ₹{savings:,.0f})",
                    "merchant": merchant_name,
                    "accepted": accepted_total,
                    "savings": savings,
                })
                
                return {
                    "status": "accepted",
                    "merchant_name": merchant_name,
                    "final_amount": accepted_total,
                    "original_total": original_total,
                    "savings": savings,
                    "rounds": round_num,
                    "items": items,
                }
            
            elif response.type == MessageType.NEGOTIATE_COUNTER:
                counter = response.payload.get("counter_total", original_total)
                # Meet closer to their counter (buyer concedes a bit)
                current_offer = round((current_offer + counter) / 2, 2)
                
                await notify("negotiation_counter", {
                    "message": f"{merchant_name} countered with ₹{counter:,.0f}. "
                               f"Adjusting to ₹{current_offer:,.0f}...",
                    "counter": counter,
                    "new_offer": current_offer,
                })
            
            elif response.type == MessageType.NEGOTIATE_REJECT:
                await notify("negotiation_rejected", {
                    "message": f"{merchant_name} rejected negotiation. "
                               f"Using catalog price ₹{original_total:,.0f}",
                })
                return {
                    "status": "accepted",  # Accept at catalog price
                    "merchant_name": merchant_name,
                    "final_amount": original_total,
                    "original_total": original_total,
                    "savings": 0,
                    "rounds": round_num,
                    "items": items,
                }
        
        # Max rounds reached, accept last offer
        return {
            "status": "accepted",
            "merchant_name": merchant_name,
            "final_amount": current_offer,
            "original_total": original_total,
            "savings": round(original_total - current_offer, 2),
            "rounds": 3,
            "items": items,
        }
    
    async def _handle_failure(self, failure_type: str, context: str, error: str) -> dict:
        """Use AI to analyze a failure and suggest recovery."""
        try:
            return await llm_reason(
                FAILURE_ANALYSIS_PROMPT,
                f"Failure type: {failure_type}\nContext: {context}\nError: {error}"
            )
        except Exception:
            return {
                "failure_type": failure_type,
                "recovery_action": "retry",
                "details": error,
                "recovery_plan": "Automatic retry with exponential backoff",
            }
    
    def _format_requirements(self, requirements: list) -> str:
        lines = []
        for req in requirements:
            lines.append(
                f"- {req.get('description', 'Unknown')} "
                f"(category: {req.get('category', 'any')}, "
                f"qty: {req.get('estimated_quantity', '?')})"
            )
        return "\n".join(lines) if lines else "No specific requirements"
    
    def _format_catalogs(self, catalogs: dict) -> str:
        lines = []
        for mid, data in catalogs.items():
            lines.append(f"\n--- {data['name']} (ID: {mid}) ---")
            lines.append(data["summary"])
        return "\n".join(lines)
    
    def get_audit_trail(self) -> list:
        """Get the complete audit trail for this session."""
        return self.event_log.copy()
    
    def get_metrics(self) -> dict:
        """Get performance metrics for the current session."""
        if not self.current_report:
            return {"status": "no active session"}
        
        r = self.current_report
        payment_summary = self.payment_client.get_payment_summary()
        
        return {
            "session_id": r.session_id,
            "merchants_contacted": r.merchants_contacted,
            "negotiations_completed": r.negotiations_completed,
            "orders_placed": len(r.orders),
            "payments_successful": r.payments_successful,
            "payments_failed": r.payments_failed,
            "total_spent": r.total_spent,
            "budget": r.budget,
            "budget_remaining": r.budget_remaining,
            "total_saved_negotiation": r.total_saved,
            "savings_percentage": f"{(r.total_saved / r.total_spent * 100):.1f}%" if r.total_spent else "0%",
            "payment_details": payment_summary,
            "failures_encountered": len(r.failures),
            "audit_trail_entries": len(self.event_log),
        }
