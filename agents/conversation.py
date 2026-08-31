"""
Conversational Buyer Agent
===========================
Multi-turn chat agent for AgentPay's chat-first UI. Understands shopping
intent, asks clarifying questions, searches real merchant catalogs,
negotiates bulk deals, and creates real Razorpay orders for checkout.

Design note: the LLM here only ever handles language — intent, replies, and
clarifying questions. It never invents product data. Whenever it decides to
search, compare, or check out, this module grounds that decision in the real
merchant catalogs and reuses BuyerAgent's existing negotiation protocol and
RazorpayPaymentClient, so every price and product ID shown in chat is real
and checkout-able — the same guarantee the older /api/shop flow makes, and
the same bug class (LLM-invented product IDs) fixed there stays fixed here.
"""

import re
import uuid
from dataclasses import dataclass, field
from typing import Optional

from agents.llm import llm_reason, CONVERSATION_PROMPT

MAX_HISTORY_LINES = 16           # ~8 exchanges — keeps the prompt small and inside rate limits
BULK_NEGOTIATION_THRESHOLD = 20  # quantities at/above this get negotiated instead of taken at list price
MAX_CLARIFICATIONS = 2           # stop asking and just search after this many clarifying questions

_STOPWORDS = {
    "i", "a", "an", "the", "want", "to", "buy", "need", "some", "for", "of", "is", "are", "in",
    "me", "my", "any", "no", "yes", "under", "over", "above", "below", "with", "and", "or", "it",
    "show", "find", "get", "looking", "like", "please", "would", "can", "you", "have", "do",
}


def _meaningful_words(text: str) -> set:
    words = "".join(c if c.isalnum() else " " for c in text.lower()).split()
    return {w for w in words if len(w) > 2 and w not in _STOPWORDS and not w.isdigit()}


@dataclass
class ChatSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    history: list = field(default_factory=list)     # [{"role": "user"/"assistant", "content": str}] for LLM context
    messages: list = field(default_factory=list)     # full rich message log returned to the frontend
    intent: str = "greeting"
    preferences: dict = field(default_factory=dict)  # category / budget_min / budget_max / quantity remembered across turns
    last_shown: list = field(default_factory=list)   # [(Product, MerchantAgent), ...] most recently shown
    cart: list = field(default_factory=list)         # order_summary contents for successfully created orders
    clarification_count: int = 0                     # consecutive clarifying questions asked — resets on search/checkout


class ConversationAgent:
    """Wraps a BuyerAgent's merchants/negotiation/payment machinery in a chat loop."""

    def __init__(self, buyer_agent):
        self.buyer_agent = buyer_agent
        self.sessions: dict[str, ChatSession] = {}

    # ── session management ──

    def get_or_create_session(self, session_id: Optional[str]) -> ChatSession:
        if session_id and session_id in self.sessions:
            return self.sessions[session_id]
        session = ChatSession(session_id=session_id) if session_id else ChatSession()
        self.sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        return self.sessions.get(session_id)

    # ── message log helpers ──

    def _emit(self, session: ChatSession, msg_type: str, content) -> dict:
        message = {"type": msg_type, "content": content, "sender": "agent"}
        session.messages.append(message)
        session.history.append({"role": "assistant", "content": self._summarize_for_history(msg_type, content)})
        return message

    def _emit_user(self, session: ChatSession, text: str):
        session.messages.append({"type": "text", "content": text, "sender": "user"})
        session.history.append({"role": "user", "content": text})

    def _summarize_for_history(self, msg_type: str, content) -> str:
        """Compact text form of a rich message, for LLM context — not shown to the user."""
        if msg_type == "text":
            return content
        if msg_type == "options":
            return f"Asked: {content.get('question')} Options offered: {', '.join(content.get('options', []))}"
        if msg_type == "product_cards":
            names = ", ".join(f"{c['name']} (₹{c['price']}, {c['merchant']})" for c in content)
            return f"Showed products: {names}"
        if msg_type == "comparison":
            names = ", ".join(f"{c['name']} (₹{c['price']}, {c['merchant']})" for c in content.get("items", []))
            return f"Compared: {names}"
        if msg_type == "order_summary":
            return f"Order summary: {content.get('merchant')} — total ₹{content.get('total')}, status {content.get('payment_status')}"
        return str(content)

    def _format_history(self, session: ChatSession) -> str:
        recent = session.history[-MAX_HISTORY_LINES:]
        if not recent:
            return "(no messages yet)"
        return "\n".join(f"{'User' if h['role'] == 'user' else 'Agent'}: {h['content']}" for h in recent)

    # ── product search (grounded in real catalogs — the LLM never invents these) ──

    def _search_products(self, category=None, keywords=None, budget_min=None, budget_max=None, limit=4):
        # Treat category as loose search terms too (split into words), not an exact-phrase
        # filter — the LLM often sends multi-word phrases like "casual shirt" that will never
        # appear verbatim in catalog text even when the product is a perfect match ("t-shirt").
        terms = set()
        if category:
            terms.update(w for w in category.lower().split() if len(w) > 2)
        for kw in (keywords or []):
            if kw:
                terms.update(w for w in kw.lower().split() if len(w) > 1)

        # Word-boundary matching — a plain substring check would let a short term like "mat"
        # false-match inside unrelated words like "Matte" (a finish/color variant name).
        term_patterns = [re.compile(r"\b" + re.escape(t) + r"\b") for t in terms]

        candidates = []
        name_matched_any = False
        for merchant in self.buyer_agent.merchants.values():
            for p in merchant.products.values():
                name_text = p.name.lower()
                full_text = f"{name_text} {p.description} {p.category}".lower()
                name_match_count = sum(1 for pat in term_patterns if pat.search(name_text))
                any_hit = name_match_count > 0 or any(pat.search(full_text) for pat in term_patterns)
                if term_patterns and not any_hit:
                    continue
                if name_match_count:
                    name_matched_any = True
                if budget_min is not None and p.base_price < budget_min:
                    continue
                if budget_max is not None and p.base_price > budget_max:
                    continue
                candidates.append((p, merchant, name_match_count))

        # If any product's NAME matched a search term, drop the ones that only matched via
        # description text — description-only hits (e.g. a fabric word mentioned in passing)
        # are much weaker signal and tend to pull in unrelated products.
        if term_patterns and name_matched_any:
            candidates = [c for c in candidates if c[2] > 0]

        # Dedup down to the best-matching, cheapest color/variant per (merchant, base product
        # name) — otherwise a single item's 6 color variants can crowd out everything else.
        best = {}
        for p, merchant, match_count in candidates:
            key = (merchant.info.id, p.name.split(" - ")[0])
            if key not in best or (match_count, -p.base_price) > (best[key][2], -best[key][0].base_price):
                best[key] = (p, merchant, match_count)

        # Rank by how many distinct search terms matched before price — otherwise a broad term
        # like "sports" (matching many cheap unrelated accessories) buries the item that actually
        # matches the specific terms (e.g. "yoga mat") beneath cheaper tangential matches.
        results = list(best.values())
        results.sort(key=lambda x: (-x[2], x[0].base_price))
        return [(p, m) for p, m, _ in results[:limit]]

    def _product_card(self, p, merchant) -> dict:
        max_discount = max((r["discount_pct"] for r in p.bulk_discount_rules), default=0)
        return {
            "id": p.id,
            "name": p.name,
            "price": p.base_price,
            "unit": p.unit,
            "min_order": p.min_order,
            "image_url": p.image_url,
            "merchant": merchant.info.name,
            "merchant_id": merchant.info.id,
            "bulk_discount_pct": max_discount,
            "in_stock": p.in_stock,
        }

    def _find_product(self, product_id: str):
        for merchant in self.buyer_agent.merchants.values():
            if product_id in merchant.products:
                return merchant.products[product_id], merchant
        return None

    # ── checkout (reuses BuyerAgent's negotiation + payment machinery) ──

    async def _start_checkout(self, session: ChatSession, product_id: str, quantity: Optional[int] = None) -> list:
        out = []
        found = self._find_product(product_id)
        if not found:
            out.append(self._emit(session, "text", "I couldn't find that product anymore — want to search again?"))
            return out

        p, merchant = found
        quantity = quantity or session.preferences.get("quantity") or p.min_order or 1
        quantity = max(quantity, p.min_order)

        bulk = quantity >= BULK_NEGOTIATION_THRESHOLD

        if bulk:
            out.append(self._emit(session, "text", f"That's a bulk order — let me negotiate with {merchant.info.name}..."))

            async def notify(event_type, data):
                if event_type == "negotiation_counter":
                    out.append(self._emit(
                        session, "text",
                        f"{merchant.info.name} countered ₹{data.get('counter', 0):,.0f}. "
                        f"I'm adjusting to ₹{data.get('new_offer', 0):,.0f}...",
                    ))
                elif event_type == "negotiation_accepted":
                    out.append(self._emit(
                        session, "text",
                        f"Deal! {merchant.info.name} accepted ₹{data.get('accepted', 0):,.0f} "
                        f"(saved ₹{data.get('savings', 0):,.0f}).",
                    ))

            order_plan = {
                "merchant_name": merchant.info.name,
                "items": [{"product_id": p.id, "quantity": quantity}],
            }
            neg_result = await self.buyer_agent.negotiate_with_merchant(
                merchant, order_plan, budget=float("inf"), notify=notify
            )
        else:
            total = p.get_total_for_quantity(quantity)
            neg_result = {
                "final_amount": total,
                "original_total": p.base_price * quantity,
                "savings": round(p.base_price * quantity - total, 2),
                "rounds": 0,
            }

        amount = neg_result["final_amount"]
        items_summary = f"{p.name} x{quantity}"
        payment_result = await self.buyer_agent.payment_client.create_order_with_retry(
            amount, merchant.info.name, items_summary
        )

        original_total = neg_result.get("original_total", amount) or amount
        savings = neg_result.get("savings", 0)

        order_summary = {
            "items": [{
                "product_id": p.id, "name": p.name, "quantity": quantity,
                "unit_price": round(amount / quantity, 2), "total": amount,
            }],
            "merchant": merchant.info.name,
            "subtotal": original_total,
            "discount": savings,
            "total": amount,
            "savings_pct": round((savings / original_total) * 100, 1) if original_total else 0,
            "payment_status": "success" if payment_result.success else "failed",
            "razorpay_order_id": payment_result.order_id or None,
            "checkout": {
                "order_id": payment_result.order_id,
                "amount": int(round(amount * 100)),
                "currency": "INR",
            } if payment_result.success else None,
        }
        if payment_result.success:
            session.cart.append(order_summary)

        out.append(self._emit(session, "order_summary", order_summary))
        return out

    # ── main turn handler ──

    async def handle_message(self, session: ChatSession, user_text: str) -> list:
        user_text = (user_text or "").strip()
        if not user_text:
            return []

        self._emit_user(session, user_text)

        # "Buy Now" on a product card is a deterministic UI action, not natural language —
        # handle it directly so checkout never depends on the LLM correctly inferring which
        # product the user means.
        if user_text.startswith("__BUY_NOW__:"):
            parts = user_text.split(":")
            product_id = parts[1] if len(parts) > 1 else ""
            quantity = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
            return await self._start_checkout(session, product_id, quantity)

        store_names = ", ".join(m.info.name for m in self.buyer_agent.merchants.values())
        categories = sorted({c for m in self.buyer_agent.merchants.values() for c in m.info.categories})
        system_prompt = CONVERSATION_PROMPT.format(
            store_names=store_names,
            categories=", ".join(categories),
            clarification_count=session.clarification_count,
        )
        user_message = f"Conversation so far:\n{self._format_history(session)}\n\nUser's latest message: {user_text}"

        try:
            decision = await llm_reason(system_prompt, user_message)
        except Exception as e:
            print(f"[conversation] llm_reason failed: {e}")
            return [self._emit(session, "text", "Sorry, I had trouble understanding that — could you rephrase?")]

        if not isinstance(decision, dict) or "error" in decision:
            return [self._emit(session, "text", "Sorry, something went wrong on my end. Could you try again?")]

        return await self._act_on_decision(session, decision)

    async def _act_on_decision(self, session: ChatSession, decision: dict) -> list:
        out = []
        action = decision.get("action", "answer")
        intent = decision.get("intent")
        if intent:
            session.intent = intent

        reply = decision.get("reply")
        if reply:
            out.append(self._emit(session, "text", reply))

        if action == "ask_clarification" and session.clarification_count < MAX_CLARIFICATIONS:
            session.clarification_count += 1
            c = decision.get("clarification") or {}
            question, options = c.get("question", ""), c.get("options", [])
            if question or options:
                out.append(self._emit(session, "options", {"question": question, "options": options}))
            else:
                action = "search"  # LLM said "ask" but gave nothing to ask — fall through to search

        if action in ("search", "compare") or (action == "ask_clarification" and session.clarification_count >= MAX_CLARIFICATIONS):
            session.clarification_count = 0
            search = decision.get("search") or {}
            if search.get("quantity"):
                session.preferences["quantity"] = search["quantity"]
            # Note: "category" is deliberately NOT persisted across turns — it's usually the topic
            # itself, and carrying it forward once the user moves on causes stale-context false
            # matches (e.g. an old "Casual" category matching an unrelated later search).
            for key in ("budget_min", "budget_max"):
                if search.get(key) is not None:
                    session.preferences[key] = search[key]

            keywords = search.get("keywords") or []
            category = search.get("category")
            if not keywords and not category:
                # The LLM gave nothing to search on — fall back to the meaningful words from the
                # last few user turns (not the whole session), so a single bare reply like "M"
                # still has recent context ("shirt") to work with, without stale old topics
                # (bug fixed here: an item mentioned many turns/topics ago used to leak in).
                recent_user_turns = [h["content"] for h in session.history if h["role"] == "user"][-3:]
                fallback_words = set()
                for turn_text in recent_user_turns:
                    fallback_words.update(_meaningful_words(turn_text))
                keywords = list(fallback_words)

            products = self._search_products(
                category=category,
                keywords=keywords,
                budget_min=search.get("budget_min", session.preferences.get("budget_min")),
                budget_max=search.get("budget_max", session.preferences.get("budget_max")),
                limit=3 if action == "compare" else 4,
            )

            if not products:
                out.append(self._emit(
                    session, "text",
                    "I couldn't find anything matching that in our stores right now — want to try a different budget or category?",
                ))
            else:
                session.last_shown = products
                cards = [self._product_card(p, m) for p, m in products]
                if action == "compare":
                    out.append(self._emit(session, "comparison", {"items": cards}))
                else:
                    out.append(self._emit(session, "product_cards", cards))

        elif action == "checkout":
            checkout = decision.get("checkout") or {}
            quantity = checkout.get("quantity") or session.preferences.get("quantity")
            if session.last_shown:
                p, merchant = session.last_shown[0]
                out.extend(await self._start_checkout(session, p.id, quantity))
            else:
                out.append(self._emit(
                    session, "text",
                    "What would you like to buy? Show me a product first and I'll get it ready for checkout.",
                ))

        if not out:
            out.append(self._emit(session, "text", "Got it! Anything else I can help you find?"))

        return out
