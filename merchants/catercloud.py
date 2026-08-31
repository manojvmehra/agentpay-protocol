"""
CaterCloud - Event catering & food services
Demo merchant for AgentPay Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_catalog

CUISINES = ["North Indian", "South Indian", "Gujarati", "Punjabi", "Continental", "Rajasthani", "Bengali"]
NONVEG_TYPES = ["Chicken", "Mutton", "Fish", "Egg", "Prawn", "Kebab", "Biryani"]
SNACK_TYPES = ["Samosa", "Sandwich", "Momos", "Spring Roll", "Cutlet", "Pakora", "Dhokla", "Bhajiya"]
BEVERAGE_FLAVORS = ["Mango", "Orange", "Mixed Fruit", "Watermelon", "Pineapple", "Litchi", "Kiwi", "Blue Curacao"]
DESSERT_TYPES = ["Gulab Jamun", "Ice Cream Cup", "Cupcake", "Brownie", "Pastry", "Rasgulla", "Kheer", "Halwa"]
COLD_DRINK_FLAVORS = ["Cola", "Lemon", "Orange", "Mixed Fruit", "Ginger Ale", "Soda"]
BREAKFAST_TYPES = ["Poha", "Idli-Sambhar", "Upma", "Paratha", "Sandwich", "Cornflakes", "Dosa", "Uttapam"]
MIDNIGHT_TYPES = ["Maggie", "Sandwich", "Tea + Biscuit", "Soup", "Bhel"]


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
    
    # ── Expanded catalog: 150+ additional SKUs across food/beverages/catering ──
    add_catalog(agent, "cc", [
        {"name": "Veg Thali Lunch Box", "category": "food", "base_price": 140, "unit": "plate",
         "description": "{variant} style veg thali — rice, rotis, dal, sabzi, salad, pickle.",
         "min_order": 25, "bulk": [(100, 10), (250, 15), (500, 20)], "variants": CUISINES},
        {"name": "Non-Veg Thali Lunch Box", "category": "food", "base_price": 190, "unit": "plate",
         "description": "Thali with {variant} curry, rice, rotis, dal, salad.",
         "min_order": 25, "bulk": [(100, 8), (250, 12), (500, 18)], "variants": NONVEG_TYPES},
        {"name": "Jain Lunch Box", "category": "food", "base_price": 150, "unit": "plate",
         "description": "{variant} style Jain thali — no onion, no garlic, no root vegetables.",
         "min_order": 25, "bulk": [(100, 10), (250, 15), (500, 20)], "variants": CUISINES},
        {"name": "Mini Snack Box", "category": "food", "base_price": 60, "unit": "plate",
         "description": "{variant} snack box, packed fresh.",
         "min_order": 50, "bulk": [(100, 10), (300, 15)], "variants": SNACK_TYPES},
        {"name": "Party Finger Food Platter", "category": "food", "base_price": 220, "unit": "plate",
         "description": "Assorted finger food platter featuring {variant}.",
         "min_order": 25, "bulk": [(50, 8), (100, 12)], "variants": SNACK_TYPES},
        {"name": "Breakfast Combo", "category": "food", "base_price": 100, "unit": "plate",
         "description": "{variant} breakfast combo with a hot beverage.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": BREAKFAST_TYPES},
        {"name": "Midnight Snack Pack", "category": "food", "base_price": 90, "unit": "plate",
         "description": "{variant} — perfect for late-night hackathon/event breaks.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": MIDNIGHT_TYPES},
        {"name": "Cold Drink (500ml)", "category": "beverages", "base_price": 30, "unit": "bottle",
         "description": "Chilled {variant} soft drink, 500ml bottle.",
         "min_order": 50, "bulk": [(200, 10), (500, 18)], "variants": COLD_DRINK_FLAVORS},
        {"name": "Mocktail (Glass)", "category": "beverages", "base_price": 60, "unit": "glass",
         "description": "Freshly made {variant} mocktail, served chilled.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": BEVERAGE_FLAVORS},
        {"name": "Lassi (Glass)", "category": "beverages", "base_price": 45, "unit": "glass",
         "description": "{variant} lassi, served chilled.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": ["Sweet", "Salted", "Mango", "Rose"]},
        {"name": "Buttermilk (Glass)", "category": "beverages", "base_price": 25, "unit": "glass",
         "description": "Spiced chilled buttermilk (chaas).",
         "min_order": 50, "bulk": [(200, 10), (500, 18)]},
        {"name": "Filter Coffee (Cup)", "category": "beverages", "base_price": 25, "unit": "cup",
         "description": "South Indian filter coffee, freshly brewed.",
         "min_order": 50, "bulk": [(200, 10), (500, 18)]},
        {"name": "Coffee Station (per hour)", "category": "beverages", "base_price": 3200, "unit": "hour",
         "description": "Live coffee station with barista, serves up to 150 people/hr.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Juice Bar (per hour)", "category": "beverages", "base_price": 3500, "unit": "hour",
         "description": "Live fresh juice bar with 4 flavors, serves up to 150 people/hr.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Dessert Counter Item", "category": "food", "base_price": 50, "unit": "plate",
         "description": "{variant}, served fresh from the dessert counter.",
         "min_order": 50, "bulk": [(150, 10), (400, 15)], "variants": DESSERT_TYPES},
        {"name": "Non-Veg Buffet (per person)", "category": "catering", "base_price": 450, "unit": "person",
         "description": "Full non-veg buffet: 3 starters, 2 mains, rice, rotis, dal, 2 desserts, beverages.",
         "min_order": 50, "bulk": [(100, 10), (250, 15), (500, 20)]},
        {"name": "Premium Buffet (per person)", "category": "catering", "base_price": 600, "unit": "person",
         "description": "Premium multi-cuisine buffet with live counters and dessert bar.",
         "min_order": 50, "bulk": [(100, 10), (250, 15), (500, 20)]},
        {"name": "Jain Buffet (per person)", "category": "catering", "base_price": 380, "unit": "person",
         "description": "Full Jain buffet — no onion, no garlic, no root vegetables.",
         "min_order": 50, "bulk": [(100, 10), (250, 15), (500, 20)]},
        {"name": "Live Dosa Counter (per hour)", "category": "catering", "base_price": 4000, "unit": "hour",
         "description": "Live dosa-making counter with 2 chefs, serves up to 120 people/hr.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Live Pasta Counter (per hour)", "category": "catering", "base_price": 4200, "unit": "hour",
         "description": "Live pasta counter with 3 sauce options.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Live Chaat Counter (per hour)", "category": "catering", "base_price": 3500, "unit": "hour",
         "description": "Live chaat counter — pani puri, bhel, sev puri.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Ice Cream Counter (per hour)", "category": "catering", "base_price": 3000, "unit": "hour",
         "description": "Live ice cream counter with 6 flavors and toppings bar.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Birthday/Celebration Party Pack (per person)", "category": "catering", "base_price": 250, "unit": "person",
         "description": "Snacks, cake slice, and a mocktail per person — great for milestone celebrations.",
         "min_order": 20, "bulk": [(50, 10), (100, 15)]},
        {"name": "High Tea Combo", "category": "food", "base_price": 180, "unit": "plate",
         "description": "{variant}-style high tea combo with finger foods and a hot beverage.",
         "min_order": 25, "bulk": [(75, 10), (200, 15)], "variants": ["English", "Indian", "Continental", "Fusion", "Royal"]},
        {"name": "BBQ/Grill Counter (per hour)", "category": "catering", "base_price": 4500, "unit": "hour",
         "description": "Live BBQ/grill counter with 2 chefs, veg and non-veg options.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Chinese Live Counter (per hour)", "category": "catering", "base_price": 4000, "unit": "hour",
         "description": "Live wok-tossed Chinese counter — noodles, fried rice, manchurian.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Live Uttapam Counter (per hour)", "category": "catering", "base_price": 3800, "unit": "hour",
         "description": "Live South Indian uttapam counter.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Paan Counter (per hour)", "category": "catering", "base_price": 2500, "unit": "hour",
         "description": "Live paan counter with assorted fillings.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)]},
        {"name": "Popcorn/Cotton Candy Counter", "category": "catering", "base_price": 2200, "unit": "hour",
         "description": "Live {variant} counter, unlimited servings.",
         "min_order": 2, "bulk": [(4, 10), (8, 15)], "variants": ["Popcorn", "Cotton Candy", "Both"]},
        {"name": "Milkshake (Glass)", "category": "beverages", "base_price": 70, "unit": "glass",
         "description": "Thick {variant} milkshake, served chilled.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": BEVERAGE_FLAVORS},
        {"name": "Energy Drink (Can)", "category": "beverages", "base_price": 60, "unit": "can",
         "description": "Chilled {variant} energy drink can.",
         "min_order": 50, "bulk": [(200, 10), (500, 18)], "variants": COLD_DRINK_FLAVORS},
        {"name": "Packaged Snack Pack", "category": "food", "base_price": 25, "unit": "pack",
         "description": "{variant} single-serve packaged snack.",
         "min_order": 50, "bulk": [(200, 12), (500, 20)], "variants": ["Chips", "Namkeen", "Popcorn", "Trail Mix", "Roasted Nuts"]},
        {"name": "Fruit Bowl (Cut Fruits)", "category": "food", "base_price": 90, "unit": "bowl",
         "description": "Seasonal cut fruit bowl.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)]},
        {"name": "Salad Bowl", "category": "food", "base_price": 80, "unit": "bowl",
         "description": "{variant} salad bowl, freshly tossed.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": ["Greek", "Caesar", "Sprouts", "Fruit", "Veg Mix"]},
        {"name": "Soup (Cup)", "category": "food", "base_price": 60, "unit": "cup",
         "description": "{variant} soup, served hot.",
         "min_order": 30, "bulk": [(100, 10), (250, 15)], "variants": ["Tomato", "Sweet Corn", "Manchow", "Hot & Sour", "Mushroom"]},
        {"name": "Ice Cream Tub (Party Pack)", "category": "food", "base_price": 350, "unit": "tub",
         "description": "{variant} ice cream party tub.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": ["Vanilla", "Chocolate", "Strawberry", "Butterscotch", "Mixed"]},
        {"name": "Cake (per kg)", "category": "food", "base_price": 600, "unit": "kg",
         "description": "{variant} cake, freshly baked.",
         "min_order": 2, "bulk": [(5, 8), (15, 12)], "variants": ["Chocolate", "Vanilla", "Red Velvet", "Butterscotch", "Black Forest"]},
        {"name": "Mineral Water Can (1L)", "category": "beverages", "base_price": 25, "unit": "can",
         "description": "Sealed 1L mineral water can.",
         "min_order": 50, "bulk": [(200, 10), (500, 18)]},
        {"name": "Energy Bar/Granola Pack", "category": "food", "base_price": 40, "unit": "pack",
         "description": "{variant} energy bar, individually wrapped.",
         "min_order": 30, "bulk": [(100, 12), (300, 18)], "variants": ["Oats & Honey", "Choco Chip", "Nuts & Berries", "Peanut Butter"]},
    ])

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
