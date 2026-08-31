# SQL Joins Quick Reference Card

**ECBS5294 - Introduction to Data Science: Working with Data**
**Day 2, Block A**

---

## Join Types Decision Tree

```
┌─────────────────────────────────────────────────────┐
│ Do you want ALL rows from one table?                │
└───────────┬─────────────────────────────────────────┘
            │
      ┌─────┴─────┐
      │           │
     YES          NO
      │           │
      │           └──> INNER JOIN
      │               (only matching rows)
      │
      └──> Which table do you want ALL rows from?
           │
           ├──> Left table  ──> LEFT JOIN
           │
           ├──> Right table ──> RIGHT JOIN
           │                    (or flip and use LEFT)
           │
           └──> Both tables ──> FULL OUTER JOIN
                                (rare!)
```

**Most common in practice:**
1. **INNER JOIN** (~60% of use cases) - "show me matches"
2. **LEFT JOIN** (~35% of use cases) - "show me ALL of X"
3. **RIGHT/FULL** (~5% combined) - rarely used

---

## Quick Syntax Reference

### INNER JOIN
```sql
SELECT
    t1.column1,
    t2.column2
FROM table1 t1
INNER JOIN table2 t2 ON t1.key = t2.key
```

**Use when:** You only want rows that exist in BOTH tables

**Example:** Orders with customer details (only valid matches)

---

### LEFT JOIN
```sql
SELECT
    t1.column1,
    t2.column2
FROM table1 t1
LEFT JOIN table2 t2 ON t1.key = t2.key
```

**Use when:** You want ALL rows from left table, even if no match in right table

**Example:** All orders, even those without reviews

---

### Anti-Join Pattern (Finding Unmatched)
```sql
SELECT
    t1.column1
FROM table1 t1
LEFT JOIN table2 t2 ON t1.key = t2.key
WHERE t2.key IS NULL
```

**Use when:** You want rows from left table that DON'T have matches in right table

**Example:** Orders that don't have reviews, customers who haven't purchased

**Critical:** Use `IS NULL` on the right table's key column

---

### RIGHT JOIN (Rarely Used)
```sql
-- These are equivalent:
SELECT * FROM orders o RIGHT JOIN customers c ON o.customer_id = c.customer_id
SELECT * FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id
```

**Tip:** Just flip your tables and use LEFT JOIN instead. Everyone does this.

---

### FULL OUTER JOIN (Very Rare)
```sql
SELECT * FROM table1 t1
FULL OUTER JOIN table2 t2 ON t1.key = t2.key
```

**Use when:** You want everything from both tables, showing unmatched from each side

**Example:** Reconciling two data sources to find discrepancies

---

## Common Table Expressions (CTEs)

### Basic CTE Syntax
```sql
WITH cte_name AS (
    SELECT column1, column2
    FROM table1
    WHERE condition
)
SELECT *
FROM cte_name
WHERE another_condition
```

**Use when:** You have multi-step logic or complex queries

**Benefit:** Reads like a recipe (step 1, step 2, step 3)

---

### Multiple CTEs
```sql
WITH step1 AS (
    -- First calculation
    SELECT ...
),
step2 AS (
    -- Second calculation using step1
    SELECT ...
    FROM step1
)
-- Final query using step2
SELECT *
FROM step2
```

**Tip:** Each CTE can reference previous CTEs. Chain them together!

---

## Critical Patterns & Pitfalls

### ⚠️ Duplicate Inflation

**Problem:** Joining across one-to-many relationships multiplies your rows

```sql
-- ❌ WRONG: Counts items, not orders!
SELECT COUNT(*) AS order_count
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
-- Returns 112,650 (number of ITEMS)

-- ✅ CORRECT: Use DISTINCT
SELECT COUNT(DISTINCT o.order_id) AS order_count
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
-- Returns 99,441 (number of ORDERS)
```

**Rule:** When counting after joins, ask yourself: "Am I counting the right thing?"

---

### ⚠️ Aggregation Grain

**Your GROUP BY defines the grain (level of detail) of your result**

```sql
-- Order grain (one row per order)
SELECT
    o.order_id,
    SUM(oi.price) AS total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id

-- Category grain (one row per category)
SELECT
    p.category,
    SUM(oi.price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
```

**Tip:** Always know what grain you're aggregating to!

---

### ⚠️ NULL Handling

**NULL is NOT equal to anything, not even NULL!**

```sql
-- ❌ WRONG: Doesn't work
WHERE column = NULL

-- ✅ CORRECT: Use IS NULL
WHERE column IS NULL

-- ✅ CORRECT: Use IS NOT NULL
WHERE column IS NOT NULL
```

**In LEFT JOIN:** Unmatched rows have NULL in right table columns

---

## Window Functions with Joins

### Top N per Group Pattern
```sql
WITH ranked AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY group_column
            ORDER BY value_column DESC
        ) AS rank
    FROM joined_tables
)
SELECT *
FROM ranked
WHERE rank <= 3
```

**Use when:** "Top 3 sellers per state", "Best products per category"

**Requires:** Window functions (Day 1 Block B) + Joins (today)

---

## Best Practices Checklist

### Before Writing Your Query

- [ ] **Identify the tables** you need
- [ ] **Find the join keys** (usually foreign keys)
- [ ] **Decide on join type** (INNER vs LEFT vs other)
- [ ] **Determine the grain** (what's one row in your result?)

### While Writing Your Query

- [ ] **Use table aliases** (`o`, `c`, `oi`) for readability
- [ ] **Be explicit** - write `INNER JOIN`, not just `JOIN`
- [ ] **Use CTEs** for multi-step logic
- [ ] **Check for NULLs** in join keys

### After Running Your Query

- [ ] **Check row count** - did it explode? Use COUNT(DISTINCT)
- [ ] **Verify results** - do the numbers make sense?
- [ ] **Test edge cases** - what about unmatched rows?

---

## Common Mistakes & Fixes

| Mistake | What Happens | Fix |
|---------|-------------|-----|
| Using INNER when you need LEFT | Silently loses unmatched data | Use LEFT JOIN when you want "ALL of X" |
| Forgetting DISTINCT after join | Over-counts across one-to-many | Use COUNT(DISTINCT ...) |
| Using `= NULL` instead of `IS NULL` | Filter doesn't work | Always use `IS NULL` |
| Wrong join key | Cartesian product (millions of rows!) | Double-check ON clause |
| Grouping at wrong grain | Incorrect aggregations | Think through: what's one row? |
| Nested subqueries | Unreadable queries | Use CTEs instead |

---

## Quick Troubleshooting

**"My query returns no rows"**
- Check your WHERE conditions (too strict?)
- Verify join keys exist in both tables
- Try LEFT JOIN to see if matches exist

**"My query returns too many rows"**
- One-to-many relationship causing duplication
- Use COUNT(DISTINCT) or aggregate at correct grain
- Check for accidental cartesian product (missing ON clause)

**"I get NULL values I don't expect"**
- Using LEFT JOIN? Unmatched rows have NULLs
- Check if right table column is actually NULL
- Consider using INNER JOIN instead

**"I don't know which join type to use"**
- Ask: "Do I want ALL of table X?" → LEFT JOIN
- Ask: "Only rows that match?" → INNER JOIN
- When in doubt, use LEFT (safer than INNER)

---

## DuckDB-Specific Notes

### Direct File Querying
```sql
-- DuckDB can query CSV files directly!
SELECT * FROM 'data/file.csv'
```

### Type Casting
```sql
-- Safe type conversion
TRY_CAST(column AS INTEGER)  -- Returns NULL on failure
CAST(column AS INTEGER)       -- Errors on failure
```

### String Functions
```sql
-- Pattern matching
WHERE column LIKE '%pattern%'

-- Case-insensitive
WHERE LOWER(column) = 'value'
```

---

## Exercise Tips

### For Query 1 (Revenue by Category)
- Need 3 tables: order_items → products → categories
- Two INNER JOINs chained together
- GROUP BY category_name_english

### For Query 2 (Unreviewed Orders)
- Need LEFT JOIN (want ALL orders)
- Filter: WHERE review_id IS NULL
- GROUP BY order_status

### For Query 3 (Top Sellers by State)
- Use a CTE for seller revenue
- Use ROW_NUMBER() OVER (PARTITION BY state ...)
- Filter WHERE rank <= 3

---

## Additional Resources

**Teaching Notebook:** `notebooks/day2/day2_block_a_joins.ipynb`
- Complete worked examples
- All concepts demonstrated with real data

**Exercise:** `notebooks/day2/day2_exercise_joins.ipynb`
- Paula Costa business scenario
- Scaffolded queries with TODOs

**Data Documentation:** `data/day2/README.md`
- Table descriptions and relationships
- Column definitions
- Known data characteristics

---

**Remember:** Joins are about connecting business entities. Focus on the relationships, not just the syntax!

**Good luck!** 🚀
