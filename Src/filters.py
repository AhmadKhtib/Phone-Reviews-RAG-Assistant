import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Filters:
    brand: Optional[str] = None
    max_price: Optional[float] = None
    min_price: Optional[float] = None

KNOWN_BRANDS = [
    "samsung", "apple", "iphone", "xiaomi", "redmi", "realme", "oppo",
    "oneplus", "huawei", "google", "pixel", "nokia", "sony", "motorola"
]


def parse_filters(question: str) -> Filters:
    q = question.lower()
    f = Filters()
    # brand detection
    for b in KNOWN_BRANDS:
        if re.search(rf"\b{re.escape(b)}\b", q):
            if b == "iphone":
                f.brand = "Apple"
            elif b == "redmi":
                f.brand = "Xiaomi"
            elif b == "pixel":
                f.brand = "Google"
            elif b== "samsung":
                f.brand='Samsung'
            else:
                f.brand = b.capitalize()
            break

    # price: "under 500", "< 500", "max 500", "$500"
    m = re.search(r"(under|below|max|<=|<)\s*\$?\s*(\d+(?:\.\d+)?)", q)
    if m:
        f.max_price = float(m.group(2))

    m = re.search(r"(over|above|min|>=|>)\s*\$?\s*(\d+(?:\.\d+)?)", q)
    if m:
        f.min_price = float(m.group(2))

    return f


def to_chroma_filter(f: Filters) -> dict:
    """
    Build Chroma metadata filter.
    Works when your metadatas include keys like 'brand' and 'price_usd'.
    """
    clauses = []

    if f.brand:
        clauses.append({"brand": {"$eq": f.brand}})
    if f.max_price is not None:
        clauses.append({"price_usd": {"$lte": f.max_price}})
    if f.min_price is not None:
        clauses.append({"price_usd": {"$gte": f.min_price}})

    if not clauses:
        return {}

    if len(clauses) == 1:
        return clauses[0]

    return {"$and": clauses}
