"""
AgentPay Merchant SDK
=====================
Make any store AI-transactable in 5 lines of code.

Usage:
    from merchants.sdk import MerchantAgent
    
    agent = MerchantAgent(
        name="FestKart",
        description="College fest merch & apparel",
        categories=["apparel", "accessories"],
    )
    agent.add_product(Product(...))
    agent.start()  # Now AI buyers can transact with this merchant
"""

from protocol.spec import (
    Product, MerchantInfo, ProtocolMessage, MessageType,
    AgentRole, NegotiationState
)
from typing import Optional
import uuid


class MerchantAgent:
    """
    A merchant's AI agent that handles:
    - Responding to catalog queries
    - Answering product questions
    - Negotiating prices with buyer agents
    - Creating orders and initiating payments
    - Upselling and cross-selling
    """
    
    def __init__(self, name: str, description: str, categories: list, location: str = "Bengaluru"):
        self.info = MerchantInfo(
            id=f"merchant_{uuid.uuid4().hex[:8]}",
            name=name,
            description=description,
            categories=categories,
            location=location,
        )
        self.products: dict[str, Product] = {}
        self.negotiations: dict[str, NegotiationState] = {}
        self.upsell_rules: list[dict] = []
        self.combo_deals: list[dict] = []
        
    def add_product(self, product: Product):
        """Add a product to the catalog."""
        self.products[product.id] = product
        
    def add_upsell_rule(self, trigger_product_id: str, suggest_product_id: str, discount_pct: float = 5):
        """When buyer orders trigger_product, suggest suggest_product at a discount."""
        self.upsell_rules.append({
            "trigger": trigger_product_id,
            "suggest": suggest_product_id,
            "discount_pct": discount_pct
        })
    
    def add_combo_deal(self, name: str, product_ids: list, combo_discount_pct: float):
        """Create a combo deal for multiple products bought together."""
        self.combo_deals.append({
            "name": name,
            "product_ids": product_ids,
            "combo_discount_pct": combo_discount_pct
        })
    
    def handle_message(self, message: ProtocolMessage) -> ProtocolMessage:
        """Process an incoming protocol message and return a response."""
        handlers = {
            MessageType.DISCOVER_REQUEST: self._handle_discover,
            MessageType.CATALOG_REQUEST: self._handle_catalog,
            MessageType.QUERY: self._handle_query,
            MessageType.NEGOTIATE_OFFER: self._handle_negotiate,
            MessageType.ORDER_CREATE: self._handle_order,
        }
        
        handler = handlers.get(message.type, self._handle_unknown)
        return handler(message)
    
    def _handle_discover(self, msg: ProtocolMessage) -> ProtocolMessage:
        """Respond to merchant discovery requests."""
        return ProtocolMessage(
            type=MessageType.DISCOVER_RESPONSE,
            sender=AgentRole.SELLER,
            receiver=AgentRole.BUYER,
            merchant_id=self.info.id,
            conversation_id=msg.conversation_id,
            payload={
                "merchant": {
                    "id": self.info.id,
                    "name": self.info.name,
                    "description": self.info.description,
                    "categories": self.info.categories,
                    "location": self.info.location,
                    "total_products": len(self.products),
                    "supports_negotiation": self.info.supports_negotiation,
                }
            }
        )
    
    def _handle_catalog(self, msg: ProtocolMessage) -> ProtocolMessage:
        """Return the full or filtered product catalog."""
        category_filter = msg.payload.get("category")
        budget_max = msg.payload.get("max_price")
        query = msg.payload.get("query", "").lower()
        
        products = list(self.products.values())
        
        if category_filter:
            products = [p for p in products if p.category == category_filter]
        if budget_max:
            products = [p for p in products if p.base_price <= budget_max]
        if query:
            products = [p for p in products if 
                       query in p.name.lower() or 
                       query in p.description.lower() or
                       query in p.category.lower()]
        
        catalog_data = []
        for p in products:
            catalog_data.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "category": p.category,
                "base_price": p.base_price,
                "unit": p.unit,
                "min_order": p.min_order,
                "in_stock": p.in_stock,
                "bulk_discounts": p.bulk_discount_rules,
                "image_url": p.image_url,
            })
        
        # Include combo deals if applicable
        applicable_combos = []
        for combo in self.combo_deals:
            combo_products = [self.products[pid] for pid in combo["product_ids"] if pid in self.products]
            if combo_products:
                applicable_combos.append({
                    "name": combo["name"],
                    "products": [p.name for p in combo_products],
                    "discount_pct": combo["combo_discount_pct"]
                })
        
        return ProtocolMessage(
            type=MessageType.CATALOG_RESPONSE,
            sender=AgentRole.SELLER,
            receiver=AgentRole.BUYER,
            merchant_id=self.info.id,
            conversation_id=msg.conversation_id,
            payload={
                "products": catalog_data,
                "combo_deals": applicable_combos,
                "total_results": len(catalog_data),
            }
        )
    
    def _handle_query(self, msg: ProtocolMessage) -> ProtocolMessage:
        """Answer specific questions about products."""
        product_id = msg.payload.get("product_id")
        quantity = msg.payload.get("quantity", 1)
        
        if product_id and product_id in self.products:
            product = self.products[product_id]
            unit_price = product.get_price_for_quantity(quantity)
            total = product.get_total_for_quantity(quantity)
            
            # Check for upsell opportunities
            upsell_suggestions = []
            for rule in self.upsell_rules:
                if rule["trigger"] == product_id and rule["suggest"] in self.products:
                    suggested = self.products[rule["suggest"]]
                    upsell_suggestions.append({
                        "product": suggested.name,
                        "product_id": suggested.id,
                        "price": suggested.base_price,
                        "discount_if_bundled": rule["discount_pct"],
                        "message": f"Add {suggested.name} and get {rule['discount_pct']}% off!"
                    })
            
            response_payload = {
                "product_id": product_id,
                "name": product.name,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": total,
                "in_stock": product.in_stock,
                "bulk_discount_applied": unit_price < product.base_price,
                "savings": round((product.base_price - unit_price) * quantity, 2),
            }
            
            if upsell_suggestions:
                response_payload["upsell_suggestions"] = upsell_suggestions
            
            return ProtocolMessage(
                type=MessageType.QUERY_RESPONSE,
                sender=AgentRole.SELLER,
                receiver=AgentRole.BUYER,
                merchant_id=self.info.id,
                conversation_id=msg.conversation_id,
                payload=response_payload,
            )
        
        return ProtocolMessage(
            type=MessageType.ERROR,
            sender=AgentRole.SELLER,
            receiver=AgentRole.BUYER,
            merchant_id=self.info.id,
            conversation_id=msg.conversation_id,
            payload={"error": f"Product '{product_id}' not found in catalog."}
        )
    
    def _handle_negotiate(self, msg: ProtocolMessage) -> ProtocolMessage:
        """Handle price negotiation from buyer."""
        conv_id = msg.conversation_id
        offered_price = msg.payload.get("offered_total")
        items = msg.payload.get("items", [])
        
        # Calculate our minimum acceptable price (cost + 5% margin)
        min_acceptable = 0
        original_total = 0
        for item in items:
            product = self.products.get(item["product_id"])
            if product:
                qty = item["quantity"]
                original_total += product.get_total_for_quantity(qty)
                # Minimum is 70% of base price (30% max discount)
                min_acceptable += product.base_price * 0.70 * qty
        
        # Initialize or get negotiation state
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
                }
            )
        
        if offered_price >= min_acceptable:
            # Accept the offer
            neg.status = "accepted"
            neg.add_round(offered_price, "seller", "Price is within acceptable range")
            
            return ProtocolMessage(
                type=MessageType.NEGOTIATE_ACCEPT,
                sender=AgentRole.SELLER,
                receiver=AgentRole.BUYER,
                merchant_id=self.info.id,
                conversation_id=conv_id,
                payload={
                    "accepted_total": offered_price,
                    "original_total": original_total,
                    "discount_given": round(original_total - offered_price, 2),
                    "discount_pct": round((1 - offered_price / original_total) * 100, 1),
                    "items": items,
                    "message": "Deal accepted! Let's proceed with the order.",
                }
            )
        else:
            # Counter offer - meet halfway between our minimum and their offer
            counter = round((min_acceptable + offered_price) / 2, 2)
            if counter < min_acceptable:
                counter = min_acceptable
            
            neg.add_round(counter, "seller", f"Counter offer - original was ₹{original_total}")
            
            return ProtocolMessage(
                type=MessageType.NEGOTIATE_COUNTER,
                sender=AgentRole.SELLER,
                receiver=AgentRole.BUYER,
                merchant_id=self.info.id,
                conversation_id=conv_id,
                payload={
                    "counter_total": counter,
                    "original_total": original_total,
                    "your_offer": offered_price,
                    "round": neg.round_number,
                    "max_rounds": neg.max_rounds,
                    "message": f"I can do ₹{counter:,.0f}. That's already a {round((1 - counter/original_total)*100, 1)}% discount.",
                }
            )
    
    def _handle_order(self, msg: ProtocolMessage) -> ProtocolMessage:
        """Create an order after negotiation is accepted."""
        items = msg.payload.get("items", [])
        agreed_total = msg.payload.get("agreed_total", 0)
        
        order_items = []
        for item in items:
            product = self.products.get(item["product_id"])
            if product:
                qty = item["quantity"]
                order_items.append({
                    "product_id": product.id,
                    "name": product.name,
                    "quantity": qty,
                    "unit_price": item.get("unit_price", product.get_price_for_quantity(qty)),
                    "total": item.get("total", product.get_total_for_quantity(qty)),
                })
        
        return ProtocolMessage(
            type=MessageType.ORDER_CONFIRM,
            sender=AgentRole.SELLER,
            receiver=AgentRole.BUYER,
            merchant_id=self.info.id,
            conversation_id=msg.conversation_id,
            payload={
                "order_id": f"ORD_{uuid.uuid4().hex[:8].upper()}",
                "merchant_name": self.info.name,
                "items": order_items,
                "total_amount": agreed_total,
                "status": "confirmed",
                "message": f"Order confirmed by {self.info.name}! Ready for payment.",
                "requires_payment": True,
            }
        )
    
    def _handle_unknown(self, msg: ProtocolMessage) -> ProtocolMessage:
        return ProtocolMessage(
            type=MessageType.ERROR,
            sender=AgentRole.SELLER,
            receiver=AgentRole.BUYER,
            merchant_id=self.info.id,
            conversation_id=msg.conversation_id,
            payload={"error": f"Unknown message type: {msg.type}"}
        )
    
    def get_catalog_summary(self, categories: Optional[list] = None, limit: int = 20) -> str:
        """
        Get a human-readable catalog summary for the LLM.

        With hundreds of products per merchant, dumping the full catalog into
        an LLM prompt blows past token/rate limits. So this filters to the
        requested categories (if given) and caps the number of lines,
        cheapest-first, noting how many were omitted.
        """
        lines = [f"=== {self.info.name} ===", f"{self.info.description}", ""]
        lines.append("Products:")

        products = list(self.products.values())
        if categories:
            wanted = {c.lower() for c in categories}
            filtered = [p for p in products if p.category.lower() in wanted]
            # Fall back to the full catalog if none of the requested categories match
            products = filtered if filtered else products

        products.sort(key=lambda p: p.base_price)
        shown = products[:limit]
        remaining = len(products) - len(shown)

        for p in shown:
            discount_info = ""
            if p.bulk_discount_rules:
                discounts = [f"{r['min_qty']}+ units: {r['discount_pct']}% off" for r in p.bulk_discount_rules]
                discount_info = f" | Bulk discounts: {', '.join(discounts)}"
            lines.append(f"  - {p.name} (ID: {p.id}): ₹{p.base_price}/{p.unit}{discount_info}")

        if remaining > 0:
            lines.append(f"  ...and {remaining} more product(s) available in this store.")

        if self.combo_deals:
            lines.append("\nCombo Deals:")
            for combo in self.combo_deals:
                products = [self.products[pid].name for pid in combo["product_ids"] if pid in self.products]
                lines.append(f"  - {combo['name']}: {' + '.join(products)} → {combo['combo_discount_pct']}% off")
        
        return "\n".join(lines)
