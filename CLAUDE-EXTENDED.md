# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a course repository for **ECBS5294: Introduction to Data Science: Working with Data** at Central European University. The course focuses on practical data literacy: tidy data principles, SQL with DuckDB, JSON/API ingestion, and reproducible multi-stage pipelines.

## 🚨 CRITICAL: TESTING REQUIREMENT

**MANDATORY FOR ALL TEACHING MATERIALS**

### Execute EVERY Query in EVERY Notebook

Before committing ANY teaching notebook or assignment:

1. **Execute the entire notebook from scratch**:
   ```bash
   uv run jupyter nbconvert --to notebook --execute notebooks/your_notebook.ipynb --inplace --ExecutePreprocessor.timeout=300
   ```

2. **Verify EVERY SINGLE query returns meaningful results**:
   - ❌ **NEVER** write queries that return empty results
   - ❌ **NEVER** use filter conditions that don't match your data
   - ❌ **NEVER** assume data constraints without checking
   - ✅ **ALWAYS** verify examples show actual data
   - ✅ **ALWAYS** test queries against actual dataset constraints

3. **Common mistakes to avoid**:
   - Writing `WHERE price > 5` when max price is $5.00 → Returns nothing!
   - Writing `WHERE item = 'Latte'` when no Latte exists → Returns nothing!
   - Writing `WHERE revenue > 30` when max revenue is $25 → Returns nothing!
   - Writing queries based on assumptions instead of data reality

4. **Data constraint verification workflow**:
   ```python
   # BEFORE writing teaching queries, check data reality:
   con.execute("SELECT MAX(price) FROM data").df()
   con.execute("SELECT DISTINCT item FROM data").df()
   con.execute("SELECT MAX(price * quantity) as max_revenue FROM data").df()

   # THEN write queries that will return meaningful results
   # THEN execute entire notebook end-to-end
   # THEN verify EVERY example shows data
   ```

### Why This Matters

**Students will think THEY made a mistake** if your teaching example returns empty results. This destroys confidence and wastes learning time. Empty results are ONLY acceptable when:
- You're explicitly teaching "this query returns nothing because..."
- The pedagogical point is understanding empty results

**Otherwise, every teaching query MUST return meaningful data.**

### Testing Checklist

Before pushing any notebook:
- [ ] Executed entire notebook from scratch (VS Code: Restart, then Run All)
- [ ] Verified EVERY SQL query returns rows (unless pedagogically intentional)
- [ ] Verified EVERY code example produces visible output
- [ ] Verified EVERY calculated column shows non-NULL values
- [ ] Checked dataset constraints match query assumptions
- [ ] Tested with actual data, not imagined data

**If you skip this, students WILL find broken queries in class. Don't skip this.**

### Notebook Output Management

**Teaching notebooks must be committed WITHOUT outputs.** Students should execute notebooks themselves and see fresh results.

#### Why Clear Outputs?

1. **Learning by doing**: Students learn better by running code themselves
2. **Clean diffs**: Git diffs are much cleaner without output noise
3. **File size**: Notebooks with large outputs bloat the repository
4. **Fresh start**: Students shouldn't see old/stale outputs from your machine

#### Automated Output Clearing

The repository has a **pre-commit hook** that automatically clears all notebook outputs before committing:

```bash
# Pre-commit hook automatically runs:
# 1. Detects any .ipynb files being committed
# 2. Clears their outputs using scripts/clear_notebook_outputs.py
# 3. Re-stages the cleaned notebooks
```

**You don't need to do anything** - the hook handles it automatically when you commit.

#### Manual Output Clearing

If you need to clear outputs manually (for testing or cleanup):

```bash
# Clear all teaching notebooks
python scripts/clear_notebook_outputs.py --all

# Clear specific notebook
python scripts/clear_notebook_outputs.py notebooks/day1_block_a_tidy_foundations.ipynb

# Clear multiple notebooks
python scripts/clear_notebook_outputs.py notebooks/day1_*.ipynb

# Dry run (see what would be cleared)
python scripts/clear_notebook_outputs.py --all --dry-run
```

#### Local Testing Workflow

When developing teaching materials:

1. **Work with outputs locally** (run cells, see results)
2. **Test end-to-end** with "Restart & Run All"
3. **Verify all queries return data** (per checklist above)
4. **Commit when ready** - pre-commit hook clears outputs automatically
5. **Pull/clone will have clean notebooks** - students run from scratch

#### Solution Notebooks Exception

**Solution notebooks are handled differently:**
- They're gitignored (never committed unencrypted)
- They can keep outputs (students won't see them)
- Only encrypted ZIPs are committed (see Solution File Management)

---

## Project Structure

Expected directories:
- `/data` - Teaching datasets (offline, provided)
- `/notebooks` - Jupyter notebooks for exercises and assignments
- `/sql` - SQL query files
- `/scripts` - Utility scripts for course management
- `/solutions` - Encrypted solution archives (password-protected ZIPs)
- `/references` - Teaching resources and documentation
- Root contains `README.md` and course materials

## Solution File Management

**CRITICAL SECURITY REQUIREMENT**: Solution files must NEVER be committed to git unencrypted.

### File Naming Conventions

**Solution Source Files** (before encryption):
- Jupyter notebooks: `{assignment}_solution.ipynb`
- Python scripts: `{assignment}_solution.py`
- SQL queries: `{assignment}_solution.sql`

Examples:
- `day1_exercise_tidy_solution.ipynb`
- `hw1_solution.ipynb`
- `query_solution.sql`

**Encrypted Archives** (for git commits):
- Pattern: `solutions/solutions-{descriptor}.zip`
- Examples:
  - `solutions/solutions-day1-blockA.zip`
  - `solutions/solutions-hw1.zip`
  - `solutions/solutions-midterm.zip`

### Encryption Workflow

**Before ANY git commit containing solutions**:

1. **Encrypt the solution**:
   ```bash
   python scripts/encrypt_solutions.py \
     notebooks/day1_exercise_tidy_solution.ipynb \
     --password "secure-password" \
     --day 1 \
     --block A
   ```

2. **Check solution status**:
   ```bash
   python scripts/list_solutions.py
   ```

3. **Commit ONLY the encrypted ZIP**:
   ```bash
   git add solutions/solutions-day1-blockA.zip
   git commit -m "Add encrypted solutions for Day 1 Block A"
   ```

4. **Document password** in `solutions/PASSWORDS.md` (gitignored):
   - File must never be committed
   - Keep backed up securely outside repository

### Git Pre-Commit Hook

The repository has an **automated pre-commit hook** that:
- ✅ **Allows**: Encrypted ZIP files in `solutions/`
- ✅ **Verifies**: ZIPs are password-protected
- ❌ **Blocks**: Any `*_solution.ipynb` or `*_solution.py` files
- ❌ **Blocks**: Any files with "solution" in path (case-insensitive) except ZIPs

**Install/activate the hook**:
```bash
./scripts/setup_hooks.sh
```

### .gitignore Patterns

The following patterns are gitignored to prevent accidental commits:
```
*_solution.ipynb
*_solution.py
*/solution.ipynb
*/solution.py
solutions/PASSWORDS.md
solutions/decrypted/
solutions/.encryption_log.txt
```

### Available Scripts

- **`scripts/clear_notebook_outputs.py`** - Clear outputs from Jupyter notebooks (manual use)
- **`scripts/encrypt_solutions.py`** - Create password-protected solution ZIPs
- **`scripts/decrypt_solutions_zip.py`** - Extract encrypted solutions (instructor/TA use)
- **`scripts/list_solutions.py`** - Show status of all solutions (encrypted vs unencrypted)
- **`scripts/setup_hooks.sh`** - Install git pre-commit hook

### Security Rules

**NEVER**:
- Commit unencrypted solution files
- Commit `solutions/PASSWORDS.md`
- Use weak or guessable passwords
- Share passwords before assignment due dates
- Disable git hooks without good reason

**ALWAYS**:
- Encrypt solutions before committing
- Test decryption before pushing
- Run `list_solutions.py` before git commits
- Document passwords in `PASSWORDS.md` immediately
- Keep `PASSWORDS.md` backed up securely (outside repo)

### For Students

Students receive encrypted ZIPs from day one but passwords are released only after assignment due dates. This approach:
- Ensures solutions are immediately available post-deadline
- Encourages attempting problems before looking at answers
- Removes anxiety about "losing" solutions

See `solutions/README.md` for student-facing instructions.

---

## Notebook Format Requirements

**MANDATORY: All Jupyter notebooks MUST use nbformat 4.5 with unique cell IDs**

### Why This Matters

Jupyter Notebook format 4.5 (introduced 2020) requires **unique cell IDs** for each cell. This enables:
- ✅ Better version control (git diffs show which cells changed)
- ✅ Improved merge conflict resolution
- ✅ Cell-level tracking across notebook versions
- ✅ Compatibility with modern Jupyter tools (VS Code, JupyterLab 3+)

**Without cell IDs:** Git diffs are noisy, merges fail, and notebooks may not load correctly in modern environments.

### Required Format

**Top-level structure:**
```json
{
  "cells": [...],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3 (ipykernel)",
      "language": "python",
      "name": "python3"
    },
    "language_info": {...}
  },
  "nbformat": 4,
  "nbformat_minor": 5
}
```

**Each cell structure:**
```json
{
  "cell_type": "markdown",
  "id": "a1b2c3d4",
  "metadata": {},
  "source": [
    "Line 1 of content\n",
    "Line 2 of content\n"
  ]
}
```

**Important:** Cell `id` field is **REQUIRED** and must be:
- **8 characters long**
- **Lowercase hexadecimal** (0-9, a-f)
- **Unique within the notebook**

**Code cells:**
```json
{
  "cell_type": "code",
  "execution_count": null,
  "id": "e5f6g7h8",
  "metadata": {},
  "outputs": [],
  "source": [
    "import pandas as pd\n",
    "print('Hello')\n"
  ]
}
```

### Automated Validation

A **pre-commit hook** automatically validates notebook format before commits:
- Checks nbformat version is 4.5+
- Verifies all cells have IDs
- Ensures IDs are unique and properly formatted (8-char hex)
- **Blocks commit if validation fails** with clear error message

**Install the hook:**
```bash
./scripts/setup_hooks.sh
```

### Creating New Notebooks

**Option 1: Use VS Code (recommended)**
```bash
code notebook.ipynb  # VS Code adds cell IDs automatically on save
code notebook.ipynb  # VS Code with Jupyter extension
```

Modern editors automatically handle cell IDs when you save.

**Option 2: Convert old notebooks**
```bash
# Jupyter can upgrade old notebooks to nbformat 4.5
uv run jupyter nbconvert --to notebook --inplace old_notebook.ipynb
```

This adds missing cell IDs automatically.

**Option 3: Manual creation (advanced)**
```python
import json
import secrets

# Generate unique 8-char hex ID
def generate_cell_id():
    return secrets.token_hex(4)  # 4 bytes = 8 hex chars

# Example cell with ID
cell = {
    "cell_type": "markdown",
    "id": generate_cell_id(),
    "metadata": {},
    "source": ["# My Title\n"]
}
```

### Verification

**Check your notebook format:**
```bash
python3 -c "import json; nb=json.load(open('notebook.ipynb')); print(f'nbformat: {nb[\"nbformat\"]}.{nb[\"nbformat_minor\"]}'); print(f'Cells with IDs: {sum(1 for c in nb[\"cells\"] if \"id\" in c)}/{len(nb[\"cells\"])}')"
```

**Expected output:**
```
nbformat: 4.5
Cells with IDs: 50/50
```

If you see `Cells with IDs: 0/50` or `nbformat: 4.4`, your notebook needs updating!

### Pre-Commit Hook Details

The validation hook checks:
1. ✅ `nbformat == 4`
2. ✅ `nbformat_minor >= 5`
3. ✅ Every cell has an `id` field
4. ✅ All IDs are 8-character lowercase hexadecimal strings
5. ✅ All IDs are unique within the notebook
6. ✅ No duplicate IDs exist

**If validation fails**, the commit is blocked and you'll see a clear error message:
```
❌ NOTEBOOK FORMAT ERROR: notebooks/example.ipynb
   - Missing cell IDs: cells at indices [0, 5, 12]
   - Invalid ID format: 'abc' (must be 8-char hex)
   - Duplicate IDs found: 'a1b2c3d4' appears 2 times

Fix these issues and try again.
Run: uv run jupyter nbconvert --to notebook --inplace notebooks/example.ipynb
```

### Common Issues & Fixes

**Issue:** "Cell IDs missing" error when committing
**Fix:** Open notebook in VS Code and save (auto-adds IDs), or run:
```bash
uv run jupyter nbconvert --to notebook --inplace your_notebook.ipynb
```

**Issue:** "Duplicate cell ID" error
**Fix:** Manually edit the notebook JSON to ensure unique IDs, or re-save in VS Code

**Issue:** "Invalid ID format" (e.g., ID is too long or contains uppercase)
**Fix:** Manually correct IDs to be exactly 8 lowercase hex characters, or regenerate

**Issue:** Old nbformat version (4.4 or lower)
**Fix:** Run `uv run jupyter nbconvert --to notebook --inplace your_notebook.ipynb`

### Why Cell IDs Were Introduced

**Historical context:** Before nbformat 4.5, Jupyter notebooks had no stable cell identifiers. This caused:
- ❌ Poor git diffs (entire notebook shown as changed even for 1-cell edit)
- ❌ Merge conflicts were nearly impossible to resolve
- ❌ No way to track "is this the same cell after refactoring?"
- ❌ Extensions couldn't reliably reference specific cells

**With cell IDs:**
- ✅ Git shows exactly which cells changed
- ✅ Merge conflicts can be resolved cell-by-cell
- ✅ Cells maintain identity across moves/edits
- ✅ Extensions can reference cells reliably

**Bottom line:** Use nbformat 4.5. It's been the standard since 2020, and all modern tools expect it.

---

## Core Technologies

- **Python 3.13** - Primary language (pinned via `.python-version`, managed by uv)
- **VS Code** - Development environment (Python 3.13 environment managed by uv)
- **DuckDB** - Embedded SQL database (Python API or CLI)
- **Git** - Version control

## Key Concepts & Patterns

### Data Pipeline Pattern (Bronze → Silver → Gold)
- **Bronze**: Raw ingestion (preserve original)
- **Silver**: Cleaned, typed, validated
- **Gold**: Analysis-ready with joins and aggregations

### Tidy Data Principles
- Each variable is a column
- Each observation is a row
- Designate UID/primary keys explicitly
- Handle types correctly (dates, floats, booleans)
- Document missing value handling

### SQL Focus Areas
- Single-table queries: `SELECT`, `WHERE`, `ORDER BY`, `GROUP BY/HAVING`
- Joins: INNER, LEFT, RIGHT, FULL (watch for duplicate inflation)
- Window functions (scoped primer):
  - `ROW_NUMBER()` for deduplication/latest records
  - `LAG()` for period-over-period calculations
  - Moving averages with `ROWS BETWEEN`
- NULL handling in conditions and aggregations

## Development Requirements

### Reproducibility Standards
- All code must **Run-All** successfully from clean clone
- Use **relative paths** only
- No hardcoded absolute paths
- Clear notebook cell execution order
- Small, logical Git commits

### Validation Patterns
Include validations as code:
- Primary key uniqueness checks
- Required field non-null assertions
- Date window/range validations
- Join cardinality checks

### Communication Standards
- Provide concise data dictionaries for outputs
- Include stakeholder-facing notes (8-10 sentences)
- Document assumptions and limitations
- Present results as clear tables/metrics

## Common Tasks

### Working with DuckDB
```python
import duckdb
con = duckdb.connect('database.db')
# Query CSVs directly
con.execute("SELECT * FROM 'data/file.csv'")
# Query Parquet
con.execute("SELECT * FROM 'data/file.parquet'")
```

### JSON Normalization Pattern
1. Ingest JSON (file or endpoint)
2. Parse to dict/list structures
3. Normalize nested structures to flat tables
4. Persist to DuckDB with proper types
5. Join with dimension tables as needed

### Performance Considerations
- Prefer dict lookups over list iteration for key-based access
- Understand join cardinality impact on result size
- Use columnar formats (Parquet) for larger datasets over CSV

## Data Handling Notes

### Common Pitfalls
- Locale-dependent CSV separators
- Floating-point precision issues
- Date parsing and timezone handling
- Header drift in spreadsheets
- Categorical codes vs labels (use reference tables)

### Preferred Approaches
- SQL for set-based operations, filtering, aggregation
- Python for complex transformations, API calls, normalization
- Assertions for data quality checks (fail fast)
- Idempotent transforms (re-runnable without side effects)

## Academic Context

**AI Tool Policy**: AI assistants (ChatGPT/Claude/Copilot) are NOT permitted for graded work. Only assist with learning/understanding, not assignment completion.

**Grading Components**: Correctness (40%), Data thinking (25%), Reproducibility (20%), Communication (15%)

---

## Adding New Day Materials (Day 2, Day 3, etc.)

This section captures the workflow and patterns established during Day 1 development to ensure consistency across all course days.

### Step-by-Step Workflow

#### 1. Plan the Day Structure

**Before creating any files:**
- Review `syllabus.md` for the day's learning objectives
- Identify what will be covered in Block A vs Block B
- Determine what datasets will be needed
- Plan the in-class exercise/deliverable
- Identify the homework assignment

**Key questions:**
- What's the "hook" or motivating problem?
- What real-world datasets exemplify these concepts?
- What will students build/produce today?
- How does this connect to previous days?

#### 2. Gather or Create Datasets

**Location:** `data/day{N}/`

**Requirements:**
- Use real-world datasets (prefer Kaggle with proper attribution)
- Datasets should be "messy enough" to be instructive
- Include intentional data quality issues students must handle
- Size: 500-10K rows for exercises, 50K+ for SQL homework
- All datasets must work **offline** (no API keys required for class)

**Create data README:**
```markdown
# Day {N} Dataset: {Name}

**Source:** {URL}  
**License:** {License}  
**File:** `{filename}`

## Dataset Description
[Description of what the data represents]

## Intentional Data Quality Issues
[List the messiness students will encounter]

## What "Clean" Looks Like
[Success criteria for cleaning]
```

**Example:** See `data/day1/README.md`

#### 3. Create Teaching Notebooks

**Naming convention:**
```
notebooks/day{N}_block_{a|b}_NN_{topic}.ipynb
```

**Examples:**
- `day2_block_a_01_joins_basics.ipynb`
- `day2_block_a_02_join_patterns.ipynb`
- `day2_block_b_01_json_ingestion.ipynb`

**Structure each teaching notebook with:**
1. **Title cell** (Markdown):
   ```markdown
   # Day {N}, Block {A|B}: {Topic Title}

   **Learning Objectives:**
   - Objective 1
   - Objective 2
   ```

2. **Setup cell** (Code):
   ```python
   import pandas as pd
   import numpy as np
   import duckdb

   # Use relative paths from repo root
   DATA_DIR = "data/day{N}"
   ```

3. **Teaching sections** with:
   - Clear markdown explanations (why, not just how)
   - Worked examples with real data
   - Common pitfalls demonstrated
   - Best practices called out

4. **Check your understanding** mini-exercises:
   - 2-3 small problems per major concept
   - Solutions provided inline (it's a teaching notebook)

**Quality checklist:**
- ✅ All cells run in order (Restart & Run All)
- ✅ Relative paths only
- ✅ Clear explanations in markdown cells
- ✅ Code comments for complex operations
- ✅ Real data, real problems
- ✅ Links to reference materials where appropriate

#### 4. Create In-Class Exercise

**Naming convention:**
```
notebooks/day{N}_exercise_{topic}.ipynb
```

**Examples:**
- `day2_exercise_joins.ipynb`
- `day2_exercise_json_pipeline.ipynb`

**Structure:**
1. **Clear deliverable** stated upfront
2. **Starter code** with TODOs:
   ```python
   # TODO: Load the customers table
   # TODO: Join with orders table
   # TODO: Calculate total revenue per customer
   ```
3. **Validation cells** students should complete:
   ```python
   # Validate: Check that customer_id is unique
   assert customers['customer_id'].is_unique, "Duplicate customer IDs!"
   ```
4. **Markdown prompts** guiding students:
   ```markdown
   ## Task 1: Load and Explore

   Load the `customers.csv` file and explore:
   - How many customers?
   - Any missing values?
   - What's the primary key?
   ```

**In-class deliverable requirements:**
- Completable in 30-45 minutes (not full homework)
- Uses concepts taught earlier in the same block
- Has clear success criteria
- Includes validation assertions

#### 5. Create Exercise Solution

**Naming convention:**
```
notebooks/day{N}_exercise_{topic}_solution.ipynb
```

**Structure:**
- Same as exercise but with TODOs completed
- Add **explanation markdown cells** after each solution:
  ```markdown
  **Why this approach?** We use an INNER JOIN here because we only want customers who have placed orders. A LEFT JOIN would include customers with zero orders, which we don't need for this analysis.
  ```
- Show alternative approaches where appropriate
- Include all assertions passing

**CRITICAL: Encrypt before committing!**
```bash
python scripts/encrypt_solutions.py \
  notebooks/day{N}_exercise_{topic}_solution.ipynb \
  --password "secure-password" \
  --day {N} \
  --block {A|B}
```

#### 6. Create Teacher Primer

**Location:** `references/teaching/day{N}_block_{a|b}_teacher_primer.md`

**Purpose:** Guidance for the instructor (or future you)

**Structure:**
```markdown
# Day {N}, Block {A|B}: {Topic}
## Teacher Primer

**Duration:** 90 minutes  
**Audience:** {Context about student level}

## Learning Objectives
[Bullet list of what students will be able to do]

## Session Flow (90 minutes)
### 1. Hook: {Motivating Problem} (10 min)
### 2. Core Concept 1 (20 min)
### 3. Core Concept 2 (20 min)
### 4. Demo/Live Coding (15 min)
### 5. Exercise Setup (10 min)
### 6. Work Time + Circulation (15 min)

## Materials Required
- Teaching notebooks
- Dataset
- Exercise starter
- Solution (encrypted)

## Pedagogical Notes
[Tips for teaching, common confusions, good examples]

## Connection to Later Material
[How this builds toward future days]
```

**Example:** See `references/teaching/day1_block_a_teacher_primer.md`

#### 7. Create Optional Block Intro Slides

**Location:** `slides/day{N}_block_{a|b}_intro.md`

**Purpose:** Quick 3-minute context setter at start of block

**Structure:**
```markdown
---
marp: true
theme: ceu
paginate: true
header: 'Day {N}, Block {A|B}: {Topic}'
footer: 'ECBS5294 | CEU'
---

<!-- _class: lead -->

# Block {A|B}
## {Topic Title}

**90 minutes**

---

# What We'll Cover

1. {Topic 1}
2. {Topic 2}
3. {Hands-on component}

---

# Learning Objectives

By the end of this block, you'll be able to:

✅ {Objective 1}
✅ {Objective 2}
✅ {Objective 3}

---

# Key Dataset

**{Dataset Name}**
- {Key fact about dataset}
- {Why it's interesting}

---

# Materials for Today

**Teaching notebooks:**
- `day{N}_block_{a|b}_01_....ipynb`

**Exercise:**
- `day{N}_exercise_{topic}.ipynb`

**Quick reference:**
- `references/{topic}_quick_reference.md`

---

<!-- _class: lead -->

# Let's Begin

Open the teaching notebook:
`day{N}_block_{a|b}_01_....ipynb`

{Transition statement}
```

**Important:**
- Keep it SHORT (5-6 slides max)
- No deep content, just roadmap
- Consistent format with other days

#### 8. Create Quick Reference Materials

**Location:** `references/{topic}_quick_reference.md`

**Purpose:** Student cheat sheet for the topic

**Structure:**
```markdown
# {Topic} Quick Reference Card

**ECBS5294 - Introduction to Data Science: Working with Data**

---

## Core Concepts

[2-3 key ideas, clearly stated]

---

## Common Patterns

| Pattern | Example | When to Use |
|---------|---------|-------------|
| ... | ... | ... |

---

## Code Snippets

```python
# Pattern 1: {Name}
{common code pattern}
```

---

## Decision Framework

Ask yourself:
1. {Question 1}
2. {Question 2}

---

## Common Mistakes

❌ **Don't do this:** {anti-pattern}
✅ **Do this instead:** {correct pattern}

---

**More resources:**
- Teaching notebook: `notebooks/...`
- Cheat sheet: `references/...`
```

**Examples:** See `references/tidy_data_checklist.md`, `references/sql_quick_reference.md`

#### 9. Create Homework Assignment

**Location:** `assignments/hw{N}/`

**Required files:**
```
assignments/hw{N}/
├── README.md          # Full assignment description
├── hw{N}_starter.ipynb (optional - if providing starter code)
└── data/              (optional - if assignment-specific data)
```

**README.md structure:**
```markdown
# Homework {N}: {Title}

**Course:** ECBS5294  
**Due:** Day {N+1}, Start of Class  
**Total Points:** 100 (+ bonus)
**Est. Time:** {X} hours

---

## 📋 Overview
[What this assignment tests]

---

## 🎯 Learning Objectives
[Skills demonstrated]

---

## 📊 Dataset
[Description, size, source, quirks]

---

## 📝 Assignment Structure

### Part 1: {Topic} (X points)
[Requirements]

### Part 2: {Topic} (X points)
[Requirements]

### Bonus (X points)
[Extra credit]

---

## 📤 Submission Requirements

**What to Submit:**
1. Completed notebook: `hw{N}_[your_name].ipynb`

**Format Requirements:**
- File must run: **Restart & Run All**
- All outputs visible
- Markdown explanations where requested

**How to Submit:**
- Upload to Moodle
- Due: {Day} at start of class

**Before Submitting - Checklist:**
- [ ] All TODO sections completed
- [ ] Notebook runs end-to-end without errors
- [ ] All query results visible
- [ ] Markdown explanations included
- [ ] File renamed to `hw{N}_[your_name].ipynb`

---

## 🎯 Grading Rubric

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Correctness | 40% | {What correct looks like} |
| Data Thinking | 25% | {What good thinking looks like} |
| Code Quality | 20% | {What clean code looks like} |
| Communication | 15% | {What clear docs look like} |

---

## 💡 Tips for Success
[Practical advice]

---

## 🚫 Academic Integrity
[Reminder of AI policy and what's allowed/not allowed]

---

## ❓ Getting Help
[Office hours, Moodle, email]
```

**Example:** See `assignments/hw1/README.md`

**Create solution:**
```
assignments/hw{N}/hw{N}_solution.ipynb
```
**CRITICAL: Encrypt before committing!**

#### 10. Update Main Course Materials

**Update `README.md`:**
- If Day 2/3 materials change the repo structure, update the directory tree
- Generally, Day 1 README should be comprehensive enough not to need updates

**Update `syllabus.md`:**
- Should already have Day 2/3 outlined
- Double-check learning objectives match what you built
- Verify due dates and deliverables

**Update `slides/` (if adding kickoff for Day 2/3):**
- Usually Day 1 kickoff is sufficient
- Consider adding a "Day 2 Kickoff" slide (5 slides max) if:
  - Returning after a week break
  - Major context switch in content
  - Need to review Day 1 concepts

#### 11. Build and Test Everything

**Before committing:**

```bash
# 1. Test all teaching notebooks
uv run jupyter nbconvert --execute --to notebook \
  notebooks/day{N}_*.ipynb

# 2. Test exercise starter (should run with TODOs)
uv run jupyter nbconvert --execute --to notebook \
  notebooks/day{N}_exercise_*.ipynb

# 3. Test solution (should run completely)
uv run jupyter nbconvert --execute --to notebook \
  notebooks/day{N}_*_solution.ipynb

# 4. Build slides
./scripts/build_slides.sh

# 5. Check solution status
python scripts/list_solutions.py

# 6. Verify no unencrypted solutions
git status | grep solution
# (Should only show encrypted ZIPs!)
```

**Quality checklist:**
- ✅ All notebooks run end-to-end
- ✅ All relative paths work from repo root
- ✅ All datasets are in `data/` and referenced correctly
- ✅ All solutions encrypted
- ✅ Slides build without errors
- ✅ README files have no broken links
- ✅ Consistent terminology throughout
- ✅ No year-specific dates (except syllabus.md)

#### 12. Commit and Push

**Commit strategy:** Separate commits for different components

```bash
# Commit teaching materials
git add notebooks/day{N}_block_*
git add references/teaching/day{N}_*
git commit -m "Add Day {N} teaching materials: {topics}"

# Commit exercise and encrypted solution
git add notebooks/day{N}_exercise_*.ipynb
git add solutions/solutions-day{N}-*.zip
git commit -m "Add Day {N} exercise and encrypted solutions"

# Commit homework assignment
git add assignments/hw{N}/
git commit -m "Add Homework {N}: {title}"

# Commit datasets
git add data/day{N}/
git commit -m "Add Day {N} datasets: {description}"

# Commit slides (if any)
git add slides/day{N}_*
./scripts/build_slides.sh
git commit -m "Add Day {N} slide decks"

# Push everything
git push origin main
```

---

## File Naming Conventions Reference

### Notebooks
```
day{N}_block_{a|b}_NN_{topic}.ipynb       # Teaching notebook
day{N}_exercise_{topic}.ipynb             # In-class exercise
day{N}_exercise_{topic}_solution.ipynb    # Exercise solution (ENCRYPT!)
day{N}_setup_check.ipynb                  # Environment check
```

### Data
```
data/day{N}/                              # All Day N datasets
data/day{N}/README.md                     # Data documentation
data/day{N}/{dataset_name}.csv            # Actual data files
```

### Slides
```
slides/day{N}_kickoff.md                  # Day kickoff (optional)
slides/day{N}_block_{a|b}_intro.md        # Block intro (optional)
```

### References
```
references/{topic}_quick_reference.md     # Student cheat sheet
references/teaching/day{N}_block_{a|b}_teacher_primer.md  # Instructor guide
references/datasets/{source}_info.md      # Dataset provenance notes
references/papers/{paper}_summary.md      # Academic paper summaries
```

### Assignments
```
assignments/hw{N}/README.md               # Full assignment description
assignments/hw{N}/hw{N}_starter.ipynb     # Starter code (optional)
assignments/hw{N}/hw{N}_solution.ipynb    # Solution (ENCRYPT!)
```

### Solutions (Encrypted)
```
solutions/solutions-day{N}-block{A|B}.zip  # Exercise solutions
solutions/solutions-hw{N}.zip              # Homework solutions
```

---

## Content Development Best Practices

### Evergreen Content Principles

**Goal:** Materials should be reusable year after year with minimal edits.

**DO:**
- ✅ Use relative dates: "Day 1", "Day 2", "start of next class"
- ✅ Reference `syllabus.md` for specific dates
- ✅ Use generic language: "this year", "current term"
- ✅ Link to external docs by concept, not by URL (URLs change)
- ✅ Use "check Moodle" not "check Moodle at https://..."

**DON'T:**
- ❌ Hardcode year-specific dates: "October 8, 2025"
- ❌ Reference current events that will be outdated
- ❌ Use semester-specific examples: "like we discussed in Fall 2024"
- ❌ Link to time-sensitive URLs: "see this week's announcement"

**Exception:** `syllabus.md` is the ONLY file that gets year-specific dates. Update it each term.

### Business Focus

**This is an MSBA course.** Every concept should connect to business value.

**Frame technical concepts with business impact:**
- ❌ "A LEFT JOIN returns all rows from the left table"
- ✅ "A LEFT JOIN ensures you see ALL customers, even those who haven't ordered yet—critical for customer retention analysis"

**Use business-relevant datasets:**
- Retail transactions, customer behavior, sales data
- Operational metrics, supply chain, logistics
- Marketing campaigns, A/B tests, user engagement
- Avoid academic datasets (iris, mtcars) unless making a specific pedagogical point

**Include stakeholder communication:**
- Data dictionaries (define metrics for non-technical audiences)
- Assumption documentation (what decisions did you make and why?)
- Limitation notes (what CAN'T this analysis answer?)
- Executive summaries (8-10 sentences for a VP)

### Real-World Messiness

**Don't sanitize the data too much.** Students need to encounter real problems.

**Include common issues:**
- Mixed date formats in same column
- Currency symbols and comma separators in numbers
- Multiple representations of missing: NULL, "N/A", "", "UNKNOWN", -999
- Duplicate primary keys (data quality issue to catch!)
- Inconsistent capitalization/spelling
- Sentinel values: "ERROR", "REDACTED", "TBD"

**But don't make it impossible:**
- Issues should be discoverable (show up in .info() or .describe())
- Issues should be fixable with concepts taught
- Document the issues in data README so instructor knows what's intentional

### Validation as Code

**Teach students to PROVE their data is correct.**

**Every notebook should include assertions:**
```python
# Primary key uniqueness
assert df['customer_id'].is_unique, "Duplicate customer IDs found!"

# Required fields
assert df['order_date'].notna().all(), "NULL order dates found!"

# Data integrity
assert (df['total'] == df['quantity'] * df['price']).all(), "Total != quantity * price!"

# Date ranges
assert df['order_date'].min() >= pd.Timestamp('2020-01-01'), "Orders before 2020!"
```

**Frame as "trust but verify":**
- Not paranoia, just good engineering
- Catches upstream data quality issues early
- Proves to stakeholders that data is clean

### Reproducibility Standards

**EVERY notebook must run from a clean state.**

**Test procedure:**
```python
# 1. Restart kernel
# 2. Run All Cells
# 3. No errors
```

**Common reproducibility issues to avoid:**
- Absolute paths: `/Users/instructor/data/file.csv` ❌
- Relative paths: `data/day1/file.csv` ✅
- Hidden state: Variables defined out of order
- External dependencies: API keys, network resources (unless cached)
- Platform-specific code: Windows-only, Mac-only paths

**Include environment check:**
```python
# At top of notebooks
import sys
print(f"Python: {sys.version}")
print(f"Pandas: {pd.__version__}")
print(f"DuckDB: {duckdb.__version__}")

# Check data file exists
import os
assert os.path.exists("data/day1/file.csv"), "Data file not found! Check your working directory."
```

### Notebook Display Best Practices

**CRITICAL: DataFrames must render as beautiful HTML tables, not ugly plain text.**

Jupyter notebooks can display DataFrames in two ways:
- ✅ **HTML tables** - Styled, readable, professional (the default if done correctly)
- ❌ **Plain text** - Ugly, hard to read, unprofessional (what happens when you print())

**The Rule:** NEVER use `print()` on DataFrames. Let Jupyter render them natively.

---

#### Single DataFrame Display

**For one DataFrame in a cell:**

```python
# ✅ CORRECT - Renders as beautiful HTML table
print("Query results:")
con.execute("SELECT * FROM table LIMIT 10").df()

# or
print("Results:")
df.head()
```

**What happens:** The last expression in the cell is automatically rendered as HTML by Jupyter.

```python
# ❌ WRONG - Renders as ugly plain text
print("Query results:")
result = con.execute("SELECT * FROM table LIMIT 10").df()
print(result)  # ← DON'T DO THIS!
```

---

#### Multiple DataFrames Display

**For multiple DataFrames in one cell, use `display()`:**

```python
# ✅ CORRECT - All three render as HTML tables
from IPython.display import display

print("Table 1:")
display(con.execute("SELECT * FROM table1").df())

print("Table 2:")
display(con.execute("SELECT * FROM table2").df())

print("Table 3:")
display(con.execute("SELECT * FROM table3").df())
```

**Why `display()` is needed:** Jupyter only auto-renders the LAST expression in a cell. If you have multiple DataFrames, only the last would show as HTML without `display()`.

```python
# ❌ WRONG - Only the last DataFrame shows as HTML
print("Table 1:")
con.execute("SELECT * FROM table1").df()  # ← Ignored!

print("Table 2:")
con.execute("SELECT * FROM table2").df()  # ← Ignored!

print("Table 3:")
con.execute("SELECT * FROM table3").df()  # ← Only this renders
```

---

#### Text Output vs DataFrame Output

**Be clear about what should be text vs what should be a table:**

```python
# ✅ Text labels and messages - use print()
print("✅ Created 'products' table: 30 rows")
print(f"Average price: ${avg_price:.2f}")
print("Processing complete!")

# ✅ DataFrames - NO print()
print("Products by category:")
con.execute("SELECT category, COUNT(*) FROM products GROUP BY category").df()

# ✅ Validation info - use print()
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"Unique products: {df['product_id'].nunique()}")
```

---

#### Common Patterns Reference

**Pattern 1: DuckDB query result**
```python
print("Top 10 customers:")
con.execute("""
    SELECT customer_id, SUM(revenue) as total_revenue
    FROM orders
    GROUP BY customer_id
    ORDER BY total_revenue DESC
    LIMIT 10
""").df()
```

**Pattern 2: Pandas DataFrame manipulation**
```python
print("After cleaning:")
df.head()
```

**Pattern 3: Multiple summary tables**
```python
from IPython.display import display

print("Summary statistics:")
display(df.describe())

print("Missing value counts:")
display(df.isnull().sum())

print("Data types:")
display(df.dtypes.to_frame('dtype'))
```

**Pattern 4: Mixed text and tables**
```python
print("Data loaded successfully!")
print(f"Total rows: {len(df):,}")
print(f"Total columns: {len(df.columns)}")
print("\nFirst 5 rows:")
df.head()
```

---

#### Anti-Patterns to Avoid

```python
# ❌ NEVER DO THIS
result = df.head()
print(result)  # Ugly plain text output

# ❌ NEVER DO THIS
query_result = con.execute("SELECT * FROM table").df()
print(query_result)  # Ugly plain text output

# ❌ NEVER DO THIS (without display)
print("Table 1:")
df1.head()  # Won't show if another DataFrame follows

print("Table 2:")
df2.head()  # Only this one renders

# ✅ DO THIS INSTEAD
from IPython.display import display

print("Table 1:")
display(df1.head())

print("Table 2:")
display(df2.head())
```

---

#### Testing Display Quality

After creating/editing a notebook, verify displays are correct:

1. **Execute the notebook:**
   ```bash
   uv run jupyter nbconvert --execute --to notebook --inplace notebook.ipynb
   ```

2. **Check output types:**
   ```python
   import json
   with open('notebook.ipynb') as f:
       nb = json.load(f)

   for cell in nb['cells']:
       if cell['cell_type'] == 'code' and 'outputs' in cell:
           for output in cell['outputs']:
               if output['output_type'] == 'execute_result':
                   if 'text/html' in output['data']:
                       print("✅ HTML table")
                   else:
                       print("❌ Not HTML - check this cell")
   ```

3. **Visual inspection:** Open notebook in VS Code and verify tables are styled and readable.

---

#### Summary: Display Best Practices

- ✅ **Single DataFrame:** Direct expression (no print)
- ✅ **Multiple DataFrames:** Use `display()` for each
- ✅ **Text labels:** Use `print()`
- ✅ **Import at top:** Add `from IPython.display import display` if needed
- ❌ **NEVER:** Use `print(dataframe)`
- ❌ **NEVER:** Store in variable then print

**Golden Rule:** If it's tabular data, let Jupyter render it as HTML. If it's text, use `print()`.

---

## Slide Development Guidelines

### Marp Best Practices

**Keep slides MINIMAL:**
- 10-15 slides for 10-minute kickoff
- 5-6 slides for 3-minute block intro
- One idea per slide
- Use bullet points sparingly (3-5 max)

**Font sizes (already configured in theme):**
- Base text: 24px
- H1: 48px
- H2: 36px
- H3: 28px
- Don't override unless absolutely necessary

**Test on projector:**
- Text should be readable from back of room
- Code blocks should be large enough (0.75em in theme)
- Don't put critical info in footer (hard to read)

**Use speaker notes:**
```markdown
---
# Slide Title

Content here

<!--
Speaker notes: Remember to mention the business impact!
Transition: "Now let's see this in action with real data..."
-->
```

### Slide Structure Patterns

**Title slide (lead class):**
```markdown
<!-- _class: lead -->
<!-- _paginate: false -->

# {Course Title}
## {Subtitle}

**{Course Code}**

{Institution}
```

**Content slide (standard):**
```markdown
# {Section Title}

**{Key point}** – {Elaboration}

{Supporting details as bullets if needed}

{Transition statement at bottom}
```

**Code slide:**
```markdown
# {Concept}

```{language}
{code example}
```

{Brief explanation of what the code does}
```

**Callout slide:**
```markdown
# {Important Concept}

> **"{Memorable quote or principle}"**

{Context or elaboration}

**{Why it matters}**
```

### Rebuild Process

**After any slide edits:**
```bash
./scripts/build_slides.sh
open slides/output/day{N}_*.html
```

**Check for:**
- Text cutoff at bottom (add `<!-- fit -->` if needed)
- Code readability (reduce font if too large)
- Emoji rendering (emojis are OK, but test display)
- Link formatting (should be blue and clickable)

---

## Platform-Specific Details

### Moodle (Not Canvas!)

**Terminology:**
- ✅ "Check Moodle for announcements"
- ✅ "Upload to Moodle"
- ✅ "Posted on Moodle"
- ❌ "Check Canvas" (wrong LMS!)

**Moodle URL pattern:**
```
https://ceulearning.ceu.edu/mod/forum/post.php?forum=XXXXX
```

**When referencing Moodle:**
- Generic: "Check Moodle for password release dates"
- Don't hardcode forum IDs (they change per course instance)

### GitHub Repository

**Primary URL:**
```
https://github.com/earino/ECBS5294
```

**Clone command:**
```bash
git clone https://github.com/earino/ECBS5294.git
```

**Reference in materials:**
- Always provide both URL and clone command
- Remind students: "This repo has everything you need"
- Point to specific files: `notebooks/day1_*.ipynb`

### CEU Branding

**Slide theme colors:**
- Primary: `#1a4d7a` (CEU dark blue)
- Accent: `#3498db` (bright blue)
- Emphasis: `#c0392b` (red for strong text)

**Official name:**
- "Central European University" (full)
- "CEU" (abbreviated)
- Not "CEU Vienna" or "CEU Budapest" (institution is one entity)

**Instructor contact:**
- Email: RubiaE@ceu.edu
- Office: Room A104
- Office hours: By appointment

---

## Quality Assurance Checklist

**Before ANY commit, verify:**

### Notebooks
- [ ] All notebooks run with "Restart & Run All"
- [ ] Notebook outputs cleared (pre-commit hook does this automatically)
- [ ] Relative paths only (no `/Users/...`)
- [ ] Clear markdown explanations between code cells
- [ ] Assertions included for data quality checks
- [ ] No API keys or passwords in code
- [ ] Data files referenced exist in `data/` directory

### Solutions
- [ ] Solutions are encrypted (`.zip` files only in git)
- [ ] Passwords documented in `solutions/PASSWORDS.md` (gitignored)
- [ ] `python scripts/list_solutions.py` shows all solutions encrypted
- [ ] Pre-commit hook is active and passes
- [ ] Decryption tested: `uv run python scripts/decrypt_solutions_zip.py solutions/solutions-*.zip`

### Slides
- [ ] Slides build without errors: `./scripts/build_slides.sh`
- [ ] No text cutoff at bottom of slides
- [ ] Code blocks are readable
- [ ] Consistent theme across all slide decks
- [ ] Speaker notes included where helpful
- [ ] Marp front matter correct (theme, paginate, header, footer)

### Documentation
- [ ] README files have no broken links
- [ ] Dataset documentation includes source and license
- [ ] Quick reference materials are concise (1-2 pages)
- [ ] Teacher primers include timing and pedagogical notes
- [ ] No year-specific dates except in `syllabus.md`

### Content Quality
- [ ] Business framing included (not just technical)
- [ ] Real-world datasets with intentional messiness
- [ ] Validation assertions demonstrate data quality checks
- [ ] Stakeholder communication examples included
- [ ] Consistent terminology throughout materials

### Platform References
- [ ] "Moodle" not "Canvas"
- [ ] GitHub URL: `https://github.com/earino/ECBS5294`
- [ ] Instructor email: `RubiaE@ceu.edu`
- [ ] No hardcoded forum IDs or time-sensitive links

### Git Hygiene
- [ ] Logical commit messages (what and why)
- [ ] Small, focused commits (not giant "add everything" commits)
- [ ] Committed files only (no `git add .` without checking)
- [ ] `.gitignore` prevents accidental commits of solutions/data
- [ ] Pre-commit hook active: `./scripts/setup_hooks.sh`

---

## Common Pitfalls to Avoid

### Don't:
- ❌ Commit unencrypted solutions (pre-commit hook will block, but don't test it!)
- ❌ Use absolute paths (`/Users/instructor/...`)
- ❌ Reference "Canvas" (we use Moodle)
- ❌ Put year-specific dates in teaching materials
- ❌ Create "perfect" datasets (students need messiness)
- ❌ Write notebooks that only work on your machine
- ❌ Skip validation assertions (students need to see the pattern)
- ❌ Forget business framing (this isn't a CS course)
- ❌ Make slides text-heavy (keep it minimal)
- ❌ Forget to rebuild slides after edits

### Do:
- ✅ Test "Restart & Run All" on every notebook
- ✅ Use relative paths from repo root
- ✅ Encrypt solutions before committing
- ✅ Include business context and stakeholder communication
- ✅ Add data quality checks with assertions
- ✅ Document your assumptions
- ✅ Keep materials evergreen (reusable next year)
- ✅ Frame concepts with real-world examples
- ✅ Test slides on a projector (or full-screen preview)
- ✅ Commit early and often with clear messages

---

## Need Help?

**For AI assistants working on this repo:**
If you're unsure about a pattern or convention:
1. Look at Day 1 materials as the reference implementation
2. Check this CLAUDE.md file for guidance
3. Maintain consistency with existing materials
4. When in doubt, ask the human for clarification

**For humans working on this repo:**
- Primary contact: Eduardo Ariño de la Rubia (RubiaE@ceu.edu)
- All patterns established during Day 1 development
- This CLAUDE.md file is the source of truth for conventions
- Update this file if you establish new patterns!
- we properly attribute datasets we use in our program, and make sure to always hae appropriate rights to use them.