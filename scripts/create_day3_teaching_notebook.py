#!/usr/bin/env python3
"""
Create Day 3 Block A teaching notebook:
- Pipelines (bronze/silver/gold)
- Validations as code
- Data survival tips
- Work habits

Following established pedagogical patterns from Day 1/2
"""

import json
from pathlib import Path

# Notebook cells
cells = []
cell_counter = 0

def add_markdown_cell(content):
    """Add a markdown cell to the notebook"""
    global cell_counter
    cell_id = f"cell-{cell_counter}"
    cell_counter += 1

    cells.append({
        "cell_type": "markdown",
        "id": cell_id,
        "metadata": {},
        "source": [line + "\n" for line in content.split("\n")]
    })

def add_code_cell(content):
    """Add a code cell to the notebook"""
    global cell_counter
    cell_id = f"cell-{cell_counter}"
    cell_counter += 1

    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in content.split("\n")]
    })

# ============================================================================
# HEADER & LEARNING OBJECTIVES
# ============================================================================

add_markdown_cell("""# Day 3, Block A: Data Pipelines & Real-World Validation

**Duration:** 100 minutes (13:30–15:10)
**Course:** ECBS5294 - Data Science 2: Working with Data
**Instructor:** Eduardo Ariño de la Rubia

---

## Learning Objectives

By the end of this session, you will be able to:

1. Explain the **bronze → silver → gold** pipeline pattern and why it matters
2. Design idempotent data transformations
3. Write **assertions** to validate data quality programmatically
4. Identify and handle common real-world data problems (dates, types, nulls)
5. Apply the **pipeline pattern** to a real dataset
6. Communicate data quality issues and limitations to stakeholders

---""")

# ============================================================================
# SECTION 1: WHY PIPELINES?
# ============================================================================

add_markdown_cell("""## 1. Why Data Pipelines?

### The Problem: One-Off Analysis Doesn't Scale

Picture this scenario:

> **Monday morning:** Your manager asks for sales analysis. You load CSV, clean it, make charts. Email results.
>
> **Tuesday:** "Can you refresh those numbers with today's data?"
> You: "Uh... let me re-run everything..."
>
> **Wednesday:** "Actually, can you also include last month?"
> You: "I need to start over... my notebook is a mess..."
>
> **Thursday:** "Why don't your numbers match Finance?"
> You: "I... I'm not sure which cleaning steps I applied..."

**You've hit the wall.** Ad-hoc analysis breaks down when:
- Data updates regularly
- Multiple people need consistent results
- Stakeholders ask "how did you get this number?"
- Requirements change
- You need to reproduce results months later

**The solution?** A systematic, repeatable pipeline.

---

### The Business Case for Pipelines

Pipelines aren't just "good engineering"—they're **strategic assets**:

| Without Pipelines | With Pipelines |
|-------------------|----------------|
| ❌ Analyst spends 2 hours manually refreshing reports | ✅ Automated refresh, analyst reviews in 10 minutes |
| ❌ "I don't remember how I cleaned this" | ✅ Every step documented in code |
| ❌ Numbers differ between teams | ✅ Single source of truth |
| ❌ Errors discovered weeks later | ✅ Validations catch problems immediately |
| ❌ New analyst takes weeks to understand | ✅ Pipeline is self-documenting |

**ROI:** A day spent building a pipeline saves weeks of manual work and prevents costly errors.

---

### Real-World Example: The $2M Mistake

**Company:** Online retailer
**Problem:** Revenue dashboard showed consistent growth
**Reality:** Data pipeline had a bug that duplicated 15% of transactions

**Impact:**
- 🔥 **$2M overstated revenue** in quarterly earnings call
- 🔥 SEC investigation
- 🔥 CFO resigned
- 🔥 Stock price dropped 25%

**Root cause:** No validation step to check for duplicate order IDs

**Lesson:** Validations aren't optional. They're insurance against career-ending mistakes.

---""")

# ============================================================================
# SECTION 2: THE BRONZE-SILVER-GOLD PATTERN
# ============================================================================

add_markdown_cell("""## 2. The Bronze-Silver-Gold Pattern

### The Three Stages

> **"Preserve the original, clean incrementally, aggregate deliberately."**

This pattern comes from data engineering (Databricks "medallion architecture"), but applies to any data work.

#### **Bronze Layer: Raw Ingestion**
- **Purpose:** Preserve original data exactly as received
- **No transformations** (except maybe decompression, format conversion)
- **Keep everything:** Even if it looks wrong
- **Why:** Reproducibility, debugging, legal/compliance

**Example:** Raw CSV as downloaded, JSON from API

#### **Silver Layer: Clean & Validated**
- **Purpose:** Analysis-ready data
- **Fix types:** Strings → dates, numbers → floats
- **Handle nulls:** Standardize representations
- **Validate:** Primary keys, foreign keys, business rules
- **Document:** What was fixed and why

**Example:** Typed tables in DuckDB with assertions

#### **Gold Layer: Business Metrics**
- **Purpose:** Aggregated, joined, ready for reporting
- **Joins:** Combine related tables
- **Aggregations:** Summaries, KPIs, metrics
- **Denormalized:** Optimized for specific analyses

**Example:** Dashboard tables, summary metrics, report views

---

### Why Three Layers?

**Can't I just clean and analyze in one step?**

You can, but:
- ❌ If you discover a cleaning mistake, start over from scratch
- ❌ Can't debug: "Was the data bad, or my logic?"
- ❌ Can't reuse cleaned data for different analyses
- ❌ Hard for others to understand your process

**With layers:**
- ✅ Fix a cleaning bug → just re-run Silver forward
- ✅ Try different aggregation → just re-run Gold
- ✅ Debug: Check Bronze (source issue?) vs Silver (cleaning issue?) vs Gold (logic issue?)
- ✅ Multiple Gold tables from same Silver source
- ✅ Clear separation of concerns

---

### Visual: Pipeline Flow

```
┌─────────────┐
│   BRONZE    │  Raw data as received
│  (orders.   │  - Preserve original
│   csv)      │  - No transformations
└──────┬──────┘
       │
       ↓  Clean & validate
┌─────────────┐
│   SILVER    │  Analysis-ready
│  (orders_   │  - Typed columns
│   clean)    │  - Nulls handled
└──────┬──────┘  - Assertions passed
       │
       ↓  Join & aggregate
┌─────────────┐
│    GOLD     │  Business metrics
│  (daily_    │  - KPIs calculated
│   sales)    │  - Joined tables
└─────────────┘  - Ready for reporting
```

---""")

# ============================================================================
# SECTION 3: EXAMPLE PIPELINE
# ============================================================================

add_markdown_cell("""## 3. Building a Pipeline: Example

We'll build a three-stage pipeline using Olist order data.

**Scenario:** You're an analyst at an e-commerce company. Every morning, you need to report yesterday's sales metrics. Let's build a pipeline that can run daily without breaking.

---

### Step 0: Setup""")

add_code_cell("""# Setup
import pandas as pd
import duckdb
import numpy as np
from IPython.display import display

# Suppress warnings for cleaner teaching output
import warnings
warnings.filterwarnings('ignore')

# Connect to DuckDB
con = duckdb.connect(':memory:')

print("✅ Setup complete")""")

add_markdown_cell("""---

### Bronze Layer: Raw Ingestion

**Goal:** Load data exactly as received. No cleaning, just load.""")

add_code_cell("""# BRONZE: Load raw data
print("=== BRONZE LAYER: Raw Ingestion ===\\n")

# Load orders as-is
bronze_orders = con.execute("""\"
    CREATE TABLE bronze_orders AS
    SELECT * FROM 'data/day3/teaching/olist_orders_subset.csv'
\"\""").df()

bronze_customers = con.execute("""\"
    CREATE TABLE bronze_customers AS
    SELECT * FROM 'data/day3/teaching/olist_customers_subset.csv'
\"\""").df()

bronze_items = con.execute("""\"
    CREATE TABLE bronze_order_items AS
    SELECT * FROM 'data/day3/teaching/olist_order_items_subset.csv'
\"\""").df()

# Check what we loaded
print("Loaded bronze tables:")
print(f"  - bronze_orders: {con.execute('SELECT COUNT(*) FROM bronze_orders').fetchone()[0]} rows")
print(f"  - bronze_customers: {con.execute('SELECT COUNT(*) FROM bronze_customers').fetchone()[0]} rows")
print(f"  - bronze_order_items: {con.execute('SELECT COUNT(*) FROM bronze_order_items').fetchone()[0]} rows")

print("\\n✅ Bronze layer complete: Raw data preserved")""")

add_markdown_cell("""**What we did:**
- Loaded CSVs directly into DuckDB
- No transformations
- No validation (yet)
- Just: "Here's what we received"

**Why keep bronze?**
- If we discover cleaning mistakes later, we can start over
- Audit trail: "What did the source system give us?"
- Legal/compliance: Original data preserved

---

### Silver Layer: Clean & Validate

**Goal:** Transform into analysis-ready format with validation.""")

add_code_cell("""# SILVER: Clean and validate
print("=== SILVER LAYER: Clean & Validate ===\\n")

# Transform orders: Fix types, validate
con.execute("""\"
    CREATE TABLE silver_orders AS
    SELECT
        order_id,
        customer_id,
        order_status,
        TRY_CAST(order_purchase_timestamp AS TIMESTAMP) as order_date,
        TRY_CAST(order_delivered_customer_date AS TIMESTAMP) as delivery_date
    FROM bronze_orders
    WHERE order_id IS NOT NULL  -- Remove any rows without ID
\"\""")

# Transform customers: Clean types
con.execute("""\"
    CREATE TABLE silver_customers AS
    SELECT
        customer_id,
        customer_zip_code_prefix as zip_code,
        customer_city as city,
        customer_state as state
    FROM bronze_customers
    WHERE customer_id IS NOT NULL
\"\""")

# Transform order items: Clean and calculate
con.execute("""\"
    CREATE TABLE silver_order_items AS
    SELECT
        order_id,
        product_id,
        seller_id,
        CAST(price AS DOUBLE) as price,
        CAST(freight_value AS DOUBLE) as freight,
        CAST(price AS DOUBLE) + CAST(freight_value AS DOUBLE) as total_value
    FROM bronze_order_items
    WHERE order_id IS NOT NULL
        AND product_id IS NOT NULL
\"\""")

print("Created silver tables with clean types")
print(f"  - silver_orders: {con.execute('SELECT COUNT(*) FROM silver_orders').fetchone()[0]} rows")
print(f"  - silver_customers: {con.execute('SELECT COUNT(*) FROM silver_customers').fetchone()[0]} rows")
print(f"  - silver_order_items: {con.execute('SELECT COUNT(*) FROM silver_order_items').fetchone()[0]} rows")""")

add_markdown_cell("""**What we did:**
- **Fixed types:** Timestamps parsed, numbers cast to numeric
- **Removed nulls:** Filtered out rows with missing critical IDs
- **Added calculated columns:** total_value = price + freight
- **Standardized names:** Dropped redundant prefixes

**Next:** Validate!

---

### Validation: Prove Data Quality""")

add_code_cell("""# VALIDATION: Assertions to check data quality
print("\\n=== VALIDATION: Checking Data Quality ===\\n")

# Validation 1: Primary key uniqueness
order_count = con.execute("SELECT COUNT(*) FROM silver_orders").fetchone()[0]
order_unique = con.execute("SELECT COUNT(DISTINCT order_id) FROM silver_orders").fetchone()[0]

print(f"✓ Check 1: Order IDs unique?")
print(f"  Total rows: {order_count}")
print(f"  Unique IDs: {order_unique}")
assert order_count == order_unique, "Duplicate order IDs found!"
print("  ✅ PASS: All order IDs are unique\\n")

# Validation 2: No null critical fields
null_order_ids = con.execute("SELECT COUNT(*) FROM silver_orders WHERE order_id IS NULL").fetchone()[0]
null_customer_ids = con.execute("SELECT COUNT(*) FROM silver_orders WHERE customer_id IS NULL").fetchone()[0]

print(f"✓ Check 2: Required fields non-null?")
print(f"  NULL order_ids: {null_order_ids}")
print(f"  NULL customer_ids: {null_customer_ids}")
assert null_order_ids == 0, "NULL order IDs found!"
assert null_customer_ids == 0, "NULL customer IDs found!"
print("  ✅ PASS: No nulls in required fields\\n")

# Validation 3: Foreign key integrity
order_ids_in_orders = con.execute("SELECT COUNT(DISTINCT order_id) FROM silver_orders").fetchone()[0]
order_ids_in_items = con.execute("SELECT COUNT(DISTINCT order_id) FROM silver_order_items").fetchone()[0]

# Check: All items belong to valid orders
orphaned_items = con.execute("""\"
    SELECT COUNT(*)
    FROM silver_order_items i
    LEFT JOIN silver_orders o ON i.order_id = o.order_id
    WHERE o.order_id IS NULL
\"\""").fetchone()[0]

print(f"✓ Check 3: Foreign key integrity?")
print(f"  Orders with items: {order_ids_in_items}")
print(f"  Orphaned items (no matching order): {orphaned_items}")
assert orphaned_items == 0, f"Found {orphaned_items} items without matching orders!"
print("  ✅ PASS: All items have valid orders\\n")

# Validation 4: Business rules
negative_prices = con.execute("SELECT COUNT(*) FROM silver_order_items WHERE price < 0").fetchone()[0]

print(f"✓ Check 4: Business rules?")
print(f"  Negative prices: {negative_prices}")
assert negative_prices == 0, f"Found {negative_prices} negative prices!"
print("  ✅ PASS: All prices are non-negative\\n")

print("="*60)
print("✅ ALL VALIDATIONS PASSED - Silver layer is clean!")
print("="*60)""")

add_markdown_cell("""**What we validated:**
1. **Primary key uniqueness:** No duplicate order IDs
2. **Required fields:** No nulls in critical columns
3. **Foreign key integrity:** All order items link to valid orders
4. **Business rules:** Prices are non-negative

**If any assertion failed?**
- Pipeline stops immediately
- Error message tells you exactly what's wrong
- Fix issue in bronze or silver
- Re-run with confidence

**This is the magic:** Failures are loud and immediate, not silent and dangerous.

---

### Gold Layer: Business Metrics

**Goal:** Create aggregated tables ready for reporting.""")

add_code_cell("""# GOLD: Business metrics
print("=== GOLD LAYER: Business Metrics ===\\n")

# Gold table 1: Daily sales summary
con.execute("""\"
    CREATE TABLE gold_daily_sales AS
    SELECT
        CAST(o.order_date AS DATE) as date,
        COUNT(DISTINCT o.order_id) as num_orders,
        COUNT(DISTINCT o.customer_id) as num_customers,
        SUM(i.total_value) as total_revenue,
        AVG(i.total_value) as avg_order_value
    FROM silver_orders o
    INNER JOIN silver_order_items i ON o.order_id = i.order_id
    WHERE o.order_date IS NOT NULL
    GROUP BY CAST(o.order_date AS DATE)
    ORDER BY date
\"\""")

print("Created gold_daily_sales table")
print("\\nSample data:")
result = con.execute("SELECT * FROM gold_daily_sales LIMIT 5").df()
display(result)

# Gold table 2: Customer summary
con.execute("""\"
    CREATE TABLE gold_customer_summary AS
    SELECT
        c.customer_id,
        c.state,
        COUNT(DISTINCT o.order_id) as num_orders,
        SUM(i.total_value) as lifetime_value,
        MIN(o.order_date) as first_order_date,
        MAX(o.order_date) as last_order_date
    FROM silver_customers c
    INNER JOIN silver_orders o ON c.customer_id = o.customer_id
    INNER JOIN silver_order_items i ON o.order_id = i.order_id
    GROUP BY c.customer_id, c.state
\"\""")

print("\\nCreated gold_customer_summary table")
print("Sample data:")
result2 = con.execute("SELECT * FROM gold_customer_summary LIMIT 5").df()
display(result2)

print("\\n✅ Gold layer complete: Metrics ready for dashboards!")""")

add_markdown_cell("""**What we created:**
- **Daily sales:** Aggregated by date for time series
- **Customer summary:** Lifetime value per customer

**Why gold layer?**
- Pre-computed aggregations are fast
- Stakeholders query gold, not raw data
- Can create multiple gold tables from same silver
- Denormalized for dashboard performance

---

### The Complete Pipeline""")

add_code_cell("""# Summary: Show the full pipeline
print("=== PIPELINE SUMMARY ===\\n")

print("BRONZE → SILVER → GOLD")
print()
print("Bronze (Raw):")
print("  • olist_orders_subset.csv → bronze_orders")
print("  • olist_customers_subset.csv → bronze_customers")
print("  • olist_order_items_subset.csv → bronze_order_items")
print()
print("Silver (Clean & Validated):")
print("  • bronze_orders → silver_orders (typed, validated)")
print("  • bronze_customers → silver_customers (clean)")
print("  • bronze_order_items → silver_order_items (calculated)")
print("  • ✅ 4 validations passed")
print()
print("Gold (Business Metrics):")
print("  • silver_* → gold_daily_sales (aggregated by date)")
print("  • silver_* → gold_customer_summary (per customer)")
print()
print("Tomorrow: Re-run with new data, validations catch problems!")""")

add_markdown_cell("""---

## 4. Key Principles

### 1. Idempotency

> **"Running the pipeline twice gives the same result."**

**Bad (not idempotent):**
```python
# Appends every time you run it
gold = pd.concat([gold, new_data])
```

If you run this twice, you get duplicates!

**Good (idempotent):**
```python
# Recreates from scratch
con.execute("DROP TABLE IF EXISTS gold_daily_sales")
con.execute("CREATE TABLE gold_daily_sales AS SELECT ...")
```

Running twice gives the same result.

**Why it matters:**
- Can re-run safely after failures
- Can refresh data without cleanup
- Deterministic results

---

### 2. Fail Fast

> **"If data is bad, stop immediately with a clear error."**

**Bad:**
```python
# Silently continues with bad data
if df['price'].min() < 0:
    print("Warning: negative prices")
# ... continues anyway
```

Analyst sees warning (maybe), results are wrong.

**Good:**
```python
# Stops with clear error
assert df['price'].min() >= 0, "Negative prices found - fix source data!"
```

Pipeline stops, error is loud, issue must be fixed.

---

### 3. Document Assumptions

Every validation is documentation:

```python
# This assertion says: "We assume order IDs are unique"
assert df['order_id'].is_unique, "Duplicate order IDs"

# This says: "We assume prices are USD and non-negative"
assert (df['price'] >= 0).all(), "Negative prices"

# This says: "We assume all items belong to valid orders"
assert orphan_count == 0, f"{orphan_count} orphaned items"
```

Six months later, someone can read your code and understand your assumptions.

---""")

# ============================================================================
# SECTION 4: REAL-WORLD DATA ISSUES
# ============================================================================

add_markdown_cell("""## 5. Real-World Data Survival Tips

### Date Handling

Dates are deceptively hard!""")

add_code_cell("""# Date horror stories
print("=== DATE HANDLING ===\\n")

# Example: Mixed date formats
mixed_dates = pd.DataFrame({
    'order_id': ['A', 'B', 'C'],
    'date_string': ['2024-01-15', '01/16/2024', '2024.01.17']
})

print("Mixed date formats:")
print(mixed_dates)

# Wrong: Try to parse all at once
try:
    mixed_dates['date'] = pd.to_datetime(mixed_dates['date_string'])
    print("\\nParsed successfully (lucky!)")
    print(mixed_dates)
except Exception as e:
    print(f"\\n❌ Error: {e}")

# Better: Standardize first, then parse
print("\\nBetter approach: Check what format you have")
print("For Olist data, we have ISO 8601 (YYYY-MM-DD HH:MM:SS)")
print("DuckDB's TRY_CAST handles this gracefully:")

result = con.execute("""\"
    SELECT
        order_purchase_timestamp as original,
        TRY_CAST(order_purchase_timestamp AS TIMESTAMP) as parsed,
        CASE
            WHEN TRY_CAST(order_purchase_timestamp AS TIMESTAMP) IS NULL
            THEN 'FAILED'
            ELSE 'OK'
        END as parse_status
    FROM bronze_orders
    LIMIT 5
\"\""").df()
display(result)

print("\\n💡 Tips for dates:")
print("  • Always check format before parsing")
print("  • Use TRY_CAST or pd.to_datetime(errors='coerce')")
print("  • Validate date ranges (no dates in future, no dates in 1900)")
print("  • Watch for timezone issues")""")

add_markdown_cell("""---

### Type Checking""")

add_code_cell("""# Type checking example
print("=== TYPE CHECKING ===\\n")

# Check types in silver layer
print("Silver layer column types:")
result = con.execute("""\"
    SELECT
        column_name,
        data_type
    FROM information_schema.columns
    WHERE table_name = 'silver_order_items'
\"\""").df()
display(result)

print("\\nValidate types match expectations:")
expected_types = {
    'order_id': 'VARCHAR',
    'product_id': 'VARCHAR',
    'price': 'DOUBLE',
    'freight': 'DOUBLE'
}

actual_types = dict(zip(result['column_name'], result['data_type']))

for col, expected in expected_types.items():
    actual = actual_types.get(col, 'MISSING')
    status = '✅' if actual == expected else '❌'
    print(f"  {status} {col}: expected {expected}, got {actual}")

print("\\n💡 Tips for types:")
print("  • Always check df.dtypes after loading")
print("  • Numbers stored as strings? Clean and convert")
print("  • Watch for mixed types in columns")
print("  • Use TRY_CAST to handle errors gracefully")""")

add_markdown_cell("""---

### NULL Handling Strategy""")

add_code_cell("""# NULL handling
print("=== NULL HANDLING ===\\n")

# Check NULL counts in silver
result = con.execute("""\"
    SELECT
        COUNT(*) as total_rows,
        COUNT(order_id) as non_null_order_id,
        COUNT(customer_id) as non_null_customer_id,
        COUNT(order_date) as non_null_order_date,
        COUNT(delivery_date) as non_null_delivery_date
    FROM silver_orders
\"\""").df()

print("NULL counts in silver_orders:")
display(result)

null_delivery = result['total_rows'].values[0] - result['non_null_delivery_date'].values[0]
print(f"\\n{null_delivery} orders have NULL delivery_date")
print("\\nInterpretation:")
print("  • These orders haven't been delivered yet")
print("  • NULL here means 'not yet', not 'missing data'")
print("  • Strategy: Keep as NULL, exclude from delivery time analysis")

print("\\n💡 Tips for NULLs:")
print("  • Understand what NULL means (not applicable? unknown? not yet?)")
print("  • Document your handling strategy")
print("  • Use COALESCE in SQL or fillna() in pandas")
print("  • Remember: COUNT() excludes NULLs, SUM() excludes NULLs")""")

add_markdown_cell("""---

### When to Use SQL vs Python""")

add_code_cell("""# When to use SQL vs Python
print("=== SQL vs PYTHON ===\\n")

print("Use SQL when:")
print("  ✅ Filtering rows (WHERE)")
print("  ✅ Joining tables (JOIN)")
print("  ✅ Grouping and aggregating (GROUP BY)")
print("  ✅ Sorting (ORDER BY)")
print("  ✅ Set operations (UNION, INTERSECT)")
print()
print("Why? Databases optimize these operations, vectorized, fast")

print("\\nUse Python when:")
print("  ✅ Complex string manipulation (regex, parsing)")
print("  ✅ API calls / web scraping")
print("  ✅ Machine learning")
print("  ✅ Custom business logic (complicated IF-THEN rules)")
print("  ✅ Visualization")
print()
print("Why? More flexible, richer libraries")

print("\\n💡 Pro tip:")
print("  Start with SQL (filter, aggregate)")
print("  Then Python (complex logic, ML, viz)")
print("  Example: Extract customers with SQL → Python ML model → SQL to store scores")""")

add_markdown_cell("""---

## 6. Work Habits

### 1. Restart & Run All

**Before committing any notebook:**
```
Kernel → Restart & Run All Cells
```

Ensures reproducibility. Your "it works on my machine" doesn't count!

---

### 2. Small, Frequent Commits

**Good:**
```
git commit -m "Add bronze layer ingestion"
git commit -m "Add silver layer with validation"
git commit -m "Add gold daily sales table"
```

**Bad:**
```
git commit -m "Everything done"  # 500 lines changed
```

Small commits make debugging easier.

---

### 3. Read the Docs

Don't guess! Official documentation is authoritative:
- **DuckDB:** https://duckdb.org/docs/
- **Pandas:** https://pandas.pydata.org/docs/
- **Python:** https://docs.python.org/3/

Pro tip: Search "duckdb try_cast" instead of guessing syntax.

---

### 4. Rubber Duck Debugging

Stuck? Explain your problem out loud (to a rubber duck, or colleague).

Often, articulating the problem reveals the solution.

**Example:**
- "My validation fails... I'm checking if order_id is unique... wait, am I checking the right table? OH! I'm checking bronze instead of silver!"

---

## Summary

### Key Takeaways

1. **Pipeline pattern:** Bronze (raw) → Silver (clean) → Gold (metrics)
2. **Validations:** Assertions catch problems early and loudly
3. **Idempotency:** Re-running gives same result
4. **Dates:** Always parse explicitly and validate
5. **Types:** Check and convert early
6. **NULLs:** Understand meaning, document strategy
7. **SQL vs Python:** Use each for its strengths
8. **Work habits:** Restart & Run All, small commits, read docs

### Why This Matters

**Without pipelines:**
- Manual work every time
- Inconsistent results
- Errors discovered late
- Hard to debug
- Can't reproduce

**With pipelines:**
- Automated, repeatable
- Validated at every step
- Errors caught immediately
- Easy to debug (check each layer)
- Fully reproducible

**You're not just analyzing data—you're building infrastructure.**

---

## Next: In-Class Exercise

**Your turn!**

Build a mini-pipeline with the smaller Olist subset:
1. Bronze: Load raw data
2. Silver: Clean, validate (write 2 assertions)
3. Gold: Create 2-3 summary metrics
4. Document: Write risk note (assumptions & limitations)

**Time:** 15 minutes
**Notebook:** `day3_exercise_mini_pipeline.ipynb`

**Let's build!** 🚀""")

# ============================================================================
# CREATE NOTEBOOK
# ============================================================================

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

# Save notebook
output_path = Path("notebooks/day3/day3_block_a_pipelines_and_validations.ipynb")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, 'w') as f:
    json.dump(notebook, f, indent=2)

print(f"✅ Created: {output_path}")
print(f"   Total cells: {len(cells)}")
print(f"   Ready for teaching!")
