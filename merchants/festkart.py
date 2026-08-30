"""
FestKart - College fest merch & apparel store
Demo merchant for AgentPay Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent


def create_festkart() -> MerchantAgent:
    agent = MerchantAgent(
        name="FestKart",
        description="Premium college fest merchandise & custom apparel. Bulk orders welcome!",
        categories=["apparel", "accessories", "merchandise"],
        location="Bengaluru",
    )
    
    # T-Shirts
    agent.add_product(Product(
        id="fk_tshirt_basic",
        name="Custom Printed T-Shirt (Basic)",
        description="Round neck cotton t-shirt with single-color print. Great for large batches.",
        category="apparel",
        base_price=250,
        unit="piece",
        min_order=10,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 10},
            {"min_qty": 100, "discount_pct": 15},
            {"min_qty": 500, "discount_pct": 20},
        ]
    ))
    
    agent.add_product(Product(
        id="fk_tshirt_premium",
        name="Custom Printed T-Shirt (Premium)",
        description="Premium cotton blend, full-color sublimation print. Perfect for team leads.",
        category="apparel",
        base_price=450,
        unit="piece",
        min_order=5,
        bulk_discount_rules=[
            {"min_qty": 25, "discount_pct": 8},
            {"min_qty": 50, "discount_pct": 12},
            {"min_qty": 100, "discount_pct": 18},
        ]
    ))
    
    # Caps
    agent.add_product(Product(
        id="fk_cap",
        name="Custom Embroidered Cap",
        description="Adjustable cotton cap with custom logo embroidery.",
        category="accessories",
        base_price=180,
        unit="piece",
        min_order=20,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 10},
            {"min_qty": 100, "discount_pct": 15},
        ]
    ))
    
    # Badges
    agent.add_product(Product(
        id="fk_badge",
        name="Custom Metal Badge",
        description="Pin-back metal badge with custom design. Great for event identification.",
        category="accessories",
        base_price=45,
        unit="piece",
        min_order=50,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 12},
            {"min_qty": 500, "discount_pct": 20},
        ]
    ))
    
    # Tote Bags
    agent.add_product(Product(
        id="fk_tote",
        name="Custom Canvas Tote Bag",
        description="Eco-friendly canvas tote with single-color screen print.",
        category="accessories",
        base_price=150,
        unit="piece",
        min_order=25,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 10},
            {"min_qty": 100, "discount_pct": 15},
        ]
    ))
    
    # Wristbands
    agent.add_product(Product(
        id="fk_wristband",
        name="Fabric Wristband (Event Entry)",
        description="Custom printed fabric wristband with tamper-proof lock. Perfect for event entry.",
        category="accessories",
        base_price=25,
        unit="piece",
        min_order=100,
        bulk_discount_rules=[
            {"min_qty": 500, "discount_pct": 15},
            {"min_qty": 1000, "discount_pct": 25},
        ]
    ))
    
    # Hoodies
    agent.add_product(Product(
        id="fk_hoodie",
        name="Custom Printed Hoodie",
        description="Fleece-lined pullover hoodie with front print.",
        category="apparel",
        base_price=850,
        unit="piece",
        min_order=10,
        bulk_discount_rules=[
            {"min_qty": 25, "discount_pct": 8},
            {"min_qty": 50, "discount_pct": 12},
        ]
    ))
    
    # Upsell rules
    agent.add_upsell_rule("fk_tshirt_basic", "fk_cap", discount_pct=8)
    agent.add_upsell_rule("fk_tshirt_basic", "fk_badge", discount_pct=10)
    agent.add_upsell_rule("fk_tshirt_premium", "fk_tote", discount_pct=10)
    agent.add_upsell_rule("fk_cap", "fk_wristband", discount_pct=5)
    
    # Combo deals
    agent.add_combo_deal(
        name="Fest Starter Pack",
        product_ids=["fk_tshirt_basic", "fk_cap", "fk_badge"],
        combo_discount_pct=15
    )
    agent.add_combo_deal(
        name="Premium Event Kit",
        product_ids=["fk_tshirt_premium", "fk_tote", "fk_wristband"],
        combo_discount_pct=18
    )
    
    return agent
