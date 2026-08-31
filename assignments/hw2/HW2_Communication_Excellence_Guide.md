# HW2 Stakeholder Communication Excellence Guide

**Course:** ECBS5294 - Introduction to Data Science: Working with Data
**Assignment:** Homework 2 - TechMart QuickBuy Acquisition
**Purpose:** Model stakeholder communications for data analysis

---

## 🎯 Communication Framework

### The Three Questions Every Stakeholder Wants Answered

1. **WHAT** - What does the data show? (Facts)
2. **SO WHAT** - Why does this matter? (Interpretation)
3. **NOW WHAT** - What should we do? (Recommendation)

### Audience Adaptation Matrix

| Stakeholder | Primary Concern | Communication Focus | Avoid |
|-------------|----------------|-------------------|--------|
| **CEO/Board** | Strategic impact, ROI | Decisions, risks, opportunities | Technical details |
| **CFO** | Financial implications | Numbers, costs, savings | Vague estimates |
| **CMO** | Customer behavior | Insights, patterns, segments | Data processing |
| **Product Team** | Development priorities | Features, user needs | Business politics |
| **Engineering** | Technical requirements | Specs, constraints, timelines | Business fluff |
| **Data Quality** | Risk assessment | Issues, monitoring, comparison | Sugar-coating |

---

## ⚖️ The Prime Directive: Evidence-Bounded Claims

**Every number in your communication must be derivable from a query you actually ran.**

This dataset contains products, reviews, and tags. It does **not** contain costs, margins, revenue, traffic, conversion rates, customer identities, repeat-purchase behavior, or return rates. A professional analyst:

- ✅ States what the data shows, with the numbers to prove it
- ✅ Names what the data *cannot* answer — and what additional data would be needed
- ❌ Never invents a plausible-sounding figure ("35% higher margins", "$800K in savings") to make a recommendation sound stronger

Inventing metrics is not persuasive communication — it is fabrication, and in a real acquisition it can be career-ending (or worse). The excellent examples below are excellent *because* every figure traces back to the dataset, and every gap is labeled as a gap.

---

## 📝 Exemplary Communication Examples

*(All figures below come from the actual HW2 dataset. Your numbers should match what your own queries return.)*

### Part 1: Initial Data Assessment

#### ❌ **Poor Example:**
"The data has 194 products and 710 reviews. There are nested objects and arrays. Everything looks fine."

**Why it's poor:** Too vague, no insight, doesn't address stakeholder concerns

#### ✅ **Excellent Example:**
"QuickBuy's catalog is structurally clean: all 194 products have complete core fields (ID, title, price, category) with zero missing values. The JSON nests dimensions and meta objects plus review and tag arrays, which need normalizing into separate tables — roughly a half-day of work. Customer sentiment coverage is good but uneven: 710 reviews spanning January 2024 through June 2025, with most products reviewed but 6 carrying no reviews at all — those will need care in any per-product satisfaction metric. The 24 product categories map cleanly to a relational model. Recommend proceeding with normalization; no blocking issues found."

**Why it's excellent:**
- Quantifies quality ("zero missing values", "6 carrying no reviews")
- Estimates effort honestly
- Flags an analytical trap (unreviewed products) before it bites
- Makes a clear recommendation
- Every figure is checkable against the data

---

### Part 2: Normalization Summary

#### ❌ **Poor Example:**
"Created three tables from the JSON. Products has 194 rows, reviews has 710 rows, and tags has 364 rows."

**Why it's poor:** Just states facts, no business value, doesn't address BI concerns

#### ✅ **Excellent Example:**
"Successfully normalized QuickBuy's nested JSON into three relational tables: products (194 rows), reviews (710 rows, one row per customer review), and product_tags (364 rows). All foreign key relationships are intact — every review and tag row joins back to a valid product ID, with zero orphaned records. Dates are standardized ISO timestamps and the nested dimensions are now separate numeric columns (width, height, depth) for easier aggregation. One modeling note for BI: reviews are one-to-many, so joining products to reviews changes the row grain — dashboards averaging ratings should aggregate the reviews table first."

**Why it's excellent:**
- Confirms success with specifics
- Verifies referential integrity with a checkable claim
- Proactively flags the join-grain trap for dashboard builders
- No invented performance or compatibility claims

---

### Part 3: Data Quality Report

#### ❌ **Poor Example:**
"Data quality is good. No major issues found. All validations passed."

**Why it's poor:** Too generic, no specifics, doesn't build confidence

#### ✅ **Excellent Example:**
"Validation results: 100% primary-key uniqueness on products, zero orphaned foreign keys in reviews and product_tags, and full row-count preservation (194 / 710 / 364) through normalization. Critical fields (id, title, price, category) show 0% nulls. Two limitations worth stating plainly: 6 products (3%) have no reviews, so satisfaction metrics silently exclude them under an INNER JOIN; and review volume varies widely per product (0–12), so per-product averages on thin review counts are noisy. We have no external benchmark for acquisition data quality — this is our first such integration — but on internal checks, risk level is LOW with no blocking issues."

**Why it's excellent:**
- Specific, checkable metrics
- States limitations without being asked
- Explicitly declines to invent a benchmark it doesn't have
- Clear risk assessment

---

### Part 4: Technical Handoff

#### ❌ **Poor Example:**
"Tables are loaded into DuckDB. Everything works fine. You can start using them."

**Why it's poor:** No technical details, doesn't help engineering team

#### ✅ **Excellent Example:**
"Schema deployed: products (194 rows, primary key `id`), with reviews (710 rows) and product_tags (364 rows) referencing it via `product_id`. All columns are typed — prices and ratings numeric, dates as ISO timestamps. Review dates span January 2024 to June 2025, so partition by month or year if you implement historical archival. At this scale DuckDB handles the three-table join instantly, but I have not load-tested beyond this dataset — flag it if you expect the full QuickBuy production volume to be orders of magnitude larger. Tables are analysis-ready; no post-processing required before your ETL picks them up."

**Why it's excellent:**
- Technical specifics an engineer can act on (keys, types, date span)
- Honest scope statement ("have not load-tested beyond this dataset")
- Proactive consideration (partitioning)
- Clear handoff point

---

### Part 5: Strategic Recommendations

#### 5.1 Category Strategy (CEO/Board)

##### ❌ **Poor Example:**
"Some categories have higher ratings than others. Mens-shirts is good. Vehicle is bad."

**Why it's poor:** No actionable insights, no supporting numbers

##### ✅ **Excellent Example:**
"Customer satisfaction is strongest in mens-shirts (4.00 average across 26 reviews), tablets (3.93), and groceries (3.89 across 74 reviews — our deepest evidence base). The weak tail is clear: vehicle (2.40) and womens-dresses (2.69) sit far below the 3.64 catalog average. I recommend prioritizing the top categories in integration marketing and putting vehicle and womens-dresses under review. One honest caveat for the board: this dataset contains ratings, not financials — we cannot see margins, revenue, or return costs, so any divestment decision needs finance data joined to these satisfaction signals before it's final."

**Why it's excellent:**
- Every number is a query result (including sample sizes)
- Distinguishes strong evidence (74 reviews) from thin evidence
- Clear recommendation with named categories
- Explicitly bounds what the data can support — and asks for the missing data

#### 5.2 Marketing Strategy (CMO)

##### ❌ **Poor Example:**
"Products with more reviews should be featured in marketing."

**Why it's poor:** Too obvious, no insight into why or how

##### ✅ **Excellent Example:**
"82 products — 42% of the catalog — have more than 3 reviews, giving us a real 'customer favorites' pool. The engagement leaders are Sports Sneakers Off White & Red (12 reviews), the Gigabyte Aorus Men Tshirt (11), and Tennis Racket (10): sports and apparel dominate the high-engagement list. I recommend a 'Customer Favorites' launch campaign built from products combining high review counts with above-average ratings. Two things this data cannot tell us: whether engagement converts to sales (we have no conversion or revenue data), and who these reviewers are (no customer segments). Treat review volume as an attention signal, not a revenue forecast, until we join QuickBuy's order data."

**Why it's excellent:**
- Specific products and counts, straight from the query
- Concrete campaign suggestion tied to evidence
- Names the two inferential gaps instead of papering over them
- Sets up the correct next data request

#### 5.3 Product Development (Product Team)

##### ❌ **Poor Example:**
"Kitchen tools and sports equipment are popular tags."

**Why it's poor:** Just states facts, no development guidance

##### ✅ **Excellent Example:**
"Tag analysis shows kitchen tools on 19 products — the most common feature in the catalog — followed by electronics and sports equipment (17 each) and smartphones (16). QuickBuy's catalog identity is practical home and sports gear, not luxury. For roadmap planning: cross-reference the tag frequencies with the category satisfaction scores from 5.1 before committing — a common tag in a low-rated category (e.g., anything vehicle-adjacent) is breadth without customer love. The dataset has no cost or margin fields, so 'which features are profitable' remains a finance question; what we can say is which features are *present* and how customers rate the products carrying them."

**Why it's excellent:**
- Exact tag counts from the data
- Synthesis across two analyses (tags × ratings)
- Clear boundary between answerable and unanswerable questions

#### 5.4 Integration Timing (CEO)

##### ❌ **Poor Example:**
"Reviews are stable. We should integrate soon."

**Why it's poor:** No trend evidence, vague timing

##### ✅ **Excellent Example:**
"QuickBuy's satisfaction trajectory is genuinely improving: average review ratings climbed from 3.20 in the first half of 2024 to 3.58 in late 2024 and 4.03 in the first half of 2025, with June 2025 alone averaging 4.38. Review volume also shows a clear November–December surge (133 of the 710 reviews), consistent with holiday-driven engagement. Both signals argue for accelerating integration ahead of Q4 to catch the seasonal peak with an improving brand. Caveat for the board: 710 reviews over 18 months is a modest evidence base and reviews are not revenue — the trend is encouraging, but I would not re-justify the $12M price on ratings alone."

**Why it's excellent:**
- The trend claim is backed by period-over-period numbers
- Seasonality claim is quantified, not asserted
- Timing recommendation follows from the evidence
- Sizes the confidence honestly

---

## 📊 Executive Summary Excellence

### ❌ **Poor Executive Summary:**
"We successfully processed QuickBuy's data. It has 194 products and 710 reviews. The data quality is good. Some categories perform better than others. We should integrate the data soon."

**Why it's poor:**
- No specific insights
- No trend or risk assessment
- No clear recommendations

### ✅ **Excellent Executive Summary:**
"We successfully normalized QuickBuy's complete catalog — 194 products, 710 customer reviews, and 24 categories — with clean validation results: unique keys, zero orphaned records, and no missing critical fields. The satisfaction picture is a genuine positive: average ratings rose from 3.20 (H1 2024) to 4.03 (H1 2025), led by mens-shirts, tablets, and groceries, while vehicle (2.40) and womens-dresses (2.69) drag the tail. Review volume peaks in November–December, so integrating before Q4 captures QuickBuy's strongest season on an improving trend. Recommended actions: proceed with integration now, feature the 82 high-engagement products in launch marketing, and put the two weakest categories under review pending financial data. To be direct about limits: this dataset contains no revenue, cost, or customer data, so ROI projections for the $12M acquisition require QuickBuy's order history — securing that is my top data request."

**Why it's excellent:**
- Opens with verified scope and quality
- Every figure traces to a query (trend, categories, seasonality, counts)
- Clear, sequenced recommendations
- Ends by naming the evidence gap and the next data request — that's what real analytical leadership sounds like

---

## 🎯 Key Principles for Excellence

### 1. **Be Specific, Not Generic**
- ❌ "Data quality is good"
- ✅ "100% key uniqueness, zero orphaned FKs, 0% nulls in critical fields"

### 2. **Show Your Evidence Base**
- ❌ "Groceries performs well"
- ✅ "Groceries averages 3.89 across 74 reviews — our deepest evidence base"

### 3. **Translate Technical to Business**
- ❌ "Reviews are one-to-many"
- ✅ "Joining products to reviews changes the row grain — aggregate first, or dashboard averages will be wrong"

### 4. **Always Include Next Steps**
- ❌ "Analysis complete"
- ✅ "Tables are analysis-ready; my top data request is QuickBuy's order history for revenue analysis"

### 5. **Quantify What the Data Supports — and Only That**
- ❌ "Divesting vehicle frees up $800K in inventory costs" *(no cost data exists — this is fabrication)*
- ✅ "Vehicle averages 2.40 across 10 reviews; a divestment decision needs finance data joined to this signal"

### 6. **Address the Unspoken Question**
- CEO wonders: "Was this $12M worth it?" — answer with what the data shows *and what it can't*
- CMO wonders: "Where should I spend my budget?"
- Engineers wonder: "How much work is this for my team?"

### 7. **Name the Gaps Proactively**
- ❌ Silently averaging ratings over products with 1 review
- ✅ "Per-product averages on 0–12 reviews are noisy; category-level numbers are more stable"

---

## 📈 Grading Rubric for Communications

### A-Level (90-100%)
- Specific metrics and numbers, **all derivable from the student's own queries**
- Actionable recommendations
- Explicitly names what the data cannot answer
- Appropriate technical depth for audience
- Clear next steps
- Professional tone

### B-Level (80-89%)
- Good insights but less specific
- Some recommendations
- Generally appropriate for audience
- Professional writing
- Addresses main concerns

### C-Level (70-79%)
- Basic observations
- Few specific numbers
- Generic recommendations
- Misses some stakeholder concerns
- Adequate writing

### Below C (<70%)
- Vague or generic statements — **or fabricated figures not derivable from the data**
- No actionable recommendations
- Wrong audience focus
- Poor writing
- Misses the business context

**Note:** an invented metric (a margin, ROI, or cost figure the dataset cannot produce) caps a communication at C-level regardless of how polished the writing is.

---

## 💡 Common Mistakes to Avoid

1. **Inventing numbers the data cannot produce**
   - This dataset has no costs, margins, revenue, conversion, or customer identities
   - If a claim needs one of those, say "we'd need X data to answer this" — that IS the professional answer

2. **Writing for the wrong audience**
   - Don't give CEOs SQL details
   - Don't give engineers business strategy

3. **Being too vague**
   - "Several products" → "82 products (42% of catalog)"
   - "Good ratings" → "4.00 average across 26 reviews"

4. **Hiding the evidence base**
   - A 3.9 average on 74 reviews and a 3.9 average on 3 reviews are not equally trustworthy — show the counts

5. **No clear recommendation**
   - Every communication should suggest action
   - Even if it's "continue monitoring"

6. **Over-promising**
   - Be realistic about timelines and effort
   - Flag potential issues proactively

---

## 🏆 The Gold Standard

Every stakeholder communication should:
1. **Answer the question asked** (not the question you wish they asked)
2. **Provide evidence** (specific numbers from your own queries, with sample sizes)
3. **Bound the claim** (say what the data cannot show, and what data would close the gap)
4. **Recommend action** (what to do next)
5. **Build confidence** (you understand both data and business — including its limits)

Remember: You're not just analyzing data - you're enabling $12M business decisions. The fastest way to lose a board's trust is one invented number. Write like it matters, because it does.

---

## 📚 Practice Exercises

Try writing stakeholder communications for these scenarios:

1. **The CEO asks:** "Should we shut down QuickBuy's weakest categories based on this data?" *(What can ratings alone justify? What can't they?)*

2. **The CMO asks:** "Which products should headline the Black Friday campaign?" *(The data has seasonality and engagement — but no sales.)*

3. **Engineering asks:** "Will this integration affect our SLA commitments?" *(What have you actually tested?)*

4. **The Board asks:** "Is customer satisfaction trending the right way to justify the price?" *(You have a real trend — state it with its size.)*

Compare your answers to the examples above. Are you being specific? Are your numbers derivable from queries? Did you name the gaps?

---
