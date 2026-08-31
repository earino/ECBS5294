# Verify Notebooks - Pedantic Cell-by-Cell Quality Check

You are tasked with performing **exhaustive cell-by-cell verification** of Jupyter notebooks to ensure teaching quality.

## 🚨 NON-NEGOTIABLE REQUIREMENT: EXECUTE FIRST

**YOU MUST EXECUTE EVERY NOTEBOOK BEFORE ANALYZING IT.**

This is not optional. This is not "if time permits." This is MANDATORY.

### Why This Matters

- **Students will run these notebooks** - if they don't work, teaching fails
- **Reading code ≠ running code** - syntax errors, path issues, empty results only appear at runtime
- **Outputs must be real** - not theoretical, not "should return", ACTUAL data from execution
- **Empty results are CRITICAL** - you cannot detect them without execution

### Execution-First Protocol

**BEFORE ANY ANALYSIS, you must:**

```bash
# 1. Execute the notebook
uv run jupyter nbconvert --execute --to notebook --inplace \
  path/to/notebook.ipynb \
  --ExecutePreprocessor.timeout=300

# 2. Check outputs for issues (utility script available!)
uv run python scripts/check_notebook_outputs.py path/to/notebook.ipynb

# If execution fails or outputs have issues, document and fix
# Do NOT proceed to verification until execution succeeds
```

**💡 TIP: Use `scripts/check_notebook_outputs.py` to quickly check for:**
- Empty DataFrames (0 rows)
- Cells without outputs
- Execution errors
- Summary statistics

**EXECUTION VERIFICATION CHECKLIST:**
- [ ] Did you run `uv run jupyter nbconvert --execute`?
- [ ] Did execution complete without errors?
- [ ] Are all cells now populated with outputs?
- [ ] Did you CHECK the outputs for empty results?
- [ ] Did you LOOK at the actual data returned?

**If you answered NO to ANY of these, STOP and execute first.**

---

## Your Mission

For each notebook specified (or ALL teaching notebooks if none specified):

1. **🚨 EXECUTE THE NOTEBOOK FIRST** - Use `uv run jupyter nbconvert --execute` (MANDATORY)
2. **Verify execution succeeded** - Check exit code, no errors
3. **Inspect ACTUAL outputs** - Look at what the execution produced
4. **Launch parallel verification agents** - one agent per notebook (AFTER execution)
5. **Each agent must verify EVERY code cell** using ACTUAL execution results
6. **Report findings** in a structured format
7. **Identify ALL issues** (no matter how minor)
8. **Fix issues found** (if requested)
9. **Re-execute notebooks** to verify fixes work

---

## What to Verify (Per Cell)

For EVERY code cell, check:

### 1. Markdown-Code Alignment
- Does the markdown immediately before the cell accurately describe what the code does?
- Are there promises made that the code doesn't fulfill?
- Are there discrepancies in numbers (e.g., markdown says "5 rows" but LIMIT 10)?

### 2. Output Accuracy (REQUIRES EXECUTION ✓)
- Does the output **AFTER YOU EXECUTED THE NOTEBOOK** match what markdown promised?
- Are there **empty results** (0 rows, empty DataFrames) that would confuse students?
- Do calculated values make sense given the data?
- **WARNING:** Do NOT say "output should show X" - report what output ACTUALLY shows after execution

### 3. Business Logic Correctness
- Do filter conditions (WHERE clauses) match data constraints?
- Do business questions align with query implementation?
- Are aggregations calculating what they claim to calculate?

### 4. NULL Handling
- Are NULL checks present where needed?
- Do queries handle missing data appropriately?
- Are IS NULL vs = NULL used correctly?

### 5. Pedagogical Soundness
- Do examples teach what they claim to teach?
- Are comparisons (e.g., WHERE vs HAVING) effective?
- Would students understand the output?

### 6. Terminology Consistency
- Is terminology consistent throughout the notebook?
- Do labels match what's being calculated?
- Are business terms used correctly?

---

## Notebooks to Verify

**IMPORTANT:** Use the Glob tool to auto-discover notebooks matching these patterns:

### Teaching Notebooks (highest priority)
**Pattern:** `notebooks/day*_block_*.ipynb`
- Matches: `day1_block_a_*.ipynb`, `day2_block_b_*.ipynb`, `day3_block_a_*.ipynb`, etc.
- Excludes: exercise notebooks, solution notebooks

### Exercise Notebooks (verify but don't fix student sections)
**Pattern:** `notebooks/day*_exercise_*.ipynb`
- Matches: `day1_exercise_tidy.ipynb`, `day2_exercise_joins.ipynb`, etc.
- Excludes: solution files (those end in `_solution.ipynb`)

### Assignment Notebooks (if they exist)
**Pattern:** `assignments/hw*/hw*_starter.ipynb`
- Matches: `assignments/hw1/hw1_starter.ipynb`, `assignments/hw2/hw2_starter.ipynb`, etc.
- Excludes: solution files

**Verification Strategy:**
1. First, use Glob with pattern `notebooks/day*_block_*.ipynb` to find all teaching notebooks
2. Then, use Glob with pattern `notebooks/day*_exercise_*.ipynb` to find exercise notebooks
3. Finally, use Glob with pattern `assignments/hw*/hw*_starter.ipynb` to find assignments
4. Launch parallel verification agents for ALL discovered notebooks

---

## Output Format

For each notebook, produce a report:

```markdown
## Cell-by-Cell Verification Report: [notebook_name]

### Cell [N]: [Brief description]
**Markdown says:** [What the markdown promises]  
**Code does:** [What the code actually does]  
**Output shows:** [What appears in the output]  
**Status:** ✅ MATCH / ⚠️ MISMATCH / ❌ ERROR
**Issue (if any):** [Describe discrepancy]

[Repeat for EVERY code cell]

---

## Summary

**Total cells checked:** [N]  
**Cells with perfect match:** [N]  
**Cells with issues:** [N]

### Issues Found:
1. **[Severity] Cell [N]**: [Brief description]
2. **[Severity] Cell [N]**: [Brief description]

**Severity levels:**
- 🟥 CRITICAL: Empty results, wrong calculations, broken examples
- 🟨 MODERATE: Misleading labels, conceptual mismatches
- 🟦 MINOR: Terminology inconsistencies, wording issues
```

---

## Execution Workflow

0. **🚨 EXECUTE ALL NOTEBOOKS FIRST (MANDATORY)**

   For EACH discovered notebook:
   ```bash
   uv run jupyter nbconvert --execute --to notebook --inplace \
     path/to/notebook.ipynb \
     --ExecutePreprocessor.timeout=300
   ```

   - If execution fails, document which cells errored
   - Note: Exercise notebooks with TODO cells may fail - that's expected
   - For exercise notebooks, verify only setup cells execute
   - **DO NOT PROCEED to agent launch until teaching notebooks execute successfully**

1. **Identify notebooks to verify**
   - If user specified paths, use those
   - Otherwise, use Glob tool to auto-discover:
     - `notebooks/day*_block_*.ipynb` (teaching notebooks)
     - `notebooks/day*_exercise_*.ipynb` (exercise notebooks)
     - `assignments/hw*/hw*_starter.ipynb` (assignment notebooks)
   - This ensures NEW notebooks are automatically included (Day 2, Day 3, etc.)

2. **Launch parallel agents** (one per notebook) **AFTER EXECUTION**
   ```
   Use Task tool with subagent_type='general-purpose'
   One task per notebook for maximum speed
   Tell agents notebooks are ALREADY EXECUTED
   ```

3. **Wait for all reports** to complete

4. **Synthesize findings**
   - Total cells verified across all notebooks
   - Total issues found
   - Breakdown by severity
   - Breakdown by issue type (empty results, mismatches, terminology, etc.)
   - **Report execution results** - which notebooks ran successfully

5. **Ask user** if they want issues fixed
   - If YES: Fix all issues using NotebookEdit
   - Re-execute notebooks with uv run jupyter nbconvert
   - Verify fixes work
   - Show before/after for each fix

6. **Offer to commit** changes if fixes were made
   - Generate comprehensive commit message
   - Include issue counts and verification stats
   - Include execution confirmation
   - Push to GitHub if approved

---

## Example Usage

### Verify All Notebooks
```
/verify-notebooks
```

### Verify Specific Notebook
```
/verify-notebooks notebooks/day1_block_b_02_aggregations.ipynb
```

### Verify and Auto-Fix
```
/verify-notebooks --fix
```

---

## Critical Reminders

### Data Constraints
ALWAYS check actual data constraints before validating queries:
```python
con.execute("SELECT MAX(price) FROM data").df()  # Don't assume max price!
con.execute("SELECT DISTINCT item FROM data").df()  # Check what items exist!
```

### Empty Results = Red Flag
If ANY teaching example returns empty results (0 rows), this is **CRITICAL**:
- Students will think they made a mistake
- Teaching point is lost
- Must be fixed immediately

### Markdown Must Match Code EXACTLY
- If markdown says "first 5 rows", code must use LIMIT 5
- If markdown says "Coffee sales", code must filter Item = 'Coffee'
- If markdown says "revenue", code must calculate price × quantity
- Be pedantic - exact matches only!

---

## Success Criteria

You've succeeded when:

✅ **EXECUTED every notebook with `uv run jupyter nbconvert --execute`** (MOST IMPORTANT)
✅ **VERIFIED all notebooks run without errors** (checked exit codes)
✅ **INSPECTED actual outputs from execution** (not theoretical - REAL data)
✅ Every code cell in every notebook has been verified against ACTUAL outputs
✅ Markdown descriptions match code behavior exactly
✅ All outputs are meaningful (no confusing empty results)
✅ All issues documented with severity levels
✅ Fixes applied (if requested) and verified working
✅ Teaching quality is production-ready

---

**⚠️ IF YOU DID NOT EXECUTE NOTEBOOKS, YOU FAILED THE VERIFICATION. ⚠️**

Reading code is not verification. Thinking about what code might do is not verification.
**EXECUTION IS VERIFICATION.**

---

**Remember:** This is about **teaching quality**. Students trust that examples work. Every empty result or mismatch erodes that trust. Be thorough, be pedantic, be rigorous.

**And EXECUTE FIRST.**
