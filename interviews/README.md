# SQL Whiteboard Interview Simulations

**ECBS5294: Data Science 2: Working with Data**

---

## Overview

This directory contains materials for conducting realistic SQL whiteboard interview simulations with students. These simulations mirror the technical screening process used by companies like Meta, Amazon, Google, and other major tech companies for Data Analyst, Analytics Engineer, and Data Scientist roles.

**Purpose:** Give students authentic interview practice in a low-stakes environment before they face real technical screens.

---

## 🔒 Instructor Materials Are Encrypted

**Interviewer guides, sample data, and test scripts are stored in an encrypted ZIP file to prevent students from seeing questions ahead of time.**

### For Instructors: How to Decrypt

The encrypted file is: **`../solutions/interview-materials.zip`**

**To decrypt:**
```bash
# From the repository root
unzip -P "<password>" solutions/interview-materials.zip

# This extracts to interviews/ directory:
#   - scenario_*/interviewer_guide.md (detailed scripts)
#   - scenario_*/data/*.csv (sample data to load)
#   - test_scenarios.py (data validation script)
```

**Password location:**
- Emailed to instructor (search inbox for "ECBS5294 Interview")
- Or contact course creator (RubiaE@ceu.edu)

**After decryption:**
- Interview guides will be in `scenario_*/interviewer_guide.md`
- Sample data will be in `scenario_*/data/*.csv`
- Load data following instructions in each interviewer guide

---

## Contents

### For Students

- **[STUDENT_ANNOUNCEMENT.md](STUDENT_ANNOUNCEMENT.md)** - Announcement to share with class (email, Moodle, Slack)
- **[student_prep_guide.md](student_prep_guide.md)** - How to prepare, what to expect, key concepts to review

### For Instructor

- **[google_sheet_template.md](google_sheet_template.md)** - Instructions for setting up booking system
- **`../solutions/interview-materials.zip`** - 🔒 Encrypted interviewer guides, sample data, and test scripts (see decryption instructions above)

---

## Quick Start Guide for Instructors

### 1. Decrypt and Review Materials (20 minutes)

- **Decrypt interviewer materials:** `unzip -P "<password>" ../solutions/interview-materials.zip`
  - Password is in your email (subject: "ECBS5294 Interview")
- Read one interviewer guide (start with Scenario 1) to understand the format
- Browse the sample data CSVs to see what students will work with
- Review the student prep guide to understand what students are told

### 2. Set Up Booking System (30 minutes)

- Follow instructions in `google_sheet_template.md`
- Create Google Sheet with available timeslots
- Configure sharing permissions (anyone with link can edit)

### 3. Announce to Students (5 minutes)

- Customize `STUDENT_ANNOUNCEMENT.md` with your dates/times/location
- Add Google Sheet link
- Post to Moodle/email/Slack
- Also share `student_prep_guide.md`

### 4. Before First Interview (15 minutes)

- Load sample data for your first scenario (instructions in interviewer guide)
- Print or open the interviewer guide on your laptop
- Prepare whiteboard (clear it, get markers)
- Review scoring rubric

### 5. Conduct Interviews

- Follow the interviewer guide step-by-step
- Focus on learning, not perfection
- Give constructive feedback

---

## The Three Scenarios

### Scenario 1: E-Commerce Analytics (Easiest)
- **Domain:** Online marketplace (similar to course materials)
- **Tables:** customers, orders, order_items, products
- **Focus:** Basic JOINs, aggregation, LEFT JOIN anti-pattern
- **Recommend for:** Students who want familiar territory

### Scenario 2: SaaS Product Analytics (Medium)
- **Domain:** B2B SaaS subscription business
- **Tables:** users, subscriptions, feature_usage, support_tickets
- **Focus:** Date arithmetic, subscription logic, window functions
- **Recommend for:** Students who want to stretch

### Scenario 3: Retail Store Operations (Medium)
- **Domain:** Multi-location retail chain
- **Tables:** stores, employees, transactions, inventory
- **Focus:** Multi-table JOINs, HAVING vs WHERE, inventory gap analysis
- **Recommend for:** Students interested in operations/retail

**All three test the same core concepts from Day 1-2.** Choice is about domain interest, not difficulty (though Scenario 1 is most similar to class).

---

## Interview Structure (25 minutes)

Each interview follows the same pattern:

| Time | Activity | What You're Testing |
|------|----------|---------------------|
| 0-2 min | Welcome, scenario setup | Setting expectations |
| 2-7 min | Question 1 (Warm-up) | Basic SELECT, WHERE, filtering |
| 7-13 min | Question 2 (Core skills) | JOINs + aggregation |
| 13-19 min | Question 3 (Advanced) | Complex JOINs, anti-patterns, date logic |
| 19-24 min | Question 4 (Data thinking) | NULL awareness, business logic, discussion |
| 24-25 min | Wrap-up, feedback | Encouragement, 1-2 areas to improve |

**Timing is tight!** Use a timer or clock. Don't let Question 1 drag—nudge students if needed.

---

## Scoring Rubric (All Scenarios)

### Technical Correctness (40 points)
- Q1: 8-10 pts (basic query)
- Q2: 10-12 pts (JOIN + aggregation)
- Q3: 10-12 pts (complex JOIN or date logic)
- Q4: 8 pts (data thinking discussion)

### SQL Best Practices (20 points)
- Readability: 8 pts
- Efficiency awareness: 6 pts
- NULL handling: 6 pts

### Communication & Process (25 points)
- Thinking out loud: 10 pts
- Asking clarifying questions: 8 pts
- Handling feedback: 7 pts

### Data & Business Thinking (15 points)
- Business context understanding: 8 pts
- Edge case awareness: 7 pts

**Total: 100 points**

**Bands:**
- 85-100: Exceptional (ready for FAANG)
- 70-84: Strong (solid interview skills)
- 55-69: Competent (needs more practice)
- <55: Needs review (revisit fundamentals)

---

## Tips for Interviewers

### Before the Interview

1. **Load the data** (takes 2 minutes):
```python
import duckdb
con = duckdb.connect(':memory:')
con.execute("CREATE TABLE customers AS SELECT * FROM 'scenario_X/data/customers.csv'")
# ... (see interviewer guide for full setup)
```

2. **Have the guide open** on your laptop for reference
3. **Clear the whiteboard** and have markers ready
4. **Set a timer** for 25 minutes

### During the Interview

**DO:**
- ✅ Be encouraging and supportive
- ✅ Give hints if they're stuck (but not too many!)
- ✅ Ask probing questions to dig deeper
- ✅ Focus on their thinking process, not just correct answers
- ✅ Take brief notes (for feedback)

**DON'T:**
- ❌ Give away answers
- ❌ Let students feel like they're failing
- ❌ Skip questions (even if running late, try to touch on all 4)
- ❌ Be overly critical
- ❌ Compare students to each other

### Giving Feedback

**Structure** (2 minutes):
1. **Positive:** "Your [X] was really strong, especially..."
2. **Improve:** "One area to practice: [Y]. Specifically, [Z]."
3. **Encouragement:** "You're [ready / on the right track / building good skills]. Keep practicing!"

**Examples:**

*Strong student:*
> "Great work! Your understanding of JOINs was solid, and I loved how you asked about NULL values before writing the query. One thing to keep refining: when you're grouping, double-check that every SELECT column is either in GROUP BY or an aggregate. Overall, you're interview-ready!"

*Struggling student:*
> "You've got the fundamentals down, which is awesome. I'd recommend practicing JOINs a bit more, especially understanding when to use INNER vs LEFT. Your data thinking in Question 4 showed good business sense. Keep practicing these patterns and you'll be ready!"

**Always end positively!** Even if they struggled, they came to practice—that's huge.

---

## Common Student Mistakes (What to Watch For)

### The Big Three (Instant Red Flags)
1. **= NULL instead of IS NULL** ← #1 killer!
2. **Aggregates in WHERE instead of HAVING**
3. **Wrong JOIN type** (INNER when they need LEFT)

### Other Common Mistakes
- Forgetting GROUP BY columns
- Missing COUNT(DISTINCT) after JOINs
- Silent (not talking through approach)
- Rushing (not asking clarifying questions)

**When you see these:** Probe with questions, don't just correct. Example:
- "How do you check for NULL values in SQL?"
- "What's the difference between WHERE and HAVING?"
- "What happens when you use INNER JOIN here?"

---

## Logistics

### Room Setup
- **Whiteboard** (essential!)
- **Markers** (2-3, test them first)
- **Your laptop** with data loaded
- **Interviewer guide** open
- **Timer** or visible clock
- **Quiet space** (minimize interruptions)

### Scheduling
- **25 min per interview**
- **5 min buffer** between interviews (bathroom, reset whiteboard, mental break)
- **Reasonable daily limit:** 4-6 interviews (you'll be mentally exhausted after more!)
- **Best times:** Mornings (students are fresh)

### If Student is Late
- Wait 5 minutes
- If no-show, mark as canceled and take a break
- Email student afterward to check in

### If Student is Early
- Great! But don't start early (respect your schedule)
- They can review notes in the hallway/waiting area

---

## Frequently Asked Questions

### Q: What if a student can't answer any questions?

**A:** This is practice! Use it as a teaching moment:
- Walk them through Question 1 step-by-step
- Point them to specific resources (Day 1 notebooks, SQL reference)
- Encourage them to come to office hours before trying again
- Frame it positively: "Now you know what to work on!"

### Q: What if a student finishes all 4 questions in 15 minutes?

**A:** Great! You have bonus questions:
- "How would you optimize this query?"
- "What would happen if [edge case]?"
- "Rewrite this query using a CTE"
- "What indexes would help this query run faster?" (if they know indexes)

Or just give them detailed feedback and let them go early.

### Q: Can students do multiple scenarios?

**A:** Only if:
- Everyone who wants one slot has gotten one
- You have capacity
- They want extra practice (not trying to "game" the system)

First priority: Everyone gets one opportunity.

### Q: What if I need to cancel a day of interviews?

**A:**
- Update the Google Sheet immediately
- Email affected students ASAP
- Offer alternative dates
- Apologize (stuff happens!)

### Q: Should I share the interviewer guides with students?

**A:** No! That defeats the purpose. They should prepare using:
- Course materials (Day 1-2 notebooks)
- Student prep guide
- Practice problems

The questions should be somewhat surprising (but fair).

---

## Advanced: Customizing Scenarios

If you want to create your own scenarios or modify existing ones:

### Keep These Elements
1. **4 questions** with clear progression (easy → hard)
2. **Business context** (not just abstract SQL)
3. **Real data** with intentional messiness (NULLs, edge cases)
4. **Data thinking question** (#4 should be discussion-based)

### Modify These Based on Your Course
- Table schemas (match your teaching datasets)
- Specific SQL features (if you taught CTEs, include them)
- Business domain (use what's relevant to your students)

### Don't Change
- **25-minute format** (industry standard)
- **Whiteboard requirement** (key skill to practice)
- **4-question structure** (proven progression)
- **Scoring dimensions** (technical, best practices, communication, thinking)

---

## Troubleshooting

### Problem: Running over time

**Solution:**
- Set a timer and stick to it
- If Student 1 struggles, don't skip Question 4—just ask it faster
- Practice saying, "We're running low on time, let me give you a hint..."

### Problem: Student is too nervous to think

**Solution:**
- Pause, smile, reassure: "This is practice. Take a breath."
- Ask easier warm-up: "What tables do we have? What columns?"
- Give explicit hint to get them started

### Problem: Student is overconfident and makes mistakes

**Solution:**
- Let them finish their query
- Ask: "Walk me through what this query returns."
- Probe gently: "What if customer_id is NULL?"
- They'll often self-correct when explaining

### Problem: You're exhausted after 4 interviews

**Solution:**
- This is normal! It's mentally taxing.
- Take real breaks between interviews (walk, coffee, snack)
- Don't schedule more than 6 per day
- Spread interviews across multiple days if possible

---

## Data Files

Each scenario includes sample CSV files in `/data/`:

**Characteristics:**
- Small (~20-100 rows total across all tables)
- Realistic IDs (hashes, not sequential numbers)
- Intentional NULLs (~10% where appropriate)
- Edge cases (stores with no transactions, etc.)
- Representative of real business data

**You can modify these!** Just:
- Keep the same column names (or update the interviewer guide)
- Maintain the key relationships (PKs/FKs)
- Include intentional edge cases for students to discover

---

## Acknowledgments

These simulations are modeled on real technical interview processes at:
- Meta (Facebook)
- Amazon
- Google
- Other major tech companies

The format, question progression, and evaluation criteria reflect actual industry practices for screening data analysts and data scientists.

**Sources consulted:**
- DataLemur SQL Interview Guide
- StrataScratch FAANG Interview Prep
- SQLPad.io Interview Patterns
- Direct experience from FAANG interviewers

---

## Feedback & Improvement

If you use these materials, please track:
- What worked well
- What didn't work
- Questions students struggled with most
- Questions that were too easy/hard
- Timing issues
- Student feedback

This will help refine the scenarios for future semesters!

---

## Contact

Questions about these materials?
**Eduardo Ariño de la Rubia** - RubiaE@ceu.edu

---

**Good luck with the interview simulations!** 🎯

Remember: The goal is learning, not perfection. Every student who shows up to practice is already ahead of the game.
