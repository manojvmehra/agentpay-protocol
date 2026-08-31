"""
AgentPay Server
===============
FastAPI server that exposes the buyer agent as an API
and serves the real-time dashboard.
"""

import asyncio
import json
import math
import sys

# Windows consoles default to a cp1252 stdout that can't encode ₹ and other
# non-ASCII characters our messages/logs use — reconfigure to UTF-8 so print()
# and logging never crash on them.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.buyer import BuyerAgent
from agents.conversation import ConversationAgent
from merchants.festkart import create_festkart
from merchants.printboss import create_printboss
from merchants.catercloud import create_catercloud
from merchants.techbazaar import create_techbazaar
from merchants.giftgenie import create_giftgenie
from merchants.sportstar import create_sportstar
from merchants.stylebazaar import create_stylebazaar
from merchants.gadgetstore import create_gadgetstore
from merchants.glowmart import create_glowmart
from config import HOST, PORT, RAZORPAY_KEY_ID

app = FastAPI(
    title="AgentPay Protocol",
    description="AI Agent-to-Agent Commerce on Razorpay",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize merchants and buyer agent
buyer_agent = BuyerAgent()

# Register demo merchants
festkart = create_festkart()
printboss = create_printboss()
catercloud = create_catercloud()
techbazaar = create_techbazaar()
giftgenie = create_giftgenie()
sportstar = create_sportstar()
stylebazaar = create_stylebazaar()
gadgetstore = create_gadgetstore()
glowmart = create_glowmart()

buyer_agent.register_merchant(festkart)
buyer_agent.register_merchant(printboss)
buyer_agent.register_merchant(catercloud)
buyer_agent.register_merchant(techbazaar)
buyer_agent.register_merchant(giftgenie)
buyer_agent.register_merchant(sportstar)
buyer_agent.register_merchant(stylebazaar)
buyer_agent.register_merchant(gadgetstore)
buyer_agent.register_merchant(glowmart)

# Conversational chat agent (Step 1: chat-first UI) — reuses buyer_agent's
# merchants, negotiation protocol, and Razorpay payment client.
conversation_agent = ConversationAgent(buyer_agent)

# Store active WebSocket connections for live updates
active_connections: list[WebSocket] = []


class ShoppingRequest(BaseModel):
    request: str
    budget: Optional[float] = None


class MerchantQuery(BaseModel):
    merchant_id: str
    query: str
    quantity: int = 1


class PaymentVerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


# ── API Endpoints ──

@app.get("/")
async def root():
    return FileResponse("dashboard/index.html")


@app.get("/api/merchants")
async def list_merchants():
    """List all registered merchants and their catalogs."""
    merchants = []
    for mid, merchant in buyer_agent.merchants.items():
        merchants.append({
            "id": mid,
            "name": merchant.info.name,
            "description": merchant.info.description,
            "categories": merchant.info.categories,
            "product_count": len(merchant.products),
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "category": p.category,
                    "base_price": p.base_price,
                    "unit": p.unit,
                    "bulk_discounts": p.bulk_discount_rules,
                }
                for p in merchant.products.values()
            ],
            "combo_deals": merchant.combo_deals,
        })
    return {"merchants": merchants, "total": len(merchants)}


@app.get("/api/config")
async def get_config():
    """Public config for the frontend — never expose key_secret."""
    return {"key_id": RAZORPAY_KEY_ID, "razorpay_enabled": True}


@app.get("/api/products")
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    merchant: Optional[str] = None,
):
    """
    Flat, paginated product listing across all merchants for the storefront.
    - category: comma-separated list of underlying category values (e.g. "apparel,accessories")
    - merchant: merchant id to filter to a single store
    - sort: "price_asc" | "price_desc" | "merchant"
    """
    all_products = []
    for mid, m in buyer_agent.merchants.items():
        if merchant and mid != merchant:
            continue
        for p in m.products.values():
            all_products.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "category": p.category,
                "base_price": p.base_price,
                "unit": p.unit,
                "min_order": p.min_order,
                "max_order": p.max_order,
                "in_stock": p.in_stock,
                "bulk_discounts": p.bulk_discount_rules,
                "image_url": p.image_url,
                "merchant_id": mid,
                "merchant_name": m.info.name,
            })

    if category:
        wanted = {c.strip().lower() for c in category.split(",") if c.strip()}
        all_products = [p for p in all_products if p["category"].lower() in wanted]

    if search:
        q = search.lower()
        all_products = [
            p for p in all_products
            if q in p["name"].lower() or q in p["description"].lower() or q in p["merchant_name"].lower()
        ]

    if sort == "price_asc":
        all_products.sort(key=lambda p: p["base_price"])
    elif sort == "price_desc":
        all_products.sort(key=lambda p: p["base_price"], reverse=True)
    elif sort == "merchant":
        all_products.sort(key=lambda p: p["merchant_name"])

    total = len(all_products)
    pages = max(1, math.ceil(total / limit))
    page = min(page, pages)
    start = (page - 1) * limit
    page_items = all_products[start:start + limit]

    return {"products": page_items, "total": total, "page": page, "pages": pages}


def build_shop_response(report) -> dict:
    """Shared shape for both POST /api/shop and the WS final_report event, so the
    frontend gets full checkout-ready order details regardless of which path it used."""
    return {
        "session_id": report.session_id,
        "request": report.user_request,
        "budget": report.budget,
        "total_spent": report.total_spent,
        "budget_remaining": report.budget_remaining,
        "total_saved": report.total_saved,
        "orders": [
            {
                "merchant": o.merchant_name,
                "merchant_id": o.merchant_id,
                "items": o.items,
                "amount": o.final_amount,
                "discount": o.discount_applied,
                "payment_status": o.payment_status,
                "razorpay_order_id": o.razorpay_order_id,
                "negotiation_rounds": o.negotiation_rounds,
                "audit_trail": o.audit_trail,
                "checkout": {
                    "order_id": o.razorpay_order_id,
                    "amount": int(round(o.final_amount * 100)),  # paise, for checkout.js
                    "currency": "INR",
                } if o.payment_status == "success" and o.razorpay_order_id else None,
            }
            for o in report.orders
        ],
        "metrics": buyer_agent.get_metrics(),
        "failures": report.failures,
    }


@app.post("/api/shop")
async def start_shopping(request: ShoppingRequest):
    """
    Start the AI shopping agent.
    Send a natural language request and the agent handles everything.
    """
    async def broadcast(event_type: str, data: dict):
        """Send live updates to all connected WebSocket clients."""
        message = json.dumps({"event": event_type, **data})
        disconnected = []
        for ws in active_connections:
            try:
                await ws.send_text(message)
            except Exception:
                disconnected.append(ws)
        for ws in disconnected:
            active_connections.remove(ws)

    report = await buyer_agent.process_request(request.request, callback=broadcast)
    return build_shop_response(report)


@app.get("/api/metrics")
async def get_metrics():
    """Get current session metrics."""
    return buyer_agent.get_metrics()


@app.get("/api/audit")
async def get_audit_trail():
    """Get the full audit trail."""
    return {"audit_trail": buyer_agent.get_audit_trail()}


@app.get("/api/payments")
async def get_payment_summary():
    """Get payment processing summary."""
    return buyer_agent.payment_client.get_payment_summary()


@app.post("/api/chat")
async def chat(payload: ChatRequest):
    """
    Send a message to the conversational buyer agent and get its response(s).
    Returns: { session_id, messages: [{type, content, sender}] }
    """
    session = conversation_agent.get_or_create_session(payload.session_id)
    messages = await conversation_agent.handle_message(session, payload.message)
    return {"session_id": session.session_id, "messages": messages}


@app.get("/api/chat/{session_id}")
async def get_chat_history(session_id: str):
    """Return the full message history for a chat session."""
    session = conversation_agent.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    return {"session_id": session.session_id, "messages": session.messages}


@app.post("/api/payment/verify")
async def verify_payment(payload: PaymentVerifyRequest):
    """
    Verify a Razorpay checkout.js payment signature. Frontend must call this
    after checkout succeeds — never trust razorpay_payment_id on its own.
    """
    verified = buyer_agent.payment_client.verify_payment_signature(
        payload.razorpay_order_id, payload.razorpay_payment_id, payload.razorpay_signature
    )
    if not verified:
        raise HTTPException(status_code=400, detail="Payment signature verification failed")
    return {
        "verified": True,
        "razorpay_order_id": payload.razorpay_order_id,
        "razorpay_payment_id": payload.razorpay_payment_id,
    }


# ── WebSocket for live updates ──

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time dashboard updates."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Keep connection alive, handle incoming messages
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "shop":
                # Start shopping from WebSocket
                async def ws_callback(event_type: str, event_data: dict):
                    await websocket.send_text(json.dumps({
                        "event": event_type, **event_data
                    }))
                
                report = await buyer_agent.process_request(
                    message["request"], callback=ws_callback
                )

                await websocket.send_text(json.dumps({
                    "event": "final_report",
                    "report": build_shop_response(report),
                }))
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# ── Branded store mini-sites ──
# Standalone storefronts at /store/<slug>. Each shares the same underlying
# MerchantAgent (and hence the same negotiation protocol and payment
# client) that the main buyer agent already discovers and transacts with —
# these are genuinely one merchant each, just with their own independent
# front door and Buy Now API in addition to the chat flow.

class StoreBuyRequest(BaseModel):
    product_id: str
    quantity: int = 1


def register_store_routes(slug: str, merchant):
    """Wire up GET /store/<slug>, its scoped products API, and its Buy Now API."""

    @app.get(f"/store/{slug}", name=f"{slug}_home")
    async def store_home():
        return FileResponse(f"store/{slug}/index.html")

    @app.get(f"/store/{slug}/api/products", name=f"{slug}_products")
    async def store_products(
        page: int = Query(1, ge=1),
        limit: int = Query(24, ge=1, le=100),
        category: Optional[str] = None,
        type: Optional[str] = None,
        size: Optional[str] = None,
        color: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
    ):
        """Paginated, filterable product listing scoped to just this store."""
        items = []
        for p in merchant.products.values():
            items.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "category": p.category,
                "type": p.metadata.get("type"),
                "size": p.metadata.get("size"),
                "color": p.metadata.get("color"),
                "base_price": p.base_price,
                "unit": p.unit,
                "min_order": p.min_order,
                "in_stock": p.in_stock,
                "bulk_discounts": p.bulk_discount_rules,
                "image_url": p.image_url,
            })

        if category:
            items = [i for i in items if i["category"] == category.lower()]
        if type:
            items = [i for i in items if i["type"] == type.lower()]
        if size:
            items = [i for i in items if i["size"] == size.upper()]
        if color:
            items = [i for i in items if (i["color"] or "").lower() == color.lower()]
        if search:
            q = search.lower()
            items = [i for i in items if q in i["name"].lower() or q in i["description"].lower()]

        if sort == "price_asc":
            items.sort(key=lambda i: i["base_price"])
        elif sort == "price_desc":
            items.sort(key=lambda i: i["base_price"], reverse=True)

        total = len(items)
        pages = max(1, math.ceil(total / limit))
        page = min(page, pages)
        start = (page - 1) * limit
        page_items = items[start:start + limit]

        return {
            "products": page_items,
            "total": total,
            "page": page,
            "pages": pages,
            "combo_deals": merchant.combo_deals,
        }

    @app.post(f"/store/{slug}/api/buy", name=f"{slug}_buy")
    async def store_buy(payload: StoreBuyRequest):
        """Buy Now: creates a real Razorpay order for one product from this store."""
        product = merchant.products.get(payload.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        quantity = max(payload.quantity, product.min_order)
        amount = product.get_total_for_quantity(quantity)
        items_summary = f"{product.name} x{quantity}"

        payment_result = await buyer_agent.payment_client.create_order_with_retry(
            amount, merchant.info.name, items_summary
        )
        if not payment_result.success:
            raise HTTPException(status_code=502, detail=f"Could not create payment order: {payment_result.error}")

        return {
            "product_id": product.id,
            "name": product.name,
            "quantity": quantity,
            "unit_price": round(amount / quantity, 2),
            "total": amount,
            "merchant": merchant.info.name,
            "checkout": {
                "order_id": payment_result.order_id,
                "amount": int(round(amount * 100)),
                "currency": "INR",
            },
        }

    # Serve any static assets referenced by this store's page
    app.mount(f"/store/{slug}/static", StaticFiles(directory=f"store/{slug}"), name=f"{slug}_static")


register_store_routes("stylebazaar", stylebazaar)
register_store_routes("gadgetstore", gadgetstore)
register_store_routes("glowmart", glowmart)


# ── Serve dashboard ──

@app.get("/dashboard")
async def dashboard():
    return FileResponse("dashboard/index.html")


# Serve any static assets referenced by the dashboard (images, css, etc.)
app.mount("/static", StaticFiles(directory="dashboard"), name="static")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  AgentPay Protocol — AI Agent-to-Agent Commerce")
    print("  Dashboard: http://localhost:8000")
    print("  API Docs:  http://localhost:8000/docs")
    print("="*60 + "\n")
    uvicorn.run(app, host=HOST, port=PORT)
