# Homework 3: Multi-City Data Integration & Pipeline

**Course:** ECBS5294 - Introduction to Data Science: Working with Data
**Due:** Wednesday, November 5, 23:59
**Total Points:** 100
**Est. Time:** 6-8 hours over 2 weeks

---

## 📋 Overview

This is your **final project** for the course. You'll demonstrate every skill you've learned across all three days by building an end-to-end data pipeline.

**What you'll do:**
- Ingest multi-format data (CSV + JSON)
- Build a bronze → silver → gold pipeline
- Normalize nested JSON
- Write validations as code
- Create business KPIs
- Document for stakeholders

**This is real data analyst work.** You're simulating what happens when your manager hands you data from multiple sources and says "make sense of this."

### Why 2 Weeks Instead of 1?

This assignment integrates **ALL skills from Days 1-3** (tidy data, SQL, JSON, pipelines). Unlike HW1 and HW2 which each focused on one day's content, HW3 is your capstone project demonstrating everything you've learned.

With 6-8 hours of work over 2 weeks, you can:
- Explore the data thoroughly without rushing
- Refine your analysis iteratively
- Produce portfolio-quality work you're proud of
- Balance this with your other coursework and commitments

**Recommended pace:** ~30-40 minutes per day = low pressure, high quality

**Questions?** Email throughout the 2 weeks—don't wait until the last day!

---

## 🏢 The Business Scenario

You've been hired as a **Data Analyst** at **PolicyMetrics**, a consulting firm that advises municipal governments on business policy.

### The Situation

Your firm has a new client: a coalition of mid-sized US cities exploring business regulation reform. They want to understand:
- How different cities manage business licensing
- Construction permit timelines and patterns
- Whether regulation affects business activity
- Best practices for streamlining processes

Your manager just dropped two data exports on your desk:

> **"We got data from Chicago and NYC's open data portals. Chicago gave us business licenses as CSV, NYC gave us building permits as JSON. They're messy—different schemas, different conventions, probably missing values.
>
> The steering committee meeting is next Monday. I need you to:
> 1. Integrate this into a clean analytical database
> 2. Pull out 5-7 key metrics comparing the cities
> 3. Write a one-page executive summary
>
> Don't overthink it—just get the data clean, validated, and ready for analysis. We'll use your database for the full report."**

### Your Mission

Build a production-ready data pipeline that:
- Handles multi-format sources (CSV + JSON)
- Validates data quality at every step
- Creates business metrics ready for reporting
- Documents assumptions and limitations clearly

**This pipeline will be reused** when the client sends updated data next quarter. Make it reproducible!

---

## 🎯 Learning Objectives

By completing this assignment, you will demonstrate ability to:

1. **Ingest multi-format data** (CSV, JSON)
2. **Build a multi-stage pipeline** (bronze → silver → gold)
3. **Normalize nested JSON** into relational tables
4. **Write data validations** as assertions
5. **Handle real-world messiness** (nulls, types, inconsistencies)
6. **Create business KPIs** with joins and aggregations
7. **Document thoroughly** (data dictionary, stakeholder communication)
8. **Ensure reproducibility** (relative paths, Restart & Run All)

---

## 📊 Datasets: Multi-City Business & Permitting Data

**Complete documentation:** `data/day3/hw3_data_pack/README.md`

### Dataset 1: Chicago Business Licenses
- **Format:** CSV
- **Records:** 50,000 business licenses
- **Source:** Chicago Data Portal (Public Domain)
- **Columns:** 37 columns including license type, business name, address, dates, status

**Key fields:**
- `license_id`: License identifier
- `legal_name`, `doing_business_as_name`: Business names
- `license_description`: Type of business
- `application_type`: ISSUE, RENEW, C_LOC (change location)
- `license_status`: AAC (active), REV (revoked), etc.
- `license_start_date`, `expiration_date`: License lifecycle
- `latitude`, `longitude`: Geolocation

### Dataset 2: NYC Building Permits
- **Format:** JSON (flat structure, 20,000 records)
- **Source:** NYC Open Data (Public Domain)
- **Key fields:**
  - `job__`: Job number (identifier)
  - `borough`: MANHATTAN, BROOKLYN, QUEENS, BRONX, STATEN ISLAND
  - `job_type`: Type of work (A1, NB, DM, etc.)
  - `permit_status`: ISSUED, EXPIRED, etc.
  - `issuance_date`, `expiration_date`, `filing_date`: Permit timeline
  - `owner_s_business_name`: Property owner
  - `gis_latitude`, `gis_longitude`: Geolocation (stored as strings!)

**Natural messiness you'll encounter:**
- Missing values in various fields
- Date formats as strings
- Lat/lon as strings (NYC) vs floats (Chicago)
- Different naming conventions
- No direct relationship between datasets (different domains)

**See full documentation:** `data/day3/hw3_data_pack/README.md`

---

## 📝 Assignment Structure

### Part 1: Data Ingestion & Exploration (15 points)

**Load both datasets and profile them.**

**Requirements:**
- Load Chicago CSV successfully
- Load NYC JSON successfully
- Display first few rows of each
- Document row counts, columns, data types
- Identify obvious data quality issues

**What to report:**
- Total records in each dataset
- Number of columns
- Sample of data (first 5-10 rows)
- Initial observations about data quality

**Grading:**
- 8 pts: Both datasets load correctly
- 4 pts: Initial profiling is thorough
- 3 pts: Clear observations documented

---

### Part 2: Bronze Layer (20 points)

**Preserve raw data exactly as received.**

**Requirements:**
- Load Chicago CSV into `bronze_chicago_licenses` table
- Load NYC JSON into `bronze_nyc_permits` table
- No transformations (except parsing JSON to DataFrame)
- Verify row counts match source files

**Why bronze matters:**
- Audit trail: "What did the source give us?"
- Debugging: If cleaning fails, start over from bronze
- Reproducibility: Original data preserved

**Grading:**
- 10 pts: Both bronze tables created correctly
- 5 pts: Row counts verified and documented
- 5 pts: Code is clean and well-commented

---

### Part 3: Silver Layer - Normalization (25 points)

**Transform into analysis-ready format.**

**Requirements for Chicago:**
- Fix date types (`application_created_date`, `license_start_date`, `expiration_date`)
- Cast numeric fields appropriately
- Standardize NULL representations
- Remove rows with NULL in critical fields (`license_id`)
- Create table: `silver_chicago_licenses`

**Requirements for NYC:**
- Parse JSON into DataFrame (if not already done)
- Fix date types (`issuance_date`, `expiration_date`, `filing_date`)
- **Convert lat/lon from strings to floats**
- Handle missing values appropriately
- Remove rows with NULL in critical fields (`job__`)
- Create table: `silver_nyc_permits`

**Document your decisions:**
- How many rows removed due to NULL critical fields?
- What did you do with other missing values?
- Any type conversion issues?

**Grading:**
- 12 pts: Chicago silver table correct (types, nulls handled)
- 12 pts: NYC silver table correct (types, lat/lon converted)
- 1 pt: Documentation of cleaning decisions

---

### Part 4: Silver Layer - Validations (15 points)

**Write assertions to prove data quality.**

**Requirements:**
You must write **at least 3 validations** (choose from these or create your own):

1. **Primary key uniqueness**
   - Chicago: `license_id` is unique (or composite key if needed)
   - NYC: `job__` is unique

2. **Required fields non-null**
   - No NULLs in critical identifier columns
   - No NULLs in key business fields

3. **Data type validation**
   - Dates are actually datetime type
   - Numeric fields are numeric
   - Lat/lon are floats (especially NYC!)

4. **Date range validation**
   - Dates fall within reasonable ranges (e.g., 2015-2025)
   - Start dates before end dates
   - No dates in the future

5. **Business rule validation**
   - Valid status codes only (if you know the valid set)
   - Geolocation within reasonable bounds (if applicable)

**Format:**
```python
# Validation 1: Primary key uniqueness
assert df['id'].is_unique, "Duplicate IDs found!"

# Validation 2: Required fields
assert df['id'].notna().all(), "NULL IDs found!"

# Validation 3: Date range
assert df['date'].min() >= pd.Timestamp('2015-01-01'), "Dates too old!"
```

**Grading:**
- 5 pts per validation (3 required = 15 pts)
- Must use assertions (not just print statements)
- Must include clear error messages
- Must actually validate something meaningful

---

### Part 5: Gold Layer - Analytics (15 points)

**Create business KPIs for the steering committee.**

**Requirements:**
Create **5-6 analytical queries** answering business questions.
- **Minimum:** 5 KPIs required (15 points)
- **Bonus:** 6th KPI earns +2 bonus points
- Quality over quantity: Five well-crafted KPIs > seven rushed queries
- Mix of single-dataset and creative analysis

**Suggested analyses (choose or create your own):**

**Chicago-focused:**
1. Top 10 license types by volume
2. License status breakdown (active vs revoked vs expired)
3. Trend over time (licenses issued per year)
4. Geographic concentration (top wards/neighborhoods)

**NYC-focused:**
1. Permits by borough
2. Average time from filing to issuance
3. Permit status distribution
4. Job types breakdown

**Cross-city (creative):**
1. Compare business density by geography
2. License/permit activity by year (both cities)
3. Any geographic insights using lat/lon

**Requirements:**
- At least 5 KPIs (6th earns +2 bonus points)
- Clear business context for each (why does this matter?)
- Use appropriate aggregations (COUNT, SUM, AVG, etc.)
- Use GROUP BY where appropriate
- Results should display clearly

**Grading:**
- 10 pts: KPIs are well-chosen and answer business questions
- 3 pts: SQL queries are correct and efficient
- 2 pts: Results display clearly with business context
- +2 pts: BONUS for 6th high-quality KPI

---

### Part 6: Documentation (10 points)

**Two deliverables:**

#### A. Data Dictionary (5 points)

Document all tables you created:

**Format:**
```
TABLE: silver_chicago_licenses

Columns:
- license_id (INTEGER): Unique license identifier [PK]
- legal_name (VARCHAR): Legal business name
- license_start_date (DATE): When license became effective
- ...

Row count: 49,123
Source: data/day3/hw3_data_pack/chicago_business_licenses.csv
Cleaning: Removed 877 rows with NULL license_id (1.75%)
```

**Requirements:**
- Document all silver and gold tables
- Include column names, types, descriptions
- Note primary keys
- Document row counts
- Explain cleaning decisions

#### B. Stakeholder Note (5 points)

Write **8-10 sentences** for non-technical executives explaining:
1. What the data shows (high-level findings)
2. What assumptions you made
3. What limitations exist
4. What questions the data CAN'T answer
5. Recommendations for next steps

**Audience:** City officials who don't know SQL but need to make policy decisions.

**Example opening:**
> "This analysis integrated 50,000 Chicago business licenses and 20,000 NYC building permits into a unified analytical database. The data shows that Chicago issues approximately 15,000 new business licenses annually, with retail and food service dominating (35% of all licenses). However, this data cannot answer questions about business closures or economic impact, as it only tracks licensing activity..."

**Grading:**
- 5 pts: Data dictionary complete and clear
- 3 pts: Stakeholder note hits all required points
- 2 pts: Writing is clear and professional

---

## 📤 Submission Requirements

### What to Submit

1. **Completed Jupyter notebook:** `hw3_starter.ipynb` with all cells run
2. File must run successfully: **Restart Kernel & Run All Cells** (in VS Code: **Restart**, then **Run All**)
3. All outputs must be visible
4. All 6 parts completed

### Submission Format

- **File name:** `hw3_[your_name].ipynb` (e.g., `hw3_jane_doe.ipynb`)
- **How:** Upload to Moodle
- **When:** **Wednesday, November 5, 23:59** (two weeks after class)

### Before Submitting - Checklist

- [ ] All 6 parts completed
- [ ] Code runs end-to-end without errors (Restart & Run All)
- [ ] All datasets load correctly with **relative paths**
- [ ] All assertions pass (validations succeed)
- [ ] At least 5 KPIs created and displayed
- [ ] Data dictionary complete (all tables documented)
- [ ] Stakeholder note written (8-10 sentences)
- [ ] File renamed to `hw3_[your_name].ipynb`

**Critical:** Your notebook must run on a fresh clone of the repo. Use **relative paths only**!
```python
# ✅ Correct
pd.read_csv('data/day3/hw3_data_pack/chicago_business_licenses.csv')

# ❌ Wrong
pd.read_csv('/Users/yourname/ECBS5294/data/...')
```

---

## 🎯 Grading Rubric

### Overall Breakdown

| Component | Points |
|-----------|--------|
| Part 1: Ingestion & Exploration | 15 |
| Part 2: Bronze Layer | 20 |
| Part 3: Silver - Normalization | 25 |
| Part 4: Silver - Validations | 15 |
| Part 5: Gold - Analytics | 15 |
| Part 6: Documentation | 10 |
| **Total** | **100** |

### Per-Question Grading

Each component is graded on:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 40% | Code works, produces correct output |
| **Data Thinking** | 25% | Handles edge cases, validates properly, considers business context |
| **Reproducibility** | 20% | Relative paths, runs end-to-end, documented assumptions |
| **Communication** | 15% | Clear comments, business framing, professional documentation |

### Grading Bands

**A-level work (90-100%):**
- All parts complete and correct
- Comprehensive validations catch real issues
- KPIs are insightful and well-chosen
- Documentation is thorough and professional
- Code is clean, reproducible, well-commented
- Goes beyond minimum requirements

**B-level work (80-89%):**
- Most parts complete and correct
- Validations implemented but basic
- KPIs answer questions adequately
- Documentation complete but could be deeper
- Code works but could be cleaner

**C-level work (70-79%):**
- Parts complete but some errors
- Missing some validations
- KPIs are basic or missing context
- Documentation incomplete
- Reproducibility issues

**Below C (<70%):**
- Multiple parts incomplete or incorrect
- Validations missing or trivial
- KPIs don't answer business questions
- Poor or missing documentation
- Notebook doesn't run end-to-end

### Common Deductions

- **-15 points**: Notebook doesn't run end-to-end (Restart & Run All fails)
- **-10 points**: Uses absolute paths instead of relative paths
- **-10 points**: Missing validations (fewer than 3)
- **-8 points**: Data dictionary incomplete
- **-8 points**: Stakeholder note missing or < 8 sentences
- **-5 points**: Fewer than 5 KPIs
- **-5 points**: Datasets don't load correctly
- **-3 points**: Poor code organization/comments
- **-3 points**: Missing business context on KPIs

---

## 💡 Tips for Success

### Start Early!

**Recommended schedule (2 weeks):**

**Week 1: Data Pipeline Foundation**
- **Oct 22 (Evening):** Read assignment thoroughly, explore data - 1 hour
- **Oct 23-24:** Parts 1-2 (Ingestion, Bronze layers) - 1 hour
- **Oct 25-27:** Part 3 (Silver normalization, type conversions) - 2-3 hours

**Week 2: Analysis & Documentation**
- **Oct 28-29:** Part 4 (Validations - write assertions) - 1.5 hours
- **Oct 30-Nov 1:** Part 5 (KPIs - start with 3-4, refine) - 2 hours
- **Nov 2-3:** Finish Part 5, complete Part 6 (Documentation) - 1.5 hours
- **Nov 4-5:** Final review, Restart & Run All, polish, submit - 1 hour

**Total: ~10 hours over 14 days = very manageable pace**

**Don't wait until November 4 to start!** Questions? Email throughout the 2 weeks.

### Pipeline Development Strategy

1. **Start simple, build up:**
   - Get bronze working first (just load data)
   - Then silver (one dataset at a time)
   - Then validations (one at a time)
   - Then gold (start with 2-3 KPIs, add more)

2. **Test incrementally:**
   - After each part, do Restart & Run All
   - Fix errors immediately (don't accumulate technical debt)
   - Use assertions to catch problems early

3. **Read the data pack README:**
   - `data/day3/hw3_data_pack/README.md` has column descriptions
   - Understanding the data saves time

### Handling Chicago CSV

```python
import pandas as pd

# Load Chicago data
chicago = pd.read_csv('data/day3/hw3_data_pack/chicago_business_licenses.csv')

# Check what you got
print(chicago.shape)
print(chicago.columns)
print(chicago.dtypes)
print(chicago.head())

# Fix dates
chicago['license_start_date'] = pd.to_datetime(chicago['license_start_date'])

# Load into DuckDB
import duckdb
con = duckdb.connect(':memory:')
con.execute("CREATE TABLE bronze_chicago_licenses AS SELECT * FROM chicago")
```

### Handling NYC JSON

```python
import json

# Load JSON
with open('data/day3/hw3_data_pack/nyc_building_permits.json', 'r') as f:
    nyc_data = json.load(f)

# Convert to DataFrame
nyc = pd.DataFrame(nyc_data)

# Check structure
print(f"Loaded {len(nyc)} permits")
print(nyc.columns)

# Critical: Convert lat/lon from strings to floats!
nyc['gis_latitude'] = pd.to_numeric(nyc['gis_latitude'], errors='coerce')
nyc['gis_longitude'] = pd.to_numeric(nyc['gis_longitude'], errors='coerce')

# Load into DuckDB
con.execute("CREATE TABLE bronze_nyc_permits AS SELECT * FROM nyc")
```

### Writing Good Validations

```python
# Validation 1: Primary key uniqueness
license_count = con.execute("SELECT COUNT(*) FROM silver_chicago_licenses").fetchone()[0]
license_unique = con.execute("SELECT COUNT(DISTINCT license_id) FROM silver_chicago_licenses").fetchone()[0]

assert license_count == license_unique, f"Duplicate license IDs! {license_count} rows but {license_unique} unique IDs"

# Validation 2: Date types
# Check that dates are actually datetime, not strings
chicago_clean = con.execute("SELECT * FROM silver_chicago_licenses LIMIT 1").df()
assert pd.api.types.is_datetime64_any_dtype(chicago_clean['license_start_date']), "Dates not parsed!"

# Validation 3: Lat/lon are numeric (especially important for NYC!)
nyc_clean = con.execute("SELECT * FROM silver_nyc_permits LIMIT 1").df()
assert pd.api.types.is_numeric_dtype(nyc_clean['gis_latitude']), "Latitude not numeric!"
```

### Creating Good KPIs

**Bad KPI (no context):**
```sql
SELECT COUNT(*) FROM silver_chicago_licenses
```

**Good KPI (business context):**
```python
print("=== KPI 1: Annual Business License Issuance ===")
print("Business Question: Is Chicago experiencing business growth?")
print()

result = con.execute("""
    SELECT
        EXTRACT(YEAR FROM license_start_date) as year,
        COUNT(*) as licenses_issued
    FROM silver_chicago_licenses
    WHERE license_start_date IS NOT NULL
        AND application_type = 'ISSUE'  -- New licenses only, not renewals
    GROUP BY EXTRACT(YEAR FROM license_start_date)
    ORDER BY year
""").df()

display(result)

print("\nInsight: Chicago issues approximately 15K new business licenses annually.")
print("Trend shows stable business formation with slight growth 2020-2023.")
```

---

## 🚫 Academic Integrity

### What You CAN Do

✅ Review all course notebooks (Day 1, 2, 3)
✅ Consult pandas/DuckDB documentation
✅ Discuss concepts with classmates (conceptual only)
✅ Ask instructor/TA for clarification on requirements
✅ Use the data pack README for column descriptions

### What You CANNOT Do

❌ Use AI tools (ChatGPT, Claude, Copilot, etc.) to write code
❌ Copy code from classmates
❌ Share your solution with others
❌ Look up complete solutions online
❌ Use solutions from previous years

**Why?** This is your final demonstration of what you've learned. Using AI or copying means we can't assess your actual skills—and you won't learn what you need for your career.

**If you're stuck:** Ask the instructor/TA! We're here to help you learn, not to watch you struggle.

### Violations

Academic integrity violations will result in:
- Zero on the assignment (25% of course grade)
- Potential course-level consequences
- Report to university administration

We check for copying and AI usage. Don't risk it!

---

## ❓ Getting Help

### If You're Stuck

1. **Check the data pack README** - Column descriptions and examples
2. **Review Day 2 Block B notebooks** - JSON normalization examples
3. **Review Day 3 Block A notebook** - Pipeline pattern examples
4. **Check your validations** - What assertion is failing? Why?
5. **Use print statements** - Debug incrementally
6. **Ask for help!** - Office hours, email, course forum

### Common Issues

**"Chicago CSV won't load"**
- Check file path (should be relative: `data/day3/hw3_data_pack/...`)
- Check for encoding issues (try `encoding='latin-1'`)
- Check that file exists (did you download the repo?)

**"NYC JSON parse error"**
- Use `json.load()` then `pd.DataFrame()`, not `pd.read_json()`
- Check that file is valid JSON (open in text editor)

**"Lat/lon aren't numeric"**
- NYC stores these as strings! Use `pd.to_numeric(..., errors='coerce')`
- Check result: some may be NULL (that's okay, document it)

**"Validation fails"**
- Good! That's the point of validations
- Read the assertion error - what does it tell you?
- Investigate: Run the query manually, inspect results
- Fix the data issue in silver layer, re-run

**"Can't think of KPIs"**
- Think about business questions: "How many X?", "What's the trend?", "Which is biggest?"
- Look at the columns: What can you count? Sum? Average? Group by?
- Refer to suggested analyses in Part 5

**"Notebook runs locally but not in fresh clone"**
- Check paths: Are they relative? (no `/Users/yourname/...`)
- Check imports: Did you import all necessary libraries?
- Check data files: Are they in the repo at the expected paths?

---

## 📚 Resources

**Course Materials:**
- Day 3 Block A notebook: Pipeline patterns, validations
- Day 2 Block B notebooks: JSON normalization
- Day 2 Block A notebook: Joins (if you want to relate datasets)
- Day 1 Block A notebook: Tidy data principles
- Data pack README: `data/day3/hw3_data_pack/README.md`

**Documentation:**
- Pandas: https://pandas.pydata.org/docs/
- DuckDB: https://duckdb.org/docs/
- Python datetime: https://docs.python.org/3/library/datetime.html

**Quick References:**
- `references/pipeline_patterns_quick_reference.md`
- `references/sql_quick_reference.md`
- `references/json_normalization_quick_reference.md`

**Remember:** Use these for learning concepts, not for copying solutions!

---

## 🎓 Learning Goals

This assignment isn't just about getting points. It's about demonstrating you can:

1. **Work with real data** - Messy, multi-format, from real sources
2. **Think systematically** - Pipeline pattern, not ad-hoc scripts
3. **Validate rigorously** - Catch problems before they become disasters
4. **Communicate clearly** - Technical work serves business decisions
5. **Work professionally** - Reproducible, documented, production-ready

**By completing this, you'll have:**
- Built a real data pipeline (portfolio-worthy!)
- Worked with government open data (common in industry)
- Demonstrated all Day 1-3 skills in one project
- Created something you can show in job interviews

**This is the capstone.** Make it count!

---

## ✉️ Questions?

If anything is unclear about the assignment requirements:

- **Office hours:** [Check Moodle for schedule]
- **Email:** RubiaE@ceu.edu
- **Course forum:** Moodle discussion board

**Don't struggle in silence!** If you're stuck for more than 30 minutes on one part, reach out.

---

**Good luck!** 🚀

You've learned a ton in three days. This is your chance to show what you can do. Build something you're proud of—something that demonstrates you're ready to be a data professional.

**We're rooting for you!**
