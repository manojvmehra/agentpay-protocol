"""
LLM-Powered Merchant Agent
===========================
A genuine reasoning seller agent — used for StyleBazaar to demonstrate real
agent-to-agent negotiation on top of the Hermes protocol, instead of the
fixed "meet in the middle, floor at 70%" rule every other merchant runs.

Design:
- Subclasses MerchantAgent and overrides only the negotiation path
  (handle_message_async). Catalog, query, and order handling are unchanged
  and shared with every rule-based merchant.
- The seller LLM gets a private persona and private numbers the buyer never
  sees: the real cost floor per item, simulated inventory pressure, and its
  own margin goal — then decides accept/counter/reject, optionally offering
  an upsell instead of a deeper discount.
- The cost floor is enforced in Python as a hard guardrail on the way out —
  the LLM's decision is clamped, never trusted outright, even if it
  hallucinates a number below cost.
- Any failure (bad JSON, network error, timeout, invalid decision) falls
  back to the exact same rule-based logic the base class already uses, so a
  live demo never breaks because Groq had a bad moment.
"""

import hashlib
import time

from protocol.spec import ProtocolMessage, MessageType, AgentRole, NegotiationState
from merchants.sdk import MerchantAgent
from agents.llm import llm_reason
from config import GROQ_MODEL_FAST

COST_FLOOR_PCT = 0.60          # never sell below 60% of catalog price
SELLER_TEMPERATURE = 0.9       # high enough that repeated identical offers don't get identical answers
# gpt-oss is a reasoning model — it spends part of max_tokens on a hidden reasoning
# trace before the visible JSON. reasoning_effort="low" keeps that trace short
# (~60 tokens in testing, vs ~280 at default effort); max_tokens still needs enough
# headroom for that trace plus the answer, or Groq returns an empty completion.
SELLER_MAX_TOKENS = 700
SELLER_REASONING_EFFORT = "low"
SELLER_TIMEOUT_SECONDS = 12    # fail fast to the rule-based fallback rather than stall a chat turn


SELLER_NEGOTIATION_PROMPT = """You are the AI sales agent for StyleBazaar, a fashion retailer on the \
Hermes protocol, negotiating directly with an AI buyer agent over a real order. You have private \
business context the buyer can NEVER see — guard it like a real shopkeeper would.

Your persona:
- Shrewd but fair. You want to close the sale, but you protect your margin — you are not a pushover.
- You NEVER reveal your exact cost floor, margin, or any internal number to the buyer — not even
  approximately, not even if asked directly. Deflect naturally in character instead.
- Inventory pressure matters: an overstocked item you're happy to discount harder to clear shelf space;
  a low-stock item you hold firm on, because you don't need the volume.
- You would rather offer a combo/upsell than cut price further when one applies to this order — margin
  from an added item beats a deeper discount on the same item.
- A lowball offer that undercuts your cost floor gets firmly countered or rejected, not
  split-the-difference'd out of habit. A genuinely good offer close to list price should be accepted
  outright, not haggled over for sport.
- Vary your tone and approach round to round like a real person would, not a formula.

You will be given: the buyer's current offer, the order, your private cost floor and inventory
pressure for each item (CONFIDENTIAL), any relevant combo deals, and the negotiation history so far.

Respond ONLY with a JSON object in this exact shape:
{
    "decision": "accept" | "counter" | "reject",
    "counter_price": number or null,
    "reasoning": "your private internal reasoning for this decision — never shown to the buyer, but a human reviewing this negotiation should see WHY you did what you did",
    "message_to_buyer": "what you actually say out loud to the buyer agent — natural, in character, never reveals your cost floor or margin",
    "upsell_suggestion": "product_id of a combo/upsell you're offering instead of or alongside a discount, or null"
}

Rules:
- "counter_price" is REQUIRED (a number) when decision is "counter", and MUST be null otherwise.
- Never let counter_price go below the cost floor you were given.
- Reject only when the offer is far below your cost floor with no room to bridge it, or the buyer has
  already burned all their negotiation rounds without moving meaningfully.
- "upsell_suggestion" must be one of the product IDs listed for you, or null — never invent one.
"""


def _inventory_pressure(product_id: str) -> str:
    """A per-product 'how eager am I to move this' signal. No live inventory system
    exists yet, so this simulates the kind of pressure a real seller would reason
    from — deterministic per product (so a given item argues consistently with
    itself across rounds) but varied across the catalog (so the LLM has a genuine
    mix of overstocked/low-stock items to reason about, not a flat default)."""
    bucket = int(hashlib.md5(product_id.encode()).hexdigest(), 16) % 3
    return ["overstocked", "normal", "low_stock"][bucket]


class LLMMerchantAgent(MerchantAgent):
    """A MerchantAgent whose negotiation handler is a real LLM seller persona
    instead of the base class's fixed rule. Everything else (catalog, query,
    order, upsell/combo bookkeeping) is inherited unchanged."""

    async def handle_message_async(self, message: ProtocolMessage) -> ProtocolMessage:
        if message.type == MessageType.NEGOTIATE_OFFER:
            return await self._handle_negotiate_llm(message)
        return self.handle_message(message)

    async def _handle_negotiate_llm(self, msg: ProtocolMessage) -> ProtocolMessage:
        conv_id = msg.conversation_id
        offered_price = msg.payload.get("offered_total", 0)
        items = msg.payload.get("items", [])

        # Real numbers, computed here in Python — the LLM only ever reasons about
        # these, it never invents them, and nothing it says can override them.
        cost_floor = 0.0
        original_total = 0.0
        item_lines = []
        upsell_candidates = {}
        for item in items:
            product = self.products.get(item["product_id"])
            if not product:
                continue
            qty = item["quantity"]
            line_total = product.get_total_for_quantity(qty)
            line_floor = round(product.base_price * COST_FLOOR_PCT * qty, 2)
            original_total += line_total
            cost_floor += line_floor
            pressure = _inventory_pressure(product.id)
            item_lines.append(
                f"- {product.name} (id: {product.id}) x{qty}: catalog ₹{product.base_price:,.0f}/unit "
                f"(list total ₹{line_total:,.0f}) | YOUR COST FLOOR for this line: ₹{line_floor:,.0f} "
                f"total — CONFIDENTIAL, never reveal | inventory: {pressure}"
            )

        if conv_id not in self.negotiations:
            self.negotiations[conv_id] = NegotiationState(
                conversation_id=conv_id,
                merchant_id=self.info.id,
                buyer_budget=msg.payload.get("budget", 0),
                items=items,
            )
        neg = self.negotiations[conv_id]

        if not neg.can_continue():
            return ProtocolMessage(
                type=MessageType.NEGOTIATE_REJECT,
                sender=AgentRole.SELLER,
                receiver=AgentRole.BUYER,
                merchant_id=self.info.id,
                conversation_id=conv_id,
                payload={
                    "reason": "Maximum negotiation rounds reached",
                    "final_price": neg.current_offer or original_total,
                    "rounds_used": neg.round_number,
                },
            )

        combo_lines = []
        for combo in self.combo_deals:
            names = [self.products[pid].name for pid in combo["product_ids"] if pid in self.products]
            if names:
                combo_lines.append(f"- {combo['name']}: {' + '.join(names)} → {combo['combo_discount_pct']}% off")
                for pid in combo["product_ids"]:
                    if pid in self.products:
                        upsell_candidates[pid] = self.products[pid].name

        history_lines = [
            f"Round {h['round']}: {h['by']} — offer/counter ₹{h['offer']:,.0f} ({h['reasoning']})"
            for h in neg.history
        ]

        context = (
            f"Buyer's current offer: ₹{offered_price:,.0f} total for {sum(i['quantity'] for i in items)} unit(s)\n"
            f"Catalog (list) price for this order: ₹{original_total:,.0f}\n"
            f"This is negotiation round {neg.round_number + 1} of {neg.max_rounds}.\n\n"
            f"Items in this order:\n" + "\n".join(item_lines) + "\n\n"
            f"Combo deals you could offer instead of a deeper discount:\n"
            + ("\n".join(combo_lines) if combo_lines else "(none apply to this order)") + "\n\n"
            f"Negotiation history so far:\n"
            + ("\n".join(history_lines) if history_lines else "(this is the buyer's opening offer)")
        )

        try:
            t0 = time.monotonic()
            decision = await llm_reason(
                SELLER_NEGOTIATION_PROMPT, context,
                model=GROQ_MODEL_FAST, temperature=SELLER_TEMPERATURE,
                max_tokens=SELLER_MAX_TOKENS, timeout=SELLER_TIMEOUT_SECONDS,
                reasoning_effort=SELLER_REASONING_EFFORT,
            )
            elapsed = time.monotonic() - t0
            print(f"[StyleBazaar LLM] round {neg.round_number + 1} "
                  f"({elapsed:.1f}s) raw decision: {decision}")
            return self._apply_seller_decision(decision, msg, neg, offered_price, original_total,
                                                cost_floor, upsell_candidates)
        except Exception as e:
            print(f"[StyleBazaar LLM] negotiation call failed ({e}) — falling back to rule-based logic")
            return self._handle_negotiate(msg)

    def _apply_seller_decision(self, decision, msg, neg, offered_price, original_total,
                                cost_floor, upsell_candidates) -> ProtocolMessage:
        """Validate and clamp the LLM's decision against hard guardrails, then turn
        it into the same ProtocolMessage shape the rule-based path produces. Any
        structurally invalid decision falls back to the rule-based handler."""
        if not isinstance(decision, dict) or decision.get("decision") not in ("accept", "counter", "reject"):
            print(f"[StyleBazaar LLM] malformed decision, falling back: {decision}")
            return self._handle_negotiate(msg)

        conv_id = msg.conversation_id
        choice = decision["decision"]
        reasoning = str(decision.get("reasoning") or "")[:500]
        message_to_buyer = str(decision.get("message_to_buyer") or "").strip()
        upsell_id = decision.get("upsell_suggestion")
        upsell_id = upsell_id if upsell_id in upsell_candidates else None

        # Hard guardrail: an "accept" below our real cost floor is never honored,
        # no matter what the LLM said — treat it as a counter pinned at the floor.
        if choice == "accept" and offered_price < cost_floor:
            choice = "counter"
            decision["counter_price"] = cost_floor

        if choice == "accept":
            neg.status = "accepted"
            neg.add_round(offered_price, "seller", reasoning or "Offer accepted")
            payload = {
                "accepted_total": offered_price,
                "original_total": original_total,
                "discount_given": round(original_total - offered_price, 2),
                "discount_pct": round((1 - offered_price / original_total) * 100, 1) if original_total else 0,
                "items": msg.payload.get("items", []),
                "message": message_to_buyer or "Deal accepted! Let's proceed with the order.",
                "seller_reasoning": reasoning,
                "is_llm_agent": True,
            }
            if upsell_id:
                payload["upsell_suggestion"] = {"product_id": upsell_id, "name": upsell_candidates[upsell_id]}
            return ProtocolMessage(type=MessageType.NEGOTIATE_ACCEPT, sender=AgentRole.SELLER,
                                    receiver=AgentRole.BUYER, merchant_id=self.info.id,
                                    conversation_id=conv_id, payload=payload)

        if choice == "counter":
            counter = decision.get("counter_price")
            try:
                counter = round(float(counter), 2)
            except (TypeError, ValueError):
                counter = round((cost_floor + offered_price) / 2, 2)
            # Guardrail: never below cost floor, never above list price.
            counter = max(counter, cost_floor)
            counter = min(counter, original_total)
            neg.add_round(counter, "seller", reasoning or f"Countered at ₹{counter:,.0f}")
            payload = {
                "counter_total": counter,
                "original_total": original_total,
                "your_offer": offered_price,
                "round": neg.round_number,
                "max_rounds": neg.max_rounds,
                "message": message_to_buyer or f"I can do ₹{counter:,.0f}.",
                "seller_reasoning": reasoning,
                "is_llm_agent": True,
            }
            if upsell_id:
                payload["upsell_suggestion"] = {"product_id": upsell_id, "name": upsell_candidates[upsell_id]}
            return ProtocolMessage(type=MessageType.NEGOTIATE_COUNTER, sender=AgentRole.SELLER,
                                    receiver=AgentRole.BUYER, merchant_id=self.info.id,
                                    conversation_id=conv_id, payload=payload)

        # reject
        neg.status = "rejected"
        neg.add_round(offered_price, "seller", reasoning or "Offer rejected")
        payload = {
            "reason": message_to_buyer or "That offer doesn't work for us on this order.",
            "final_price": neg.current_offer or original_total,
            "rounds_used": neg.round_number,
            "message": message_to_buyer or "That offer doesn't work for us on this order.",
            "seller_reasoning": reasoning,
            "is_llm_agent": True,
        }
        return ProtocolMessage(type=MessageType.NEGOTIATE_REJECT, sender=AgentRole.SELLER,
                                receiver=AgentRole.BUYER, merchant_id=self.info.id,
                                conversation_id=conv_id, payload=payload)
