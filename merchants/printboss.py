"""
PrintBoss - Printing & signage services
Demo merchant for AgentPay Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_catalog

BANNER_SIZES = ["3x4 ft", "4x6 ft", "4x8 ft", "6x10 ft", "8x12 ft", "10x15 ft"]
PRINT_SIZES = ["A3", "A2", "A1", "2x3 ft", "3x4 ft", "4x6 ft"]
PHOTO_SIZES = ["4x6 in", "5x7 in", "8x10 in", "A4", "A3", "A2"]
PAPER_TYPES = ["80gsm", "130gsm", "170gsm", "250gsm", "300gsm", "350gsm"]
CARD_FINISHES = ["Matte", "Glossy", "Textured", "Metallic", "Recycled Kraft", "Pearl"]
CERT_FINISHES = ["Matte", "Glossy", "Textured Cream", "Gold Foil", "Silver Foil", "Embossed"]
NAMEPLATE_MATERIALS = ["Acrylic", "Wood", "Metal", "Glass", "Laminated", "Marble"]
POSTER_SIZES = ["A4", "A3", "A2", "A1", "A0", "A00 (Jumbo)"]


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
    
    # ── Expanded catalog: 150+ additional SKUs across printing/signage/stationery ──
    add_catalog(agent, "pb", [
        {"name": "Flex Banner (Outdoor)", "category": "signage", "base_price": 700, "unit": "piece",
         "description": "Weatherproof outdoor flex banner, {variant}.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": BANNER_SIZES, "variant_step": 300},
        {"name": "Mesh Banner (Wind-Resistant)", "category": "signage", "base_price": 850, "unit": "piece",
         "description": "Perforated mesh banner for windy outdoor spots, {variant}.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": BANNER_SIZES, "variant_step": 350},
        {"name": "Backdrop Banner (Stage)", "category": "signage", "base_price": 2200, "unit": "piece",
         "description": "Large stage backdrop banner, {variant}.",
         "min_order": 1, "bulk": [(3, 8), (8, 12)], "variants": BANNER_SIZES, "variant_step": 600},
        {"name": "Pop-up Standee", "category": "signage", "base_price": 1300, "unit": "piece",
         "description": "Curved pop-up display standee with carry case.",
         "min_order": 1, "bulk": [(5, 10), (10, 15)]},
        {"name": "X-Banner Stand", "category": "signage", "base_price": 1100, "unit": "piece",
         "description": "Portable X-frame banner stand.",
         "min_order": 1, "bulk": [(5, 10), (10, 15)]},
        {"name": "L-Banner Stand", "category": "signage", "base_price": 1250, "unit": "piece",
         "description": "L-shaped floor banner stand.",
         "min_order": 1, "bulk": [(5, 10), (10, 15)]},
        {"name": "Foam Board Print (5mm)", "category": "printing", "base_price": 350, "unit": "piece",
         "description": "5mm foam board mounted print, {variant}.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": PRINT_SIZES, "variant_step": 150},
        {"name": "Acrylic Print (Photo)", "category": "printing", "base_price": 900, "unit": "piece",
         "description": "Photo print face-mounted on acrylic, {variant}.",
         "min_order": 1, "bulk": [(5, 8), (15, 12)], "variants": PRINT_SIZES, "variant_step": 300},
        {"name": "Canvas Print (Gallery Wrap)", "category": "printing", "base_price": 750, "unit": "piece",
         "description": "Gallery-wrapped canvas print, {variant}.",
         "min_order": 1, "bulk": [(5, 8), (15, 12)], "variants": PRINT_SIZES, "variant_step": 250},
        {"name": "Photo Print (Glossy)", "category": "printing", "base_price": 15, "unit": "piece",
         "description": "Glossy photo print, {variant}.",
         "min_order": 20, "bulk": [(100, 15), (300, 22)], "variants": PHOTO_SIZES, "variant_step": 20},
        {"name": "Poster Print (Custom)", "category": "printing", "base_price": 60, "unit": "piece",
         "description": "Custom poster print, {variant} size, matte or glossy finish.",
         "min_order": 5, "bulk": [(25, 12), (50, 18)], "variants": POSTER_SIZES, "variant_step": 80},
        {"name": "Visiting Card (Pack of 100)", "category": "stationery", "base_price": 250, "unit": "pack",
         "description": "Premium visiting cards, {variant} finish, pack of 100.",
         "min_order": 1, "bulk": [(5, 10), (15, 18)], "variants": CARD_FINISHES},
        {"name": "Certificate Print (Premium)", "category": "stationery", "base_price": 25, "unit": "piece",
         "description": "Premium certificate print, {variant}.",
         "min_order": 25, "bulk": [(100, 15), (300, 22)], "variants": CERT_FINISHES},
        {"name": "Name Plate (Desk)", "category": "stationery", "base_price": 350, "unit": "piece",
         "description": "Desk name plate, {variant} finish.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": NAMEPLATE_MATERIALS},
        {"name": "Name Plate (Door)", "category": "stationery", "base_price": 500, "unit": "piece",
         "description": "Door name plate, {variant} finish.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": NAMEPLATE_MATERIALS},
        {"name": "Table Tent Card", "category": "stationery", "base_price": 20, "unit": "piece",
         "description": "Table tent card, {variant}.",
         "min_order": 20, "bulk": [(100, 15), (300, 22)], "variants": ["3x4 in", "4x6 in", "5x7 in"]},
        {"name": "Flyer (Single Side)", "category": "printing", "base_price": 8, "unit": "piece",
         "description": "Single-side flyer print, {variant} paper.",
         "min_order": 100, "bulk": [(500, 20), (1000, 30)], "variants": PAPER_TYPES},
        {"name": "Flyer (Double Side)", "category": "printing", "base_price": 12, "unit": "piece",
         "description": "Double-side flyer print, {variant} paper.",
         "min_order": 100, "bulk": [(500, 20), (1000, 30)], "variants": PAPER_TYPES},
        {"name": "Brochure (Bi-fold)", "category": "printing", "base_price": 20, "unit": "piece",
         "description": "Bi-fold brochure, {variant} paper.",
         "min_order": 100, "bulk": [(500, 20), (1000, 30)], "variants": PAPER_TYPES},
        {"name": "Letterhead Print", "category": "stationery", "base_price": 6, "unit": "piece",
         "description": "Custom letterhead print, {variant} paper.",
         "min_order": 100, "bulk": [(500, 20), (1000, 30)], "variants": PAPER_TYPES},
        {"name": "Envelope (Custom Print)", "category": "stationery", "base_price": 5, "unit": "piece",
         "description": "Custom-printed envelope, {variant} size.",
         "min_order": 100, "bulk": [(500, 20), (1000, 30)], "variants": ["DL", "C5", "C4", "A4", "Custom"]},
        {"name": "Backdrop Print (Photo Booth)", "category": "signage", "base_price": 1800, "unit": "piece",
         "description": "Photo booth backdrop print, {variant}.",
         "min_order": 1, "bulk": [(3, 8), (8, 12)], "variants": BANNER_SIZES, "variant_step": 400},
        {"name": "Wall Cling Print", "category": "signage", "base_price": 300, "unit": "piece",
         "description": "Removable wall cling print, {variant}.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": PRINT_SIZES, "variant_step": 100},
        {"name": "Window Vinyl Print", "category": "signage", "base_price": 280, "unit": "piece",
         "description": "Window vinyl decal print, {variant}.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)], "variants": PRINT_SIZES, "variant_step": 100},
        {"name": "Menu Card Print", "category": "stationery", "base_price": 15, "unit": "piece",
         "description": "Restaurant/event menu card, {variant} paper.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": PAPER_TYPES},
        {"name": "Invitation Card", "category": "printing", "base_price": 18, "unit": "piece",
         "description": "Event invitation card, {variant} finish.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": CERT_FINISHES},
        {"name": "Foam Board Cutout (Standee Shape)", "category": "signage", "base_price": 2500, "unit": "piece",
         "description": "Custom-cut foam board standee cutout.",
         "min_order": 1, "bulk": [(3, 8), (8, 12)]},
        {"name": "Danglers (Ceiling Hanging)", "category": "signage", "base_price": 60, "unit": "piece",
         "description": "Ceiling-hanging dangler print for aisle/booth branding.",
         "min_order": 20, "bulk": [(100, 12), (300, 18)]},
        {"name": "Table Cover Print", "category": "signage", "base_price": 450, "unit": "piece",
         "description": "Branded table cover print, fitted.",
         "min_order": 5, "bulk": [(20, 10), (50, 15)]},
        {"name": "Car Sticker/Wrap Print", "category": "signage", "base_price": 500, "unit": "piece",
         "description": "Custom car sticker or partial wrap print.",
         "min_order": 1, "bulk": [(5, 8), (15, 12)]},
        {"name": "Rubber Stamp", "category": "stationery", "base_price": 150, "unit": "piece",
         "description": "Self-inking custom rubber stamp.",
         "min_order": 1, "bulk": [(10, 10), (25, 15)]},
        {"name": "Custom Badge (Printed)", "category": "stationery", "base_price": 20, "unit": "piece",
         "description": "Printed paper/plastic name badge.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)]},
        {"name": "ID Card (Basic, No Lanyard)", "category": "stationery", "base_price": 35, "unit": "piece",
         "description": "Basic PVC ID card print without lanyard.",
         "min_order": 25, "bulk": [(100, 15), (500, 25)]},
        {"name": "RFID Access Card", "category": "stationery", "base_price": 85, "unit": "piece",
         "description": "RFID-enabled printed access card.",
         "min_order": 25, "bulk": [(100, 15), (500, 25)]},
        {"name": "Event Wristband Print (Paper)", "category": "stationery", "base_price": 12, "unit": "piece",
         "description": "Printed paper event wristband.",
         "min_order": 100, "bulk": [(500, 18), (1000, 25)]},
        {"name": "Photo ID Lanyard Card", "category": "stationery", "base_price": 55, "unit": "piece",
         "description": "Printed photo ID card with lanyard clip.",
         "min_order": 25, "bulk": [(100, 15), (500, 25)]},
        {"name": "Standee Cutout (Character)", "category": "signage", "base_price": 2200, "unit": "piece",
         "description": "Life-size custom character cutout standee.",
         "min_order": 1, "bulk": [(3, 8), (8, 12)]},
        {"name": "Digital Print on Fabric", "category": "printing", "base_price": 650, "unit": "piece",
         "description": "Digital print on fabric, {variant}.",
         "min_order": 1, "bulk": [(5, 8), (15, 12)], "variants": PRINT_SIZES, "variant_step": 200},
        {"name": "3D Lenticular Print", "category": "printing", "base_price": 250, "unit": "piece",
         "description": "3D lenticular print with depth/motion effect, {variant}.",
         "min_order": 5, "bulk": [(20, 10), (50, 15)], "variants": PHOTO_SIZES, "variant_step": 60},
        {"name": "Custom Rubber Keychain Print", "category": "stationery", "base_price": 55, "unit": "piece",
         "description": "Custom-shaped rubber keychain print.",
         "min_order": 25, "bulk": [(100, 12), (300, 18)]},
        {"name": "Embossed Business Card (Pack of 100)", "category": "stationery", "base_price": 450, "unit": "pack",
         "description": "Embossed premium business cards, {variant}, pack of 100.",
         "min_order": 1, "bulk": [(5, 10), (15, 18)], "variants": CARD_FINISHES},
    ])

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
