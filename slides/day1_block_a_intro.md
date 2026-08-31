---
marp: true
theme: ceu
paginate: true
header: 'Day 1, Block A: Tidy Data Foundations'
footer: 'ECBS5294 | CEU'
---

<!-- _class: lead -->

# Block A
## Data Thinking & Tidy Foundations

**90 minutes**

---

# What We'll Cover

1. **Why data structure matters** (strategically)
2. **The three rules of tidy data**
3. **Five common messiness patterns**
4. **Primary keys** (unique identifiers)
5. **Types & common pitfalls** (dates, floats, strings)
6. **Missing values** (NULL vs empty vs sentinel values)
7. **Hands-on exercise** (clean a messy café dataset)

---

# Learning Objectives

By the end of this block, you'll be able to:

✅ State the three rules of tidy data
✅ Recognize common messiness patterns
✅ Identify and validate a primary key
✅ Handle type issues (dates, numbers, booleans)
✅ Make defensible choices about missing values
✅ Transform messy data into tidy format

---

# Key Insight

> **"When you define how data is structured, you're not just organizing information—you're defining the language your entire organization will use to make decisions."**

Every "customer," "order," "product" becomes a **noun** the business uses.

Every "purchase," "return," "review" becomes a **verb** that drives metrics.

---

# Materials for Today

**Teaching notebook:**
`notebooks/day1/day1_block_a_tidy_foundations.ipynb`

**Exercise dataset:**
`data/day1/dirty_cafe_sales.csv`

**Exercise starter:**
`notebooks/day1/day1_exercise_tidy.ipynb`

**Quick reference:**
`references/tidy_data_checklist.md`

---

<!-- _class: lead -->

# Let's Begin

Open the teaching notebook:
`day1_block_a_tidy_foundations.ipynb`

We'll work through examples together, then you'll practice.
