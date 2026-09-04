"""
GlowMart - Beauty & personal care store (Nykaa-style)
Demo merchant for Hermes Protocol.

Beauty-advisor personality: upsell rules build out a skincare routine
(sunscreen->moisturizer, serum->face wash), and combo deals are framed as
routines/occasions (Morning Routine, Date Night Glam, Self Care Sunday).
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_fashion_catalog

SHADES = ["Red", "Coral", "Nude", "Pink", "Berry", "Brown", "Mauve", "Wine"]
SKIN_TONES = ["Fair", "Light", "Medium", "Tan", "Deep"]
SCENTS = ["Lavender", "Rose", "Sandalwood", "Citrus", "Vanilla", "Jasmine"]


def create_glowmart() -> MerchantAgent:
    agent = MerchantAgent(
        name="GlowMart",
        description=(
            "Your friendly beauty advisor — skincare, makeup, haircare, fragrances, bath & body, "
            "and wellness, with routines tailored to your skin type and trending ingredients called out."
        ),
        categories=["skincare", "makeup", "haircare", "fragrances", "bath-body", "wellness"],
        location="Mumbai",
    )

    items = []

    # ── Skincare ──
    for style, price in [("Daily Moisturizer", 299), ("Night Cream", 799), ("Gel Moisturizer", 449),
                          ("Deep Hydration Cream", 999), ("Anti-Aging Moisturizer", 1499)]:
        for size in ["50ml", "100ml"]:
            items.append({"name": style, "category": "skincare", "type": "moisturizer", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Matte Sunscreen SPF50", 399), ("Gel Sunscreen SPF30", 199),
                          ("Tinted Sunscreen SPF50", 599), ("Sunscreen Stick SPF40", 899)]:
        for size in ["30ml", "50ml"]:
            items.append({"name": style, "category": "skincare", "type": "sunscreen", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Vitamin C Serum", 599), ("Niacinamide Serum", 499), ("Hyaluronic Acid Serum", 799),
                          ("Retinol Serum", 1499), ("Salicylic Acid Serum", 999)]:
        for size in ["15ml", "30ml"]:
            items.append({"name": style, "category": "skincare", "type": "serum", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Foaming Face Wash", 149), ("Gel Face Wash", 249), ("Cream Face Wash", 299),
                          ("Charcoal Face Wash", 349), ("Salicylic Face Wash", 449)]:
        for size in ["100ml", "150ml"]:
            items.append({"name": style, "category": "skincare", "type": "face-wash", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Sheet Mask", 99), ("Clay Mask", 399), ("Charcoal Mask", 449),
                          ("Hydrating Mask", 499), ("Sleeping Mask", 599)]:
        items.append({"name": style, "category": "skincare", "type": "face-mask", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Hydrating Toner", 349), ("Exfoliating Toner", 449), ("Rose Water Toner", 199)]:
        for size in ["100ml", "200ml"]:
            items.append({"name": style, "category": "skincare", "type": "toner", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Under Eye Cream", 599), ("De-Puff Eye Gel", 499)]:
        items.append({"name": style, "category": "skincare", "type": "eye-cream", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Lip Balm", 149), ("Tinted Lip Balm", 199), ("Overnight Lip Mask", 349)]:
        for c in ["Vanilla", "Rose", "Berry"]:
            items.append({"name": style, "category": "skincare", "type": "lip-care", "base_price": price,
                           "color": c, "sizes": None, "description": f"{style}, {c} flavor."})

    for style, price in [("Face Oil (Rosehip)", 599), ("Face Oil (Argan)", 699), ("Face Oil (Jojoba)", 549)]:
        for size in ["15ml", "30ml"]:
            items.append({"name": style, "category": "skincare", "type": "face-oil", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    # ── Makeup ──
    for style, price in [("Matte Lipstick", 399), ("Glossy Lipstick", 349), ("Liquid Lipstick", 549), ("Satin Lipstick", 449)]:
        for shade in SHADES:
            items.append({"name": style, "category": "makeup", "type": "lipstick", "base_price": price,
                           "color": shade, "sizes": None, "description": f"{style} in {shade}."})

    for style, price in [("Liquid Foundation", 699), ("Matte Foundation", 799), ("BB Cream", 499)]:
        for tone in SKIN_TONES:
            items.append({"name": style, "category": "makeup", "type": "foundation", "base_price": price,
                           "color": tone, "sizes": None, "description": f"{style}, shade {tone}."})

    for style, price in [("Kajal Pencil", 149), ("Liquid Eyeliner", 299), ("Gel Eyeliner", 349)]:
        for c in ["Black", "Brown"]:
            items.append({"name": style, "category": "makeup", "type": "eyeliner", "base_price": price,
                           "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Volumizing Mascara", 399), ("Waterproof Mascara", 449)]:
        items.append({"name": style, "category": "makeup", "type": "mascara", "base_price": price,
                       "color": "Black", "sizes": None, "description": style})

    for style, price in [("Powder Blush", 349), ("Cream Blush", 399)]:
        for c in ["Peach", "Rose", "Coral"]:
            items.append({"name": style, "category": "makeup", "type": "blush", "base_price": price,
                           "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Compact Powder", 399), ("Loose Setting Powder", 449)]:
        for tone in ["Fair", "Medium", "Deep"]:
            items.append({"name": style, "category": "makeup", "type": "powder", "base_price": price,
                           "color": tone, "sizes": None, "description": f"{style}, shade {tone}."})

    # ── Haircare ──
    for style, price in [("Anti-Dandruff Shampoo", 249), ("Volumizing Shampoo", 349), ("Color Protect Shampoo", 449),
                          ("Keratin Shampoo", 599), ("Herbal Shampoo", 199)]:
        for size in ["200ml", "400ml"]:
            items.append({"name": style, "category": "haircare", "type": "shampoo", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Daily Conditioner", 299), ("Deep Conditioner", 449), ("Leave-In Conditioner", 399)]:
        for size in ["200ml", "400ml"]:
            items.append({"name": style, "category": "haircare", "type": "conditioner", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Coconut Hair Oil", 199), ("Argan Hair Oil", 599), ("Onion Hair Oil", 349), ("Almond Hair Oil", 299)]:
        for size in ["100ml", "200ml"]:
            items.append({"name": style, "category": "haircare", "type": "hair-oil", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Anti-Frizz Hair Serum", 449), ("Shine Hair Serum", 399)]:
        items.append({"name": style, "category": "haircare", "type": "hair-serum", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Deep Repair Hair Mask", 549), ("Hydrating Hair Mask", 499)]:
        items.append({"name": style, "category": "haircare", "type": "hair-mask", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Dry Shampoo", 399), ("Dry Shampoo (Travel Size)", 249)]:
        items.append({"name": style, "category": "haircare", "type": "dry-shampoo", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Hair Spray (Strong Hold)", 349), ("Hair Spray (Flexible Hold)", 299)]:
        items.append({"name": style, "category": "haircare", "type": "hair-styling", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Styling Hair Gel", 249), ("Texturizing Hair Gel", 299)]:
        items.append({"name": style, "category": "haircare", "type": "hair-styling", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    # ── Fragrances ──
    for style, price in [("Floral Eau de Parfum", 1499), ("Woody Eau de Parfum", 1799), ("Citrus Eau de Parfum", 1299),
                          ("Musk Eau de Parfum", 1999), ("Oriental Eau de Parfum", 2499)]:
        for size in ["30ml", "50ml", "100ml"]:
            items.append({"name": style, "category": "fragrances", "type": "perfume", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Body Spray", 349), ("Roll-On Deodorant", 199)]:
        for scent in SCENTS[:4]:
            items.append({"name": style, "category": "fragrances", "type": "deodorant", "base_price": price,
                           "color": scent, "sizes": None, "description": f"{style}, {scent} scent."})

    for style, price in [("Hydrating Body Mist", 449), ("Refreshing Body Mist", 399), ("Floral Body Mist", 499)]:
        items.append({"name": style, "category": "fragrances", "type": "body-mist", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for scent, price in [("Rose Attar", 799), ("Oudh Attar", 1299), ("Musk Attar", 999)]:
        items.append({"name": scent, "category": "fragrances", "type": "attar", "base_price": price,
                       "color": "", "sizes": None, "description": f"{scent}, alcohol-free oil perfume."})

    # ── Bath & Body ──
    for style, price in [("Daily Body Lotion", 249), ("Cocoa Butter Lotion", 399), ("Shea Butter Lotion", 449)]:
        for size in ["100ml", "200ml"]:
            items.append({"name": style, "category": "bath-body", "type": "body-lotion", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Moisturizing Body Wash", 299), ("Exfoliating Body Wash", 349), ("Foaming Body Wash", 249)]:
        for size in ["200ml", "400ml"]:
            items.append({"name": style, "category": "bath-body", "type": "body-wash", "base_price": price,
                           "color": "", "sizes": [size], "description": f"{style}, {size}."})

    for style, price in [("Handmade Soap", 149), ("Charcoal Soap", 199), ("Glycerin Soap", 129)]:
        for scent in SCENTS[:3]:
            items.append({"name": style, "category": "bath-body", "type": "soap", "base_price": price,
                           "color": scent, "sizes": None, "description": f"{style}, {scent}."})

    for style, price in [("Hand Cream", 199), ("Nourishing Hand Cream", 249)]:
        items.append({"name": style, "category": "bath-body", "type": "hand-cream", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Coffee Body Scrub", 349), ("Sugar Body Scrub", 399)]:
        items.append({"name": style, "category": "bath-body", "type": "body-scrub", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for scent, price in [("Lavender Bath Bomb", 199), ("Rose Bath Bomb", 199), ("Citrus Bath Bomb", 199)]:
        items.append({"name": scent, "category": "bath-body", "type": "bath-bomb", "base_price": price,
                       "color": "", "sizes": None, "description": scent})

    for style, price in [("Moisturizing Hand Wash", 149), ("Foaming Hand Wash", 179)]:
        items.append({"name": style, "category": "bath-body", "type": "hand-wash", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    # ── Wellness ──
    for style, price in [("Glossy Nail Polish", 149), ("Matte Nail Polish", 179)]:
        for shade in SHADES[:6]:
            items.append({"name": style, "category": "wellness", "type": "nail-polish", "base_price": price,
                           "color": shade, "sizes": None, "description": f"{style} in {shade}."})

    for style, price in [("Nail Care Kit", 449), ("Manicure Set", 599)]:
        items.append({"name": style, "category": "wellness", "type": "nail-care", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Daily Multivitamin", 599), ("Hair Skin Nails Multivitamin", 799)]:
        items.append({"name": style, "category": "wellness", "type": "supplement", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for style, price in [("Jade Face Roller", 399), ("Gua Sha Stone", 349)]:
        items.append({"name": style, "category": "wellness", "type": "face-tool", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    for scent, price in [("Lavender Essential Oil", 349), ("Tea Tree Essential Oil", 299),
                          ("Eucalyptus Essential Oil", 299), ("Peppermint Essential Oil", 329)]:
        items.append({"name": scent, "category": "wellness", "type": "essential-oil", "base_price": price,
                       "color": "", "sizes": None, "description": f"{scent}, 100% pure."})

    for style, price in [("Relaxing Bath Salts", 299), ("Detox Bath Salts", 349)]:
        items.append({"name": style, "category": "wellness", "type": "bath-salts", "base_price": price,
                       "color": "", "sizes": None, "description": style})

    add_fashion_catalog(agent, "gm", items)

    # ── Beauty-advisor upsell rules & routine combo deals ──
    agent.add_upsell_rule("gm_matte_sunscreen_spf50_30ml", "gm_daily_moisturizer_50ml", discount_pct=10)
    agent.add_upsell_rule("gm_vitamin_c_serum_15ml", "gm_foaming_face_wash_100ml", discount_pct=8)
    agent.add_upsell_rule("gm_matte_lipstick_red", "gm_liquid_foundation_medium", discount_pct=5)

    agent.add_combo_deal(
        name="Morning Routine",
        product_ids=["gm_foaming_face_wash_100ml", "gm_vitamin_c_serum_15ml", "gm_matte_sunscreen_spf50_30ml"],
        combo_discount_pct=15,
    )
    agent.add_combo_deal(
        name="Date Night Glam",
        product_ids=["gm_matte_lipstick_wine", "gm_liquid_foundation_medium", "gm_floral_eau_de_parfum_30ml"],
        combo_discount_pct=12,
    )
    agent.add_combo_deal(
        name="Self Care Sunday",
        product_ids=["gm_clay_mask", "gm_coffee_body_scrub", "gm_lavender_bath_bomb"],
        combo_discount_pct=20,
    )

    return agent
