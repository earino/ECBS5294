# FOOLPROOF Solution Encryption Workflow

**NEVER LOSE PASSWORDS AGAIN**

## 🚨 What Went Wrong Before

The old `encrypt_solutions.py` script had a CRITICAL FLAW:
- It **told you** to add passwords to PASSWORDS.md manually
- It **didn't verify** passwords actually worked
- Result: **Passwords were lost forever** because manual steps were forgotten

## ✅ The New Foolproof System

### Use `encrypt_solutions_v2.py` - ALWAYS

This script is **FOOLPROOF** because it:
1. ✅ **AUTO-DOCUMENTS** passwords immediately (not later, not manually)
2. ✅ **VERIFIES** passwords work before finishing
3. ✅ **TRIPLE-BACKS-UP** passwords to 3 different locations
4. ✅ **FAILS SAFELY** - if anything goes wrong, it cleans up and tells you

### The Triple Backup System

Every password is automatically saved to:
1. **`solutions/PASSWORDS.md`** - Human-readable reference (gitignored)
2. **`solutions/.password_backup.json`** - Machine-readable backup (gitignored)
3. **`solutions/.encryption_log.txt`** - Full history with timestamps (gitignored)

## 📝 How to Use (The Right Way)

### For Day/Block Exercises:

```bash
uv run python scripts/encrypt_solutions_v2.py \
  solutions/decrypted/day1_exercise_tidy_solution.ipynb \
  --password "TidyData2024CEU!" \
  --day 1 \
  --block A \
  --description "Day 1 in-class exercise: Tidy data principles and foundations"
```

### For Homework:

```bash
uv run python scripts/encrypt_solutions_v2.py \
  assignments/hw2/hw2_solution.ipynb \
  --password "TechMart2024QuickBuy!" \
  --output solutions/solutions-hw2-complete.zip \
  --description "Homework 2: TechMart acquisition data integration with stakeholder communications"
```

## 🎯 Password Requirements

Choose passwords that are:
- **Memorable:** Use course-related themes (TidyData2024!, SQL2024DuckDB!)
- **Strong:** Mix of letters, numbers, symbols
- **Unique:** Different for each solution
- **Documented:** This happens automatically now!

## 📋 What Happens When You Run It

```
🔒 Encrypting: your_solution.ipynb
📦 Output: solutions/solutions-hw2.zip
🔑 Password: TechMart2024QuickBuy!
📝 Description: HW2 solution

🔐 Verifying password works...
✅ Password verified - decryption works!

📝 Auto-documenting password...
✅ Password documented in solutions/PASSWORDS.md
✅ Password backed up to solutions/.password_backup.json
✅ Encryption logged to solutions/.encryption_log.txt

✅ SUCCESS! EVERYTHING DOCUMENTED AUTOMATICALLY!
```

## ⚠️ DO NOT Use Old Script

**NEVER use `encrypt_solutions.py` anymore!**

It's still there for backward compatibility, but:
- ❌ Requires manual password documentation (easy to forget)
- ❌ Doesn't verify passwords work
- ❌ No automatic backup

**Always use `encrypt_solutions_v2.py`**

## 🔍 How to Verify Passwords

At any time, check that all passwords are documented and working:

```bash
# Check PASSWORDS.md
cat solutions/PASSWORDS.md

# Check machine-readable backup
cat solutions/.password_backup.json

# Test all passwords work
python -c "
import zipfile, json
with open('solutions/.password_backup.json') as f:
    passwords = json.load(f)
for zip_file, info in passwords.items():
    with zipfile.ZipFile(f'solutions/{zip_file}', 'r') as zf:
        zf.read(zf.namelist()[0], pwd=info['password'].encode())
    print(f'✅ {zip_file} - {info[\"password\"]}')"
```

## 🔐 Password Recovery Plan

Even with triple backup, here's the recovery plan:

### If PASSWORDS.md is Accidentally Deleted:

1. **Check `.password_backup.json`:**
   ```bash
   cat solutions/.password_backup.json
   ```
   This has all passwords in machine-readable format.

2. **Check `.encryption_log.txt`:**
   ```bash
   cat solutions/.encryption_log.txt
   ```
   Since Oct 12, 2024, this includes passwords in the log.

3. **Regenerate PASSWORDS.md from backup:**
   ```bash
   python3 -c "
   import json
   with open('solutions/.password_backup.json') as f:
       data = json.load(f)
   for zip_file, info in data.items():
       print(f\"File: {zip_file}\")
       print(f\"Password: {info['password']}\")
       print(f\"Description: {info['description']}\")
       print()
   "
   ```

### If ALL Password Files Are Lost:

**This should be IMPOSSIBLE now, but if it happens:**

1. The decrypted versions exist in `solutions/decrypted/` (gitignored)
2. Re-encrypt them with new passwords using the v2 script
3. Update students with new passwords via Moodle

## 📝 Workflow Checklist

**Before encrypting:**
- [ ] Solution file is complete and tested
- [ ] File is in a safe location (gitignored or `solutions/decrypted/`)

**When encrypting:**
- [ ] Use `encrypt_solutions_v2.py` (NOT the old script)
- [ ] Provide meaningful description
- [ ] Wait for "SUCCESS! EVERYTHING DOCUMENTED AUTOMATICALLY!"

**After encrypting:**
- [ ] Verify password is in PASSWORDS.md
- [ ] Verify password is in .password_backup.json
- [ ] Verify the encrypted ZIP is in `solutions/`
- [ ] Git add ONLY the encrypted ZIP
- [ ] Git commit and push

**Before releasing to students:**
- [ ] Test decryption works
- [ ] Post password on Moodle after deadline
- [ ] DO NOT email or Slack passwords

## 🎓 Current Solution Passwords

As of Oct 12, 2024, all solution passwords are documented:

| File | Password | Description |
|------|----------|-------------|
| `solutions-day1-blockA.zip` | `TidyData2024CEU!` | Day 1 exercise |
| `solutions-hw1.zip` | `SQL2024DuckDB!` | Homework 1 |
| `solutions-day2-blockA.zip` | `SQLJoins2024CEU!` | Day 2 exercise |
| `solutions-hw2.zip` | `techmart2024merge` | HW2 (OLD - deprecated) |
| `solutions-hw2-complete.zip` | `TechMart2024QuickBuy!` | HW2 (NEW - use this) |

All verified working on Oct 12, 2024.

## 🛡️ Prevention Checklist

To ensure passwords are NEVER lost again:

1. **✅ ALWAYS use `encrypt_solutions_v2.py`** (auto-documents passwords)
2. **✅ NEVER commit PASSWORDS.md** (it's gitignored for security)
3. **✅ BACKUP `.password_backup.json`** regularly to secure location outside repo
4. **✅ VERIFY** passwords work before considering encryption complete
5. **✅ CHECK** PASSWORDS.md file exists and has the password immediately after encrypting

## 📞 If Something Goes Wrong

1. **Don't panic** - decrypted files likely exist in `solutions/decrypted/`
2. **Check all three backup locations** (PASSWORDS.md, .password_backup.json, .encryption_log.txt)
3. **Re-encrypt if needed** using `encrypt_solutions_v2.py`
4. **Test the password** immediately after encryption

## 🔄 Migration from Old System

If you have old encrypted files with unknown passwords:

1. **If you have the decrypted version:**
   - Re-encrypt with `encrypt_solutions_v2.py`
   - Use a new, documented password
   - Delete the old file with unknown password

2. **If you don't have the decrypted version:**
   - Try common password patterns
   - Check old documentation/emails
   - Last resort: Re-create the solution

---

**Remember: With `encrypt_solutions_v2.py`, passwords are AUTOMATICALLY documented in 3 places. You can't forget because it's not a manual step anymore!**

**Last Updated:** Oct 12, 2024
**Status:** All 5 solution files have verified passwords ✅
