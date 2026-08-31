"""
StyleBazaar - Fashion & lifestyle store (Myntra-style)
Demo merchant for AgentPay Protocol.

Unlike the other event-supply stores, StyleBazaar sells individual retail
items (min_order=1) with structured size/color attributes, and its combo
deals are framed as styled outfit suggestions rather than event kits — the
"friendly stylist" personality shows up in its description, upsell rules,
and combo deals.
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_fashion_catalog

COLORS = ["White", "Black", "Navy", "Grey", "Sky Blue", "Red", "Olive", "Maroon", "Beige", "Mustard"]
CLOTHING_SIZES = ["S", "M", "L", "XL", "XXL"]
WOMEN_SIZES = ["XS", "S", "M", "L", "XL"]
MEN_JEANS_SIZES = ["28", "30", "32", "34", "36"]
WOMEN_JEANS_SIZES = ["26", "28", "30", "32", "34"]
SHOE_SIZES = ["7", "8", "9", "10", "11"]
BELT_SIZES = ["S", "M", "L"]


def _color(i: int) -> str:
    return COLORS[i % len(COLORS)]


def create_stylebazaar() -> MerchantAgent:
    agent = MerchantAgent(
        name="StyleBazaar",
        description=(
            "Your friendly neighborhood fashion stylist — shirts, tees, jeans, dresses, kurtas, "
            "shoes and bags for men and women, with outfit combos and styling suggestions built in."
        ),
        categories=["men", "women", "accessories"],
        location="Mumbai",
    )

    # ── Men: Formal Shirts ──
    formal_shirts = [
        "Slim Fit Formal Shirt", "Classic Fit Formal Shirt", "Checked Formal Shirt",
        "Striped Formal Shirt", "Oxford Formal Shirt", "Linen Formal Shirt",
        "Formal Shirt (Spread Collar)", "Premium Cotton Formal Shirt",
    ]
    formal_shirt_prices = [899, 849, 949, 949, 1099, 1299, 899, 1199]

    # ── Men: Casual Shirts ──
    casual_shirts = [
        "Casual Check Shirt", "Denim Shirt", "Printed Casual Shirt",
        "Flannel Shirt", "Linen Casual Shirt", "Chambray Shirt",
    ]
    casual_shirt_prices = [799, 1099, 849, 999, 1199, 899]

    # ── Men: T-Shirts ──
    tshirts = [
        "Crew Neck T-Shirt", "V-Neck T-Shirt", "Polo T-Shirt", "Graphic Print T-Shirt",
        "Henley T-Shirt", "Full Sleeve T-Shirt", "Oversized T-Shirt", "Striped T-Shirt",
    ]
    tshirt_prices = [399, 399, 599, 499, 549, 499, 549, 449]

    idx = 0
    men_items = []
    for names, prices, ptype in [
        (formal_shirts, formal_shirt_prices, "shirt"),
        (casual_shirts, casual_shirt_prices, "shirt"),
        (tshirts, tshirt_prices, "tshirt"),
    ]:
        for name, price in zip(names, prices):
            men_items.append({
                "name": name, "category": "men", "type": ptype, "base_price": price,
                "color": _color(idx), "sizes": CLOTHING_SIZES,
                "description": f"{name} for men, in {_color(idx)}.",
            })
            idx += 1

    # ── Men: Jeans ──
    for name, price in [
        ("Slim Fit Jeans", 1499), ("Skinny Fit Jeans", 1399), ("Straight Fit Jeans", 1599),
        ("Distressed Jeans", 1699), ("Relaxed Fit Jeans", 1499),
    ]:
        men_items.append({
            "name": name, "category": "men", "type": "jeans", "base_price": price,
            "color": _color(idx), "sizes": MEN_JEANS_SIZES,
            "description": f"{name} for men, in {_color(idx)}.",
        })
        idx += 1

    # ── Men: Shoes ──
    for name, price in [
        ("Casual Sneakers", 1999), ("Formal Leather Shoes", 2499),
        ("Running Shoes", 2199), ("Loafers", 1899),
    ]:
        men_items.append({
            "name": name, "category": "men", "type": "shoes", "base_price": price,
            "color": _color(idx), "sizes": SHOE_SIZES,
            "description": f"{name} for men, in {_color(idx)}.",
        })
        idx += 1

    add_fashion_catalog(agent, "sb", men_items)

    # ── Women: Dresses, Kurtas, Tops ──
    women_items = []
    for name, price in [
        ("A-Line Dress", 1299), ("Maxi Dress", 1599), ("Bodycon Dress", 1199),
        ("Floral Print Dress", 1399), ("Wrap Dress", 1499),
    ]:
        women_items.append({
            "name": name, "category": "women", "type": "dress", "base_price": price,
            "color": _color(idx), "sizes": WOMEN_SIZES,
            "description": f"{name} for women, in {_color(idx)}.",
        })
        idx += 1

    for name, price in [
        ("Printed Cotton Kurta", 799), ("Embroidered Kurta", 999), ("Straight Kurta", 749),
        ("Anarkali Kurta", 1299), ("Chikankari Kurta", 1499),
    ]:
        women_items.append({
            "name": name, "category": "women", "type": "kurta", "base_price": price,
            "color": _color(idx), "sizes": WOMEN_SIZES,
            "description": f"{name}, in {_color(idx)}.",
        })
        idx += 1

    for name, price in [
        ("Crop Top", 499), ("Casual Top", 549), ("Peplum Top", 699), ("Off-Shoulder Top", 649),
    ]:
        women_items.append({
            "name": name, "category": "women", "type": "top", "base_price": price,
            "color": _color(idx), "sizes": WOMEN_SIZES,
            "description": f"{name} for women, in {_color(idx)}.",
        })
        idx += 1

    for name, price in [
        ("High Waist Jeans", 1499), ("Skinny Jeans", 1399), ("Bootcut Jeans", 1599),
    ]:
        women_items.append({
            "name": name, "category": "women", "type": "jeans", "base_price": price,
            "color": _color(idx), "sizes": WOMEN_JEANS_SIZES,
            "description": f"{name} for women, in {_color(idx)}.",
        })
        idx += 1

    add_fashion_catalog(agent, "sb", women_items)

    # ── Accessories: Bags (3 colors each), Belts, Wallets, Watches ──
    accessory_items = []
    for name, price in [
        ("Tote Bag", 1299), ("Sling Bag", 899), ("Backpack", 1599),
        ("Laptop Bag", 1899), ("Clutch", 799), ("Duffel Bag", 1699),
    ]:
        for c in range(3):
            accessory_items.append({
                "name": name, "category": "accessories", "type": "bag", "base_price": price,
                "color": _color(idx), "sizes": None,
                "description": f"{name} in {_color(idx)}.",
            })
            idx += 1

    for name, price in [("Leather Belt", 599), ("Casual Belt", 499), ("Reversible Belt", 699)]:
        accessory_items.append({
            "name": name, "category": "accessories", "type": "belt", "base_price": price,
            "color": _color(idx), "sizes": BELT_SIZES,
            "description": f"{name} in {_color(idx)}.",
        })
        idx += 1

    for name, price in [
        ("Bifold Wallet", 499), ("Card Holder", 349), ("Zip Wallet", 599),
        ("Slim Wallet", 449), ("Travel Wallet", 699),
    ]:
        for c in range(2):
            accessory_items.append({
                "name": name, "category": "accessories", "type": "wallet", "base_price": price,
                "color": _color(idx), "sizes": None,
                "description": f"{name} in {_color(idx)}.",
            })
            idx += 1

    for name, price in [
        ("Analog Watch", 1499), ("Chronograph Watch", 2499), ("Digital Watch", 999),
        ("Smart Watch", 3499), ("Classic Leather Watch", 1999),
    ]:
        accessory_items.append({
            "name": name, "category": "accessories", "type": "watch", "base_price": price,
            "color": _color(idx), "sizes": None,
            "description": f"{name} in {_color(idx)}.",
        })
        idx += 1

    add_fashion_catalog(agent, "sb", accessory_items)

    # ── Friendly-stylist upsell rules & outfit combo deals ──
    agent.add_upsell_rule("sb_slim_fit_formal_shirt_white_m", "sb_leather_belt_olive_s", discount_pct=10)
    agent.add_upsell_rule("sb_slim_fit_jeans_navy_30", "sb_casual_sneakers_maroon_9", discount_pct=8)
    agent.add_upsell_rule("sb_crew_neck_t_shirt_sky_blue_m", "sb_slim_fit_jeans_navy_30", discount_pct=5)

    agent.add_combo_deal(
        name="Office Ready Combo",
        product_ids=["sb_slim_fit_formal_shirt_white_m", "sb_leather_belt_olive_s", "sb_formal_leather_shoes_beige_9"],
        combo_discount_pct=15,
    )
    agent.add_combo_deal(
        name="Weekend Casual Combo",
        product_ids=["sb_crew_neck_t_shirt_sky_blue_m", "sb_slim_fit_jeans_navy_30", "sb_casual_sneakers_maroon_9"],
        combo_discount_pct=12,
    )
    agent.add_combo_deal(
        name="Ethnic Occasion Combo",
        product_ids=["sb_anarkali_kurta_mustard_m", "sb_clutch_navy", "sb_bifold_wallet_mustard"],
        combo_discount_pct=10,
    )

    return agent
