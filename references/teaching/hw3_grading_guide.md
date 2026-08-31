# HW3 Grading Guide

**Assignment:** End-to-End Data Integration Project
**Total Points:** 100
**Due:** See syllabus.md (two weeks after Day 3)

---

## Grading Philosophy

**HW3 is the capstone** - it integrates everything from Days 1-3:
- SQL querying and aggregation
- Multi-format data loading (CSV + JSON)
- JSON normalization
- Bronze → Silver → Gold pipelines
- Data validations
- Business thinking and communication

**Grade for:**
- ✅ Correctness: Does it work?
- ✅ Data thinking: Do they understand the data?
- ✅ Reproducibility: Can you run it?
- ✅ Communication: Can you understand their decisions?

**Don't grade for:**
- ❌ Code elegance (this isn't a CS course)
- ❌ Optimization (slow queries are fine if correct)
- ❌ Advanced techniques not taught

---

## Rubric Breakdown

### Part 1: Data Ingestion (15 points)

**What to look for:**

✅ **Full credit (15 pts):**
- Loaded both Chicago CSV and NYC JSON
- Used relative paths (`data/day3/hw3_data_pack/...`)
- Displayed sample rows with `.head()` or similar
- Printed row/column counts
- No errors when running cells

✅ **Partial credit:**
- 12 pts: Loaded both but absolute paths used
- 10 pts: Loaded only one dataset correctly
- 5 pts: Attempted but has errors

❌ **No credit (0 pts):**
- Didn't attempt or completely wrong approach

**Common issues:**
- Absolute paths: `/Users/student/...` instead of `data/...`
- Not displaying data (just loads silently)
- JSON not properly read (kept as string)

---

### Part 2: Bronze Layer (20 points)

**What to look for:**

✅ **Full credit (20 pts):**
- Created `bronze_chicago` and `bronze_nyc` tables
- Tables are exact copies of loaded data (no transformations)
- Used `CREATE TABLE AS SELECT * FROM ...` or similar
- Verified with row count checks
- Code runs without errors

✅ **Partial credit:**
- 15 pts: Both tables created but minor issues (extra columns, filtering)
- 10 pts: Only one bronze table created correctly
- 5 pts: Attempted but tables don't contain right data

❌ **No credit (0 pts):**
- No bronze tables created
- Bronze layer includes cleaning (that's silver!)

**Common issues:**
- Students clean data in bronze (mixing bronze/silver)
- Column selection instead of SELECT *
- Not actually creating tables (just DataFrames)

**Quick check:**
```python
# Run this in their notebook
bronze_count_chicago = con.execute("SELECT COUNT(*) FROM bronze_chicago").fetchone()[0]
bronze_count_nyc = con.execute("SELECT COUNT(*) FROM bronze_nyc").fetchone()[0]
# Should match CSV/JSON row counts
```

---

### Part 3: Silver Layer - Normalization (25 points)

**What to look for:**

✅ **Full credit (25 pts):**

**Chicago table (10 pts):**
- Correct data types (dates as DATE, numbers as FLOAT)
- Key columns present (license_id, legal_name, license_description, etc.)
- NULL handling documented

**NYC table (15 pts):**
- `silver_nyc_permits` (15 pts)
  - Correct types (dates cast, lat/lon numeric)
  - Primary key is `permit_id` (from `permit_si_no`) — 5 of these points are
    for correctly identifying the grain: `job_number` is NOT unique (one job
    spans many permits) and dropping "duplicate" job numbers destroys real
    permits
  - Key columns selected and named sensibly

✅ **Partial credit:**
- 20 pts: Chicago perfect, NYC partially normalized
- 15 pts: Chicago perfect, NYC not normalized (single table)
- 10 pts: Both attempted but type issues
- 5 pts: Basic cleaning but no normalization

❌ **No credit (0 pts):**
- No silver tables created
- Just copied bronze (no transformations)

**Common issues:**
- Asserting `job_number` uniqueness (it legitimately repeats — one job, many permits)
- Deduplicating on `job_number` and silently discarding ~30% of the permits
- Lat/lon kept as strings instead of floats
- Dates kept as strings

**Quick check:**
```python
# Check NYC grain handling
permit_count = con.execute("SELECT COUNT(*) FROM silver_nyc_permits").fetchone()[0]
unique_permits = con.execute("SELECT COUNT(DISTINCT permit_id) FROM silver_nyc_permits").fetchone()[0]
unique_jobs = con.execute("SELECT COUNT(DISTINCT job_number) FROM silver_nyc_permits").fetchone()[0]
# permit_count == unique_permits (permit_id is the PK)
# unique_jobs < permit_count (one job -> many permits; ~14.1k jobs over 20k permits)
```

---

### Part 4: Silver Layer - Validations (15 points)

**What to look for:**

✅ **Full credit (15 pts):**
- At least 3 meaningful validations (3 pts each)
- Clear error messages (don't just write `assert condition`)
- Validations actually run (not commented out)
- Examples:
  - Primary key uniqueness
  - Required fields non-null
  - Data type checks
  - Date range validation
  - Business rule validation

✅ **Partial credit:**
- 12 pts: 2 good validations
- 9 pts: 1 good validation
- 6 pts: Validations written but don't work
- 3 pts: Attempted but all trivial (`assert True`)

❌ **No credit (0 pts):**
- No validations
- All validations commented out

**Examples of GOOD validations:**
```python
# ✅ Primary key uniqueness
total = con.execute("SELECT COUNT(*) FROM silver_chicago").fetchone()[0]
unique = con.execute("SELECT COUNT(DISTINCT license_id) FROM silver_chicago").fetchone()[0]
assert total == unique, f"Duplicate license_ids! Total: {total}, Unique: {unique}"

# ✅ Required field non-null
null_count = con.execute("SELECT COUNT(*) FROM silver_nyc_permits WHERE permit_id IS NULL").fetchone()[0]
assert null_count == 0, f"Found {null_count} rows with NULL permit_id!"

# ✅ Business rule
neg_count = con.execute("SELECT COUNT(*) FROM silver_chicago WHERE license_fee < 0").fetchone()[0]
assert neg_count == 0, f"Found {neg_count} licenses with negative fees!"
```

**Examples of WEAK validations:**
```python
# ❌ Too vague
assert len(df) > 0, "No data"

# ❌ Trivial
assert True, "Data loaded"

# ❌ No error message
assert df['id'].is_unique
```

---

### Part 5: Gold Layer - Analytics (15 points)

**What to look for:**

✅ **Full credit (15 pts):**
- Created 5-7 KPI tables/queries (3 pts each, max 15)
- Each answers a clear business question
- Results are properly aggregated (GROUP BY, JOINs)
- Output displayed and makes sense
- Examples:
  - Licenses by business type
  - Permits by borough
  - Top license descriptions
  - Trend over time
  - Cross-dataset comparison

✅ **Partial credit:**
- 12 pts: 4 good KPIs
- 9 pts: 3 good KPIs
- 6 pts: 2 KPIs
- 3 pts: 1 KPI or attempted but incorrect

❌ **No credit (0 pts):**
- No gold layer
- Just SELECT * (no aggregation)

**Examples of GOOD KPIs:**
```sql
-- ✅ Clear business question: "Which business types are most common?"
SELECT
    license_description,
    COUNT(*) as num_licenses
FROM silver_chicago
GROUP BY license_description
ORDER BY num_licenses DESC
LIMIT 10

-- ✅ Trend analysis
SELECT
    YEAR(issue_date) as year,
    COUNT(*) as permits_issued
FROM silver_nyc_permits
GROUP BY YEAR(issue_date)
ORDER BY year

-- ✅ Cross-dataset insight
SELECT
    'Chicago' as city,
    COUNT(*) as business_count
FROM silver_chicago
UNION ALL
SELECT
    'NYC' as city,
    COUNT(*) as permit_count
FROM silver_nyc_permits
```

**Examples of WEAK KPIs:**
```sql
-- ❌ No aggregation
SELECT * FROM silver_chicago LIMIT 10

-- ❌ Too simple
SELECT COUNT(*) FROM silver_chicago

-- ❌ No business meaning
SELECT license_id FROM silver_chicago WHERE license_id > 1000
```

---

### Part 6: Documentation (10 points)

**What to look for:**

✅ **Full credit (10 pts):**
- **README or markdown cells** explaining the project (3 pts)
  - What datasets were used
  - What the pipeline does
  - How to run the notebook
- **Assumptions documented** (4 pts)
  - NULL handling decisions
  - Why certain rows were filtered
  - Data quality issues encountered
- **KPI interpretations** (3 pts)
  - What each gold query tells you
  - Business insights from results
  - Limitations of the analysis

✅ **Partial credit:**
- 7 pts: Has README/overview but missing assumptions
- 5 pts: Minimal documentation (only code comments)
- 3 pts: Very sparse, hard to understand what they did

❌ **No credit (0 pts):**
- No documentation at all
- Just code with no explanations

**What good documentation looks like:**

```markdown
## Assumptions

### Chicago Data
- Filtered out licenses with NULL `license_start_date` (847 rows, 1.7% of data)
- These appear to be incomplete applications
- Kept licenses with NULL `expiration_date` (assumed perpetual licenses)

### NYC Data
- Kept one row per permit keyed by `permit_id`; documented that `job_number` legitimately repeats (one job, many permits)
- Converted lat/lon strings to floats, 523 rows had invalid coordinates (set to NULL)
- Permits without valid addresses excluded from geographic analysis

## KPI Insights

### Top Business Types
- "Retail Food Establishment" is most common (8,234 licenses)
- Suggests Chicago has vibrant food scene
- Note: This doesn't account for business size or revenue

### Limitations
- Can't compare Chicago vs NYC directly (different permit types)
- Chicago data is licenses, NYC is building permits
- No revenue data, so can't assess economic impact
```

---

## Overall Grading Rubric (Meta)

### Correctness (40 points)
- Parts 1, 2, 3, 5 primarily
- Does the code run?
- Are results correct?

### Data Thinking (25 points)
- Parts 3, 4, 6 primarily
- Do they understand what the data means?
- Did they normalize appropriately?
- Did they validate meaningfully?
- Did they interpret results correctly?

### Reproducibility (20 points)
- Spans all parts
- Can you run their notebook?
- Relative paths used?
- Clear instructions?
- No hardcoded values that break on other machines?

### Communication (15 points)
- Part 6 primarily
- Can you understand their decisions?
- Are assumptions documented?
- Are results explained?

---

## Quick Grading Workflow

**Estimated time per assignment: 15-20 minutes**

### Step 1: Run notebook (5 min)
```bash
uv run jupyter nbconvert --to notebook --execute hw3_starter.ipynb --inplace
```
- If it runs without errors → good sign for reproducibility
- If it crashes → check if it's absolute paths or real logic errors

### Step 2: Spot check outputs (5 min)
- Bronze row counts match source data?
- Silver tables have correct structure (check schema)?
- Validations actually ran (not commented out)?
- Gold queries return sensible results?

### Step 3: Grade by rubric (5 min)
- Use scorecard (see below)
- Mark off points for each section
- Note specific issues

### Step 4: Written feedback (3 min)
- Highlight what they did well
- Note 1-2 areas for improvement
- Keep it concise

### Step 5: Final score (2 min)
- Sum up all parts
- Double-check math
- Enter in Moodle

---

## Grading Scorecard Template

```
Student Name: _______________
Total: ____/100

Part 1: Data Ingestion          ____/15
  - Chicago CSV loaded          ____/7
  - NYC JSON loaded             ____/7
  - Sample output shown         ____/1

Part 2: Bronze Layer            ____/20
  - bronze_chicago              ____/10
  - bronze_nyc                  ____/10

Part 3: Silver Normalization    ____/25
  - silver_chicago (types)      ____/10
  - silver_nyc_permits (types)  ____/10
  - NYC grain/key identified    ____/5

Part 4: Validations             ____/15
  - Validation 1                ____/5
  - Validation 2                ____/5
  - Validation 3                ____/5

Part 5: Gold Analytics          ____/15
  - KPIs created (3 pts each)   ____/15
  - Count: ___ KPIs

Part 6: Documentation           ____/10
  - Overview/README             ____/3
  - Assumptions documented      ____/4
  - KPI interpretations         ____/3

Reproducibility Bonus/Penalty:  ____/0
  - Runs without errors: +0
  - Absolute paths: -2
  - Won't run at all: -5

Notes:
_________________________________
_________________________________
_________________________________
```

---

## Common Student Mistakes

### 1. Absolute paths
**Issue:** `/Users/student/Downloads/data.csv`
**Impact:** Won't run on grader's machine
**Penalty:** -2 to -5 points (reproducibility)
**Fix guidance:** "Use relative paths: `data/day3/hw3_data_pack/...`"

### 2. Skipping validations
**Issue:** Part 4 empty or trivial
**Impact:** Major conceptual gap
**Penalty:** 0-6 points (instead of 15)
**Fix guidance:** "Validations ensure data quality. Add assertions for primary keys, non-null fields, and business rules."

### 3. Wrong NYC grain
**Issue:** Treated `job_number` as the primary key — asserted its uniqueness or deduplicated on it
**Impact:** Either a failing validation, or ~30% of real permits silently discarded
**Penalty:** -5 to -10 points
**Fix guidance:** "One job can carry many permits. The unique key is `permit_si_no` (permit_id); validate THAT, and document the one-to-many job->permit relationship."

### 4. Weak gold layer
**Issue:** Just SELECT * queries, no aggregation
**Impact:** Doesn't demonstrate analytical thinking
**Penalty:** 0-6 points (instead of 15)
**Fix guidance:** "Use GROUP BY, JOINs, and aggregates (COUNT, SUM, AVG) to answer business questions."

### 5. No documentation
**Issue:** Just code, no explanations
**Impact:** Can't understand their decisions
**Penalty:** 0-3 points (instead of 10)
**Fix guidance:** "Add markdown cells explaining your assumptions, especially how you handled NULLs and why you filtered certain rows."

---

## Edge Cases

### What if their approach is different but correct?

**Example:** Student uses pandas instead of SQL for everything

**Answer:** That's fine! Grade based on:
- Does it work?
- Did they create the 3 layers?
- Are validations present?
- Are results correct?

Method doesn't matter as long as concepts are demonstrated.

### What if they found a data quality issue you didn't notice?

**Example:** Student discovers that Chicago has duplicate license IDs for renewals

**Answer:**
- This is GOOD data thinking!
- Give full credit even if their approach differs from yours
- Consider bonus points for excellent analysis
- Update your own solution notes

### What if notebook won't run?

**Try:**
1. Check for absolute paths - fix manually and re-run
2. Check for missing datasets - are files in right location?
3. Check for hardcoded values - adjust and re-run

**If still won't run:**
- Grade what you can see (code structure, logic)
- Deduct reproducibility points
- Leave feedback: "Couldn't run notebook - please use relative paths and test with Restart & Run All"

### What if they went WAY above and beyond?

**Example:** Created 15 KPIs, beautiful visualizations, perfect documentation

**Answer:**
- Cap at 100 points (no extra credit)
- Leave enthusiastic feedback
- Consider sharing (anonymously) as example for future students
- Mention in class (if appropriate): "Someone did an amazing job on HW3!"

---

## Time-Saving Tips

### Batch grade similar issues
- If 5 students made same mistake, write feedback once and copy/paste

### Use rubric strictly
- Don't overthink - if validation is there and works, give points
- Don't deduct for style issues (unless specifically wrong)

### Prioritize correctness over elegance
- Ugly code that works > beautiful code that doesn't
- This is a data course, not a software engineering course

### Focus on big picture
- Did they demonstrate understanding of pipelines?
- Can they validate data?
- Can they think analytically?

---

## Feedback Templates

### Excellent work (95-100)
```
Excellent work on HW3! Your pipeline is well-structured, validations are thorough, and your KPIs provide genuine business insights. Your documentation clearly explains your decisions and assumptions. This is exactly what we're looking for in data analysis work. Keep it up!
```

### Good work with room for improvement (85-94)
```
Nice job on HW3! Your pipeline works correctly and produces good results. A few suggestions: [specific feedback]. Overall, solid understanding of the concepts. Well done!
```

### Solid effort but key gaps (75-84)
```
Good effort on HW3. You've got the basic structure right, but there are some important areas to improve: [specific feedback]. Please review [specific topic] from Day 3 materials. Reach out if you have questions!
```

### Needs significant improvement (< 75)
```
Thank you for submitting HW3. There are some fundamental issues that need addressing: [specific feedback]. I strongly recommend reviewing the Day 3 materials and attending office hours to discuss. This is important for the final exam.
```

---

## Post-Grading Actions

**After grading all submissions:**

1. **Calculate statistics**
   - Average score
   - Distribution
   - Common mistakes

2. **Create summary for class**
   - Don't name names
   - Highlight common issues
   - Share best practices observed

3. **Update teaching notes**
   - What did students struggle with?
   - What needs more emphasis next year?
   - Were instructions clear?

4. **Prepare for final exam**
   - Students weak on validations → review in exam prep
   - Students strong on SQL → can focus elsewhere

---

## Summary

**HW3 is comprehensive** - it tests everything from the course:
- Technical skills (SQL, Python, data processing)
- Conceptual understanding (pipelines, normalization)
- Professional skills (documentation, reproducibility)

**Grade fairly but firmly:**
- Give credit for correct work
- Deduct for missing key concepts
- Provide constructive feedback

**Remember:**
- This is a learning exercise, not a job evaluation
- Students are still developing these skills
- Your feedback shapes their understanding

**Estimated grading time:** 4-6 hours for 20 students

**Good luck with grading!** 🎓
