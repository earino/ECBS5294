# Data Pipeline Patterns - Quick Reference

**ECBS5294: Data Science 2: Working with Data**

---

## Bronze → Silver → Gold Pattern

A layered approach to data processing that separates concerns and enables reproducibility.

```
RAW DATA → [BRONZE] → [SILVER] → [GOLD] → ANALYSIS
           Preserve    Clean      Aggregate
```

---

## 🥉 Bronze Layer

**Purpose:** Preserve raw data exactly as received

**Operations:**
- Load data AS-IS from source
- No transformations
- No filtering
- No type conversions

**Why?**
- Audit trail: See exactly what you received
- Reprocessability: If silver/gold logic changes, start fresh from bronze
- Debugging: Trace problems to source

**Example:**
```python
# Just load it
bronze_df = pd.read_csv('data/orders.csv')

# Or create table directly
con.execute("""
    CREATE TABLE bronze_orders AS
    SELECT * FROM 'data/orders.csv'
""")
```

**Golden Rule:** Bronze = read-only archive

---

## 🥈 Silver Layer

**Purpose:** Clean, validated, analysis-ready data

**Transformations:**
1. **Fix data types**
   ```python
   # Convert strings to proper types
   df['order_date'] = pd.to_datetime(df['order_date'])
   df['price'] = df['price'].astype(float)
   ```

2. **Handle NULLs**
   ```python
   # Remove rows with NULL keys
   df = df[df['order_id'].notna()]

   # Or document why NULLs exist
   # "price NULL = pending quote"
   ```

3. **Standardize formats**
   ```python
   # Lowercase, trim whitespace
   df['email'] = df['email'].str.lower().str.strip()

   # Consistent date formats
   df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
   ```

4. **Validate with assertions**
   ```python
   # Primary key uniqueness
   assert df['order_id'].is_unique, "Duplicate order IDs!"

   # Required fields non-null
   assert df['customer_id'].notna().all(), "NULL customer IDs!"

   # Business rules
   assert (df['price'] >= 0).all(), "Negative prices found!"
   ```

5. **Filter invalid rows**
   ```sql
   WHERE order_date IS NOT NULL
     AND total_amount > 0
     AND status IN ('completed', 'pending', 'canceled')
   ```

**Example:**
```python
# Create clean silver table
con.execute("""
    CREATE TABLE silver_orders AS
    SELECT
        order_id,
        customer_id,
        TRY_CAST(order_date AS DATE) as order_date,
        CAST(total_amount AS DECIMAL(10,2)) as total_amount,
        LOWER(TRIM(status)) as status
    FROM bronze_orders
    WHERE order_id IS NOT NULL
      AND order_date IS NOT NULL
      AND total_amount > 0
""")

# Validate
order_count = con.execute("SELECT COUNT(*) FROM silver_orders").fetchone()[0]
unique_count = con.execute("SELECT COUNT(DISTINCT order_id) FROM silver_orders").fetchone()[0]
assert order_count == unique_count, "Duplicate order IDs in silver!"
```

---

## 🥇 Gold Layer

**Purpose:** Business-specific aggregations and analytics

**Operations:**
- JOIN related tables
- Calculate KPIs
- Aggregate to reporting level (daily, monthly, by category)
- Denormalize for performance

**Example:**
```sql
-- Daily revenue by product category
CREATE TABLE gold_daily_category_revenue AS
SELECT
    CAST(o.order_date AS DATE) as date,
    p.category,
    COUNT(DISTINCT o.order_id) as num_orders,
    SUM(oi.quantity) as units_sold,
    SUM(oi.price * oi.quantity) as revenue
FROM silver_orders o
INNER JOIN silver_order_items oi ON o.order_id = oi.order_id
INNER JOIN silver_products p ON oi.product_id = p.product_id
GROUP BY CAST(o.order_date AS DATE), p.category
ORDER BY date, category
```

**Multiple gold tables are OK:**
- `gold_customer_ltv` - customer lifetime value
- `gold_daily_sales` - daily sales metrics
- `gold_product_performance` - product analytics
- Each serves a specific business question

---

## Why Not Do Everything in One Step?

**❌ Single-step approach:**
```python
# Load, clean, and analyze all at once
df = pd.read_csv('data.csv')
df['date'] = pd.to_datetime(df['date'])
df = df[df['amount'] > 0]
result = df.groupby('category')['amount'].sum()
```

**Problems:**
- Can't re-run if logic changes (must reload from source)
- Can't debug which step failed
- Can't share cleaned data with others
- No audit trail

**✅ Layered approach:**
```python
# Bronze: preserve
bronze_df = pd.read_csv('data.csv')

# Silver: clean
silver_df = bronze_df.copy()
silver_df['date'] = pd.to_datetime(silver_df['date'])
silver_df = silver_df[silver_df['amount'] > 0]

# Gold: aggregate
gold_df = silver_df.groupby('category')['amount'].sum()
```

**Benefits:**
- Re-run silver/gold without reloading
- Debug layer by layer
- Share silver with team
- Clear separation of concerns

---

## Common Validations

### Primary Key Uniqueness
```python
assert df['id'].is_unique, "Duplicate IDs!"
```

### Required Fields Non-NULL
```python
assert df['customer_id'].notna().all(), "NULL customer IDs!"
```

### Data Type Validation
```python
assert df['date'].dtype == 'datetime64[ns]', "Date not parsed!"
```

### Range Validation
```python
assert (df['price'] >= 0).all(), "Negative prices!"
assert (df['quantity'] > 0).all(), "Zero/negative quantities!"
```

### Date Range
```python
assert (df['order_date'] >= '2020-01-01').all(), "Dates before 2020!"
assert (df['order_date'] <= pd.Timestamp.now()).all(), "Future dates!"
```

### Business Rules
```python
# Revenue = price * quantity
revenue_check = (df['revenue'] - (df['price'] * df['quantity'])).abs()
assert (revenue_check < 0.01).all(), "Revenue calculation mismatch!"
```

### Referential Integrity (Foreign Keys)
```python
# All customer_ids must exist in customers table
customer_ids = con.execute("SELECT DISTINCT customer_id FROM customers").df()['customer_id']
assert df['customer_id'].isin(customer_ids).all(), "Invalid customer IDs!"
```

---

## Idempotency

**Principle:** Re-running the same pipeline produces the same result

**Why it matters:**
- Can re-run after failures
- Reproducible results
- Safe to automate

**How to achieve:**

### Use CREATE OR REPLACE
```sql
CREATE OR REPLACE TABLE silver_orders AS
SELECT * FROM bronze_orders WHERE ...
```

### Or DROP then CREATE
```sql
DROP TABLE IF EXISTS silver_orders;
CREATE TABLE silver_orders AS ...
```

### Avoid appending without clearing
```python
# ❌ BAD: Re-run doubles the data
df.to_sql('silver_orders', con, if_exists='append')

# ✅ GOOD: Re-run replaces data
df.to_sql('silver_orders', con, if_exists='replace')
```

---

## Fail-Fast Principle

**Principle:** Detect problems immediately, don't silently continue

**Why?**
- Bad data in = bad analysis out
- Earlier detection = easier debugging
- Prevents downstream confusion

**Examples:**

### ❌ Silent failures (BAD)
```python
# Missing values silently become NaN
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# Invalid dates silently become NaT
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Analysis continues with bad data...
```

### ✅ Fail-fast (GOOD)
```python
# Raise error if conversion fails
df['price'] = pd.to_numeric(df['price'], errors='raise')

# Validate immediately
assert df['price'].notna().all(), "Failed to parse all prices!"

# Pipeline stops here if data is bad
```

---

## Quick Checklist

Before moving to next layer:

**Bronze → Silver:**
- [ ] All data types correct (DATE, FLOAT, INT)
- [ ] Primary keys unique and non-null
- [ ] Required fields non-null
- [ ] Invalid rows filtered out
- [ ] Formats standardized
- [ ] Assertions pass

**Silver → Gold:**
- [ ] JOINs return expected row counts
- [ ] Aggregations make business sense
- [ ] No unexpected NULLs
- [ ] Metrics match known totals (if available)

---

## Real-World Tips

**Start simple, add layers:**
- Don't build complex pipelines upfront
- Start with bronze → silver
- Add gold when you know the questions

**Document assumptions:**
```python
# ASSUMPTION: NULL prices mean "quote pending"
# These orders excluded from revenue calculations
df = df[df['price'].notna()]
```

**Keep bronze small for practice:**
- Sample large datasets (1000 rows is plenty)
- Faster iteration during development
- Run full dataset when stable

**Version your pipelines:**
```python
# pipeline_v1.py: Initial version
# pipeline_v2.py: Added category validation
# Use git to track changes
```

**Monitor your data:**
```python
print(f"Bronze: {len(bronze_df)} rows")
print(f"Silver: {len(silver_df)} rows ({len(bronze_df) - len(silver_df)} filtered)")
print(f"Gold: {len(gold_df)} aggregated groups")
```

---

## Summary

| Layer | Purpose | Operations | Example |
|-------|---------|------------|---------|
| **Bronze** | Preserve raw | Load as-is | `SELECT * FROM 'file.csv'` |
| **Silver** | Clean & validate | Types, NULLs, assertions | `CAST(date AS DATE)`, `WHERE id IS NOT NULL` |
| **Gold** | Analyze | JOINs, aggregates, KPIs | `GROUP BY category`, `SUM(revenue)` |

**Remember:**
- Bronze = read-only archive
- Silver = analysis-ready foundation
- Gold = business-specific answers
- Validate at each layer
- Fail fast on bad data
- Make pipelines idempotent

---

**Questions?** Review Day 3 Block A notebook for detailed examples!
