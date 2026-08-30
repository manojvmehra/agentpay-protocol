"""
CaterCloud - Event catering & food services
Demo merchant for AgentPay Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent


def create_catercloud() -> MerchantAgent:
    agent = MerchantAgent(
        name="CaterCloud",
        description="Event catering made simple — lunch boxes, snack packs, beverages & full-course meals.",
        categories=["food", "beverages", "catering"],
        location="Bengaluru",
    )
    
    # Lunch Boxes
    agent.add_product(Product(
        id="cc_lunch_veg",
        name="Veg Lunch Box",
        description="Rice, 2 rotis, dal, sabzi, salad, pickle. Packed in eco-friendly container.",
        category="food",
        base_price=120,
        unit="plate",
        min_order=25,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 10},
            {"min_qty": 250, "discount_pct": 15},
            {"min_qty": 500, "discount_pct": 20},
        ]
    ))
    
    agent.add_product(Product(
        id="cc_lunch_nonveg",
        name="Non-Veg Lunch Box",
        description="Rice, 2 rotis, chicken curry, dal, salad, pickle.",
        category="food",
        base_price=180,
        unit="plate",
        min_order=25,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 8},
            {"min_qty": 250, "discount_pct": 12},
            {"min_qty": 500, "discount_pct": 18},
        ]
    ))
    
    # Snack Packs
    agent.add_product(Product(
        id="cc_snack_tea",
        name="Tea-Time Snack Pack",
        description="Samosa, vada pav, cookies, and chai. Perfect for breaks.",
        category="food",
        base_price=80,
        unit="plate",
        min_order=50,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 10},
            {"min_qty": 300, "discount_pct": 15},
        ]
    ))
    
    agent.add_product(Product(
        id="cc_snack_premium",
        name="Premium Snack Platter",
        description="Mini sandwiches, spring rolls, paneer tikka, fruit cup, cold coffee.",
        category="food",
        base_price=200,
        unit="plate",
        min_order=25,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 8},
            {"min_qty": 100, "discount_pct": 12},
        ]
    ))
    
    # Beverages
    agent.add_product(Product(
        id="cc_water_bottle",
        name="Packaged Water Bottle (500ml)",
        description="Sealed 500ml drinking water bottle.",
        category="beverages",
        base_price=15,
        unit="bottle",
        min_order=50,
        bulk_discount_rules=[
            {"min_qty": 200, "discount_pct": 10},
            {"min_qty": 500, "discount_pct": 20},
        ]
    ))
    
    agent.add_product(Product(
        id="cc_juice",
        name="Fresh Juice Pack (250ml)",
        description="Freshly packed fruit juice — mango, orange, or mixed fruit.",
        category="beverages",
        base_price=40,
        unit="pack",
        min_order=50,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 8},
            {"min_qty": 250, "discount_pct": 12},
        ]
    ))
    
    agent.add_product(Product(
        id="cc_chai_station",
        name="Live Chai Station (per hour)",
        description="Unlimited chai service with a dedicated chai maker for your event. Serves up to 200 people/hr.",
        category="beverages",
        base_price=3000,
        unit="hour",
        min_order=2,
        bulk_discount_rules=[
            {"min_qty": 4, "discount_pct": 10},
            {"min_qty": 8, "discount_pct": 15},
        ]
    ))
    
    # Full Course
    agent.add_product(Product(
        id="cc_buffet_veg",
        name="Veg Buffet (per person)",
        description="Full buffet: 3 starters, 2 mains, rice, rotis, dal, 2 desserts, beverages.",
        category="catering",
        base_price=350,
        unit="person",
        min_order=50,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 10},
            {"min_qty": 250, "discount_pct": 15},
            {"min_qty": 500, "discount_pct": 20},
        ]
    ))
    
    # Upsell rules
    agent.add_upsell_rule("cc_lunch_veg", "cc_water_bottle", discount_pct=10)
    agent.add_upsell_rule("cc_lunch_nonveg", "cc_juice", discount_pct=8)
    agent.add_upsell_rule("cc_snack_tea", "cc_chai_station", discount_pct=5)
    agent.add_upsell_rule("cc_buffet_veg", "cc_juice", discount_pct=15)
    
    # Combo deals
    agent.add_combo_deal(
        name="Full Day Event Combo",
        product_ids=["cc_lunch_veg", "cc_snack_tea", "cc_water_bottle"],
        combo_discount_pct=18
    )
    agent.add_combo_deal(
        name="Premium Event Package",
        product_ids=["cc_buffet_veg", "cc_snack_premium", "cc_juice", "cc_chai_station"],
        combo_discount_pct=20
    )
    
    return agent
