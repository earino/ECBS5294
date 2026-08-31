---
marp: true
theme: ceu
paginate: true
header: 'Day 2, Block A: Multi-Table Joins'
footer: 'ECBS5294 | CEU'
---

<!-- _class: lead -->

# Block A
## Multi-Table Joins: Connecting Your Data

**90 minutes**

---

# What We'll Cover

1. **Why joins exist** (normalized databases)
2. **Four JOIN types:** INNER, LEFT, RIGHT, FULL
3. **Decision framework:** Which JOIN to use when
4. **Primary/Foreign keys** (the "glue" between tables)
5. **Join cardinality** (1:1, 1:N, N:M and row explosion)
6. **Common pitfalls** (duplicate keys, missing matches)
7. **Hands-on exercise:** Olist e-commerce (8 related tables)

---

# Learning Objectives

By the end of this block, you'll be able to:

✅ Choose the correct JOIN type for a business question
✅ Write multi-table JOIN queries in SQL
✅ Diagnose and prevent row explosion
✅ Validate join results (row counts, NULL checks)
✅ Handle unmatched rows appropriately
✅ Join 3+ tables to answer complex questions

---

# The Real-World Problem

**Business question:**
> "What's the revenue per customer, broken down by product category?"

**The problem:**
- Revenue is in the `orders` table
- Customer names are in the `customers` table
- Product categories are in the `products` table

**You need JOINs to combine them.**

---

# Mental Model: JOINs vs VLOOKUP

| VLOOKUP | SQL JOIN |
|---------|----------|
| One value at a time | Entire tables at once |
| Breaks with duplicates | Handles duplicates |
| Slow on large data | Millions of rows in seconds |

**JOINs are how professionals combine data.**

---

# The Four JOIN Types

| JOIN Type | What It Does | When To Use |
|-----------|--------------|-------------|
| **INNER** | Only matching rows | "Show customers **who ordered**" |
| **LEFT** | All from left + matches | "Show **all customers** (even if no orders)" |
| **RIGHT** | All from right + matches | "Show **all products** (even if not sold)" |
| **FULL** | All from both sides | "Show everything, matched or not" |

**We'll practice deciding which to use for different business questions.**

---

# The Dataset: Olist Brazilian E-Commerce

**8 related tables:**
- `orders` (100K orders)
- `order_items` (order line items)
- `customers` (customer info)
- `products` (product catalog)
- `sellers` (who fulfilled orders)
- `order_payments` (payment details)
- `order_reviews` (customer feedback)
- `geolocation` (latitude/longitude)

**Real business data with real relationships.**

This is what you'll encounter in the wild.

---

# Key Insight

> **"The strength of SQL is in JOINs. Master them, and you can answer any question that spans multiple tables."**

- Single-table queries: **20% of business questions**
- Multi-table queries: **80% of business questions**

**Today you graduate from beginner to practitioner.**

---

# Materials for Today

**Teaching notebook:**
`notebooks/day2/day2_block_a_joins.ipynb`

**Exercise dataset:**
`data/day2/block_a/` (8 CSV files)

**Exercise starter:**
`notebooks/day2/day2_exercise_joins.ipynb`

**Quick reference:**
`references/sql_joins_quick_reference.md`

---

<!-- _class: lead -->

# Let's Connect Some Tables

Open the teaching notebook:
`day2_block_a_joins.ipynb`

We'll start with simple two-table joins and build up to complex multi-table scenarios.

---
