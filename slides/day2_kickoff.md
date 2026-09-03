---
marp: true
theme: ceu
paginate: true
header: 'Day 2: Multi-Table Joins & API Ingestion'
footer: 'ECBS5294 | CEU'
---

<!-- _class: lead -->

# Day 2
## Connecting Data & Ingesting APIs

**ECBS5294 - Data Science 2: Working with Data**

Central European University

---

# Welcome Back!

**Day 1 Recap:**
- ✅ Tidy data foundations (structure, types, primary keys)
- ✅ SQL fundamentals (filtering, aggregating, window functions)
- ✅ DuckDB for fast analytics

**Today we build on that foundation:**
- 🔗 **Block A:** Multi-table JOINs (combining datasets)
- 📡 **Block B:** API ingestion & JSON normalization

---

# Why Today Matters

**Real data pipelines aren't one table.**

You'll need to:
- **Join** customer data + order data + product data
- **Fetch** data from REST APIs (Shopify, Stripe, Salesforce)
- **Normalize** nested JSON into relational tables
- **Persist** everything for SQL analysis

**By end of day:** You'll build a complete API → DuckDB → SQL pipeline.

---

# Day 2 Agenda

### Block A: Multi-Table Joins (90 minutes)
- INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN
- When to use which type
- Join cardinality and "explosion" pitfalls
- Hands-on: Olist e-commerce dataset (8 tables!)

### Block B: APIs & JSON (90 minutes)
- REST API fundamentals (GET requests, JSON responses)
- Safe JSON navigation (handling missing fields)
- Normalizing nested structures to relational tables
- Hands-on: DummyJSON products API → DuckDB

---

# Homework 1 Check-In

**Homework 1 was due today.**

- Submitted? Great!
- Running late? Talk to me after class.

**Solutions will be released after class** (check Moodle for password).

---

# Homework 2 Preview

**Assigned at end of today:**
- Multi-table JOIN analysis (Olist dataset)
- API data pipeline (fetch, normalize, persist, query)
- Due: Start of Day 3

**Estimated time:** 3-4 hours

---

# Learning Objectives: Day 2

By the end of today, you'll be able to:

✅ Choose the correct JOIN type for a business question
✅ Diagnose and prevent row explosion in joins
✅ Fetch data from REST APIs using Python `requests`
✅ Navigate nested JSON safely (`.get()` pattern)
✅ Normalize one-to-many relationships into separate tables
✅ Build complete API → DuckDB → SQL pipelines

---

# Materials You'll Need

**Datasets:**
- `data/day2/block_a/` - Multi-table e-commerce data
- DummyJSON API (live endpoint, no auth required)

**Teaching notebooks:**
- `day2_block_a_joins.ipynb`
- `day2_block_b_01_api_json_basics.ipynb`
- `day2_block_b_02_json_to_duckdb.ipynb`

**Quick references:**
- `references/sql_joins_quick_reference.md`
- `references/api_pipeline_quick_reference.md`

---

# Key Mindset Shift

**Day 1:** Work with data structures you're given

**Day 2:** **Connect** disparate data sources & **ingest** from external systems

> **"Modern data professionals spend 80% of their time on data integration. Today you learn how."**

---

# Two Critical Skills

### 1. JOINs (Block A)
**Without this:** You can only analyze isolated tables.
**With this:** You can answer questions spanning customers, orders, products, reviews.

### 2. API Ingestion (Block B)
**Without this:** You're limited to static CSV files.
**With this:** You can build live dashboards pulling real-time data from external systems.

**These two skills unlock 80% of real-world data work.**

---

<!-- _class: lead -->

# Let's Get Started

**Block A begins now:**
Open `day2_block_a_joins.ipynb`

We'll start with a simple two-table join and build up to complex multi-table scenarios.

---
