# ECBS5294: Introduction to Data Science: Working with Data

[![CI](https://github.com/earino/ECBS5294/actions/workflows/ci.yml/badge.svg)](https://github.com/earino/ECBS5294/actions/workflows/ci.yml)

**Central European University**

Welcome! This repository contains everything you need for this course: teaching materials, datasets, exercises, assignments, and resources for learning practical data skills.

---

## 📚 What This Course Is About

Real data is messy. Real questions require SQL. Real work needs reproducible pipelines.

In this course, you'll learn the **day-one skills** that analysts and data scientists use every day:

- **Tidy data principles** – structuring data for analysis
- **SQL with DuckDB** – querying, aggregating, joining, and window functions
- **JSON/API ingestion** – turning messy nested data into clean tables
- **Multi-stage pipelines** – bronze → silver → gold patterns
- **Validations as code** – proving your data is correct
- **Stakeholder communication** – explaining what you found and why it matters

By the end, you'll handle 500K-row datasets, write production-quality queries, and build reproducible analysis pipelines.

---

## 🗓️ Course Details

**Instructor:** Eduardo Ariño de la Rubia  
**Email:** RubiaE@ceu.edu  
**Office:** Room A104  
**Office Hours:** [Schedule at cal.com/earino](https://cal.com/earino)

**Format:** Three full-day sessions (2 blocks per day)  
**Credits:** 1.0 (runs alongside Coding 1 and Data Science 1)

📄 **Full syllabus with dates:** [syllabus.md](syllabus.md)

---

## 🚀 Quick Start

### Before Day 1

This course uses the standard CEU environment: **uv**, **VS Code**, and **Python 3.13**. If you attended the prep session you already have uv, VS Code, Git, and a GitHub account set up. If not, see the [CEU environment reference](https://github.com/zoltanctoth/example-uv-based-project) for one-time installation of uv and VS Code.

1. **Clone this repository:**
   ```bash
   git clone https://github.com/earino/ECBS5294.git
   cd ECBS5294
   ```

2. **Set up your environment:**
   ```bash
   uv sync
   ```

   That's it. This creates a `.venv` folder with Python 3.13 (downloaded automatically if you don't have it) and every package the course needs — pandas, numpy, duckdb, requests, and more — at the exact versions the course was tested with.

   > **Migrating from the old pip setup?** Delete your old virtual environment and run `uv sync`.

3. **Test your setup:**
   - Open the `ECBS5294` folder in VS Code (`File → Open Folder...`)
   - Install the recommended extensions when VS Code offers them (Python + Jupyter)
   - Open `notebooks/day1/day1_setup_check.ipynb`
   - Click **Select Kernel** (top right) and choose the `.venv` Python environment
   - Click **Run All** — every check should pass

4. **Bring your laptop to every class!**

---

## 📂 Repository Structure

```
ECBS5294/
│
├── data/                    # Teaching datasets (offline, provided)
│   ├── day1/                  # Dirty cafe sales data for practice
│   ├── day2/                  # Olist e-commerce marketplace data
│   └── day3/                  # Chicago + NYC government data + Olist subsets
│
├── notebooks/               # Teaching notebooks and exercises
│   ├── day1/
│   │   ├── day1_block_a_tidy_foundations.ipynb
│   │   ├── day1_block_b_01_sql_foundations.ipynb
│   │   ├── day1_block_b_02_aggregations.ipynb
│   │   ├── day1_block_b_03_window_functions_primer.ipynb
│   │   ├── day1_block_b_04_window_functions_deep_dive.ipynb
│   │   ├── day1_exercise_tidy.ipynb
│   │   └── day1_setup_check.ipynb
│   ├── day2/
│   │   ├── day2_block_a_joins.ipynb
│   │   ├── day2_block_b_01_api_json_basics.ipynb
│   │   ├── day2_block_b_02_json_to_duckdb.ipynb
│   │   └── day2_exercise_joins.ipynb
│   └── day3/
│       ├── day3_block_a_pipelines_and_validations.ipynb
│       └── day3_exercise_mini_pipeline.ipynb
│
├── assignments/             # Homework assignments with instructions
│   ├── hw1/                   # SQL single-table + window functions
│   ├── hw2/                   # JSON normalization + multi-table queries
│   └── hw3/                   # End-to-end data integration project
│
├── solutions/               # Encrypted solution ZIPs (see below!)
│   ├── README.md              # How to use encrypted solutions
│   └── solutions-*.zip        # Password-protected (released after due dates)
│
├── references/              # Quick references and cheat sheets
│   ├── tidy_data_checklist.md
│   ├── sql_quick_reference.md
│   ├── pipeline_patterns_quick_reference.md
│   ├── datasets/              # Dataset documentation
│   ├── images/                # Diagrams and visual aids
│   ├── papers/                # Summaries of key papers
│   └── teaching/              # Teacher notes (for your benefit!)
│
├── scripts/                 # Utility scripts
│   ├── decrypt_solutions_zip.py    # Extract encrypted solutions
│   ├── encrypt_solutions.py   # (Instructor use)
│   └── build_slides.sh        # Generate HTML slides from Markdown
│
├── slides/                  # Marp-based presentation slides
│   ├── day1_kickoff.md        # Course introduction (~10 min)
│   ├── day1_block_a_intro.md  # Optional: Tidy data intro (~3 min)
│   ├── day1_block_b_intro.md  # Optional: SQL intro (~3 min)
│   └── themes/                # Custom CEU theme
│
├── syllabus.md              # Full course syllabus with schedule
├── CLAUDE.md                # Repository development guide
└── README.md                # You are here!
```

**Note:** All course materials (Days 1-3) are complete and ready to use.

---

## 🔐 About Solutions (They're Here, But Locked!)

**Good news:** All solutions are in this repo from day one.  
**Smart design:** They're password-protected until after deadlines.

### Why This Approach?

- ✅ No anxiety about "losing" solutions
- ✅ Available immediately after due dates
- ✅ Encourages trying before looking
- ✅ Lets you verify your work once released

### How to Use Solutions

1. **Try the assignment first** – Even partial attempts build understanding
2. **Check Moodle for password release dates** – Posted after deadlines
3. **Decrypt when available:**
   ```bash
   uv run python scripts/decrypt_solutions_zip.py solutions/solutions-day1-blockA.zip
   ```
4. **Learn, don't copy** – Type out solutions to build muscle memory

📖 **Full guide:** [solutions/README.md](solutions/README.md)

---

## 📅 Course Overview

### Day 1 – Tidy Data & SQL Foundations
- **Block A:** Tidy data foundations, primary keys, types, missing values
- **Block B:** SQL basics + window functions primer (ROW_NUMBER, LAG, moving averages)
- **Assigned:** Homework 1 (due start of Day 2)

### Day 2 – Joins & JSON Ingestion
- **Block A:** SQL joins & relational modeling (INNER/LEFT, diagnosing join issues)
- **Block B:** JSON & APIs → tidy tables
- **Assigned:** Homework 2 (due start of Day 3)

### Day 3 – Pipelines & Assessment
- **Block A:** Pipeline patterns + validations (bronze/silver/gold layers)
- **Block B:** In-class exam (paper/pen, 90 minutes, one A4 reference sheet)
- **Assigned:** Homework 3 (due one week after class)

📅 **Specific dates:** See [syllabus.md](syllabus.md) for the current term's schedule.

---

## 📊 Grading

| Component | Weight | What It Tests |
|-----------|--------|---------------|
| **Homework 1** (SQL + windows) | 20% | Query writing, aggregations, window functions |
| **Homework 2** (JSON pipeline) | 25% | Data ingestion, normalization, persistence |
| **Homework 3** (End-to-end) | 25% | Complete pipeline with validation + communication |
| **In-class deliverables** | 5% | Short exercises (completion-based) |
| **In-class exam** (Day 3) | 25% | SQL, joins, data thinking (paper/pen, closed-book) |

**Late policy:** −10% per 24 hours (48-hour max)  
**Median target:** B+ (roughly ⅓ of class at A/A-)

---

## 🎯 Key Resources

### Quick References
- [Tidy Data Checklist](references/tidy_data_checklist.md) – Primary keys, types, missing values
- [SQL Quick Reference](references/sql_quick_reference.md) – Syntax cheat sheet
- [Pipeline Patterns Quick Reference](references/pipeline_patterns_quick_reference.md) – Bronze/silver/gold layers

### Textbooks & Docs
- Arthur Turrell, *Coding for Economists* (selected chapters)
- [The Carpentries](https://carpentries.org/) (Unix, Git, Python episodes)
- [DuckDB Documentation](https://duckdb.org/docs/)

### Teaching Materials
- All notebooks in `notebooks/` – worked examples with explanations

---

## 💡 Tips for Success

### Reproducibility Is Everything
- ✅ **Restart & Run All** before submitting (in VS Code: **Restart**, then **Run All**) – If it doesn't run cleanly, you'll lose points
- ✅ **Use relative paths** – `data/file.csv`, not `/Users/yourname/...`
- ✅ **Commit often** – Small, logical commits help you track changes

### Data Thinking Habits
- Always identify and validate your **primary key**
- Handle **NULL values** consciously (they affect everything!)
- Use **assertions as tests** – Prove your data is correct
- **Document your choices** – Why did you handle missing values this way?

### SQL Strategies
- **Start small:** Use `LIMIT 10` while developing queries
- **Build incrementally:** Add one clause at a time
- **Format for readability:** Uppercase keywords, indentation, one clause per line
- **Check for NULLs:** Always consider `IS NULL` / `IS NOT NULL`

### Window Functions Mental Model
- **Windows KEEP row count** (every row gets a value)
- **GROUP BY COLLAPSES rows** (aggregates reduce rows)
- You can't filter on window functions directly – use a subquery!

### When You're Stuck
1. Review teaching notebooks
2. Check the quick references
3. Read error messages carefully
4. Start simpler (remove complexity, then add back)
5. **Ask for help!** Office hours, email

---

## 🚫 Academic Integrity

### What You CAN Do
✅ Review course materials and documentation
✅ Discuss concepts with classmates (conceptually, not code)
✅ Ask instructor/TA for clarification
✅ Use official documentation (pandas, DuckDB, etc.)

### What You CANNOT Do
❌ Use AI tools (ChatGPT, Claude, Copilot) for graded work
❌ Copy code from classmates
❌ Share your solutions with others
❌ Use solutions from previous years

**Why?** We need to assess YOUR understanding so we can help where you're stuck.

**Policy:** To align with parallel courses (Coding 1, Data Science 1), AI assistants are not permitted for homework or exams. Use them for personal study only.

---

## 🎓 Learning Outcomes

By the end of this course, you will:

1. **Apply tidy data principles** to messy real-world datasets
2. **Write SQL queries** confidently (SELECT, WHERE, JOIN, GROUP BY, window functions)
3. **Ingest JSON/APIs** and normalize into analysis-ready tables
4. **Build reproducible pipelines** with validations as code
5. **Communicate findings** to stakeholders with data dictionaries and clear narratives
6. **Develop performance intuition** for data operations
7. **Handle real data problems** (NULL values, type issues, missing data, duplicate keys)

These are the skills you'll use **on day one** of any analyst or data science role.

---

## 🌟 Philosophy

> **Real data is messy. Embrace it.**

This course doesn't hide the messiness – we work with dirty CSVs, inconsistent types, missing values, and 500K-row datasets because **that's what you'll face in the real world**.

Your job isn't to memorize syntax. It's to:
- **Think clearly** about data structure
- **Make defensible choices** about how to handle issues
- **Document your work** so others (and future you) understand
- **Validate everything** – trust, but verify!

By the end, you'll feel confident tackling real data problems, not just textbook examples.

---

## 📬 Getting Help

**Stuck on something?** Don't suffer in silence!

- **Office hours:** By appointment (Room A104)
- **Email:** RubiaE@ceu.edu
- **In class:** Ask questions! Everyone else probably has the same question.

**Rule of thumb:** If you're stuck for more than 15 minutes, reach out.

---

## 🛠️ Technical Setup

Everything you need — Python 3.13, pandas, numpy, DuckDB — comes from one command: `uv sync`. See the [Quick Start](#-quick-start) at the top of this README for the full steps (clone, `uv sync`, open in VS Code, run the setup check).

All teaching datasets are **provided offline** in this repo – no downloads needed!

---

## 🎉 Let's Get Started!

This course moves fast, but that's because every minute is practical, hands-on skill-building. By the end of three sessions, you'll have built:

- A cleaned dataset from messy CSV data
- SQL queries on 500K+ row datasets
- A JSON-to-database pipeline
- An end-to-end analysis with validation and stakeholder communication

These are portfolio pieces. These are interview talking points. These are **real skills**.

Ready? Open up `notebooks/day1/day1_setup_check.ipynb` in VS Code and let's make sure you're ready to go.

**See you in class!** 🚀

---

## 📄 License

Course materials are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (Creative Commons Attribution 4.0 International) — see [`LICENSE.md`](LICENSE.md).

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, including commercially

…as long as you give appropriate credit.

**Datasets are the exception.** Files under `data/` are third-party works redistributed for teaching, and each keeps its original license — several carry NonCommercial and/or ShareAlike terms that this repo cannot relax. See `LICENSE.md` for the per-dataset breakdown and the `README.md` in each `data/` subdirectory for full attribution.

---

*Questions about this README or the course? Contact the instructor.*
