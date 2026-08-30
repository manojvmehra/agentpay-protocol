"""
AgentPay Server
===============
FastAPI server that exposes the buyer agent as an API
and serves the real-time dashboard.
"""

import asyncio
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from agents.buyer import BuyerAgent
from merchants.festkart import create_festkart
from merchants.printboss import create_printboss
from merchants.catercloud import create_catercloud
from config import HOST, PORT

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

buyer_agent.register_merchant(festkart)
buyer_agent.register_merchant(printboss)
buyer_agent.register_merchant(catercloud)

# Store active WebSocket connections for live updates
active_connections: list[WebSocket] = []


class ShoppingRequest(BaseModel):
    request: str
    budget: Optional[float] = None


class MerchantQuery(BaseModel):
    merchant_id: str
    query: str
    quantity: int = 1


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
                "items": o.items,
                "amount": o.final_amount,
                "discount": o.discount_applied,
                "payment_status": o.payment_status,
                "razorpay_order_id": o.razorpay_order_id,
                "negotiation_rounds": o.negotiation_rounds,
                "audit_trail": o.audit_trail,
            }
            for o in report.orders
        ],
        "metrics": buyer_agent.get_metrics(),
        "failures": report.failures,
    }


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
                    "report": {
                        "session_id": report.session_id,
                        "total_spent": report.total_spent,
                        "budget_remaining": report.budget_remaining,
                        "total_saved": report.total_saved,
                        "orders_count": len(report.orders),
                        "metrics": buyer_agent.get_metrics(),
                    }
                }))
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)


# ── Serve dashboard ──

@app.get("/dashboard")
async def dashboard():
    return FileResponse("dashboard/index.html")


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("  AgentPay Protocol — AI Agent-to-Agent Commerce")
    print("  Dashboard: http://localhost:8000")
    print("  API Docs:  http://localhost:8000/docs")
    print("="*60 + "\n")
    uvicorn.run(app, host=HOST, port=PORT)
