# ECBS5294 — Data Science 2: Working with Data

**Program:** MSBA (core) · **Credits:** 1.0 · **Academic year:** 2026–2027  
**Format:** 3 sessions × 2 blocks of 100 minutes (13:30–15:10, 15:30–17:10), with the final exam in the last block  
**Instructor:** Eduardo Ariño de la Rubia · [RubiaE@ceu.edu](mailto:RubiaE@ceu.edu) · Room A104 · [office hours](https://cal.com/earino)

---

## What this course is for

Real data arrives messy. Types are wrong, values are missing in three different notations, there is no obvious key, and the interesting part is buried in nested JSON that nobody documented. The analysis you actually want to run is rarely the hard part — getting the data into a shape where that analysis is possible, and being able to show the shape is right, is where the work goes.

This course is one credit of practical instruction in exactly that layer. You will learn to structure tables so they can be joined and trusted, to query them in SQL with DuckDB, to turn JSON and API responses into tidy tables, and to build a small pipeline whose correctness you can demonstrate rather than assert. It is a core MSBA course, following Data Science 1 and running alongside Coding 1, and it is what the Data Engineering and analytics electives are built on top of. These are day-one skills in analyst and data science roles.

---

## What you will be able to do

1. **Structure data so it can be trusted** — tidy tables, an explicit primary key, correct types, and a documented decision about what the missing values mean.
2. **Query relational data with SQL** — filter, calculate, aggregate, and group, and know what `NULL` does to each of those.
3. **Join tables without corrupting the result** — choose the join the question calls for, and recognize when a join has silently inflated your row count.
4. **Use window functions for common analytics** — the latest record per entity, period-over-period change, and a moving average.
5. **Turn JSON into tables** — normalize nested structures from a file or an endpoint, and persist them to a database.
6. **Build a small reproducible pipeline** — raw to clean to analysis-ready, with validations written as code rather than checked by eye.
7. **Communicate a result to a stakeholder** — the metric, the assumptions behind it, and an honest account of what the data cannot answer.
8. **Reason about cost** — why aggregating before joining matters once the tables stop being small.

---

## Format and workload

Each session runs two 100-minute blocks with a break between: teaching interleaved with hands-on work in notebooks you run yourself, on a laptop you bring. Most blocks close with a short in-class deliverable — a notebook you finish and submit, graded on completion — so that the ideas land while you can still ask about them. Come with your environment working; class time is not setup time.

All teaching datasets are provided offline in the course repository. Nothing in this course depends on a network connection or on somebody's API being up.

---

## Prerequisites and setup

No prior SQL or database experience is assumed. Bring a laptop to every session.

The course uses the MSBA-standard stack from the program prep session — Python 3.13 managed by `uv`, VS Code, and Git — plus DuckDB, which installs with the course environment. **Before Session 1**, clone the course repository at <https://github.com/earino/ECBS5294>, run `uv sync`, then open `notebooks/day1/day1_setup_check.ipynb` in VS Code and run it; every check should pass. The repository README covers setup in full, and quick references for SQL, joins, and pipeline patterns live in `references/`.

Optional background: A. Turrell, *Coding for Economists* (selected chapters); The Carpentries lessons on the Unix shell, Git, and Python; and the DuckDB documentation.

---

## AI policy

AI assistants — ChatGPT, Claude, Copilot, and the rest — are **not permitted for graded work**: the three homeworks, the in-class deliverables, and the exam. Coding 1 and Data Science 1 share this policy, so there is one rule to keep track of rather than three.

You may use AI freely for personal study: explaining a concept, working through an example that is not your submission. Do not submit AI-generated code or text. The exam is on paper, which is the honest check on all of this — in the end the skills have to be yours.

---

## Assessment

| Component | Weight |
|---|---:|
| Homework 1 — Single-table SQL and window functions | 15% |
| Homework 2 — JSON into tables, with KPIs and validations | 15% |
| Homework 3 — End-to-end pipeline, KPIs, and stakeholder note | 15% |
| In-class deliverables (completion-based) | 5% |
| Final exam (in class, paper and pen) | 50% |

**Homework** is graded against a rubric published with the assignment, weighted toward correctness and data thinking, with reproducibility and communication carrying real weight as well. Submissions must run end-to-end from a clean clone using relative paths: a notebook that does not restart-and-run-all loses credit regardless of what its saved outputs once showed.

**In-class deliverables** are short notebooks completed during the session and graded on completion rather than correctness.

**The final exam** is individual, on paper, no computers, in the last block of Session 3. It runs 90 minutes and tests the same skills as the homeworks applied to new scenarios. You may bring one A4 reference sheet — both sides, typed or handwritten — and nothing else.

**Department grading guidance.** The department targets a class median around B+, with no more than roughly one-third of grades at A/A−. Final grades remain at instructor discretion within university policy.

---

## Schedule

| Session | Date | Arc | Homework |
|---|---|---|---|
| 1 — Getting data into shape | Mon 5 Oct 2026 | Tidy data, keys, types, missing values; single-table SQL and a window-function primer | HW1 due **Mon 12 Oct, start of class** |
| 2 — Combining and ingesting | Mon 12 Oct 2026 | Joins and relational modeling; JSON and APIs into tidy tables | HW2 due **Mon 19 Oct, start of class** |
| 3 — Pipelines and assessment | Mon 19 Oct 2026 | Data in the wild, pipeline patterns, validations as code; exam in Block B | HW3 due **Mon 2 Nov, 23:59** |

All deadlines are on Moodle, which is authoritative.

---

## Submitting your work

Everything is submitted through **Moodle** (<https://ceulearning.ceu.edu/course/view.php?id=19138>); nothing is graded from GitHub. Course materials — notebooks, datasets, assignments, and references — live in the course repository, and each homework README states exactly what to hand in. Submissions must run from a clean clone with relative paths, and must contain nothing you cannot explain.

Solutions ship with the repository from day one, encrypted. Passwords are released on Moodle after each deadline has passed.

---

## Policies

- **Late homework:** accepted up to 48 hours late at −10% per 24 hours; after 48 hours, no credit.
- **Extensions:** ask before the deadline, by email, with a reason. Documented illness or emergencies are always accommodated.
- **Missed exam:** a documented emergency is accommodated through a resit arranged with me; an undocumented absence scores 0. The exam is half your grade — if something is going wrong, tell me before the session rather than after.
- **Missed in-class deliverable:** these are graded on completion and cannot be made up. A documented absence excludes that deliverable from your average rather than scoring 0.
- **Regrading:** within 7 days, in writing, naming the rubric criterion you believe was misapplied. The whole submission is re-read, and the grade can move either way.
- **Grade conversion:** CEU letter scale — A 94+ · A− 88–93 · B+ 80–87 · B 71–79 · B− 63–70 · C+ 58–62 (minimum pass) · F below.
- **Oversubscription:** this is a core MSBA course. If oversubscribed, seats go to MSBA students first, then EDP/Data track students, then others as space permits — in order of sign-up and subject to program rules.

---

## Academic integrity and accessibility

CEU academic integrity and accessibility policies apply. Contact me and the relevant university office early if you need accommodations. Accessible-format exam papers are available on request per your CEU accommodation letter; please ask at least a week ahead.
