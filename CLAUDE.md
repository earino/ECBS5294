# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

**Course:** ECBS5294: Data Science 2: Working with Data at CEU
**Focus:** Practical data literacy - tidy data, SQL with DuckDB, JSON/API ingestion, reproducible pipelines
**Context:** MSBA course - frame everything with business value

## 🚨 CRITICAL: Testing Requirements

**MANDATORY:** Every teaching notebook must work perfectly.

### Core Rules
1. **Execute entire notebook:** `uv run jupyter nbconvert --to notebook --execute notebooks/your_notebook.ipynb --inplace`
2. **Every query must return data** (unless teaching about empty results)
3. **Verify constraints before writing queries:**
   ```python
   # Check data reality first
   con.execute("SELECT MAX(price) FROM data").df()
   con.execute("SELECT DISTINCT item FROM data").df()
   ```
4. **Test with actual data, not assumptions**
5. **Clear outputs before committing** (pre-commit hook handles this)

**Why:** Students think THEY made a mistake when examples return empty results.

## Project Structure

```
/data          # Teaching datasets (offline, with README)
/notebooks     # Jupyter notebooks for teaching and exercises
/solutions     # Encrypted solution ZIPs only
/scripts       # Utility scripts for course management
/references    # Teaching resources and quick references
/assignments   # Homework descriptions and starters
/slides        # Marp slide decks (optional)
```

## Solution File Security

**CRITICAL:** Never commit unencrypted solutions to git.

### Workflow
1. **Encrypt before committing:**
   ```bash
   uv run python scripts/encrypt_solutions.py notebooks/solution.ipynb \
     --password "secure-password" --day 1 --block A
   ```
2. **Verify encryption:** `uv run python scripts/list_solutions.py`
3. **Commit only ZIPs:** `solutions/solutions-*.zip`
4. **Document passwords:** in `solutions/PASSWORDS.md` (gitignored)

### Git Protection
- Pre-commit hook blocks `*_solution.ipynb` files
- Install: `./scripts/setup_hooks.sh`
- Students get encrypted ZIPs, passwords released after deadlines

## Core Technologies

- **Python 3.13** managed by **uv** (`uv sync`), notebooks in **VS Code**
- **DuckDB** for SQL (embedded database)
- **Git** for version control
- **Marp** for slides (optional)

## Key Concepts

### Data Pipeline Pattern
- **Bronze:** Raw ingestion (preserve original)
- **Silver:** Cleaned, typed, validated
- **Gold:** Analysis-ready with joins/aggregations

### Tidy Data
- Each variable is a column
- Each observation is a row
- Explicit primary keys
- Correct types (dates, floats, booleans)
- Document missing value handling

### SQL Focus
- Single-table: SELECT, WHERE, GROUP BY, ORDER BY
- Joins: INNER, LEFT, RIGHT (watch for inflation)
- Window functions: ROW_NUMBER(), LAG(), moving averages
- NULL handling in conditions and aggregations

## Development Requirements

### Reproducibility
- **Relative paths only** (`data/file.csv` not `/Users/...`)
- **Restart & Run All** must work on any machine
- **No external dependencies** without caching
- **Include assertions** to verify data quality:
  ```python
  assert df['id'].is_unique, "Duplicate IDs!"
  assert df['date'].notna().all(), "NULL dates!"
  ```

### Business Focus
- Frame technical concepts with business impact
- Use business datasets (retail, customers, operations)
- Include stakeholder communication (data dictionaries, assumptions)
- Document what the analysis CAN'T answer

### Real-World Messiness
Include intentional data issues:
- Mixed date formats
- Currency symbols in numbers
- Multiple NULL representations ("N/A", "", -999)
- Inconsistent capitalization
- But keep it fixable with concepts taught

## Notebook Display Rules

**Critical:** DataFrames must render as HTML tables, not plain text.

### Single DataFrame
```python
# ✅ CORRECT - HTML table
print("Results:")
df.head()  # or con.execute("...").df()

# ❌ WRONG - Plain text
print(df.head())
```

### Multiple DataFrames
```python
# ✅ CORRECT - All render as HTML
from IPython.display import display

print("Table 1:")
display(df1.head())
print("Table 2:")
display(df2.head())

# ❌ WRONG - Only last renders
print("Table 1:")
df1.head()  # Ignored!
print("Table 2:")
df2.head()  # Only this shows
```

**Golden Rule:** Never `print(dataframe)`. Use `display()` for multiple.

## File Naming Conventions

### Notebooks
```
day{N}_block_{a|b}_NN_{topic}.ipynb       # Teaching
day{N}_exercise_{topic}.ipynb             # In-class exercise
day{N}_exercise_{topic}_solution.ipynb    # Solution (ENCRYPT!)
```

### Data
```
data/day{N}/README.md                     # Documentation with attribution
data/day{N}/{dataset}.csv                 # Actual data files
```

### Solutions
```
solutions/solutions-day{N}-block{A|B}.zip # Encrypted exercises
solutions/solutions-hw{N}.zip             # Encrypted homework
```

### References
```
references/{topic}_quick_reference.md     # Student cheat sheets
(instructor guides live in the private ECBS5294-instructor repo)
```

## Academic Context

- **AI Policy:** AI tools NOT permitted for graded work
- **Grading:** Correctness (40%), Data thinking (25%), Reproducibility (20%), Communication (15%)
- **LMS:** Moodle (not Canvas)
- **Repository:** https://github.com/earino/ECBS5294

## Critical Checklist

Before ANY commit:
- [ ] All notebooks pass "Restart & Run All"
- [ ] All queries return meaningful data
- [ ] Solutions encrypted (only ZIPs in git)
- [ ] Relative paths only
- [ ] DataFrames display as HTML (not print())
- [ ] Business context included
- [ ] Assertions verify data quality
- [ ] No year-specific dates (except syllabus.md)
- [ ] Pre-commit hook installed and passing
- [ ] Datasets have proper attribution/licenses

## Quick DuckDB Reference

```python
import duckdb
con = duckdb.connect('database.db')

# Query CSV/Parquet directly
con.execute("SELECT * FROM 'data/file.csv'").df()
con.execute("SELECT * FROM 'data/file.parquet'").df()

# Create tables
con.execute("CREATE TABLE orders AS SELECT * FROM 'data/orders.csv'")

# Always verify results render
print("Results:")
con.execute("SELECT * FROM orders LIMIT 5").df()
```

## Common Pitfalls

### DON'T
- Commit unencrypted solutions
- Use absolute paths
- Print DataFrames
- Write queries without checking data
- Create perfect/clean datasets
- Skip validation assertions
- Forget business framing
- Hardcode dates or URLs

### DO
- Test everything with Restart & Run All
- Use relative paths
- Display DataFrames properly
- Verify data constraints first
- Include realistic messiness
- Add assertions everywhere
- Frame with business value
- Keep materials evergreen

## Additional Resources

For detailed workflows, extended examples, and verbose explanations, see:
- **CLAUDE-EXTENDED.md** - Full original documentation (1700+ lines)
- **Day 1 materials** - Reference implementation patterns
- **scripts/** - Automation tools for solutions, notebooks, slides

---

**Contact:** Eduardo Ariño de la Rubia (RubiaE@ceu.edu)
**Note:** This is the simplified guide. See CLAUDE-EXTENDED.md for comprehensive documentation.