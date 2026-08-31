# **(ECBS5294) Introduction to Data Science: Working with Data**

**Academic year:** 2026–2027  
**Credits:** 1.0 (600 minutes; runs alongside Coding 1 and Data Science 1\)  
**Dates / Time:** **TBD**, **TBD**, **TBD** *(update at term start)*  
**Meeting blocks:** 13:30–15:10 and 15:30–17:10

---

## **Background and overall aim**

**Content.** Practical literacy for working with data: tidy tables and keys, types and missing values, essential **SQL** with **DuckDB**, turning **JSON/APIs** into analysis-ready tables, and simple multi-stage pipeline habits (raw → clean → analysis) with light validations-as-code and stakeholder-focused communication.

**Relevance.** These skills are day-one requirements in analyst/DS roles and prepare students for Data Engineering and advanced analytics.

---

## **Course prerequisites**

* None.  
* Bring a laptop to all meetings.

---

## **Waiting list handling (priority)**

This is a **core** MSBA course. If oversubscribed, seats and the waiting list will be managed with the following **priority order**:

1. **MSBA students (core)**  
2. **EDP/Data track students**  
3. **All other students** (space permitting)

Within each priority group, places will be offered in order of sign-up and subject to program rules.

---

## **Learning outcomes**

By the end, students can:

1. Apply **tidy data** principles; identify/construct **UID/primary keys**; manage types (dates, floats, booleans) and missing values.

2. Query with **DuckDB/SQL**: `SELECT`, `WHERE`, `ORDER BY`, **aggregations** (`GROUP BY/HAVING`), **JOINs** (INNER/LEFT/RIGHT/FULL), and handle `NULL` correctly.

3. Use a **window functions primer** for common analytics: `ROW_NUMBER()` (latest/dedupe), `LAG()` (period change), and a simple moving average.

4. Ingest **JSON** (file or simple endpoint), normalize nested structures into tidy tables, and **persist** to DuckDB.

5. Build a small, **reproducible** pipeline (bronze → silver → gold) with 2–3 **validations as code** (e.g., PK uniqueness, required non-nulls, date window).

6. Communicate results clearly with concise tables/metrics and a short data dictionary, noting assumptions and limits.

7. Demonstrate basic **performance intuition** (join cardinality and row explosion, aggregation before joining).

---

## **Counting towards degree**

* Core to **MSBA**; complements **Coding 1 (Intro to Python)** and **Data Science 1 (Reproducible Research/Git)** taught in parallel.

* Preparation for **Data Engineering** and analytics electives.

---

## **Technical requirements**

* **Software:** Python 3.13 (managed by uv), VS Code, DuckDB (installed via the course environment), Git.
* **Course repository:** https://github.com/earino/ECBS5294
  * Clone before Day 1: `git clone https://github.com/earino/ECBS5294.git`
  * Contains: `/data`, `/notebooks`, `/assignments`, `/scripts`, `/solutions`, `/references`
* All teaching datasets are provided **offline**.

---

## **Course resources**

* **Moodle:** https://ceulearning.ceu.edu/course/view.php?id=19138
  * Announcements and updates
  * Assignment submissions
  * Solution password releases (after due dates)
  * Discussion forum
  * Grades

* **GitHub repository:** https://github.com/earino/ECBS5294
  * All course materials (notebooks, datasets, assignments)
  * Teaching references and documentation
  * Encrypted solutions (passwords on Moodle)

---

## **Materials and references**

* A. Turrell, *Coding for Economists* (selected chapters).  
* The Carpentries (Unix shell, Git, Python — selected episodes).  
* DuckDB docs (CSV/Parquet querying, SQL reference).  
* Instructor notes and example notebooks in the repo.

---

## **Course requirements and responsibilities**

* **Attendance & participation** expected.  
* **Environment ready** each class.  
* **Reproducibility:** Submissions must “Run-All” from a clean clone with relative paths.

---

## **Course assessment and grading**

* **Homework 1 (SQL single-table \+ window primer)** – 20%
* **Homework 2 (JSON → tables mini-pipeline)** – 25%
* **Homework 3 (end-to-end pipeline \+ KPIs \+ stakeholder note)** – 25%
* **In-class deliverables** (short notebook write-ups, completion-based) – 5%
* **In-class exam (paper/pen, Oct 22\)** – 25%

**Department grading guidance.** The department targets a **class median around B+**, with **no more than roughly one-third** of grades at **A/A-** across sections. Final grades remain at instructor discretion within university policy.

**Late policy.** HW accepted up to 48 hours late at −10% per 24 hours. In-class exam and in-class deliverables occur as scheduled; extensions require documented emergencies and approval.

**Use of AI tools.** To align with parallel courses, **AI assistants (ChatGPT/Claude/Copilot, etc.) are not permitted for graded work** (HWs, in-class exam). You may use them for personal study; do not submit AI-generated code/text.

**Academic integrity & accessibility.** CEU policies apply. Contact the instructor and university office early for accommodations.

---

## **Schedule (3 days, 2 blocks/day)**

### **Day 1 — Wed Oct 8**

**Block A (13:30–15:10) — Data thinking & tidy foundations**

* Tidy data; UID/PK; required vs optional fields; types & pitfalls (floating-point, dates); missing values; notebook state hygiene.

* **In-class deliverable:** Short notebook: load a messy CSV → tidy → designate UID → one summary table.

**Block B (15:30–17:10) — SQL I with DuckDB: single-table mastery (+ window primer)**

* Core SQL: `SELECT`, `WHERE`, `ORDER BY`, calculated columns, `GROUP BY/HAVING`, `NULL` behavior.

* **Window functions (primer, scoped):**

  * `ROW_NUMBER()` to select “latest per id” (dedupe/update).

  * `LAG()` for period-over-period change.

  * 7-row moving average via  
     `AVG(..) OVER (PARTITION BY id ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)`.

  * Mental model: windows **keep row count**; `GROUP BY` **collapses**. Minimal gotchas (explicit `ORDER BY`, simple frames).

* **Assigned:** **HW1** (single-table SQL \+ 1–2 small window tasks). **Due Wed Oct 15 (start of class).**

---

### **Day 2 — Wed Oct 15**

**Block A (13:30–15:10) — SQL II: joins & relational modeling**

* ERD basics; PK/FK; INNER/LEFT/RIGHT/FULL; anti/semi-join patterns; grouping after joins; duplicate inflation; join keys.

* **In-class deliverable:** JOIN queries answering short stakeholder prompts \+ brief rationale.

**Block B (15:30–17:10) — JSON & APIs → tidy tables**

* REST basics (no-auth endpoint or local JSON); JSON → dict/list; normalization; persist to DuckDB; quick join to a dimension; basic typing.

* **Assigned:** **HW2** (mini-pipeline: JSON → tables \+ 3–5 SQL KPIs \+ validations \+ data dictionary). **Due Wed Oct 22 (start of class).**

---

### **Day 3 — Wed Oct 22**

**Block A (13:30–15:10) — Data in the wild \+ mini-pipeline patterns \+ how to work**

* **Data in the wild:** spreadsheet/CSV traps (locale separators, header drift), dates/time zones & coverage checks, categoricals & reference tables (codes vs labels), basic geodata (lat/lon, geocoding caveats), columnar formats (Parquet/Arrow vs CSV).

* **Pipeline patterns:** bronze → silver → gold; idempotent transforms; **validations as code** (PK unique, required non-nulls, date window).

* **Work habits:** Run-All discipline, small commits, reading docs, rubber-duck debugging, when to choose SQL vs Python.

* **Micro-exercise:** 3-step pipeline (bronze → silver → gold) with two assertions \+ a one-paragraph risk note. This prepares you for **HW3**.

**Block B (15:30–17:10) — In-class exam**

* **In-class exam (paper/pen, no computers):** Individual assessment covering SQL fundamentals, joins, window functions, JSON normalization concepts, data validation patterns, and data thinking principles.

  * Format: Short-answer questions, SQL query writing, scenario-based problems (e.g., choosing appropriate join types, identifying data quality issues).

  * Duration: 90 minutes.

  * One A4 reference sheet (both sides, typed or handwritten) permitted.

* **Assigned:** **HW3** (end-to-end pipeline using an **offline data pack** — CSV \+ JSON).

  * Deliver: ingest/normalize; persist to DuckDB; 3–5 KPIs with joins and grouping; 2–3 validations as code; concise data dictionary; **stakeholder note** (8–10 sentences).

  * **Submission:** Git-tracked repo/notebook; **Run-All** succeeds on a clean clone.

  * **Due: Wed Oct 29 (23:59)** — one full week after class.

---

## **Contact details**

**Instructor**: Eduardo Ariño de la Rubia  
**Department**: Economics and Business, Central European University

**Email**: RubiaE@ceu.edu  
**Office**: Room A104  
**Office hours**: [Schedule at cal.com/earino](https://cal.com/earino)

