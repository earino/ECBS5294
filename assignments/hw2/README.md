# Homework 2: TechMart Acquisition Data Integration

**Course:** ECBS5294 - Introduction to Data Science: Working with Data
**Due:** Day 3, Start of Class
**Total Points:** 100
**Est. Time:** 3-4 hours

---

## 🏢 The Business Scenario

You've just been hired as a Junior Data Analyst at **TechMart**, a rapidly growing e-commerce company that sells electronics, beauty products, and home goods online.

### The Situation

TechMart recently acquired **QuickBuy**, a smaller competitor, for $12 million. QuickBuy's entire product catalog and customer review system runs on a NoSQL database that exports everything as nested JSON.

Your manager walks into your cubicle on Monday morning:

> "We need QuickBuy's product data integrated into our analytics warehouse by Wednesday morning. Their API dumps everything as one massive JSON file - products, reviews, tags, everything nested together. Our BI team uses SQL and can't work with JSON.
>
> Can you normalize this into proper tables so we can analyze their product performance? The board meeting is Wednesday at 9 AM, and the executives need to know:
> 1. Which QuickBuy product categories we should keep vs discontinue
> 2. How their customer satisfaction compares to ours
> 3. Which products drive the most engagement
> 4. If there are any concerning patterns in negative reviews
>
> This is your first big project - nail this and you'll be presenting to the CFO next quarter!"

### Your Mission

Transform QuickBuy's messy JSON export into clean, normalized database tables that answer critical business questions before the board meeting.

### Why This Matters

- **$2.5M inventory decision**: Which product lines to keep
- **Customer retention**: Understanding satisfaction levels
- **Marketing budget**: Where to invest based on engagement
- **Integration timeline**: 50 developers waiting for your schema

---

## 📋 Overview

This assignment tests your ability to:
- Parse and understand complex JSON structures
- Normalize nested data into relational tables
- Implement data quality validations
- Load data into DuckDB
- Write SQL queries on normalized data
- Document your schema for technical teams

You'll work with QuickBuy's **COMPLETE product catalog: 194 products** containing **582 customer reviews** from their e-commerce platform.

---

## 🎯 Learning Objectives

By completing this assignment, you will demonstrate ability to:

1. Parse nested JSON data structures
2. Identify and extract nested objects and arrays
3. Normalize data into tidy relational tables
4. Maintain foreign key relationships during transformation
5. Implement data validation as code
6. Query normalized data with SQL joins
7. Create clear data documentation

---

## 📊 Dataset: QuickBuy Product Catalog

### Attribution & License
**Source:** DummyJSON - Free Fake REST API for Testing and Prototyping
**URL:** https://dummyjson.com/docs/products
**License:** Public API - Free to use for testing, prototyping, and educational purposes
**Attribution:** Not required but appreciated
**Downloaded:** Complete dataset (all 194 products)
**Educational Use:** ✅ Explicitly permitted

> **Note for students:** This is a public API designed for learning. In real work, always verify data licenses and usage rights!

### Dataset Details
- **Complete catalog:** All 194 products from QuickBuy's acquisition
- **Customer reviews:** 582 reviews across all products
- **Product-tag relationships:** 364 tags
- **Unique categories:** 24 product categories
- **File size:** 316 KB
- **Location:** `data/products_hw2.json`

### Why This Dataset?
DummyJSON provides realistic e-commerce data that mirrors real-world API responses:
- Complex nested structures (like production NoSQL exports)
- Realistic business data (products, reviews, ratings)
- No authentication required (focus on transformation, not API complexity)
- Designed for educational use

### JSON Structure

Each product contains:
```json
{
  "id": 1,
  "title": "Product Name",
  "price": 9.99,
  "category": "beauty",
  "dimensions": {
    "width": 23.17,
    "height": 14.43,
    "depth": 28.01
  },
  "meta": {
    "createdAt": "2024-05-23T08:56:21.618Z",
    "updatedAt": "2024-05-23T08:56:21.618Z",
    "barcode": "9164035109868"
  },
  "reviews": [
    {
      "rating": 2,
      "comment": "Very unhappy with my purchase!",
      "date": "2024-05-23T08:56:21.618Z",
      "reviewerName": "John Doe",
      "reviewerEmail": "john.doe@x.dummyjson.com"
    }
  ],
  "tags": ["beauty", "mascara"]
}
```

### Data Characteristics

**Nested Objects to Flatten:**
- `dimensions` → width, height, depth columns
- `meta` → created_at, updated_at, barcode columns

**Arrays to Normalize:**
- `reviews` → Separate reviews table (one-to-many, 582 total reviews)
- `tags` → Separate product_tags table (many-to-many, 364 relationships)

**Data Quality Notes:**
- All products have at least one review
- No missing core fields (id, title, price, category)
- Dates in ISO 8601 format
- Prices in USD (float)
- Average 3 reviews per product
- Categories span electronics, beauty, groceries, and more

---

## 📝 Assignment Structure

### Part 1: Data Ingestion & Exploration (15 points)
**The Head of Analytics needs to understand what we acquired**

Tests: JSON loading, structure exploration, data profiling

**4 questions**, 3-4 points each

### Part 2: Data Normalization (35 points)
**The BI team needs clean, relational tables for Tableau**

Tests: Flattening nested objects, extracting arrays, maintaining relationships

**3 transformations**, 11-12 points each

### Part 3: Data Validation (20 points)
**The Head of Data Quality warns: "QuickBuy had issues - verify everything!"**

Tests: Primary key uniqueness, foreign key integrity, data types, completeness

**4 validations**, 5 points each

### Part 4: Database Persistence (10 points)
**The Data Engineering team needs this in DuckDB by Tuesday night**

Tests: Table creation, data loading, verification

**2 tasks**, 5 points each

### Part 5: SQL Analysis (15 points)
**Answer the board's critical questions**

Tests: Joins, aggregations, business insights

**4 queries**, 3-4 points each

### Part 6: Data Dictionary (5 points)
**Document the schema for 50 developers**

Tests: Complete documentation of all tables and columns

**1 deliverable**, 5 points

---

## 📤 Submission Requirements

### What to Submit

1. **Completed Jupyter notebook:** `hw2_starter.ipynb` with all cells run
2. File must run successfully: **Restart Kernel & Run All Cells**
3. All outputs must be visible (transformations + query results)
4. Data dictionary must be complete

### Submission Format

- **File name:** `hw2_[your_name].ipynb` (e.g., `hw2_john_smith.ipynb`)
- **How:** Upload to Moodle
- **When:** Before start of Day 3 class

### Before Submitting - Checklist

- [ ] All TODO sections completed
- [ ] All code cells run without errors
- [ ] Three tables created: products (194 rows), reviews (582 rows), product_tags (364 rows)
- [ ] All assertions pass (no assertion errors)
- [ ] SQL queries return results
- [ ] Data dictionary complete (all columns from all 3 tables)
- [ ] Business insights included in markdown
- [ ] Notebook runs end-to-end: **Kernel → Restart & Run All**
- [ ] File renamed to `hw2_[your_name].ipynb`

**If your notebook doesn't run end-to-end, you will lose points!**

---

## 🎯 Grading Rubric

### Per Question Breakdown

Each question is graded on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 40% | Code works, produces correct output |
| **Data Thinking** | 25% | Handles edge cases, validates properly, considers relationships |
| **Code Quality** | 20% | Clean, readable, well-structured, proper types |
| **Communication** | 15% | Clear comments, business insights, good documentation |

### Overall Expectations

**A-level work (90-100%):**
- All transformations correct
- Clean normalization with proper relationships
- All validations pass
- SQL queries answer business questions insightfully
- Excellent documentation
- Shows understanding of business context

**B-level work (80-89%):**
- Most transformations correct
- Good normalization, minor issues
- Most validations implemented
- SQL queries work
- Adequate documentation

**C-level work (70-79%):**
- Some transformations incorrect
- Normalization has issues
- Missing some validations
- Basic SQL queries
- Minimal documentation

**Below C (<70%):**
- Multiple incorrect transformations
- Poor normalization
- Missing validations
- SQL queries don't work
- Missing documentation

### Common Deductions

- **-10 points**: Notebook doesn't run end-to-end
- **-5 points**: Missing foreign key relationships
- **-5 points**: Primary keys not unique
- **-5 points**: Data loss during transformation
- **-3 points**: Poor variable naming
- **-3 points**: No business insights in analysis
- **-2 points**: Incomplete data dictionary

---

## 💡 Tips for Success

### Normalization Strategy

1. **Start with exploration:** Understand the JSON structure first
2. **Flatten incrementally:**
   - First: Create products table (flatten dimensions, meta)
   - Then: Extract reviews (maintain product_id)
   - Finally: Extract tags (create bridge table)
3. **Verify relationships:** Check foreign keys match
4. **Count everything:** Ensure no data loss

### Common Patterns

**Flattening nested objects:**
```python
# Extract nested fields
df['width'] = df['dimensions'].apply(lambda x: x['width'])
df['height'] = df['dimensions'].apply(lambda x: x['height'])
```

**Extracting arrays to separate table:**
```python
# Extract reviews with foreign key
reviews_list = []
for product in products:
    product_id = product['id']
    for review in product['reviews']:
        review_row = {'product_id': product_id, **review}
        reviews_list.append(review_row)
```

**Creating bridge table for many-to-many:**
```python
# Product-tag relationships
tags_list = []
for product in products:
    for tag in product['tags']:
        tags_list.append({
            'product_id': product['id'],
            'tag': tag
        })
```

### Validation Best Practices

Always verify:
```python
# Primary keys are unique
assert df['id'].is_unique, "Duplicate IDs found!"

# Foreign keys are valid
assert reviews_df['product_id'].isin(products_df['id']).all()

# No data lost
assert len(reviews_df) == total_reviews_in_json

# Correct types
assert pd.api.types.is_datetime64_any_dtype(df['created_at'])
```

### Business Context

Remember you're answering board questions:
- **Category decisions:** Which have best reviews?
- **Engagement metrics:** Which products get most feedback?
- **Quality concerns:** Any patterns in low ratings?
- **Integration priorities:** What needs attention first?

---

## 🚫 Academic Integrity

### What You CAN Do

✅ Review course notebooks and materials
✅ Consult pandas/DuckDB documentation
✅ Discuss concepts with classmates (conceptual only)
✅ Ask instructor/TA for clarification
✅ Use the validation script to check your work

### What You CANNOT Do

❌ Use AI tools (ChatGPT, Claude, Copilot, etc.)
❌ Copy code from classmates
❌ Share your solution with others
❌ Look up complete solutions online
❌ Use solutions from previous years

**Why?** We need to assess YOUR understanding. The board meeting depends on accurate analysis!

### Violations

Academic integrity violations will result in:
- Zero on the assignment
- Report to CEO (course instructor)
- Potential termination (course failure)

---

## ❓ Getting Help

### If You're Stuck

1. **Review Day 2 Block B notebooks** - normalization examples
2. **Check the JSON structure carefully** - print intermediate steps
3. **Verify your transformations** - use .head() and .shape
4. **Read error messages** - they often tell you the issue
5. **Ask for help!** - Office hours, email, course forum

### Common Issues

**"KeyError when accessing nested field"**
- Check if field exists: `product.get('dimensions', {})`
- Handle missing values gracefully

**"Assertion fails on foreign keys"**
- Print both sets of IDs to compare
- Check for type mismatches (int vs string)

**"Wrong number of rows after normalization"**
- Count in original JSON first
- Check your loops aren't skipping items

**"SQL JOIN returns empty"**
- Verify table names
- Check column names match
- Ensure foreign keys align

---

## 🗓️ Timeline

**Recommended schedule:**

- **Day 2, After Block B:** Start Part 1 & 2 (Ingestion & Normalization) - 1.5 hours
- **Day 2, Evening:** Complete Part 3 & 4 (Validation & DuckDB) - 1 hour
- **Between classes:** Part 5 & 6 (SQL Analysis & Documentation) - 1 hour
- **Before Day 3:** Review, test end-to-end, submit - 30 minutes

**Don't wait!** The board meeting (and your grade) depends on this!

---

## 🎓 Learning Goals

This assignment simulates real data integration work:

1. **Understanding messy data** - Real APIs return nested JSON
2. **Normalization skills** - Converting NoSQL to relational
3. **Data quality mindset** - Never trust, always verify
4. **Business thinking** - Technical work serves business decisions
5. **Documentation habits** - Others depend on your work

By completing this, you'll have done actual data analyst work that companies need every day during mergers and acquisitions.

---

## 📚 Resources

**Course Materials:**
- Day 2 Block B notebooks: JSON normalization examples
- Day 2 Block A notebooks: SQL join patterns
- `references/json_normalization_guide.md` (if available)

**External Documentation:**
- Pandas JSON normalization: https://pandas.pydata.org/docs/user_guide/io.html#json
- DuckDB Python API: https://duckdb.org/docs/api/python/overview
- JSON structure viewer: https://jsonviewer.stack.hu/

**Business Context:**
- Think like an analyst: What would the CFO want to know?
- Consider the integration team: What documentation would help them?
- Remember the deadline: Board meeting is Wednesday!

---

## ✉️ Questions?

If anything is unclear about the requirements:

- **Office hours:** [Time/Location TBD]
- **Email:** [Instructor email]
- **Course forum:** Post questions for all to benefit

**Remember:** This is your first big project at TechMart. The executives are watching. Make it count!

---

## 🏆 Final Thought

**You're not just doing homework - you're making a $2.5M business decision.**

QuickBuy's data holds the key to TechMart's expansion strategy. Your analysis will directly influence which products appear on TechMart's website next quarter.

Thousands of customers, hundreds of suppliers, and your career at TechMart depend on getting this right.

**Good luck, analyst. The board is counting on you! 💼**