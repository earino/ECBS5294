"""The Day 2 block B notebooks fall back to this file when the live API is
unreachable — it must exist and carry the structure those notebooks consume."""

import json
from pathlib import Path

BACKUP = Path(__file__).resolve().parent.parent / "data/day2/block_b/products_backup.json"


def test_backup_exists_and_parses():
    data = json.loads(BACKUP.read_text())
    assert isinstance(data["products"], list)
    assert len(data["products"]) >= 30  # notebooks slice [:10] and [:30]
    for key in ("total", "skip", "limit"):
        assert key in data


def test_backup_product_fields():
    product = json.loads(BACKUP.read_text())["products"][0]
    for key in ("id", "title", "price", "category", "rating", "reviews", "tags"):
        assert key in product, f"backup product missing {key}"
