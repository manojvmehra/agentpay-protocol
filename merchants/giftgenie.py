"""
GiftGenie - Gifts & stationery store
Demo merchant for AgentPay Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_catalog

COLORS = ["Red", "Blue", "Green", "Purple", "Black", "Gold", "Silver", "Rose Gold"]
CANDLE_SCENTS = ["Lavender", "Vanilla", "Rose", "Sandalwood", "Citrus", "Ocean Breeze", "Jasmine"]
CARD_OCCASIONS = ["Birthday", "Thank You", "Congratulations", "Farewell", "Welcome", "Festive", "Anniversary"]
CHOCOLATE_TYPES = ["Assorted", "Dark Chocolate", "Milk Chocolate", "Truffle", "Nutty", "Fruit & Nut"]
DRYFRUIT_TYPES = ["Almonds & Cashews", "Premium Mix", "Dates & Figs", "Pista Special", "Mixed Nuts", "Royal Selection"]


def create_giftgenie() -> MerchantAgent:
    agent = MerchantAgent(
        name="GiftGenie",
        description="Gifts, stationery, and hampers for events and corporate giveaways. Bulk personalization available.",
        categories=["gifts"],
        location="Bengaluru",
    )

    agent.add_product(Product(
        id="gg_notebook_a5_ruled",
        name="Notebook (A5, Ruled)",
        description="A5 ruled notebook with custom cover print.",
        category="gifts",
        base_price=80,
        unit="piece",
        min_order=25,
        bulk_discount_rules=[
            {"min_qty": 100, "discount_pct": 12},
            {"min_qty": 300, "discount_pct": 20},
        ]
    ))

    agent.add_product(Product(
        id="gg_chocolate_box_12",
        name="Chocolate Gift Box (12 pcs)",
        description="Assorted chocolate gift box, 12 pieces, custom wrap.",
        category="gifts",
        base_price=350,
        unit="box",
        min_order=20,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 10},
            {"min_qty": 150, "discount_pct": 16},
        ]
    ))

    add_catalog(agent, "gg", [
        {"name": "Notebook (A5, Dotted)", "category": "gifts", "base_price": 90, "unit": "piece",
         "description": "A5 dotted notebook in {variant} cover.",
         "min_order": 25, "bulk": [(100, 12), (300, 20)], "variants": COLORS},
        {"name": "Premium Hardcover Notebook", "category": "gifts", "base_price": 220, "unit": "piece",
         "description": "Hardcover notebook in {variant} with ribbon bookmark.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Ball Pen (Premium)", "category": "gifts", "base_price": 40, "unit": "piece",
         "description": "Premium metal-body ball pen in {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Metal Pen (Engraved)", "category": "gifts", "base_price": 150, "unit": "piece",
         "description": "Engraved metal pen in {variant}, gift-boxed.",
         "min_order": 25, "bulk": [(100, 12), (300, 18)], "variants": COLORS},
        {"name": "Daily Planner (Undated)", "category": "gifts", "base_price": 250, "unit": "piece",
         "description": "Undated daily planner in {variant} cover.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Desk Organizer (Metal Mesh)", "category": "gifts", "base_price": 350, "unit": "piece",
         "description": "Mesh desk organizer in {variant}.",
         "min_order": 15, "bulk": [(40, 10), (100, 15)], "variants": COLORS},
        {"name": "Desk Organizer (Wooden)", "category": "gifts", "base_price": 400, "unit": "piece",
         "description": "Wooden multi-compartment desk organizer.",
         "min_order": 15, "bulk": [(40, 10), (100, 15)]},
        {"name": "Photo Frame (Table)", "category": "gifts", "base_price": 200, "unit": "piece",
         "description": "Table photo frame, {variant} size.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": ["4x6 in", "5x7 in", "8x10 in"], "variant_step": 100},
        {"name": "Photo Frame (Wall Collage)", "category": "gifts", "base_price": 600, "unit": "piece",
         "description": "Multi-photo wall collage frame set.",
         "min_order": 10, "bulk": [(30, 8), (60, 12)]},
        {"name": "Plant Pot (Ceramic)", "category": "gifts", "base_price": 180, "unit": "piece",
         "description": "Ceramic plant pot in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Succulent Plant Gift Set", "category": "gifts", "base_price": 350, "unit": "piece",
         "description": "Succulent plant in decorative pot, ready to gift.",
         "min_order": 15, "bulk": [(40, 10), (100, 15)]},
        {"name": "Scented Candle", "category": "gifts", "base_price": 220, "unit": "piece",
         "description": "{variant}-scented soy candle in gift jar.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": CANDLE_SCENTS},
        {"name": "Bookmark (Metal)", "category": "gifts", "base_price": 45, "unit": "piece",
         "description": "Engraved metal bookmark in {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Coaster Set (4 pcs)", "category": "gifts", "base_price": 250, "unit": "set",
         "description": "Set of 4 custom coasters in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Fridge Magnet (Custom)", "category": "gifts", "base_price": 60, "unit": "piece",
         "description": "Custom-printed fridge magnet in {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Greeting Card (Custom)", "category": "gifts", "base_price": 40, "unit": "piece",
         "description": "{variant} themed custom greeting card.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": CARD_OCCASIONS},
        {"name": "Gift Wrap Sheet", "category": "gifts", "base_price": 25, "unit": "piece",
         "description": "Premium gift wrap sheet in {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Gift Hamper Box (Empty)", "category": "gifts", "base_price": 150, "unit": "piece",
         "description": "Decorative empty hamper box in {variant}, ready to fill.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Dry Fruits Gift Box", "category": "gifts", "base_price": 500, "unit": "box",
         "description": "{variant} dry fruits gift box, premium packaging.",
         "min_order": 15, "bulk": [(40, 10), (100, 16)], "variants": DRYFRUIT_TYPES},
        {"name": "Personalized Keychain Gift", "category": "gifts", "base_price": 90, "unit": "piece",
         "description": "Personalized engraved keychain in {variant}, gift-boxed.",
         "min_order": 25, "bulk": [(100, 12), (300, 18)], "variants": COLORS},
        {"name": "Corporate Gift Hamper", "category": "gifts", "base_price": 800, "unit": "piece",
         "description": "Curated corporate hamper — notebook, pen, chocolates, and a desk item.",
         "min_order": 10, "bulk": [(30, 8), (80, 14)]},
        {"name": "Diary (Executive)", "category": "gifts", "base_price": 300, "unit": "piece",
         "description": "Executive-style diary in {variant} leather-look cover.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Sticky Notes Set", "category": "gifts", "base_price": 60, "unit": "set",
         "description": "Assorted sticky notes set with custom cover.",
         "min_order": 30, "bulk": [(100, 12), (300, 18)]},
        {"name": "Highlighter Set (5 colors)", "category": "gifts", "base_price": 120, "unit": "set",
         "description": "Set of 5 pastel highlighters.",
         "min_order": 30, "bulk": [(100, 12), (300, 18)]},
        {"name": "Desk Calendar", "category": "gifts", "base_price": 150, "unit": "piece",
         "description": "Custom-printed desk calendar.",
         "min_order": 25, "bulk": [(75, 10), (200, 16)]},
        {"name": "Chocolate Gift Box (Variety Pack)", "category": "gifts", "base_price": 380, "unit": "box",
         "description": "{variant} variety gift box, 12 pieces, custom wrap.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": CHOCOLATE_TYPES},
        {"name": "Ribbon Spool (Decorative)", "category": "gifts", "base_price": 45, "unit": "piece",
         "description": "Decorative ribbon spool in {variant} for gift wrapping.",
         "min_order": 30, "bulk": [(100, 12), (300, 18)], "variants": COLORS},
    ])

    # Upsell rules
    agent.add_upsell_rule("gg_notebook_a5_ruled", "gg_ball_pen_premium_black", discount_pct=8)
    agent.add_upsell_rule("gg_chocolate_box_12", "gg_greeting_card_custom_thank_you", discount_pct=10)

    # Combo deals
    agent.add_combo_deal(
        name="Corporate Welcome Kit",
        product_ids=["gg_notebook_a5_ruled", "gg_ball_pen_premium_black", "gg_chocolate_box_12"],
        combo_discount_pct=15
    )
    agent.add_combo_deal(
        name="Festive Hamper Pack",
        product_ids=["gg_gift_hamper_box_empty_gold", "gg_chocolate_box_12", "gg_greeting_card_custom_festive"],
        combo_discount_pct=18
    )

    return agent
