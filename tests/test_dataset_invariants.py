"""Assignment-dataset invariants.

Every fact an assignment's README or starter states about its dataset is
asserted here, so a dataset regeneration or doc edit that breaks the
contract fails CI instead of reaching students.
"""

import json
from datetime import datetime
from pathlib import Path

import duckdb
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def con():
    return duckdb.connect()


# ---------------- HW1: online retail ----------------

HW1_CSV = REPO_ROOT / "assignments/hw1/data/online_retail_hw1.csv"


def test_hw1_grain_counts(con):
    row = con.execute(f"""
        SELECT COUNT(*),
               COUNT(DISTINCT Invoice),
               COUNT(DISTINCT "Customer ID")
        FROM '{HW1_CSV}'
    """).fetchone()
    assert row == (525_461, 28_816, 4_383), f"HW1 grain drifted: {row}"


def test_hw1_guest_checkouts(con):
    guests = con.execute(f"""
        SELECT COUNT(*), COUNT(DISTINCT Invoice)
        FROM '{HW1_CSV}' WHERE "Customer ID" IS NULL
    """).fetchone()
    assert guests == (107_927, 5_229), f"HW1 guest counts drifted: {guests}"


# ---------------- HW2: products catalog ----------------

HW2_JSON = REPO_ROOT / "assignments/hw2/data/products_hw2.json"


@pytest.fixture(scope="module")
def hw2_products():
    return json.loads(HW2_JSON.read_text())["products"]


def test_hw2_counts(hw2_products):
    assert len(hw2_products) == 194
    assert sum(len(p["reviews"]) for p in hw2_products) == 710
    assert sum(len(p["tags"]) for p in hw2_products) == 364


def test_hw2_review_distribution(hw2_products):
    counts = [len(p["reviews"]) for p in hw2_products]
    # Q5.2 requires a non-empty ">3 reviews" answer
    assert sum(1 for c in counts if c > 3) >= 20
    # unreviewed products must exist (INNER JOIN teaching point)
    assert sum(1 for c in counts if c == 0) >= 3


def test_hw2_dates_span_and_trend(hw2_products):
    dates = sorted(r["date"] for p in hw2_products for r in p["reviews"])
    first = datetime.strptime(dates[0][:10], "%Y-%m-%d")
    last = datetime.strptime(dates[-1][:10], "%Y-%m-%d")
    # Q5.4 (timeline/trend) needs a real time axis
    assert (last - first).days >= 400, "review dates no longer span a usable window"
    assert len({d[:10] for d in dates}) > 100, "review dates collapsed onto few days"


def test_hw2_rating_derived_from_reviews(hw2_products):
    for p in hw2_products:
        if p["reviews"]:
            mean = sum(r["rating"] for r in p["reviews"]) / len(p["reviews"])
            assert abs(p["rating"] - round(mean, 2)) < 0.011, p["id"]


# ---------------- HW3: Chicago + NYC ----------------

CHICAGO = REPO_ROOT / "data/day3/hw3_data_pack/chicago_business_licenses.csv"
NYC = REPO_ROOT / "data/day3/hw3_data_pack/nyc_building_permits.json"


def test_hw3_chicago_license_id_unique(con):
    total, unique = con.execute(
        f"SELECT COUNT(*), COUNT(DISTINCT license_id) FROM '{CHICAGO}'"
    ).fetchone()
    assert total == 50_000 and total == unique


def test_hw3_nyc_grain(con):
    total, permits, jobs = con.execute(f"""
        SELECT COUNT(*), COUNT(DISTINCT permit_si_no), COUNT(DISTINCT job__)
        FROM '{NYC}'
    """).fetchone()
    assert total == 20_000
    assert permits == total, "permit_si_no must be the unique per-row key"
    assert jobs < total, "job__ must stay one-to-many (one job, many permits)"


def test_hw3_nyc_dates_are_us_format(con):
    # The starter/solution parse with strptime('%m/%d/%Y'); if the export
    # format changes, those cells silently break.
    sample = con.execute(
        f"SELECT filing_date FROM '{NYC}' WHERE filing_date IS NOT NULL LIMIT 1"
    ).fetchone()[0]
    datetime.strptime(sample, "%m/%d/%Y")
