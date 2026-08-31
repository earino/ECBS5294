#!/usr/bin/env python3
"""Regenerate products_hw2.json with realistic review distributions.

The original file was a raw dummyjson.com/products dump in which every
product had exactly 3 reviews and all 582 review dates were stamped at
fetch time (one millisecond apart). That made several HW2 questions
unanswerable: "products with more than 3 reviews" was provably empty and
no time trend existed.

This script deterministically post-processes the catalog (same schema,
same products/tags) so that:
  - review counts per product follow a skewed 0-15 distribution
    (some products unreviewed, a meaningful set with >3 reviews)
  - review dates span ~18 months with seasonal volume (Nov-Dec heavier)
    and mildly improving satisfaction over time
  - product `rating` is recomputed from its reviews (catalog rating kept
    for unreviewed products)
  - product meta.createdAt precedes its first review

Usage (from assignments/hw2/):
    uv run python scripts/generate_products_hw2.py

Rerunning always produces the identical file (seeded RNG). The final
invariants are printed for pasting into README/tests.
"""

import json
import random
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
DATA = HERE / "data" / "products_hw2.json"

SEED = 5294
WINDOW_START = datetime(2024, 1, 1)
WINDOW_END = datetime(2025, 6, 30)

# Skewed review-count distribution (counts 0..15)
COUNT_WEIGHTS = {
    0: 6, 1: 12, 2: 18, 3: 20, 4: 14, 5: 10, 6: 7,
    7: 4, 8: 3, 9: 2, 10: 1.5, 11: 1, 12: 0.7, 13: 0.4, 14: 0.2, 15: 0.2,
}

# Month weights within a year: gentle seasonality, Nov/Dec heavier
MONTH_WEIGHTS = {1: 8, 2: 7, 3: 8, 4: 8, 5: 8, 6: 8,
                 7: 7, 8: 7, 9: 8, 10: 9, 11: 12, 12: 14}


def pick_date(rng: random.Random, rating: int) -> datetime:
    """Random date in the window; higher ratings skew later (mild trend)."""
    span_days = (WINDOW_END - WINDOW_START).days
    while True:
        # Bias: rating 1-2 -> earlier half, 4-5 -> later half, 3 -> uniform
        u = rng.random()
        if rating >= 4:
            u = u ** 0.7        # skew toward 1 (later)
        elif rating <= 2:
            u = 1 - (1 - u) ** 0.7  # skew toward 0 (earlier)
        day = WINDOW_START + timedelta(days=int(u * span_days))
        if rng.random() * 14 < MONTH_WEIGHTS[day.month]:
            return day.replace(
                hour=rng.randrange(8, 22),
                minute=rng.randrange(60),
                second=rng.randrange(60),
            )


def iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z"


def main() -> None:
    rng = random.Random(SEED)
    envelope = json.loads(DATA.read_text())
    products = envelope["products"]

    # Pool of (rating, comment) pairs from the original dump keeps the
    # comment text consistent with its rating sentiment; reviewer
    # identities are reused as a pool too.
    pairs = [(r["rating"], r["comment"]) for p in products for r in p["reviews"]]
    people = [(r["reviewerName"], r["reviewerEmail"]) for p in products for r in p["reviews"]]

    counts = [rng.choices(list(COUNT_WEIGHTS), weights=COUNT_WEIGHTS.values())[0]
              for _ in products]

    for product, n in zip(products, counts):
        reviews = []
        for _ in range(n):
            rating, comment = rng.choice(pairs)
            name, email = rng.choice(people)
            when = pick_date(rng, rating)
            reviews.append({
                "rating": rating,
                "comment": comment,
                "date": iso(when),
                "reviewerName": name,
                "reviewerEmail": email,
            })
        reviews.sort(key=lambda r: r["date"])
        product["reviews"] = reviews
        if reviews:
            product["rating"] = round(sum(r["rating"] for r in reviews) / len(reviews), 2)
        # else: keep the catalog rating for unreviewed products

        created = WINDOW_START - timedelta(days=rng.randrange(30, 400))
        if reviews:
            first = datetime.strptime(reviews[0]["date"][:10], "%Y-%m-%d")
            created = min(created, first - timedelta(days=rng.randrange(7, 90)))
        updated = created + timedelta(days=rng.randrange(0, 200))
        product["meta"]["createdAt"] = iso(created)
        product["meta"]["updatedAt"] = iso(min(updated, WINDOW_END))

    envelope["total"] = len(products)
    DATA.write_text(json.dumps(envelope, indent=2) + "\n")

    # ---- invariants report ----
    all_reviews = [r for p in products for r in p["reviews"]]
    dist = Counter(len(p["reviews"]) for p in products)
    dates = sorted(r["date"] for r in all_reviews)
    tag_rows = sum(len(p["tags"]) for p in products)
    over3 = sum(1 for p in products if len(p["reviews"]) > 3)
    by_half = Counter()
    rating_by_half = {}
    for r in all_reviews:
        half = r["date"][:4] + ("-H1" if int(r["date"][5:7]) <= 6 else "-H2")
        by_half[half] += 1
        rating_by_half.setdefault(half, []).append(r["rating"])

    print(f"products: {len(products)}")
    print(f"reviews: {len(all_reviews)}")
    print(f"product-tag rows: {tag_rows}")
    print(f"review-count distribution: {dict(sorted(dist.items()))}")
    print(f"products with >3 reviews: {over3}")
    print(f"products with 0 reviews: {dist.get(0, 0)}")
    print(f"date range: {dates[0][:10]} .. {dates[-1][:10]} "
          f"({(datetime.strptime(dates[-1][:10], '%Y-%m-%d') - datetime.strptime(dates[0][:10], '%Y-%m-%d')).days} days)")
    for half in sorted(by_half):
        rs = rating_by_half[half]
        print(f"  {half}: {by_half[half]:4d} reviews, avg rating {sum(rs)/len(rs):.2f}")

    assert over3 >= 20, "need >=20 products with more than 3 reviews"
    assert dist.get(0, 0) >= 3, "need a few unreviewed products"
    assert (datetime.strptime(dates[-1][:10], "%Y-%m-%d")
            - datetime.strptime(dates[0][:10], "%Y-%m-%d")).days >= 400
    print("\nAll invariants satisfied.")


if __name__ == "__main__":
    main()
