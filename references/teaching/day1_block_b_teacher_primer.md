# Day 1, Block B: SQL with DuckDB - Teacher Primer

**For Instructor/TA Use**
**Duration:** 90 minutes  
**Prerequisites:** Block A completed (tidy data, types, primary keys)

---

## 📋 Overview

Block B introduces students to SQL using DuckDB. This is students' **first exposure to SQL** - treat it as foundational. By the end, they should feel comfortable writing queries and understand when SQL is the right tool.

**Why DuckDB?**
- Zero setup (a single Python package, installed via `uv sync`)
- Query files directly (no loading step)
- Real performance on large files
- Same SQL as PostgreSQL/BigQuery

**Key pedagogical challenge:** Window functions (Notebook 3) are conceptually difficult. See detailed teaching strategy below.

---

## 🎯 Learning Objectives

By the end of Block B, students will be able to:

1. **Explain** why SQL matters for data analysis (declarative, set-based)
2. **Write** basic queries (SELECT, WHERE, ORDER BY)
3. **Handle NULL values** correctly (IS NULL, not = NULL)
4. **Aggregate data** with GROUP BY/HAVING
5. **Distinguish** WHERE vs HAVING
6. **Apply window functions** for common patterns (ROW_NUMBER, LAG, moving average)
7. **Understand** when to use windows vs GROUP BY

---

## ⏱️ Session Flow (90 minutes)

### Timing Breakdown

**Notebook 1: SQL Foundations** (30-40 minutes)
- Introduction & DuckDB setup: 5 min
- SELECT, WHERE basics: 10 min
- NULL handling (emphasize!): 5 min
- ORDER BY, calculated columns: 5 min
- Examples & practice: 10-15 min

**Notebook 2: Aggregations** (20-25 minutes)
- Aggregate functions: 5 min
- GROUP BY concept: 5 min
- WHERE vs HAVING: 10 min (critical!)
- Examples: 5-10 min

**Break** (5 minutes)
- Students need a brain break before window functions!

**Notebook 3: Window Functions** (25-30 minutes)
- Mental model (windows vs GROUP BY): 5-7 min
- ROW_NUMBER: 8-10 min
- LAG: 5-7 min
- Moving average: 5-7 min
- Summary & HW1 intro: 3-5 min

**Buffer: 5-10 minutes**
- For questions, technical issues, or going longer on difficult concepts

### Pacing Strategy

**If running short on time:**
- Notebook 3 can be assigned as async reading
- Students watch instructor demo, try on their own later
- Still cover mental model and ROW_NUMBER in class

**If running long:**
- Skip some intermediate examples
- Focus on core concepts over edge cases
- Move quickly through Notebook 1 (it's easier)

---

## 👨‍🏫 Pedagogical Approach

### General Teaching Principles

**1. Concrete before abstract**
- Always show an example BEFORE explaining syntax
- "Here's a business question → here's the query → now let's break down how it works"

**2. Business context always**
- Never "SELECT * FROM table1"
- Always "Find customers who spent over £1000"

**3. Compare to what they know**
- "In Python you'd write a loop... in SQL you write this"
- "GROUP BY is like pandas .groupby()"

**4. Call out common mistakes explicitly**
- Show the WRONG way, then the RIGHT way
- "Students often try `WHERE column = NULL` - this doesn't work!"

**5. Build incrementally**
- Start with `SELECT *`
- Add WHERE
- Add calculations
- Add ORDER BY
- This shows query construction process

### Live Coding vs Pre-written Notebooks

**Recommended approach:**
- Have notebooks pre-written (they're done!)
- **But:** Live-code key examples anyway
- Students learn by watching you think through it
- Make deliberate "mistakes" and fix them

**Example live-coding moment:**
```sql
-- Try this first (deliberately wrong)
SELECT category, price, COUNT(*)
FROM sales
GROUP BY category
-- Wait for error...

-- Now fix it
SELECT category, AVG(price), COUNT(*)
FROM sales
GROUP BY category
-- Explain WHY this works
```

---

## 🪟 Teaching Window Functions (The Hard Part!)

### The Challenge

Window functions are the most difficult concept in this block because:
- Students just learned GROUP BY (which collapses rows)
- Now we're saying "but what if you DON'T want to collapse?"
- The syntax is unfamiliar
- The mental model is new

**Expect:** Confusion, lots of questions, students mixing up windows and GROUP BY.

### The Approach (Proven to work)

**Step 1: Show the limitation (5 min)**
```
"You want to see each transaction AND the category total.
With GROUP BY, you get EITHER transactions OR totals.
You can't have both... or can you?"
```

**Step 2: Side-by-side comparison (5 min)**
- Run GROUP BY query → 3 rows
- Run window function query → 10,000 rows (but with totals added!)
- Visual comparison is KEY

**Step 3: The mental model**
```
GROUP BY: Collapses rows → fewer rows out
Windows: Preserves rows → same rows out, calculation added
```

**Say this multiple times throughout Notebook 3!**

**Step 4: Start with easiest use case**
- ROW_NUMBER for "latest per group" is most intuitive
- Students understand "rank orders by date"
- Build confidence before LAG

**Step 5: Emphasize WHEN to use each**
```
Want summary only? → GROUP BY
Want detail + calculation? → Windows
```

### Common Student Questions & Answers

**Q: "When do I use GROUP BY vs window functions?"**

A: Great question! Ask yourself: "Do I want to see individual rows, or just summaries?"
- Just summaries (e.g., "total per category") → GROUP BY
- Individual rows with calculations (e.g., "each order + its category total") → Window functions

**Q: "What does PARTITION BY do?"**

A: It's like GROUP BY for window functions. "PARTITION BY category" means "for each category, do this calculation." But unlike GROUP BY, we keep all the rows!

**Q: "Why do I need ORDER BY in OVER?"**

A: Some functions need to know the order:
- ROW_NUMBER - which row is "first"?
- LAG - which row is "previous"?
- Moving average - which rows come before?

If order doesn't matter (like COUNT or SUM), ORDER BY is optional.

**Q: "Can I filter on a window function?"**

A: Not directly! You need a subquery:
```sql
-- ❌ Doesn't work
SELECT *, ROW_NUMBER() OVER (...) as rn
FROM table
WHERE rn = 1

-- ✅ Works
SELECT * FROM (
    SELECT *, ROW_NUMBER() OVER (...) as rn
    FROM table
)
WHERE rn = 1
```

**Q: "Is this the same as pandas .rolling()?"**

A: Yes! Good connection. Moving averages in SQL are like `df.rolling(window=7).mean()` in pandas.

**Q: "Can I use window functions and GROUP BY together?"**

A: Yes, but it's advanced. You GROUP BY first, then use window functions on the aggregated results. The bonus question shows this - skip if you're short on time.

---

## 🎓 Teaching WHERE vs HAVING

This is THE key distinction in Notebook 2. Students will mix these up constantly.

### Teaching Strategy

**1. Use a timeline visual**
```
[Load data] → WHERE filters rows → GROUP BY creates groups → HAVING filters groups → Result
```

**2. Show side-by-side examples**
```sql
-- WHERE: Filters before grouping
WHERE price > 5           -- "Only include rows where price > 5"

-- HAVING: Filters after grouping
HAVING COUNT(*) > 100     -- "Only show groups with >100 items"
```

**3. The rule**
```
WHERE: Can't use aggregates (COUNT, SUM, etc.)
HAVING: MUST involve aggregates (that's its purpose!)
```

**4. Show the common mistake**
```sql
-- ❌ WRONG - aggregate in WHERE
WHERE COUNT(*) > 100

-- ✅ CORRECT
HAVING COUNT(*) > 100
```

Deduct heavily in homework if students make this mistake!

### Decision Tree (Show on board)
```
"Am I filtering individual rows or groups?"
  ↓
Rows → WHERE
Groups → HAVING
```

---

## 🚨 Critical Concepts (Emphasize These!)

### 1. NULL Handling (Mentioned in every notebook!)

**This is the #1 mistake beginners make.**

Show this early and often:
```sql
-- ❌ NEVER works
WHERE column = NULL

-- ✅ ALWAYS use this
WHERE column IS NULL
```

**Why it matters:**
- NULL means "unknown"
- Nothing is equal to unknown (not even unknown!)
- SQL is mathematically consistent here, but it's not intuitive

### 2. WHERE vs HAVING

Already covered above. This is #2 most common mistake.

### 3. Windows Preserve, GROUP BY Collapses

The core mental model for window functions. Say it multiple times!

---

## 📊 Using the Datasets

### Cafe Sales (Notebooks 1 & 2)

**Strengths:**
- Students saw it in Block A (familiar)
- Shows continuity
- Good variety for WHERE/GROUP BY

**Use for:**
- SELECT, WHERE, ORDER BY examples
- GROUP BY examples
- Practice queries

### Superstore (Notebook 3)

**Strengths:**
- Better time series (4 years, daily data)
- Multiple orders per customer (great for ROW_NUMBER)
- Clean structure

**Why switch datasets:**
- Window functions need good time-series data
- Cafe sales doesn't have as rich temporal patterns
- Switching shows SQL works on any structured data

**Explain the switch:**
"We're moving to Superstore because it has better time-series data. Window functions shine with time-series analysis!"

---

## 🎯 Assessment & HW1

### What HW1 Tests

**Part 1:** Can they write basic queries?
**Part 2:** Do they understand WHERE vs HAVING?
**Part 3:** Can they apply window functions to new problems?

### Grading Focus

Look for:
1. **NULL handling** - Do they use IS NULL correctly?
2. **WHERE vs HAVING** - Do they know when to use each?
3. **Window function structure** - Do they include ORDER BY when needed?
4. **Data thinking** - Do they filter for positive values, exclude bad data?

### Common Student Struggles (From Past Experience)

**1. "My query returns 0 rows"**
- Usually `= NULL` instead of `IS NULL`
- Or too many AND conditions
- Teach debugging: Remove conditions one by one

**2. "I get an error about aggregates"**
- Using aggregate in WHERE instead of HAVING
- Or missing column in GROUP BY

**3. "Window function gives weird results"**
- Forgot ORDER BY in OVER clause
- Order matters for ROW_NUMBER, LAG, moving average!

**4. "How do I filter window function results?"**
- Need subquery - this is advanced but required for ROW_NUMBER pattern

### Office Hours Strategy

If students are stuck:
1. Ask them to show their query
2. Ask them to explain in English what they want
3. Build it incrementally together
4. Don't just give the answer - guide them

---

## 🔗 Connections

### From Block A

Students learned:
- Tidy data principles
- Types and NULL handling
- Primary keys

**Reference these:**
- "Remember how we talked about NULL in Block A? Same concept here!"
- "This column is the primary key - that's why it's unique"
- "We cleaned this data in Block A, now we're querying it"

### To Day 2

Day 2 will cover:
- JOINs (multi-table queries)
- More complex window functions
- CTEs and subqueries
- JSON (maybe)

**Preview:**
"Today you learned single-table queries. Tomorrow we'll join multiple tables together. Everything you learned today still applies!"

### Skills for Real Work

**Emphasize:**
- SQL is used everywhere (analytics, data science, engineering)
- These patterns (GROUP BY, window functions) are what professionals use daily
- Portfolio-worthy: Put completed HW1 on GitHub!

---

## 💡 Teaching Tips

### Energy Management

**90 minutes is long.** Keep energy up:
- Take a 5-minute break before Notebook 3
- Vary teaching style (lecture → demo → discussion)
- Ask questions to the class
- Have students try quick queries themselves

### Handling Different Skill Levels

**Some students will have SQL experience:**
- Let them help others during practice time
- Challenge them with bonus questions
- Ask them to explain concepts to class

**Some will be completely new:**
- Reassure them this is normal (first SQL exposure)
- Emphasize that examples are in notebooks
- Office hours available
- HW1 is scaffolded to help

### Technical Issues

**If DuckDB won't install:**
- Usually pip/Python version issue
- Try `pip3 install duckdb`
- Or re-run `uv sync` from the repo root
- Have backup: SQLite online

**If query is slow:**
- Probably missing LIMIT during development
- Or very complex JOIN (but we don't have JOINs yet)

### Creating Engagement

**Ask questions:**
- "Who can tell me why this query returns 0 rows?"
- "What do you think will happen if we run this?"
- "How would you write this in Python?"

**Use polls:**
- "Raise hand: WHO vs HAVING for this scenario?"
- Gets everyone involved

---

## 📝 Pre-Class Checklist

- [ ] Review all 3 notebooks
- [ ] Test queries on your machine
- [ ] Prepare breakpoints (where to pause for questions)
- [ ] Have backup examples ready
- [ ] Print SQL Quick Reference for students
- [ ] Test screenshare/projector
- [ ] Have HW1 ready to assign

---

## 🎬 Session Opening (First 5 min)

**Script:**

"Welcome to Block B! Today we're learning SQL - the language of data.

By the end of today, you'll be able to query 500,000 rows of data in milliseconds. You'll answer business questions like 'What's our top product per country?' with just a few lines of SQL.

We're using DuckDB - it's lightweight, fast, and perfect for learning. The SQL you learn works everywhere: PostgreSQL, MySQL, BigQuery, Snowflake.

We have 3 notebooks:
1. SQL Foundations - SELECT, WHERE, ORDER BY
2. Aggregations - GROUP BY, the classic WHERE vs HAVING distinction
3. Window Functions - GROUP BY's more flexible cousin

The last one is challenging but incredibly powerful. Don't worry - we'll build up to it.

Let's dive in!"

---

## 🎓 Session Closing (Last 5 min)

**Script:**

"Great work today! You've learned a LOT:
- How to filter and sort data
- How to aggregate with GROUP BY
- The critical WHERE vs HAVING distinction
- Window functions - you can now do 'latest per group' and moving averages!

HW1 is available. It uses a 525,000 row dataset - real scale. You'll see why SQL matters.

Tips for HW1:
- Use LIMIT while developing
- Build queries incrementally
- Check for NULLs early
- Remember: IS NULL, not = NULL!
- Remember: WHERE for rows, HAVING for groups

Due: Day 2, start of class.

Questions?"

---

## 📚 Additional Resources

**For you (the instructor):**
- DuckDB docs: https://duckdb.org/docs/sql/introduction
- PostgreSQL window function tutorial: https://www.postgresqltutorial.com/postgresql-window-function/
- Mode SQL tutorial: https://mode.com/sql-tutorial/

**For students:**
- Included in notebooks
- SQL Quick Reference (`references/sql_quick_reference.md`)
- HW1 README with tips

---

## ✅ Success Criteria

**You'll know students "got it" when:**
- They can explain WHERE vs HAVING without notes
- They use IS NULL (not = NULL)
- They understand "windows preserve, GROUP BY collapses"
- They can write a ROW_NUMBER query for "latest per group"
- HW1 submissions show good SQL formatting and NULL handling

**It's okay if:**
- They're still confused about complex window functions (LAG, frames)
- They need to reference syntax
- They're slow writing queries

**Red flags to address:**
- Using = NULL repeatedly (core concept not understood)
- Can't distinguish WHERE vs HAVING (needs review)
- Completely lost on window functions (needs office hours)

---

## 🚀 You've Got This!

Teaching SQL for the first time can feel overwhelming, but:
- The notebooks are comprehensive
- The examples are clear
- The homework is tested and solvable
- Students will learn!

**Remember:**
- Emphasize the "why" not just the "how"
- Business context always
- Concrete before abstract
- Windows are hard - that's normal!

**Questions for the instructor:** [Your contact info]

Good luck! 🎉
