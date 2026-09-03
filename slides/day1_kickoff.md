---
marp: true
theme: ceu
paginate: true
header: 'ECBS5294: Working with Data'
footer: 'Central European University'
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Data Science 2
## Working with Data

**ECBS5294**

Central European University

---

<!-- _class: lead -->

# Welcome! 👋

**Eduardo Ariño de la Rubia**

📧 RubiaE@ceu.edu
🏢 Room A104
🕒 Office hours by appointment

---

# What This Course Is About

This is **not** a theory course.

This is **not** about machine learning or advanced statistics.

---

# What This Course **Is** About

This is about the **day-one skills** every analyst and data scientist needs:

- Working with **messy, real-world data**
- Writing **SQL** to answer business questions
- Building **reproducible pipelines**
- **Validating** your work
- **Communicating** findings clearly

---

# The Reality of Data Work

> **80% of data science is cleaning and preparing data**

The other 20% is:
- Analysis
- Modeling
- Visualization
- Communication

**This course teaches you the 80%.**

---

# Course Structure

**Three full-day sessions** (2 blocks each)

📅 Check syllabus.md for specific dates

**Day 1:** Tidy data + SQL foundations
**Day 2:** SQL joins + JSON ingestion
**Day 3:** Pipelines + in-class exam

---

# What You'll Build

By the end of three weeks, you'll have:

✅ Cleaned a messy 10,000-row CSV dataset
✅ Written SQL queries on 500,000+ rows
✅ Built a JSON-to-database pipeline
✅ Created an end-to-end analysis with validation

**These are portfolio pieces.**

---

# Grading Breakdown

| Component | Weight |
|-----------|--------|
| Homework 1 (SQL basics) | 15% |
| Homework 2 (JSON pipeline) | 15% |
| Homework 3 (End-to-end) | 15% |
| In-class deliverables | 5% |
| In-class exam (Day 3) | 50% |

**Target median:** B+ (roughly ⅓ at A/A-)

---

# Late Policy & Expectations

**Late work:** -10% per 24 hours (48-hour max)

**Reproducibility requirement:**
- All submissions must **"Restart & Run All"** successfully (VS Code: **Restart**, then **Run All**)
- Use relative paths only
- If it doesn't run, you'll lose points

**This is not negotiable.** Real work must be reproducible.

---

# Academic Integrity ⚠️

To align with Coding 1 and Data Science 1:

❌ **AI tools NOT permitted** for graded work
   - No ChatGPT, Claude, Copilot for homework/exam
   - Use for personal study only

❌ No copying from classmates
❌ No sharing solutions

✅ Ask instructor/TA for help
✅ Review course materials
✅ Discuss concepts (not code)

**Why?** We need to assess YOUR understanding to help where you're stuck.

---

# Solutions: Available, But Locked 🔐

**Good news:** All solutions are in the repo from day one

**Smart design:** Password-protected until after deadlines

**Why?**
- No anxiety about "losing" them
- Available immediately after due dates
- Encourages trying before looking
- You can verify your work

**Check Moodle** for password release dates:
https://ceulearning.ceu.edu/course/view.php?id=19138

---

# Course Philosophy

> **"Real data is messy. Embrace it."**

We work with:
- Dirty CSVs with inconsistent formats
- 500K-row datasets
- Missing values, wrong types, duplicate keys
- Real-world messiness

**Because that's what you'll face in every job.**

---

# Success Tips

**Start early** – Don't wait until the last minute

**Practice "Restart & Run All"** – Test before every submission

**Use assertions as tests** – Prove your data is correct

**Come to office hours** – If stuck >15 minutes, ask for help

**Document your assumptions** – Explain your choices

---

# Today's Plan

**Block A (13:30–15:10):** Tidy Data Foundations
- What makes data "tidy"?
- Primary keys and unique identifiers
- Types and missing values
- **In-class exercise:** Clean a messy café sales dataset

**Block B (15:30–17:10):** SQL Foundations + Windows
- Basic SQL queries with DuckDB
- Aggregations and grouping
- Window functions primer (ROW_NUMBER, LAG, moving averages)

**Assigned:** Homework 1 (due start of Day 2)

---

# Tools & Setup

Make sure you have:
- ✅ uv (manages Python 3.13 for you)
- ✅ VS Code (with Python + Jupyter extensions)
- ✅ Git

**Setup:** `uv sync` in the repo root — installs Python 3.13, pandas, DuckDB, everything

**Test it:** open `notebooks/day1/day1_setup_check.ipynb` in VS Code, Run All

All datasets provided offline in the repo.

---

# Get the Course Repository

**Clone it now if you haven't already:**

```bash
git clone https://github.com/earino/ECBS5294.git
cd ECBS5294
uv sync
```

**Or browse online:**
https://github.com/earino/ECBS5294

Everything you need is in this repo:
- Teaching notebooks
- Datasets
- Assignments
- Solutions (encrypted)
- References

---

# Course Resources

**🔗 Moodle (your home base):**
https://ceulearning.ceu.edu/course/view.php?id=19138

- Assignment submissions
- Announcements
- Solution passwords (released after due dates)
- Grades
- Discussion forum

**📦 GitHub (all materials):**
https://github.com/earino/ECBS5294

**Bookmark both!**

---

# One More Thing...

**Questions are encouraged.**

- Ask during class
- Come to office hours
- Email me

**Everyone struggles with this stuff at first.**
That's why we practice together.

---

<!-- _class: lead -->

# Let's Get Started! 🚀

Open your laptops.

Navigate to the course repo.

Let's make sure everyone's setup works.

Then we'll dive into tidy data...
