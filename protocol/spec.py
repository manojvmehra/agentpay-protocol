"""
AgentPay Protocol v1.0
======================
A standardized protocol for AI agent-to-agent commerce.

This defines the message types and schemas that allow any AI buyer agent
to discover, browse, negotiate with, and pay any merchant that implements
this protocol. Think of it as "UPI for AI agents."

Protocol Flow:
    1. DISCOVER  → Buyer finds available merchants
    2. CATALOG   → Buyer requests product catalog
    3. QUERY     → Buyer asks about specific products
    4. NEGOTIATE → Buyer and seller negotiate price/terms
    5. ORDER     → Both agree, order is created
    6. PAY       → Payment processed via Razorpay
    7. CONFIRM   → Transaction confirmed with audit trail
    8. FAIL      → Failure handling at any step
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional
from datetime import datetime
import uuid
import json


class MessageType(str, Enum):
    """All possible message types in the AgentPay Protocol."""
    # Discovery
    DISCOVER_REQUEST = "discover.request"
    DISCOVER_RESPONSE = "discover.response"
    
    # Catalog
    CATALOG_REQUEST = "catalog.request"
    CATALOG_RESPONSE = "catalog.response"
    
    # Query
    QUERY = "query"
    QUERY_RESPONSE = "query.response"
    
    # Negotiation
    NEGOTIATE_OFFER = "negotiate.offer"
    NEGOTIATE_COUNTER = "negotiate.counter"
    NEGOTIATE_ACCEPT = "negotiate.accept"
    NEGOTIATE_REJECT = "negotiate.reject"
    
    # Order & Payment
    ORDER_CREATE = "order.create"
    ORDER_CONFIRM = "order.confirm"
    PAYMENT_INITIATE = "payment.initiate"
    PAYMENT_SUCCESS = "payment.success"
    PAYMENT_FAILED = "payment.failed"
    PAYMENT_RETRY = "payment.retry"
    
    # Errors
    ERROR = "error"


class AgentRole(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"


@dataclass
class Product:
    """A product in a merchant's catalog."""
    id: str
    name: str
    description: str
    category: str
    base_price: float  # Price per unit in INR
    unit: str  # "piece", "plate", "sqft", etc.
    min_order: int = 1
    max_order: int = 10000
    in_stock: bool = True
    bulk_discount_rules: list = field(default_factory=list)
    # Example: [{"min_qty": 50, "discount_pct": 10}, {"min_qty": 100, "discount_pct": 15}]
    metadata: dict = field(default_factory=dict)
    image_url: str = ""

    def __post_init__(self):
        if not self.image_url:
            from urllib.parse import quote
            self.image_url = f"https://via.placeholder.com/300x300?text={quote(self.name)}"

    def get_price_for_quantity(self, qty: int) -> float:
        """Calculate price per unit after applicable bulk discounts."""
        discount = 0
        for rule in sorted(self.bulk_discount_rules, key=lambda r: r["min_qty"], reverse=True):
            if qty >= rule["min_qty"]:
                discount = rule["discount_pct"]
                break
        return self.base_price * (1 - discount / 100)

    def get_total_for_quantity(self, qty: int) -> float:
        """Calculate total price for a given quantity."""
        return round(self.get_price_for_quantity(qty) * qty, 2)


@dataclass
class MerchantInfo:
    """Public information about a merchant."""
    id: str
    name: str
    description: str
    categories: list  # What they sell
    location: str
    rating: float = 4.5
    response_time_ms: int = 100
    supports_negotiation: bool = True
    max_negotiation_rounds: int = 3


@dataclass 
class ProtocolMessage:
    """A single message in the AgentPay protocol."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    type: MessageType = MessageType.DISCOVER_REQUEST
    sender: AgentRole = AgentRole.BUYER
    receiver: AgentRole = AgentRole.SELLER
    merchant_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    payload: dict = field(default_factory=dict)
    conversation_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    
    def to_dict(self) -> dict:
        d = asdict(self)
        d["type"] = self.type.value
        d["sender"] = self.sender.value
        d["receiver"] = self.receiver.value
        return d
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


@dataclass
class NegotiationState:
    """Tracks the state of a negotiation between buyer and seller."""
    conversation_id: str
    merchant_id: str
    round_number: int = 0
    max_rounds: int = 3
    buyer_budget: float = 0
    current_offer: float = 0
    items: list = field(default_factory=list)
    status: str = "active"  # active, accepted, rejected, expired
    history: list = field(default_factory=list)
    
    def can_continue(self) -> bool:
        return self.status == "active" and self.round_number < self.max_rounds
    
    def add_round(self, offer: float, by: str, reasoning: str):
        self.round_number += 1
        self.history.append({
            "round": self.round_number,
            "offer": offer,
            "by": by,
            "reasoning": reasoning,
            "timestamp": datetime.now().isoformat()
        })
        self.current_offer = offer


@dataclass
class OrderSummary:
    """Summary of a completed order."""
    order_id: str
    merchant_id: str
    merchant_name: str
    items: list  # List of {product_id, name, qty, unit_price, total}
    subtotal: float
    discount_applied: float
    final_amount: float
    razorpay_order_id: str = ""
    razorpay_payment_id: str = ""
    payment_status: str = "pending"  # pending, success, failed, retrying
    negotiation_rounds: int = 0
    negotiation_savings: float = 0
    audit_trail: list = field(default_factory=list)
    
    def add_audit(self, action: str, details: str):
        self.audit_trail.append({
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })


@dataclass
class TransactionReport:
    """Full report of the entire multi-merchant transaction."""
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    user_request: str = ""
    budget: float = 0
    orders: list = field(default_factory=list)  # List of OrderSummary
    total_spent: float = 0
    total_saved: float = 0
    budget_remaining: float = 0
    merchants_contacted: int = 0
    negotiations_completed: int = 0
    payments_successful: int = 0
    payments_failed: int = 0
    payments_recovered: int = 0
    failures: list = field(default_factory=list)
    start_time: str = field(default_factory=lambda: datetime.now().isoformat())
    end_time: str = ""
    duration_seconds: float = 0
    
    def finalize(self):
        self.end_time = datetime.now().isoformat()
        self.total_spent = sum(o.final_amount for o in self.orders if o.payment_status == "success")
        self.budget_remaining = self.budget - self.total_spent
        self.payments_successful = sum(1 for o in self.orders if o.payment_status == "success")
        self.payments_failed = sum(1 for o in self.orders if o.payment_status == "failed")
