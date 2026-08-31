# Homework 1: SQL Foundations with DuckDB

**Course:** ECBS5294 - Introduction to Data Science: Working with Data  
**Due:** Day 2, Start of Class  
**Total Points:** 100 (+ 10 bonus)
**Est. Time:** 2-2.5 hours

---

## 📋 Overview

This assignment tests your understanding of SQL fundamentals:
- Basic queries (SELECT, WHERE, ORDER BY)
- Aggregations (GROUP BY, HAVING)
- Window functions (ROW_NUMBER, LAG, moving averages)

You'll work with **525,461 real transactions** from an online retail company. This is real-scale data - you'll see why SQL + DuckDB matters for data analysis!

---

## 🎯 Learning Objectives

By completing this assignment, you will demonstrate ability to:

1. Write SQL queries to answer business questions
2. Use WHERE and HAVING appropriately
3. Handle NULL values correctly
4. Apply GROUP BY for aggregations
5. Use window functions for analytics
6. Work with real-scale data (500K+ rows)

---

## 📊 Dataset: Online Retail

### Source
UK-based online retail company specializing in unique all-occasion gifts. Data covers Dec 2009 - Dec 2010 (1 year).

### Size
- **525,461 transactions**
- 8 columns
- Date range: 2009-12-01 to 2010-12-09
- Multiple countries, ~4,000 customers

### Columns

| Column | Type | Description | Notes |
|--------|------|-------------|-------|
| `Invoice` | Text | Invoice number (6-digit)| Prefix 'C' indicates cancellation |
| `StockCode` | Text | Product code | 5-6 characters |
| `Description` | Text | Product name | ~2,900 NULLs (0.6%) |
| `Quantity` | Integer | Number of items | Can be negative (returns) |
| `InvoiceDate` | Datetime | Transaction timestamp | |
| `Price` | Float | Price per unit (GBP) | |
| `Customer ID` | Float | Customer identifier | ~107,000 NULLs (20.5%) - guest checkouts |
| `Country` | Text | Customer country | 38 different countries |

### Data Quality Notes

**NULL Values:**
- **Customer ID**: 107,927 nulls (20.5%) - These are guest checkouts (no account)
- **Description**: 2,928 nulls (0.6%) - Missing product descriptions
- You'll need to handle these appropriately in your queries!

**Negative Quantities:**
- Some transactions have negative quantities (returns/cancellations)
- Check if your business question should include or exclude these

**Cancelled Transactions:**
- Invoices starting with 'C' are cancellations
- Consider whether to include or exclude them

### Performance Notes

With DuckDB, you can query all 525K rows efficiently:
- Simple SELECT: <0.3 seconds
- GROUP BY aggregation: <0.1 seconds
- Window functions: <0.5 seconds

**Tip:** Use `LIMIT 10` while developing queries, then remove LIMIT for final answers.

---

## 📝 Assignment Structure

### Part 1: Basic Queries (30 points)
Tests: SELECT, WHERE, ORDER BY, NULL handling, pattern matching

**4 questions**, ~7-8 points each

### Part 2: Aggregations (40 points)
Tests: COUNT, SUM, AVG, GROUP BY, HAVING, WHERE vs HAVING

**4 questions**, 10 points each

### Part 3: Window Functions (30 points)
Tests: ROW_NUMBER, LAG, moving averages

**3 questions**, 8-12 points each

### Bonus (10 points)
Tests: Synthesis of multiple concepts

**1 question**, combining window functions with aggregations

---

## 📤 Submission Requirements

### What to Submit

1. **Completed Jupyter notebook:** `hw1_starter.ipynb` with all cells run
2. File must run successfully: **Restart Kernel & Run All Cells** (in VS Code: **Restart**, then **Run All**)
3. All outputs must be visible (queries + results)

### Submission Format

- **File name:** `hw1_[your_name].ipynb` (e.g., `hw1_john_smith.ipynb`)
- **How:** Upload to Moodle
- **When:** Before start of Day 2 class

### Before Submitting - Checklist

- [ ] All TODO sections completed
- [ ] All code cells run without errors
- [ ] All query results are visible (don't clear outputs!)
- [ ] Markdown explanations included where requested
- [ ] Notebook runs end-to-end: **Restart & Run All** (VS Code: **Restart**, then **Run All**)
- [ ] File renamed to `hw1_[your_name].ipynb`

**If your notebook doesn't run end-to-end, you will lose points!**

---

## 🎯 Grading Rubric

### Per Question Breakdown

Each question is graded on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 40% | Query produces correct results |
| **Data Thinking** | 25% | Shows understanding of SQL concepts, handles NULLs, considers edge cases |
| **Code Quality** | 20% | Clean, readable, formatted SQL (uppercase keywords, indented) |
| **Communication** | 15% | Markdown explanations clear and accurate |

### Overall Expectations

**A-level work (90-100%):**
- All queries correct
- Handles NULL values appropriately
- SQL is clean and formatted
- Explanations demonstrate understanding
- Goes beyond minimum requirements

**B-level work (80-89%):**
- Most queries correct
- Some NULL handling issues
- SQL mostly clean
- Explanations adequate

**C-level work (70-79%):**
- Some queries incorrect
- Missing NULL checks
- SQL formatting inconsistent
- Minimal explanations

**Below C (<70%):**
- Multiple incorrect queries
- Doesn't handle NULLs
- Poor formatting
- Missing explanations

### Common Deductions

- **-5 points**: Using `= NULL` instead of `IS NULL`
- **-5 points**: Using aggregate in WHERE instead of HAVING
- **-5 points**: Notebook doesn't run end-to-end
- **-3 points**: Missing NULL checks where needed
- **-3 points**: Poor SQL formatting (no indentation, lowercase keywords)
- **-2 points**: Missing or unclear explanations

---

## 💡 Tips for Success

### Query Development Strategy

1. **Start small:** Use `LIMIT 10` to test queries quickly
2. **Build incrementally:**
   - Start with simple SELECT
   - Add WHERE conditions
   - Add ORDER BY
   - Remove LIMIT when ready
3. **Check for NULLs:** Always consider whether NULLs affect your answer
4. **Verify results:** Does the answer make business sense?

### SQL Best Practices

**Formatting:**
```sql
-- ✅ Good: Uppercase keywords, indented, clear
SELECT
    Country,
    COUNT(*) AS transaction_count,
    SUM(Quantity * Price) AS revenue
FROM retail
WHERE Price IS NOT NULL
GROUP BY Country
HAVING COUNT(*) > 100
ORDER BY revenue DESC
LIMIT 10
```

```sql
-- ❌ Bad: Hard to read
select country,count(*),sum(quantity*price) from retail where price is not null group by country having count(*)>100 order by 3 desc limit 10
```

### Common Mistakes to Avoid

1. **NULL handling:**
   ```sql
   -- ❌ Wrong
   WHERE customer_id = NULL

   -- ✅ Correct
   WHERE customer_id IS NULL
   ```

2. **WHERE vs HAVING:**
   ```sql
   -- ❌ Wrong - aggregate in WHERE
   WHERE COUNT(*) > 100

   -- ✅ Correct - aggregate in HAVING
   HAVING COUNT(*) > 100
   ```

3. **GROUP BY rules:**
   ```sql
   -- ❌ Wrong - Description not in GROUP BY or aggregated
   SELECT Country, Description, COUNT(*)
   FROM retail
   GROUP BY Country

   -- ✅ Correct - all non-aggregated columns in GROUP BY
   SELECT Country, Description, COUNT(*)
   FROM retail
   GROUP BY Country, Description
   ```

4. **Window function filtering:**
   ```sql
   -- ❌ Wrong - can't filter directly
   SELECT *, ROW_NUMBER() OVER (...) AS rn
   FROM retail
   WHERE rn = 1  -- Error!

   -- ✅ Correct - use subquery
   SELECT * FROM (
       SELECT *, ROW_NUMBER() OVER (...) AS rn
       FROM retail
   )
   WHERE rn = 1
   ```

### Performance Tips

- **Use LIMIT during development:** `LIMIT 10` makes queries instant
- **Check row counts:** Use `COUNT(*)` to verify your filters
- **Be specific:** Select only columns you need (not `SELECT *`)
- **Order matters:** For window functions, ORDER BY is often required

---

## 🚫 Academic Integrity

### What You CAN Do

✅ Review course notebooks and materials
✅ Consult SQL documentation
✅ Discuss concepts with classmates (conceptual only)
✅ Ask instructor/TA for clarification on requirements
✅ Use DuckDB documentation for syntax

### What You CANNOT Do

❌ Use AI tools (ChatGPT, Claude, Copilot, etc.) to write queries
❌ Copy queries from classmates
❌ Share your query code with others
❌ Look up answers to specific homework questions online
❌ Use query solutions from previous years

**Why?** We need to assess YOUR understanding. Using AI or copying means we can't help you where you're stuck.

**If you're stuck:** Ask the instructor/TA! That's what we're here for.

### Violations

Academic integrity violations will result in:
- Zero on the assignment
- Potential course-level consequences
- Report to university administration

We check for copying and AI usage. Don't risk it!

---

## ❓ Getting Help

### If You're Stuck

1. **Review the teaching notebooks** - examples are there!
2. **Check the SQL Quick Reference** (`references/sql_quick_reference.md`)
3. **Read error messages carefully** - they often tell you the problem
4. **Start simpler** - remove complexity until query works, then add back
5. **Ask for help!** - Office hours, email, course forum

### Common Issues

**"My query has a syntax error"**
- Check for missing commas
- Check quote marks around strings
- Check parentheses are balanced

**"I get way more/fewer rows than expected"**
- Check your WHERE conditions
- Check for NULL handling
- Use COUNT(*) to debug

**"My window function isn't working"**
- Did you include ORDER BY if needed?
- Check PARTITION BY column names
- Try simplifying the frame specification

**"Query is too slow"**
- Are you using LIMIT while testing?
- Check you're not doing nested queries unnecessarily

---

## 🗓️ Timeline

**Recommended schedule:**

- **Day 1, After Block B:** Start Part 1 (Basic Queries) - 30 minutes
- **Day 1, Evening:** Complete Part 1, start Part 2 (Aggregations) - 1 hour
- **Between classes:** Complete Part 2, Part 3 (Windows) - 1 hour
- **Before Day 2:** Review, test end-to-end, submit - 30 minutes

**Don't wait until the last minute!** Start early so you can ask questions if stuck.

---

## 🎓 Learning Goals

This assignment isn't just about getting the right answer. It's about:

1. **Building intuition** for when to use SQL vs Python
2. **Thinking in sets** instead of loops
3. **Understanding NULL** behavior (critical for real data!)
4. **Practicing incrementally** (build complex queries step-by-step)
5. **Working with real scale** (525K rows - this is actual analytics work!)

By the end, you should feel confident writing SQL to answer business questions on real datasets.

---

## 📚 Resources

**Course Materials:**
- Teaching notebooks: `notebooks/day1_block_b_01_sql_foundations.ipynb`, `02_aggregations.ipynb`, `03_window_functions.ipynb`
- SQL Quick Reference: `references/sql_quick_reference.md`
- Teacher Primer: `references/teaching/day1_block_b_teacher_primer.md`

**DuckDB Documentation:**
- SQL Introduction: https://duckdb.org/docs/sql/introduction
- Window Functions: https://duckdb.org/docs/sql/window_functions
- Aggregate Functions: https://duckdb.org/docs/sql/functions/aggregates

**External Resources (for concept clarification only):**
- Mode Analytics SQL Tutorial: https://mode.com/sql-tutorial/
- PostgreSQL Window Functions: https://www.postgresqltutorial.com/postgresql-window-function/

**Remember:** Use these for learning concepts, not for copying answers!

---

## ✉️ Questions?

If anything is unclear about the assignment requirements, ask!

- **Office hours:** [Time/Location TBD]
- **Email:** [Instructor email]
- **Course forum:** [If applicable]

**Don't struggle in silence.** If you're stuck for more than 15 minutes on one question, reach out for help!

---

**Good luck! 🚀 You've got this.**

Remember: This is real data analysis work. By completing this assignment, you're doing what data professionals do every day. Be proud of your work!
