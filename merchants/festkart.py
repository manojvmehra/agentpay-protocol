"""
FestKart - College fest merch & apparel store
Demo merchant for Hermes Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_catalog

COLORS = ["White", "Black", "Red", "Navy Blue", "Grey", "Maroon"]
PHONE_MODELS = ["iPhone 13", "iPhone 14", "iPhone 15", "Samsung S23", "Samsung S24", "OnePlus 11", "Redmi Note 13"]
POSTER_SIZES = ["A4", "A3", "A2", "A1"]


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
    
    # ── Expanded catalog: 160+ additional SKUs across apparel/accessories/merch ──
    add_catalog(agent, "fk", [
        {"name": "Round Neck T-Shirt (Cotton)", "category": "apparel", "base_price": 220, "unit": "piece",
         "description": "Soft 100% cotton round-neck tee in {variant}. Great base for custom prints.",
         "min_order": 10, "bulk": [(50, 10), (100, 15), (500, 20)], "variants": COLORS},
        {"name": "V-Neck T-Shirt (Cotton)", "category": "apparel", "base_price": 240, "unit": "piece",
         "description": "V-neck cotton tee in {variant}, slim fit.",
         "min_order": 10, "bulk": [(50, 10), (100, 15), (500, 20)], "variants": COLORS},
        {"name": "Polo T-Shirt (Pique Cotton)", "category": "apparel", "base_price": 380, "unit": "piece",
         "description": "Collared pique-cotton polo in {variant}, ideal for organizer/staff kits.",
         "min_order": 10, "bulk": [(25, 8), (50, 12), (100, 18)], "variants": COLORS},
        {"name": "Oversized T-Shirt (Streetwear Fit)", "category": "apparel", "base_price": 320, "unit": "piece",
         "description": "Drop-shoulder oversized tee in {variant} for a streetwear look.",
         "min_order": 10, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Full Sleeve T-Shirt", "category": "apparel", "base_price": 280, "unit": "piece",
         "description": "Full-sleeve cotton tee in {variant}.",
         "min_order": 10, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Tank Top (Sleeveless)", "category": "apparel", "base_price": 200, "unit": "piece",
         "description": "Sleeveless cotton tank top in {variant}, great for sports days.",
         "min_order": 10, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Zipper Hoodie", "category": "apparel", "base_price": 950, "unit": "piece",
         "description": "Fleece-lined zip-up hoodie in {variant}.",
         "min_order": 5, "bulk": [(25, 8), (50, 12)], "variants": COLORS},
        {"name": "Pullover Sweatshirt", "category": "apparel", "base_price": 750, "unit": "piece",
         "description": "Crew-neck pullover sweatshirt in {variant}.",
         "min_order": 5, "bulk": [(25, 8), (50, 12)], "variants": COLORS},
        {"name": "Bomber Jacket (Fest Edition)", "category": "apparel", "base_price": 1400, "unit": "piece",
         "description": "Lightweight bomber jacket in {variant} with custom back print.",
         "min_order": 5, "bulk": [(20, 8), (40, 12)], "variants": COLORS},
        {"name": "Varsity Jacket", "category": "apparel", "base_price": 1600, "unit": "piece",
         "description": "Varsity-style jacket in {variant} for core organizing team.",
         "min_order": 5, "bulk": [(20, 8), (40, 12)], "variants": COLORS},
        {"name": "Knit Scarf (Winter Fest)", "category": "apparel", "base_price": 220, "unit": "piece",
         "description": "Soft knit scarf in {variant} for winter-season fests.",
         "min_order": 10, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Ankle Socks (Pair)", "category": "apparel", "base_price": 80, "unit": "pair",
         "description": "Cotton ankle socks in {variant}, sold by the pair.",
         "min_order": 20, "bulk": [(100, 12), (300, 20)], "variants": COLORS},

        {"name": "Baseball Cap", "category": "accessories", "base_price": 190, "unit": "piece",
         "description": "Adjustable baseball cap in {variant} with embroidered logo.",
         "min_order": 20, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Bucket Hat", "category": "accessories", "base_price": 210, "unit": "piece",
         "description": "Cotton bucket hat in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Trucker Cap (Mesh Back)", "category": "accessories", "base_price": 200, "unit": "piece",
         "description": "Mesh-back trucker cap in {variant}, breathable fit.",
         "min_order": 20, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Beanie (Winter Cap)", "category": "accessories", "base_price": 160, "unit": "piece",
         "description": "Ribbed knit beanie in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Canvas Tote Bag", "category": "accessories", "base_price": 150, "unit": "piece",
         "description": "Eco-friendly canvas tote in {variant} with screen print.",
         "min_order": 25, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Drawstring Backpack", "category": "accessories", "base_price": 220, "unit": "piece",
         "description": "Lightweight drawstring backpack in {variant}.",
         "min_order": 25, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Silicone Wristband", "category": "accessories", "base_price": 20, "unit": "piece",
         "description": "Debossed silicone wristband in {variant}.",
         "min_order": 100, "bulk": [(500, 15), (1000, 25)], "variants": COLORS},
        {"name": "Tyvek Wristband (Tear-Proof)", "category": "accessories", "base_price": 18, "unit": "piece",
         "description": "Tamper-proof Tyvek paper wristband in {variant} for event entry.",
         "min_order": 100, "bulk": [(500, 15), (1000, 25)], "variants": COLORS},
        {"name": "Lanyard with ID Holder", "category": "accessories", "base_price": 45, "unit": "piece",
         "description": "Woven lanyard in {variant} with PVC ID holder.",
         "min_order": 50, "bulk": [(200, 12), (500, 20)], "variants": COLORS},

        {"name": "Metal Keychain", "category": "merchandise", "base_price": 60, "unit": "piece",
         "description": "Engraved metal keychain in {variant} finish.",
         "min_order": 25, "bulk": [(100, 12), (300, 18)], "variants": COLORS},
        {"name": "Acrylic Keychain", "category": "merchandise", "base_price": 45, "unit": "piece",
         "description": "Custom-shaped acrylic keychain in {variant}.",
         "min_order": 25, "bulk": [(100, 12), (300, 18)], "variants": COLORS},
        {"name": "Ceramic Mug (Custom Print)", "category": "merchandise", "base_price": 180, "unit": "piece",
         "description": "11oz ceramic mug in {variant} with full-color print.",
         "min_order": 20, "bulk": [(50, 10), (150, 15)], "variants": COLORS},
        {"name": "Phone Case (Custom Print)", "category": "merchandise", "base_price": 250, "unit": "piece",
         "description": "Custom-printed phone case for {variant}.",
         "min_order": 20, "bulk": [(50, 10), (100, 15)], "variants": PHONE_MODELS},
        {"name": "Vinyl Sticker Sheet", "category": "merchandise", "base_price": 30, "unit": "piece",
         "description": "Waterproof vinyl sticker sheet, custom designs.",
         "min_order": 50, "bulk": [(200, 15), (500, 25)]},
        {"name": "Poster Print (Fest Theme)", "category": "merchandise", "base_price": 90, "unit": "piece",
         "description": "Fest-themed poster print, {variant} size.",
         "min_order": 10, "bulk": [(50, 12), (100, 18)], "variants": POSTER_SIZES, "variant_step": 60},
        {"name": "Table Flag (Mini)", "category": "merchandise", "base_price": 120, "unit": "piece",
         "description": "Mini table flag in {variant} with custom emblem.",
         "min_order": 10, "bulk": [(50, 10), (100, 15)], "variants": COLORS},
        {"name": "Fest Flag (Large Fabric)", "category": "merchandise", "base_price": 450, "unit": "piece",
         "description": "Large fabric fest flag in {variant}, 3x5 ft.",
         "min_order": 5, "bulk": [(20, 10), (50, 15)], "variants": COLORS},
    ])

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
