"""
Catalog generation helpers
===========================
Shared utility for expanding a small set of "base" product templates into
large, realistic catalogs (variants by color/flavor/size/pack) without
hand-writing hundreds of near-identical Product() calls per merchant.
"""

import re
from protocol.spec import Product


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def add_catalog(agent, prefix: str, items: list) -> dict:
    """
    Expand `items` into Product objects and register them on `agent`.

    Each entry in `items` is a dict:
        {
            "name": str,                      # base product name
            "category": str,
            "base_price": float,               # INR, price of the first/base variant
            "unit": str,                       # "piece", "plate", "pack", ...
            "description": str,                # may use {variant} placeholder
            "min_order": int (optional, default 10),
            "max_order": int (optional, default 10000),
            "bulk": [(min_qty, discount_pct), ...] (optional),
            "variants": [str, ...] (optional)  # e.g. colors/flavors/sizes
            "variant_step": float (optional)   # price added per variant index
        }

    Returns a dict mapping "base_name" -> first generated product id, so
    callers can reference specific products for combo deals / upsell rules.
    """
    default_bulk = [(50, 10), (150, 18), (400, 25)]
    first_id_by_name = {}

    for item in items:
        variants = item.get("variants") or [None]
        step = item.get("variant_step", 0)
        bulk_rules = [
            {"min_qty": mq, "discount_pct": pct}
            for mq, pct in item.get("bulk", default_bulk)
        ]

        for idx, variant in enumerate(variants):
            display_name = f"{item['name']} - {variant}" if variant else item["name"]
            pid = f"{prefix}_{_slugify(display_name)}"

            price = round(item["base_price"] + step * idx, 2)
            description = item.get("description", display_name)
            if variant:
                description = description.format(variant=variant) if "{variant}" in description else f"{description} ({variant})"

            agent.add_product(Product(
                id=pid,
                name=display_name,
                description=description,
                category=item["category"],
                base_price=price,
                unit=item.get("unit", "piece"),
                min_order=item.get("min_order", 10),
                max_order=item.get("max_order", 10000),
                bulk_discount_rules=bulk_rules,
            ))

            if item["name"] not in first_id_by_name:
                first_id_by_name[item["name"]] = pid

    return first_id_by_name
