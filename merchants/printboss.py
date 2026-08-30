"""
PrintBoss - Printing & signage services
Demo merchant for AgentPay Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent


def create_printboss() -> MerchantAgent:
    agent = MerchantAgent(
        name="PrintBoss",
        description="Fast, reliable printing services — banners, posters, ID cards, standees & more.",
        categories=["printing", "signage", "stationery"],
        location="Bengaluru",
    )
    
    # Banners
    agent.add_product(Product(
        id="pb_banner_vinyl",
        name="Vinyl Banner (4x8 ft)",
        description="Full-color outdoor vinyl banner with metal grommets.",
        category="signage",
        base_price=800,
        unit="piece",
        min_order=1,
        bulk_discount_rules=[
            {"min_qty": 10, "discount_pct": 10},
            {"min_qty": 25, "discount_pct": 15},
        ]
    ))
    
    agent.add_product(Product(
        id="pb_banner_fabric",
        name="Fabric Banner (4x8 ft)",
        description="Premium fabric banner, wrinkle-free. Great for indoor events.",
        category="signage",
        base_price=1200,
        unit="piece",
        min_order=1,
        bulk_discount_rules=[
            {"min_qty": 5, "discount_pct": 8},
            {"min_qty": 15, "discount_pct": 12},
        ]
    ))
    
    # Posters
    agent.add_product(Product(
        id="pb_poster_a2",
        name="A2 Poster (Matte/Glossy)",
        description="High-quality A2 size poster print on 200gsm paper.",
        category="printing",
        base_price=120,
        unit="piece",
        min_order=5,
        bulk_discount_rules=[
            {"min_qty": 25, "discount_pct": 12},
            {"min_qty": 50, "discount_pct": 18},
        ]
    ))
    
    agent.add_product(Product(
        id="pb_poster_a3",
        name="A3 Poster (Matte/Glossy)",
        description="A3 size poster print on 200gsm paper.",
        category="printing",
        base_price=60,
        unit="piece",
        min_order=10,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 15},
            {"min_qty": 100, "discount_pct": 20},
        ]
    ))
    
    # ID Cards
    agent.add_product(Product(
        id="pb_idcard",
        name="PVC ID Card with Lanyard",
        description="Full-color PVC ID card with custom lanyard. Includes badge holder.",
        category="stationery",
        base_price=65,
        unit="piece",
        min_order=25,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 15},
            {"min_qty": 500, "discount_pct": 25},
        ]
    ))
    
    # Standees
    agent.add_product(Product(
        id="pb_standee",
        name="Roll-up Standee (3x6 ft)",
        description="Retractable roll-up standee with carrying case.",
        category="signage",
        base_price=1500,
        unit="piece",
        min_order=1,
        bulk_discount_rules=[
            {"min_qty": 5, "discount_pct": 10},
            {"min_qty": 10, "discount_pct": 15},
        ]
    ))
    
    # Stickers
    agent.add_product(Product(
        id="pb_sticker",
        name="Custom Die-Cut Sticker",
        description="Waterproof vinyl die-cut sticker, any shape.",
        category="stationery",
        base_price=15,
        unit="piece",
        min_order=50,
        bulk_discount_rules=[
            {"min_qty": 200, "discount_pct": 15},
            {"min_qty": 500, "discount_pct": 25},
        ]
    ))
    
    # Brochures
    agent.add_product(Product(
        id="pb_brochure",
        name="Tri-fold Brochure (A4)",
        description="Full-color tri-fold brochure on 170gsm art paper.",
        category="printing",
        base_price=18,
        unit="piece",
        min_order=100,
        bulk_discount_rules=[
            {"min_qty": 500, "discount_pct": 20},
            {"min_qty": 1000, "discount_pct": 30},
        ]
    ))
    
    # Upsell rules
    agent.add_upsell_rule("pb_banner_vinyl", "pb_standee", discount_pct=10)
    agent.add_upsell_rule("pb_idcard", "pb_sticker", discount_pct=8)
    agent.add_upsell_rule("pb_poster_a2", "pb_poster_a3", discount_pct=12)
    
    # Combo deals
    agent.add_combo_deal(
        name="Event Signage Pack",
        product_ids=["pb_banner_vinyl", "pb_standee", "pb_poster_a2"],
        combo_discount_pct=15
    )
    agent.add_combo_deal(
        name="Attendee Kit",
        product_ids=["pb_idcard", "pb_sticker", "pb_brochure"],
        combo_discount_pct=20
    )
    
    return agent
