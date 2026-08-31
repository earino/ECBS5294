# Encrypted Solutions

This directory contains password-protected ZIP files with solution notebooks and code.

## Why Encrypted?

To support your learning, solutions are available from day one, but password-protected until after the assignment due date. This approach:

- ✅ Ensures you can access solutions immediately after deadlines
- ✅ Removes anxiety about "losing" the solutions
- ✅ Encourages you to attempt problems before looking at answers
- ✅ Allows you to verify your work once released

## File Naming Convention

Encrypted solution files follow this pattern:

```
solutions-day{N}-block{X}.zip
```

Examples:
- `solutions-day1-blockA.zip` - Day 1, Block A solutions
- `solutions-day2-blockB.zip` - Day 2, Block B solutions
- `solutions-hw1.zip` - Homework 1 solutions

## How to Use

### 1. Check the Password Release Schedule

Passwords are released after the assignment due date. Check Moodle or the course schedule for release dates.

### 2. View Available Passwords

Once released, passwords will be announced in Moodle and documented in the course materials.

### 3. Decrypt a Solution File

**Option A: Using the Decryption Script (Recommended)**

```bash
uv run python scripts/decrypt_solution.py solutions/solutions-day1-blockA.zip
```

This will prompt you for the password and extract files to `solutions/decrypted/`.

**Option B: Manual Extraction**

Right-click the ZIP file and select "Extract" or use command line:

```bash
unzip solutions/solutions-day1-blockA.zip -d solutions/decrypted/
```

Enter the password when prompted.

### 4. Open the Solution Notebook

After extraction, open the solution notebook in VS Code:

```bash
code solutions/decrypted/day1_exercise_tidy_solution.ipynb
```

## Learning Tips

### Before Looking at Solutions

1. **Attempt the problem yourself** - Even partial attempts build understanding
2. **Document where you got stuck** - Note specific error messages or concepts
3. **Try debugging first** - Use print statements, check types, verify data
4. **Ask for hints** - Office hours and discussion forums are there to help

### When Using Solutions

1. **Don't just copy** - Type out the solution yourself to build muscle memory
2. **Understand each line** - Add comments explaining what each step does
3. **Try variations** - Change parameters, try different approaches
4. **Compare your approach** - Identify what you did well and what to improve

### After Reviewing Solutions

1. **Restart and run all** - Verify you understand the complete flow
2. **Modify the solution** - Try a different analysis or visualization
3. **Apply to new data** - Can you use these techniques on a different dataset?
4. **Explain to someone** - Teaching others solidifies your understanding

## Support

If you have trouble accessing solutions:
- Check that you're using the correct password
- Ensure you have the decryption script: `scripts/decrypt_solution.py`
- Verify Python and required packages are installed
- Contact the instructor or TA if issues persist

## Academic Integrity

**Remember**: Solutions are learning tools, not shortcuts. Using solutions from previous assignments to complete current work without understanding violates academic integrity policies.

- ✅ **Allowed**: Reviewing solutions after deadlines to learn
- ✅ **Allowed**: Using solution patterns in your own work with understanding
- ❌ **Not Allowed**: Copying solutions without understanding
- ❌ **Not Allowed**: Sharing passwords before release dates
- ❌ **Not Allowed**: Using solutions from previous terms for graded work

---

**Questions?** Contact the instructor or TA through Moodle.
