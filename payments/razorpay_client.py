"""
Razorpay Payment Integration
=============================
Handles all payment operations through Razorpay test-mode APIs.
Creates orders, processes payments, handles failures with retries.
"""

import razorpay
import time
import random
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from config import RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, MAX_PAYMENT_RETRIES, PAYMENT_RETRY_DELAY_SECONDS

# Demo mode: randomly fail payment attempts to exercise the retry/recovery
# logic in create_order_with_retry(). Toggle on to show failure recovery live.
SIMULATE_FAILURE = True
SIMULATE_FAILURE_RATE = 0.2  # 1 in 5 attempts


@dataclass
class PaymentResult:
    """Result of a payment attempt."""
    success: bool
    order_id: str = ""
    payment_id: str = ""
    amount: float = 0
    currency: str = "INR"
    status: str = ""
    merchant_name: str = ""
    attempts: int = 0
    error: str = ""
    razorpay_order: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class RazorpayPaymentClient:
    """
    Handles Razorpay payment operations for the Hermes protocol.
    Uses test-mode APIs — no real money is involved.
    """
    
    def __init__(self):
        self.client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        self.payment_log: list[PaymentResult] = []
    
    async def create_order(self, amount: float, merchant_name: str, items_summary: str, 
                           receipt_id: str = None) -> PaymentResult:
        """
        Create a Razorpay order for the agreed deal.
        
        Args:
            amount: Total amount in INR
            merchant_name: Name of the merchant
            items_summary: Brief description of items
            receipt_id: Optional receipt identifier
        
        Returns:
            PaymentResult with order details
        """
        if not receipt_id:
            receipt_id = f"hermes_{int(time.time())}"

        if SIMULATE_FAILURE and random.random() < SIMULATE_FAILURE_RATE:
            result = PaymentResult(
                success=False,
                amount=amount,
                merchant_name=merchant_name,
                attempts=1,
                error="Simulated payment failure (SIMULATE_FAILURE demo mode)",
                status="failed",
            )
            self.payment_log.append(result)
            return result

        try:
            order_data = {
                "amount": int(amount * 100),  # Razorpay expects paise
                "currency": "INR",
                "receipt": receipt_id,
                "payment_capture": 1,  # Auto-capture
                "notes": {
                    "merchant": merchant_name,
                    "items": items_summary[:256],  # Razorpay limits note length
                    "protocol": "hermes_v1",
                    "agent_type": "buyer",
                }
            }
            
            # Run in executor since razorpay SDK is synchronous
            loop = asyncio.get_event_loop()
            order = await loop.run_in_executor(None, lambda: self.client.order.create(order_data))
            
            result = PaymentResult(
                success=True,
                order_id=order["id"],
                amount=amount,
                status=order["status"],
                merchant_name=merchant_name,
                attempts=1,
                razorpay_order=order,
            )
            self.payment_log.append(result)
            return result
            
        except Exception as e:
            result = PaymentResult(
                success=False,
                amount=amount,
                merchant_name=merchant_name,
                attempts=1,
                error=str(e),
                status="failed",
            )
            self.payment_log.append(result)
            return result
    
    async def create_order_with_retry(self, amount: float, merchant_name: str, 
                                       items_summary: str) -> PaymentResult:
        """
        Create an order with automatic retry on failure.
        Implements exponential backoff.
        """
        last_result = None
        
        for attempt in range(1, MAX_PAYMENT_RETRIES + 1):
            result = await self.create_order(amount, merchant_name, items_summary)
            result.attempts = attempt
            
            if result.success:
                if attempt > 1:
                    result.razorpay_order["recovery_note"] = f"Succeeded on attempt {attempt}"
                return result
            
            last_result = result
            
            if attempt < MAX_PAYMENT_RETRIES:
                delay = PAYMENT_RETRY_DELAY_SECONDS * (2 ** (attempt - 1))  # Exponential backoff
                await asyncio.sleep(delay)
        
        # All retries exhausted
        last_result.error = f"Failed after {MAX_PAYMENT_RETRIES} attempts: {last_result.error}"
        return last_result
    
    async def fetch_order_status(self, order_id: str) -> dict:
        """Check the status of an existing order."""
        try:
            loop = asyncio.get_event_loop()
            order = await loop.run_in_executor(None, lambda: self.client.order.fetch(order_id))
            return {
                "success": True,
                "order_id": order_id,
                "status": order.get("status"),
                "amount_paid": order.get("amount_paid", 0) / 100,
                "amount_due": order.get("amount_due", 0) / 100,
            }
        except Exception as e:
            return {
                "success": False,
                "order_id": order_id,
                "error": str(e),
            }
    
    async def fetch_payments_for_order(self, order_id: str) -> list:
        """Get all payment attempts for an order."""
        try:
            loop = asyncio.get_event_loop()
            payments = await loop.run_in_executor(
                None, lambda: self.client.order.payments(order_id)
            )
            return payments.get("items", [])
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_payment_summary(self) -> dict:
        """Get a summary of all payment operations in this session."""
        total = len(self.payment_log)
        successful = sum(1 for p in self.payment_log if p.success)
        failed = sum(1 for p in self.payment_log if not p.success)
        total_amount = sum(p.amount for p in self.payment_log if p.success)
        retried = sum(1 for p in self.payment_log if p.attempts > 1)
        recovered = sum(1 for p in self.payment_log if p.success and p.attempts > 1)
        
        return {
            "total_transactions": total,
            "successful": successful,
            "failed": failed,
            "total_amount_processed": total_amount,
            "transactions_retried": retried,
            "failures_recovered": recovered,
            "recovery_rate": f"{(recovered/retried*100):.0f}%" if retried else "N/A",
        }
    
    def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        """Verify a checkout.js payment signature against key_secret. Never trust an unverified payment."""
        try:
            self.client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
            })
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

    def generate_payment_link(self, order_id: str, amount: float, merchant_name: str) -> str:
        """
        Generate a Razorpay checkout URL for the order.
        In test mode, this leads to a mock payment page.
        """
        # In a real implementation, this would generate a payment link
        # For the demo, we create the order and the frontend handles checkout
        return f"https://api.razorpay.com/v1/checkout/embedded?order_id={order_id}"
