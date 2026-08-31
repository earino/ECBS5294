# Solution Management - Instructor Guide

This guide documents the workflow for managing encrypted solution files in the course repository.

## Overview

The solution management system uses:
- **Password-protected ZIPs** for distributing solutions
- **Git pre-commit hooks** to prevent accidental commits of unencrypted files
- **Automated scripts** for encryption, decryption, and status checking
- **Consistent naming conventions** for easy organization

## Directory Structure

```
solutions/
├── README.md                    # Student-facing documentation
├── INSTRUCTOR.md               # This file
├── PASSWORDS.md                # Password tracking (gitignored)
├── .encryption_log.txt         # Auto-generated encryption history (gitignored)
├── solutions-day1-blockA.zip   # Encrypted solution files
├── solutions-day2-blockB.zip
└── decrypted/                  # Decrypted files (gitignored)
```

## Workflow

### 1. Create Solution Materials

Develop solution notebooks following the naming convention:

- `day1_exercise_tidy_solution.ipynb` (your local, uncommitted copy)
- `hw1_solution.ipynb` (your local, uncommitted copy)
- `sql/day3_query_solution.sql`

**Important**: Keep solution files OUTSIDE the repository or ensure they're gitignored until encrypted.

### 2. Encrypt Solutions

Use the encryption script to create password-protected ZIPs:

```bash
uv run python scripts/encrypt_solutions.py \
  notebooks/day1_exercise_tidy_solution.ipynb \
  --password "your-secure-password" \
  --day 1 \
  --block A
```

This will:
- Create `solutions/solutions-day1-blockA.zip`
- Verify the ZIP is password-protected
- Log the encryption event to `.encryption_log.txt`
- Provide next steps for git commit

**Alternative**: Specify custom output path:

```bash
uv run python scripts/encrypt_solutions.py \
  notebooks/hw1_solution.ipynb \
  --password "homework-password" \
  --output solutions/solutions-hw1.zip
```

### 3. Document the Password

Add the password to `solutions/PASSWORDS.md`:

```markdown
## Day 1 Block A
- **File**: `solutions-day1-blockA.zip`
- **Password**: `your-secure-password`
- **Release Date**: 2025-10-15
- **Contents**: Tidy data exercise solution
```

**Note**: `PASSWORDS.md` is gitignored and should NOT be committed.

### 4. Commit Encrypted Solutions

The git pre-commit hook will verify you're only committing encrypted files:

```bash
git add solutions/solutions-day1-blockA.zip
git commit -m "Add encrypted solutions for Day 1 Block A"
git push
```

The hook will:
- ✅ Allow encrypted ZIP files in `solutions/`
- ✅ Verify ZIPs are password-protected
- ❌ Block any `*_solution.ipynb` or `*_solution.py` files
- ❌ Block any unencrypted solution files

### 5. Release Passwords

After the assignment due date:
1. Announce password in Moodle
2. Update course schedule documentation
3. Optionally, create a password release file (not in repo)

## Management Scripts

### Check Solution Status

See what solutions exist and their encryption status:

```bash
uv run python scripts/list_solutions.py
```

Output shows:
- 📦 Encrypted solutions (safe to commit)
- ⚠️ Unencrypted solutions (DO NOT COMMIT)
- 📝 Encryption log history

### Decrypt for Testing

Test that encrypted files work correctly:

```bash
uv run python scripts/decrypt_solutions_zip.py solutions/solutions-day1-blockA.zip
```

Files will be extracted to `solutions/decrypted/` (gitignored).

### Setup Git Hooks

If working on a fresh clone, install git hooks:

```bash
./scripts/setup_hooks.sh
```

This makes the pre-commit hook executable and verifies it's working.

## File Naming Conventions

### Solution Source Files

Before encryption, use these patterns:

- `{assignment}_solution.ipynb` - Jupyter notebooks
- `{assignment}_solution.py` - Python scripts
- `{topic}_solution.sql` - SQL queries

Examples:
- `day1_exercise_tidy_solution.ipynb`
- `hw1_solution.ipynb`
- `data_cleaning_solution.py`

### Encrypted Archives

After encryption, use this pattern:

```
solutions-{descriptor}.zip
```

Examples:
- `solutions-day1-blockA.zip` - Day/block format
- `solutions-hw1.zip` - Homework format
- `solutions-midterm.zip` - Exam format

## Security Best Practices

### DO:
- ✅ Encrypt ALL solution files before committing
- ✅ Use strong, unique passwords for each archive
- ✅ Test decryption before pushing
- ✅ Keep `PASSWORDS.md` secure and gitignored
- ✅ Run `list_solutions.py` before committing
- ✅ Verify git hooks are active with `./scripts/setup_hooks.sh`

### DON'T:
- ❌ Commit unencrypted solution files
- ❌ Commit `PASSWORDS.md` to the repository
- ❌ Use weak or guessable passwords
- ❌ Share passwords before due dates
- ❌ Skip testing that ZIPs are password-protected
- ❌ Disable git hooks without good reason

## Troubleshooting

### Git Hook Blocks My Commit

**Symptom**: Pre-commit hook says "COMMIT BLOCKED! Unencrypted solution files cannot be committed"

**Solution**:
1. Run `uv run python scripts/list_solutions.py` to see which files are unencrypted
2. Encrypt the solution: `uv run python scripts/encrypt_solutions.py <file> --password <pwd> --day X --block Y`
3. Unstage the unencrypted file: `git reset HEAD <file>`
4. Stage the encrypted ZIP: `git add solutions/solutions-dayX-blockY.zip`
5. Commit again

### ZIP is Not Password Protected

**Symptom**: Pre-commit hook says "ZIP is NOT password-protected"

**Solution**:
1. Delete the weak ZIP file
2. Re-encrypt with the script: `uv run python scripts/encrypt_solutions.py <source> --password <pwd> --output <zip>`
3. The script uses `zip -P` which creates proper password protection

### Can't Decrypt ZIP

**Symptom**: `decrypt_solutions_zip.py` fails with "Bad password"

**Solution**:
1. Verify password in `PASSWORDS.md`
2. Check for typos (passwords are case-sensitive)
3. Ensure ZIP was created with the encryption script

### Lost Password

**Prevention**: Always document passwords in `PASSWORDS.md` immediately after encryption

**Recovery**:
- If ZIP was created recently, check `.encryption_log.txt` for filename/timestamp
- Check Moodle announcements if already released
- In worst case, re-create solution and re-encrypt

## Collaboration with TAs

If TAs are creating solutions:

1. **Share this guide** - Ensure they understand the workflow
2. **Coordinate passwords** - Use a shared secure method (not email/Slack)
3. **Review encrypted files** - Test decryption before students receive them
4. **Document ownership** - Note in PASSWORDS.md who created each solution

## Maintenance

### Beginning of Semester

1. Run `./scripts/setup_hooks.sh` to install git hooks
2. Create `solutions/PASSWORDS.md` from template
3. Test the encryption workflow with a dummy file
4. Verify `.gitignore` has solution patterns

### During Semester

1. Run `uv run python scripts/list_solutions.py` weekly
2. Verify no unencrypted solutions in repo
3. Keep `PASSWORDS.md` updated
4. Back up `PASSWORDS.md` securely (outside repo)

### End of Semester

1. Archive `PASSWORDS.md` securely for next year
2. Review `.encryption_log.txt` for complete history
3. Document any workflow improvements for next term

## Questions or Issues?

- Check git hook logs: `.git/hooks/pre-commit`
- Review encryption log: `solutions/.encryption_log.txt`
- Test scripts individually: `uv run python scripts/<script>.py --help`
- Consult CLAUDE.md for Claude Code assistance

---

**Last Updated**: 2025-10-07
