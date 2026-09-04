"""
SportStar - Sports & fitness gear store
Demo merchant for Hermes Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_catalog

COLORS = ["Black", "Red", "Blue", "Green", "Yellow", "Grey", "White", "Orange"]
SIZES = ["S", "M", "L", "XL", "XXL"]


def create_sportstar() -> MerchantAgent:
    agent = MerchantAgent(
        name="SportStar",
        description="Sports gear, fitness accessories, and event trophies. Bulk pricing for tournaments & fests.",
        categories=["sports"],
        location="Bengaluru",
    )

    agent.add_product(Product(
        id="ss_gym_bottle",
        name="Gym Shaker Bottle",
        description="700ml gym shaker bottle with mixer ball.",
        category="sports",
        base_price=150,
        unit="piece",
        min_order=20,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 10},
            {"min_qty": 150, "discount_pct": 16},
        ]
    ))

    agent.add_product(Product(
        id="ss_yoga_mat_6mm",
        name="Yoga Mat (6mm)",
        description="Non-slip 6mm yoga mat with carry strap.",
        category="sports",
        base_price=400,
        unit="piece",
        min_order=15,
        bulk_discount_rules=[
            {"min_qty": 40, "discount_pct": 10},
            {"min_qty": 100, "discount_pct": 16},
        ]
    ))

    add_catalog(agent, "ss", [
        {"name": "Sports Water Bottle", "category": "sports", "base_price": 120, "unit": "piece",
         "description": "1L sports water bottle in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Resistance Band (Light)", "category": "sports", "base_price": 100, "unit": "piece",
         "description": "Light-tension resistance band in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Resistance Band (Heavy)", "category": "sports", "base_price": 150, "unit": "piece",
         "description": "Heavy-tension resistance band in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Yoga Mat (10mm)", "category": "sports", "base_price": 600, "unit": "piece",
         "description": "Extra-cushioned 10mm yoga mat in {variant}.",
         "min_order": 15, "bulk": [(40, 10), (100, 16)], "variants": COLORS},
        {"name": "Skipping Rope", "category": "sports", "base_price": 120, "unit": "piece",
         "description": "Adjustable speed skipping rope in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Sports Wristband (Sweatband)", "category": "sports", "base_price": 40, "unit": "piece",
         "description": "Terry cloth sweatband in {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Headband (Sports)", "category": "sports", "base_price": 45, "unit": "piece",
         "description": "Elastic sports headband in {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Gym Towel", "category": "sports", "base_price": 150, "unit": "piece",
         "description": "Quick-dry gym towel in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Protein Shaker (700ml)", "category": "sports", "base_price": 180, "unit": "piece",
         "description": "Leak-proof protein shaker in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Arm Sleeve (Compression)", "category": "sports", "base_price": 200, "unit": "piece",
         "description": "Compression arm sleeve in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Knee Cap (Compression)", "category": "sports", "base_price": 250, "unit": "piece",
         "description": "Compression knee support, size {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": SIZES},
        {"name": "Ankle Support", "category": "sports", "base_price": 200, "unit": "piece",
         "description": "Elastic ankle support brace, size {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": SIZES},
        {"name": "Shuttlecock (Nylon, Box of 10)", "category": "sports", "base_price": 300, "unit": "box",
         "description": "Nylon shuttlecocks, box of 10, tournament grade.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)]},
        {"name": "Shuttlecock (Feather, Box of 10)", "category": "sports", "base_price": 600, "unit": "box",
         "description": "Feather shuttlecocks, box of 10, competition grade.",
         "min_order": 10, "bulk": [(30, 8), (80, 14)]},
        {"name": "Cricket Ball (Leather)", "category": "sports", "base_price": 350, "unit": "piece",
         "description": "Match-grade leather cricket ball.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)]},
        {"name": "Cricket Ball (Tennis)", "category": "sports", "base_price": 60, "unit": "piece",
         "description": "Tennis cricket ball for casual matches.",
         "min_order": 20, "bulk": [(60, 12), (150, 18)]},
        {"name": "Football (Size 5)", "category": "sports", "base_price": 500, "unit": "piece",
         "description": "Match-size 5 football.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)]},
        {"name": "Football (Size 4)", "category": "sports", "base_price": 400, "unit": "piece",
         "description": "Youth-size 4 football.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)]},
        {"name": "Basketball", "category": "sports", "base_price": 550, "unit": "piece",
         "description": "Standard size-7 basketball.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)]},
        {"name": "Volleyball", "category": "sports", "base_price": 450, "unit": "piece",
         "description": "Standard match volleyball.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)]},
        {"name": "Frisbee (Flying Disc)", "category": "sports", "base_price": 150, "unit": "piece",
         "description": "Flying disc in {variant} for outdoor games.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Medal (Custom)", "category": "sports", "base_price": 80, "unit": "piece",
         "description": "{variant} custom medal with ribbon.",
         "min_order": 25, "bulk": [(100, 12), (300, 18)], "variants": ["Gold", "Silver", "Bronze"]},
        {"name": "Trophy (Small)", "category": "sports", "base_price": 250, "unit": "piece",
         "description": "Small custom-engraved trophy.",
         "min_order": 5, "bulk": [(20, 10), (50, 15)]},
        {"name": "Trophy (Medium)", "category": "sports", "base_price": 450, "unit": "piece",
         "description": "Medium custom-engraved trophy.",
         "min_order": 5, "bulk": [(15, 10), (40, 15)]},
        {"name": "Trophy (Large)", "category": "sports", "base_price": 800, "unit": "piece",
         "description": "Large championship trophy.",
         "min_order": 2, "bulk": [(10, 8), (25, 12)]},
        {"name": "Sports Cap", "category": "sports", "base_price": 150, "unit": "piece",
         "description": "Breathable sports cap in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Sports Bag (Duffel)", "category": "sports", "base_price": 700, "unit": "piece",
         "description": "Duffel sports bag in {variant} with shoe compartment.",
         "min_order": 10, "bulk": [(30, 8), (80, 14)], "variants": COLORS},
        {"name": "Whistle (Referee)", "category": "sports", "base_price": 60, "unit": "piece",
         "description": "Referee whistle with lanyard.",
         "min_order": 20, "bulk": [(50, 12), (150, 18)]},
        {"name": "Table Tennis Bat", "category": "sports", "base_price": 300, "unit": "piece",
         "description": "Table tennis bat in {variant} with rubber grip.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)], "variants": COLORS},
        {"name": "Table Tennis Ball (Box of 6)", "category": "sports", "base_price": 90, "unit": "box",
         "description": "Competition-grade table tennis balls, box of 6.",
         "min_order": 15, "bulk": [(40, 10), (100, 16)]},
        {"name": "Badminton Racket", "category": "sports", "base_price": 450, "unit": "piece",
         "description": "Lightweight badminton racket in {variant} with cover.",
         "min_order": 10, "bulk": [(30, 8), (80, 14)], "variants": COLORS},
        {"name": "Hockey Stick", "category": "sports", "base_price": 650, "unit": "piece",
         "description": "Composite hockey stick, standard length.",
         "min_order": 10, "bulk": [(30, 8), (80, 14)]},
        {"name": "Boxing Gloves", "category": "sports", "base_price": 550, "unit": "pair",
         "description": "Training boxing gloves, size {variant}.",
         "min_order": 10, "bulk": [(30, 10), (80, 16)], "variants": SIZES},
        {"name": "Gym Gloves", "category": "sports", "base_price": 180, "unit": "pair",
         "description": "Padded gym workout gloves, size {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": SIZES},
    ])

    # Upsell rules
    agent.add_upsell_rule("ss_gym_bottle", "ss_gym_towel_black", discount_pct=8)
    agent.add_upsell_rule("ss_yoga_mat_6mm", "ss_resistance_band_light_black", discount_pct=10)

    # Combo deals
    agent.add_combo_deal(
        name="Sports Day Starter Kit",
        product_ids=["ss_gym_bottle", "ss_sports_cap_black", "ss_medal_custom_gold"],
        combo_discount_pct=15
    )
    agent.add_combo_deal(
        name="Tournament Winner Pack",
        product_ids=["ss_trophy_medium", "ss_medal_custom_gold", "ss_football_size_5"],
        combo_discount_pct=12
    )

    return agent
