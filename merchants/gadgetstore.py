"""
GadgetStore - Electronics & gadgets store (Croma/Amazon-style)
Demo merchant for Hermes Protocol.

Tech-expert personality: upsell rules pair accessories with the gear they
belong to (earphones->case, laptop stand->keyboard), and combo deals are
framed as ready-made setups (WFH, Creator, Gaming) rather than event kits.
"""

from protocol.spec import Product
from merchants.sdk import MerchantAgent
from merchants.catalog_utils import add_fashion_catalog

COLORS = ["Black", "White", "Blue", "Red", "Silver", "Space Grey"]
PHONE_MODELS = ["iPhone 13", "iPhone 14", "iPhone 15", "Samsung S23", "Samsung S24", "OnePlus 12", "Pixel 8"]


def create_gadgetstore() -> MerchantAgent:
    agent = MerchantAgent(
        name="GadgetStore",
        description=(
            "Your go-to tech expert — phones accessories, audio, computing gear, smart home, "
            "cameras and gaming setups, with spec comparisons and compatible-accessory suggestions built in."
        ),
        categories=["phones-accessories", "audio", "computing", "smart-home", "cameras", "gaming"],
        location="Bengaluru",
    )

    items = []

    # ── Phones & Accessories ──
    for style, price in [("Silicone Phone Case", 299), ("Leather Phone Case", 599),
                          ("Clear Phone Case", 249), ("Rugged Phone Case", 449)]:
        for model in PHONE_MODELS:
            items.append({"name": f"{style} ({model})", "category": "phones-accessories", "type": "phone-case",
                           "base_price": price, "color": "Clear" if "Clear" in style else COLORS[len(items) % len(COLORS)],
                           "sizes": None, "description": f"{style} designed for {model}."})

    for style, price in [("10000mAh Power Bank", 899), ("20000mAh Power Bank", 1499),
                          ("5000mAh Compact Power Bank", 699), ("Wireless Power Bank", 1299)]:
        for c in COLORS[:4]:
            items.append({"name": style, "category": "phones-accessories", "type": "power-bank",
                           "base_price": price, "color": c, "sizes": None,
                           "description": f"{style} in {c}."})

    for model in PHONE_MODELS:
        items.append({"name": f"Tempered Glass Screen Protector ({model})", "category": "phones-accessories",
                       "type": "screen-protector", "base_price": 249, "color": "Clear", "sizes": None,
                       "description": f"9H tempered glass screen protector for {model}."})

    for style, price in [("Type-C Cable (1m)", 199), ("Lightning Cable (1m)", 249),
                          ("Micro USB Cable (1m)", 149), ("Fast Charger 20W", 799),
                          ("Fast Charger 33W", 1099)]:
        for c in COLORS[:3]:
            items.append({"name": style, "category": "phones-accessories", "type": "charging",
                           "base_price": price, "color": c, "sizes": None,
                           "description": f"{style} in {c}."})

    for style, price in [("Car Phone Mount", 449), ("Desk Phone Stand", 349), ("Bike Phone Mount", 399)]:
        for c in COLORS[:2]:
            items.append({"name": style, "category": "phones-accessories", "type": "phone-mount",
                           "base_price": price, "color": c, "sizes": None,
                           "description": f"{style} in {c}."})

    for style, price in [("Pop Socket Grip", 199), ("Phone Grip Stand", 249)]:
        for c in COLORS[:4]:
            items.append({"name": style, "category": "phones-accessories", "type": "phone-grip",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    # ── Audio ──
    for style, price in [("Wired Earphones", 499), ("Wired Earphones (Bass Boost)", 699),
                          ("Wired Earphones (Metal Body)", 899)]:
        for c in COLORS[:4]:
            items.append({"name": style, "category": "audio", "type": "earphones",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Wireless Earbuds (TWS)", 1499), ("Wireless Earbuds Pro (ANC)", 2499),
                          ("Wireless Earbuds Sport", 1799), ("Wireless Earbuds Lite", 999)]:
        for c in COLORS[:4]:
            items.append({"name": style, "category": "audio", "type": "earbuds",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Bluetooth Neckband", 899), ("Bluetooth Neckband (Sports)", 1099),
                          ("Bluetooth Neckband Pro", 1399)]:
        for c in COLORS[:3]:
            items.append({"name": style, "category": "audio", "type": "neckband",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Portable Bluetooth Speaker", 1299), ("Mini Bluetooth Speaker", 799),
                          ("Party Bluetooth Speaker", 2999), ("Waterproof Bluetooth Speaker", 1799)]:
        for c in COLORS[:3]:
            items.append({"name": style, "category": "audio", "type": "speaker",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    # ── Computing ──
    for style, price in [("Mechanical Keyboard", 2499), ("Wireless Keyboard", 1499),
                          ("Membrane Keyboard", 799), ("Compact 60% Keyboard", 1999)]:
        for c in COLORS[:3]:
            items.append({"name": style, "category": "computing", "type": "keyboard",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Wireless Mouse", 599), ("Ergonomic Mouse", 899),
                          ("Silent Click Mouse", 749), ("Vertical Mouse", 1199)]:
        for c in COLORS[:3]:
            items.append({"name": style, "category": "computing", "type": "mouse",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for size_label, price in [('21" Monitor', 8999), ('24" Monitor', 11999),
                               ('27" Monitor', 16999), ('32" Monitor', 22999)]:
        items.append({"name": size_label, "category": "computing", "type": "monitor",
                       "base_price": price, "color": "Black", "sizes": None,
                       "description": f"Full HD {size_label} for work and entertainment."})

    for style, price in [("USB-C Hub (7-in-1)", 1499), ("USB-C Hub (4-Port)", 899), ("USB 3.0 Hub", 599)]:
        for c in COLORS[:2]:
            items.append({"name": style, "category": "computing", "type": "usb-hub",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Adjustable Laptop Stand", 999), ("Aluminum Laptop Stand", 1499),
                          ("Foldable Laptop Stand", 699)]:
        items.append({"name": style, "category": "computing", "type": "laptop-stand",
                       "base_price": price, "color": "Silver", "sizes": None, "description": style})

    for style, price in [("1080p Webcam", 1799), ("4K Webcam", 3499), ("Webcam with Ring Light", 2299)]:
        items.append({"name": style, "category": "computing", "type": "webcam",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for style, price in [("Cable Organizer Box", 399), ("Cable Clips (Set of 10)", 149)]:
        items.append({"name": style, "category": "computing", "type": "cable-organizer",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for cap, price in [("256GB External SSD", 3499), ("512GB External SSD", 5499), ("1TB External SSD", 8999)]:
        items.append({"name": cap, "category": "computing", "type": "storage",
                       "base_price": price, "color": "Black", "sizes": None, "description": f"Portable {cap}."})

    # ── Smart Home ──
    for style, price in [("Smart LED Bulb", 599), ("Smart LED Bulb (Color)", 899), ("Smart Bulb Starter Pack (2pc)", 1499)]:
        for c in ["Warm White", "Cool White"]:
            items.append({"name": style, "category": "smart-home", "type": "smart-bulb",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style}, {c}."})

    for style, price in [("Smart Plug", 799), ("Smart Power Strip", 1299)]:
        items.append({"name": style, "category": "smart-home", "type": "smart-plug",
                       "base_price": price, "color": "White", "sizes": None, "description": style})

    for style, price in [("Smart Speaker (Voice Assistant)", 2999), ("Smart Display (7-inch)", 4999), ("Mini Smart Speaker", 1799)]:
        items.append({"name": style, "category": "smart-home", "type": "smart-speaker",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for style, price in [("Indoor Security Camera", 1999), ("Outdoor Security Camera", 2999), ("Video Doorbell Camera", 3499)]:
        items.append({"name": style, "category": "smart-home", "type": "security-camera",
                       "base_price": price, "color": "White", "sizes": None, "description": style})

    for style, price in [("Smart Doorbell (Basic)", 2499), ("Smart Doorbell Pro", 3999)]:
        items.append({"name": style, "category": "smart-home", "type": "smart-doorbell",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for c, price in [("RGB", 1299), ("Warm White", 899), ("Cool White", 899)]:
        items.append({"name": "Smart LED Strip Light (5m)", "category": "smart-home", "type": "led-strip",
                       "base_price": price, "color": c, "sizes": None, "description": f"5m smart LED strip, {c}."})

    for style, price in [("Smart Wall Switch (1-Gang)", 999), ("Smart Wall Switch (2-Gang)", 1499)]:
        items.append({"name": style, "category": "smart-home", "type": "smart-switch",
                       "base_price": price, "color": "White", "sizes": None, "description": style})

    for style, price in [("Smart Curtain Motor", 3999), ("Smart Thermostat", 4499)]:
        items.append({"name": style, "category": "smart-home", "type": "smart-climate",
                       "base_price": price, "color": "White", "sizes": None, "description": style})

    for style, price in [("Smart Water Leak Sensor", 1499), ("Smart Motion Sensor", 999), ("Smart Smoke Detector", 1999)]:
        items.append({"name": style, "category": "smart-home", "type": "smart-sensor",
                       "base_price": price, "color": "White", "sizes": None, "description": style})

    # ── Cameras ──
    for style, price in [("Action Camera 4K", 5999), ("Action Camera Mini", 3499)]:
        items.append({"name": style, "category": "cameras", "type": "action-camera",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for style, price in [("Mini Tripod", 399), ("Standard Tripod", 899), ("Professional Tripod", 2499)]:
        for c in COLORS[:2]:
            items.append({"name": style, "category": "cameras", "type": "tripod",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for size_label, price in [('8" Ring Light', 999), ('10" Ring Light', 1499), ('14" Ring Light', 2299)]:
        items.append({"name": f"{size_label} with Stand", "category": "cameras", "type": "ring-light",
                       "base_price": price, "color": "White", "sizes": None,
                       "description": f"{size_label} with adjustable stand."})

    for style, price in [("Camera Sling Bag", 1499), ("Camera Backpack", 2499), ("Camera Case (Hard Shell)", 1999)]:
        items.append({"name": style, "category": "cameras", "type": "camera-bag",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for style, price in [("Selfie Stick with Tripod", 599), ("Bluetooth Selfie Stick", 799)]:
        for c in COLORS[:2]:
            items.append({"name": style, "category": "cameras", "type": "selfie-stick",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("3-Axis Gimbal Stabilizer", 4999), ("Mini Gimbal Stabilizer", 2999)]:
        items.append({"name": style, "category": "cameras", "type": "gimbal",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for cap, price in [("32GB Memory Card", 499), ("64GB Memory Card", 799), ("128GB Memory Card", 1299)]:
        items.append({"name": cap, "category": "cameras", "type": "memory-card",
                       "base_price": price, "color": "Black", "sizes": None, "description": f"High-speed {cap}."})

    for style, price in [("Camera Lens Filter Kit", 899), ("Camera Cleaning Kit", 399)]:
        items.append({"name": style, "category": "cameras", "type": "camera-accessory",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    # ── Gaming ──
    for style, price in [("Gaming Mouse (RGB)", 1499), ("Gaming Mouse Pro", 2499), ("Gaming Mouse Lite", 899)]:
        for c in ["Black", "White"]:
            items.append({"name": style, "category": "gaming", "type": "gaming-mouse",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Gaming Keyboard (RGB Mechanical)", 3499), ("Gaming Keyboard Compact", 2499), ("Gaming Keyboard Membrane", 1499)]:
        for c in ["Black", "White"]:
            items.append({"name": style, "category": "gaming", "type": "gaming-keyboard",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Gaming Headset (7.1 Surround)", 2999), ("Gaming Headset Pro", 4499), ("Gaming Headset Lite", 1499)]:
        for c in ["Black", "Red"]:
            items.append({"name": style, "category": "gaming", "type": "gaming-headset",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Wireless Game Controller", 2499), ("Wired Game Controller", 1299)]:
        for c in ["Black", "White", "Blue"]:
            items.append({"name": style, "category": "gaming", "type": "controller",
                           "base_price": price, "color": c, "sizes": None, "description": f"{style} in {c}."})

    for style, price in [("Gaming Mouse Pad (XL)", 899), ("Gaming Mouse Pad (RGB)", 1299), ("Gaming Mouse Pad Standard", 399)]:
        items.append({"name": style, "category": "gaming", "type": "mouse-pad",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    for style, price in [("Gaming Chair (Ergonomic)", 12999), ("Gaming Chair Pro (Recliner)", 18999)]:
        items.append({"name": style, "category": "gaming", "type": "gaming-chair",
                       "base_price": price, "color": "Black", "sizes": None, "description": style})

    add_fashion_catalog(agent, "gs", items)

    # ── Tech-expert upsell rules & setup combo deals ──
    agent.add_upsell_rule("gs_wired_earphones_black", "gs_silicone_phone_case_iphone_15_blue", discount_pct=8)
    agent.add_upsell_rule("gs_adjustable_laptop_stand_silver", "gs_mechanical_keyboard_black", discount_pct=10)
    agent.add_upsell_rule("gs_wireless_earbuds_tws_black", "gs_10000mah_power_bank_black", discount_pct=5)

    agent.add_combo_deal(
        name="WFH Setup",
        product_ids=["gs_adjustable_laptop_stand_silver", "gs_mechanical_keyboard_black", "gs_wireless_mouse_black"],
        combo_discount_pct=15,
    )
    agent.add_combo_deal(
        name="Creator Kit",
        product_ids=["gs_10_ring_light_with_stand_white", "gs_standard_tripod_black", "gs_1080p_webcam_black"],
        combo_discount_pct=12,
    )
    agent.add_combo_deal(
        name="Gaming Bundle",
        product_ids=["gs_gaming_mouse_rgb_black", "gs_gaming_keyboard_rgb_mechanical_black", "gs_gaming_headset_7_1_surround_black"],
        combo_discount_pct=18,
    )

    return agent
