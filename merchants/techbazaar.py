"""
TechBazaar - Electronics & gadgets store
Demo merchant for Hermes Protocol
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_catalog

COLORS = ["Black", "White", "Blue", "Red", "Silver", "Rose Gold"]
PHONE_MODELS = ["iPhone 13", "iPhone 14", "iPhone 15", "Samsung S23", "Samsung S24", "OnePlus 11", "Redmi Note 13", "Pixel 8", "iPhone SE"]
CABLE_TYPES = ["Type-C", "Micro USB", "Lightning", "Type-C to Type-C", "USB-C to Lightning"]
LED_COLORS = ["Warm White", "Cool White", "RGB", "Blue", "Green", "Purple"]


def create_techbazaar() -> MerchantAgent:
    agent = MerchantAgent(
        name="TechBazaar",
        description="Electronics & gadgets for events, offices, and creator setups. Bulk pricing available.",
        categories=["electronics"],
        location="Bengaluru",
    )

    agent.add_product(Product(
        id="tb_powerbank_10000",
        name="Power Bank (10000mAh)",
        description="Compact 10000mAh power bank with dual USB output.",
        category="electronics",
        base_price=650,
        unit="piece",
        min_order=10,
        bulk_discount_rules=[
            {"min_qty": 50, "discount_pct": 10},
            {"min_qty": 150, "discount_pct": 16},
        ]
    ))

    agent.add_product(Product(
        id="tb_earbuds_tws",
        name="Wireless Earbuds (TWS)",
        description="True wireless earbuds with charging case, 20hr battery.",
        category="electronics",
        base_price=1200,
        unit="piece",
        min_order=10,
        bulk_discount_rules=[
            {"min_qty": 30, "discount_pct": 8},
            {"min_qty": 100, "discount_pct": 14},
        ]
    ))

    add_catalog(agent, "tb", [
        {"name": "Power Bank", "category": "electronics", "base_price": 500, "unit": "piece",
         "description": "Portable power bank, {variant} capacity.",
         "min_order": 10, "bulk": [(50, 10), (150, 16)],
         "variants": ["5000mAh", "10000mAh", "20000mAh", "30000mAh"], "variant_step": 250},
        {"name": "USB Cable (1m)", "category": "electronics", "base_price": 120, "unit": "piece",
         "description": "1-meter durable charging cable, {variant}.",
         "min_order": 20, "bulk": [(100, 12), (300, 20)], "variants": CABLE_TYPES},
        {"name": "USB Cable (2m)", "category": "electronics", "base_price": 180, "unit": "piece",
         "description": "2-meter durable charging cable, {variant}.",
         "min_order": 20, "bulk": [(100, 12), (300, 20)], "variants": CABLE_TYPES},
        {"name": "Wired Earphones", "category": "electronics", "base_price": 250, "unit": "piece",
         "description": "In-ear wired earphones in {variant} with mic.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Phone Holder (Desk Stand)", "category": "electronics", "base_price": 150, "unit": "piece",
         "description": "Adjustable desk phone stand in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Phone Holder (Car Mount)", "category": "electronics", "base_price": 220, "unit": "piece",
         "description": "Dashboard/vent car phone mount in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Ring Light (10 inch)", "category": "electronics", "base_price": 800, "unit": "piece",
         "description": "10-inch LED ring light with phone clip and tripod.",
         "min_order": 5, "bulk": [(20, 10), (50, 15)]},
        {"name": "Ring Light (14 inch)", "category": "electronics", "base_price": 1400, "unit": "piece",
         "description": "14-inch LED ring light, 3 color modes.",
         "min_order": 5, "bulk": [(15, 10), (40, 15)]},
        {"name": "Tripod Stand (Mobile)", "category": "electronics", "base_price": 450, "unit": "piece",
         "description": "Flexible mobile tripod stand with Bluetooth remote.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)]},
        {"name": "Tripod Stand (DSLR)", "category": "electronics", "base_price": 1200, "unit": "piece",
         "description": "Heavy-duty DSLR tripod, extendable to 5.5 ft.",
         "min_order": 5, "bulk": [(15, 8), (30, 12)]},
        {"name": "Bluetooth Speaker (Portable)", "category": "electronics", "base_price": 900, "unit": "piece",
         "description": "Portable Bluetooth speaker in {variant}, 10hr battery.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
        {"name": "Bluetooth Speaker (Party)", "category": "electronics", "base_price": 3500, "unit": "piece",
         "description": "Large party Bluetooth speaker with LED lights.",
         "min_order": 2, "bulk": [(5, 8), (10, 12)]},
        {"name": "Mouse Pad (Standard)", "category": "electronics", "base_price": 90, "unit": "piece",
         "description": "Standard desk mouse pad in {variant}.",
         "min_order": 25, "bulk": [(100, 12), (300, 20)], "variants": COLORS},
        {"name": "Mouse Pad (RGB Gaming)", "category": "electronics", "base_price": 450, "unit": "piece",
         "description": "Extended RGB gaming mouse pad.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)]},
        {"name": "Webcam Cover Slide", "category": "electronics", "base_price": 40, "unit": "piece",
         "description": "Slide-to-close webcam privacy cover, {variant}.",
         "min_order": 50, "bulk": [(200, 15), (500, 22)], "variants": COLORS},
        {"name": "Cable Organizer Box", "category": "electronics", "base_price": 250, "unit": "piece",
         "description": "Desk cable management box in {variant}.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Cable Ties (Pack of 20)", "category": "electronics", "base_price": 60, "unit": "pack",
         "description": "Reusable velcro cable ties, pack of 20.",
         "min_order": 30, "bulk": [(100, 12), (300, 20)]},
        {"name": "USB Hub (4-Port)", "category": "electronics", "base_price": 350, "unit": "piece",
         "description": "4-port USB 3.0 hub.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)]},
        {"name": "USB-C Hub (Multiport)", "category": "electronics", "base_price": 900, "unit": "piece",
         "description": "7-in-1 USB-C hub with HDMI, SD card, and PD charging.",
         "min_order": 10, "bulk": [(30, 8), (80, 12)]},
        {"name": "LED Strip Light (5m)", "category": "electronics", "base_price": 500, "unit": "piece",
         "description": "5-meter LED strip light, {variant}, remote controlled.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": LED_COLORS},
        {"name": "Laptop Stand (Adjustable)", "category": "electronics", "base_price": 700, "unit": "piece",
         "description": "Ergonomic adjustable laptop stand in {variant}.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
        {"name": "Wireless Keyboard", "category": "electronics", "base_price": 850, "unit": "piece",
         "description": "Slim wireless keyboard in {variant}.",
         "min_order": 10, "bulk": [(30, 8), (80, 12)], "variants": COLORS},
        {"name": "Wired Keyboard", "category": "electronics", "base_price": 450, "unit": "piece",
         "description": "Standard wired keyboard in {variant}.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
        {"name": "Wireless Mouse", "category": "electronics", "base_price": 400, "unit": "piece",
         "description": "Ergonomic wireless mouse in {variant}.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
        {"name": "Screen Protector (Tempered Glass)", "category": "electronics", "base_price": 150, "unit": "piece",
         "description": "Tempered glass screen protector for {variant}.",
         "min_order": 20, "bulk": [(100, 15), (300, 22)], "variants": PHONE_MODELS},
        {"name": "Laptop Sleeve (13-15 inch)", "category": "electronics", "base_price": 350, "unit": "piece",
         "description": "Padded laptop sleeve in {variant}, fits 13-15 inch laptops.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
        {"name": "Selfie Stick with Tripod", "category": "electronics", "base_price": 380, "unit": "piece",
         "description": "3-in-1 selfie stick, tripod, and Bluetooth remote.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)]},
        {"name": "Smartwatch (Basic)", "category": "electronics", "base_price": 1800, "unit": "piece",
         "description": "Basic fitness smartwatch in {variant} with heart-rate monitor.",
         "min_order": 5, "bulk": [(20, 8), (50, 12)], "variants": COLORS},
        {"name": "Webcam (1080p)", "category": "electronics", "base_price": 1500, "unit": "piece",
         "description": "1080p HD webcam with built-in mic.",
         "min_order": 5, "bulk": [(20, 8), (50, 12)]},
        {"name": "Portable Projector (Mini)", "category": "electronics", "base_price": 4500, "unit": "piece",
         "description": "Mini portable LED projector for event screenings.",
         "min_order": 2, "bulk": [(5, 6), (10, 10)]},
        {"name": "Extension Cord (4-Socket)", "category": "electronics", "base_price": 300, "unit": "piece",
         "description": "4-socket power extension cord with surge protection.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)]},
        {"name": "Wireless Charger Pad", "category": "electronics", "base_price": 550, "unit": "piece",
         "description": "15W wireless charging pad in {variant}.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
        {"name": "Car Charger (Dual Port)", "category": "electronics", "base_price": 280, "unit": "piece",
         "description": "Dual USB car charger in {variant}, fast charging.",
         "min_order": 20, "bulk": [(50, 10), (150, 16)], "variants": COLORS},
        {"name": "Bluetooth Neckband", "category": "electronics", "base_price": 650, "unit": "piece",
         "description": "Magnetic Bluetooth neckband earphones in {variant}.",
         "min_order": 15, "bulk": [(40, 10), (100, 16)], "variants": COLORS},
        {"name": "Gaming Headset", "category": "electronics", "base_price": 1100, "unit": "piece",
         "description": "Over-ear gaming headset in {variant} with mic.",
         "min_order": 10, "bulk": [(30, 8), (80, 14)], "variants": COLORS},
        {"name": "Portable SSD (256GB)", "category": "electronics", "base_price": 2800, "unit": "piece",
         "description": "Compact 256GB portable SSD, USB-C.",
         "min_order": 5, "bulk": [(15, 6), (40, 10)]},
        {"name": "Portable SSD (512GB)", "category": "electronics", "base_price": 4200, "unit": "piece",
         "description": "Compact 512GB portable SSD, USB-C.",
         "min_order": 5, "bulk": [(15, 6), (40, 10)]},
        {"name": "Anti-Radiation Laptop Pad", "category": "electronics", "base_price": 500, "unit": "piece",
         "description": "Cooling laptop pad with dual fans.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)]},
        {"name": "Wireless Charging Stand", "category": "electronics", "base_price": 900, "unit": "piece",
         "description": "2-in-1 wireless charging stand for phone + earbuds, {variant}.",
         "min_order": 10, "bulk": [(30, 10), (80, 15)], "variants": COLORS},
    ])

    # Upsell rules
    agent.add_upsell_rule("tb_powerbank_10000", "tb_usb_cable_1m_type_c", discount_pct=10)
    agent.add_upsell_rule("tb_earbuds_tws", "tb_cable_organizer_box_black", discount_pct=8)

    # Combo deals
    agent.add_combo_deal(
        name="Creator Kit",
        product_ids=["tb_ring_light_10_inch", "tb_tripod_stand_mobile", "tb_earbuds_tws"],
        combo_discount_pct=15
    )
    agent.add_combo_deal(
        name="Delegate Tech Kit",
        product_ids=["tb_powerbank_10000", "tb_usb_cable_1m_type_c", "tb_wired_earphones_black"],
        combo_discount_pct=18
    )

    return agent
