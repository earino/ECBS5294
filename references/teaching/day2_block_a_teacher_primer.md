# Day 2, Block A: SQL Joins & Relational Modeling
## Teacher Primer

**Duration:** 90 minutes (13:30–15:10)
**Audience:** MSBA students, Day 2 of program
**Teaching Mode:** Demonstration-based (students watch, don't code along)
**Context:** Building on Day 1 Block B (SQL foundations, aggregations, window functions)

---

## Learning Objectives

By the end of Block A, students will be able to:

1. **Explain** primary keys and foreign keys in relational databases
2. **Read** basic ERDs (entity-relationship diagrams)
3. **Write INNER JOIN queries** to combine matching records
4. **Write LEFT JOIN queries** to keep all records from one table
5. **Use anti-join pattern** (LEFT JOIN + IS NULL) to find unmatched records
6. **Use CTEs** (WITH clause) for readable multi-step queries
7. **Recognize and avoid duplicate inflation** when joining one-to-many relationships
8. **Aggregate correctly** after joins with proper GROUP BY grain
9. **Combine joins with window functions** for advanced analytics

---

## Session Flow (90 minutes)

### 0:00-0:05 | Block Introduction & Context (5 min)

**Opening statement:**
> "Yesterday you learned SQL for single tables. Today we connect tables together - this is where SQL becomes truly powerful for business analysis."

**Key points:**
- Data lives in multiple tables, not one giant spreadsheet
- Joins are how you answer cross-table questions
- This is foundational for analytics work

**Set expectations:**
- Students will WATCH demonstrations (no coding along)
- Take notes on concepts, not syntax
- Hands-on practice comes in the exercise (25 min later)

---

### 0:05-0:15 | Setup & ERD Walkthrough (10 min)

**Materials:** `day2_block_a_joins.ipynb` projected

**Run the setup cells:**
- Import libraries, connect to DuckDB
- Load all 7 Olist tables
- Show row counts (99K orders, 112K order_items, etc.)

**Show the ERD diagram:**
- Point out customers → orders → order_items flow
- Explain PK (primary key) vs FK (foreign key)
- "FK tells you HOW to join tables"

**Business framing:**
- "This is a real Brazilian marketplace with sellers, customers, products"
- "Same structure you'll see at Amazon, eBay, Shopify"

**Pedagogical note:** Don't dwell on ERD theory. Show it, explain enough to understand joins, move on.

---

### 0:15-0:35 | INNER JOIN: The Workhorse (20 min)

**Core concept:** INNER JOIN returns only matching rows from both tables

**Show Venn diagram** (in notebook)

**Example 1: Basic INNER JOIN (5 min)**
- Orders with customer location
- Run the query, show results
- Point out: `ON o.customer_id = c.customer_id` (this is the join condition)
- Point out: Table aliases (`o`, `c`) make queries readable

**Example 2: INNER JOIN with aggregation (5 min)**
- Count orders by customer state
- Show: São Paulo dominates
- Business insight: "This tells us where to focus regional marketing"

**Example 3: Multi-table INNER JOIN (8 min)**
- Revenue by product category (English names)
- Three tables chained: order_items → products → categories
- Run query, show top 10 categories
- Business insight: "Health & beauty, watches, bed/bath are revenue drivers"

**Example 4: Implicit INNER JOIN (2 min)**
- Show that `JOIN` = `INNER JOIN` (same thing)
- Run both, prove identical results
- "Be explicit in your code - write INNER JOIN"

**Common confusion to address:**
- "Why do we need multiple tables?" → Avoid redundancy, easier to update
- "What if the FK doesn't match?" → That's next: LEFT JOIN!

---

### 0:35-0:50 | LEFT JOIN: Keeping Unmatched Rows (15 min)

**Core concept:** LEFT JOIN keeps ALL rows from left table, with NULLs if no match

**Show Venn diagram** (in notebook)

**Example 5: Basic LEFT JOIN (4 min)**
- Orders with review scores (some orders have no reviews)
- Run query, point out `NaN` values
- "NULL means: order exists, but no review found"

**Example 6: The Anti-Join Pattern (6 min)**
- Find orders WITHOUT reviews
- LEFT JOIN + `WHERE review_id IS NULL`
- Run query, count results: 768 unreviewed orders (0.77%)
- Business insight: "These orders need follow-up for customer feedback"

**Why this is called anti-join:**
- "Anti" = opposite of match
- LEFT JOIN finds all, WHERE IS NULL filters to unmatched
- This is a CRITICAL pattern for analytics

**Example 7: LEFT JOIN with aggregation (5 min)**
- Average review score by order status
- Show how COUNT() handles NULLs differently than COUNT(DISTINCT)
- Point out: AVG automatically excludes NULLs
- Business insight: "Delivered orders have 4.1-star average"

**Common mistake to address:**
- Using INNER JOIN when you mean LEFT JOIN → silently loses data!
- "If you want ALL of something, use LEFT JOIN"

---

### 0:50-0:55 | RIGHT JOIN & FULL JOIN: Quick Mention (5 min)

**RIGHT JOIN:**
- "It's just LEFT JOIN with tables flipped"
- Show the equivalence: `A RIGHT JOIN B` = `B LEFT JOIN A`
- "Industry reality: People just use LEFT JOIN. RIGHT JOIN is rare."
- "Our dataset: No natural RIGHT JOIN examples (all products have orders)"

**FULL OUTER JOIN:**
- "Returns everything from both tables"
- "Use case: Reconciling two data sources, finding discrepancies"
- "Rare in day-to-day analytics"

**Key message:** Focus on INNER and LEFT - they cover 95% of real-world use cases.

---

### 0:55-1:05 | CTEs: Modern SQL Pattern (10 min)

**Core concept:** CTEs (WITH clause) break complex queries into readable steps

**The problem:** Nested subqueries are hard to read

**Example 8: Without vs With CTE (5 min)**
- Show nested subquery (ugly, hard to read)
- Show same query with CTE (clean, clear)
- "This is how professionals write SQL"
- Run both, prove identical results

**Example 9: Multiple CTEs (5 min)**
- São Paulo vs other states comparison
- Three clear steps chained together
- "Recipe-style: Step 1, then Step 2, then Step 3"
- Business insight: "Sellers perform similarly across states"

**Why CTEs matter:**
- Reads top-to-bottom (like a recipe)
- Each step is clearly named
- Easier to debug (test each CTE separately)
- Can chain as many as you need

**Pedagogical note:** Students LOVE CTEs once they see them. This often gets "aha!" reactions.

---

### 1:05-1:10 | BREAK POINT - Questions (5 min)

**Explicit pause for questions**

**What we've covered so far:**
- ERDs and PK/FK relationships
- INNER JOIN (matching rows only)
- LEFT JOIN (all from left table)
- Anti-join pattern (finding unmatched)
- CTEs (readable structure)

**What's coming:**
- The dangers (duplicate inflation, aggregation mistakes)
- The grand finale (everything together)
- Hands-on exercise

**Encourage questions:** "This is complex. What's unclear?"

---

### 1:10-1:25 | The Dangers: Duplicate Inflation & Aggregation (15 min)

**Setup:** "This is the #1 mistake beginners make with joins. Pay attention!"

**The Problem: Duplicate Inflation (10 min)**

**Example 10: Demonstrating the problem**
- Count orders three ways:
  1. Direct from orders table: 99,441 ✅
  2. After joining to order_items: 112,650 ❌ (WRONG!)
  3. Using COUNT(DISTINCT): 99,441 ✅
- Run all three, compare results

**Why it happens:**
- orders has 99K rows (one per order)
- order_items has 112K rows (multiple items per order)
- When you join them, orders with 2 items appear TWICE!

**Example 11: See the duplication**
- Show one order with multiple items
- Same order_id appears 3 times in result
- "If you count rows, you're counting ITEMS, not ORDERS"

**The fix: COUNT(DISTINCT ...)**
- Always use DISTINCT when counting after joins
- Or aggregate at correct grain first (next topic)

**Aggregating Correctly (5 min)**

**Key principle:** Your GROUP BY defines the GRAIN of your result

**Example 12: Correct aggregation**
- Revenue per order (order grain)
- GROUP BY order_id collapses multiple items back to one row
- SUM(price) adds up all items in each order
- Result: One row per order ✅

**Example 13: Multi-level aggregation**
- Average order value per seller state
- CTE 1: Calculate at order grain
- CTE 2: Aggregate to state grain
- "Clear two-step logic prevents mistakes"

**Common confusion to address:**
- "Why did my row count explode?" → One-to-many relationship
- "Should I use DISTINCT everywhere?" → No, understand your grain first

---

### 1:25-1:35 | Grand Finale: Everything Together (10 min)

**Setup:** "Now we combine EVERYTHING from Day 1 and today. Watch this!"

**The Query: Top 3 sellers per state by revenue**

**Walk through step by step (don't rush!):**

**Step 1 - CTE seller_revenue:**
- INNER JOIN order_items → sellers
- GROUP BY seller_id, seller_state
- Calculate total revenue per seller
- "This is our base data"

**Step 2 - CTE ranked_sellers:**
- Add ROW_NUMBER() OVER (PARTITION BY seller_state ORDER BY revenue DESC)
- "Remember window functions from yesterday?"
- "PARTITION BY restarts ranking for each state"
- "ORDER BY ranks highest revenue first"

**Step 3 - Main query:**
- Filter WHERE rank_in_state <= 3
- ORDER BY seller_state, rank_in_state
- "Top 3 per state, sorted nicely"

**Run the query, show results**

**Point out what's combined:**
- ✅ INNER JOIN (today)
- ✅ CTE (today)
- ✅ GROUP BY + aggregation (Day 1)
- ✅ ROW_NUMBER() OVER (PARTITION BY...) (Day 1)
- ✅ Filtering on window function result (Day 1)

**Business value:**
- "Who are top performers in each region?"
- "This is analytics in the real world"
- "You'll write queries like this constantly"

**This should be a showman moment:** "Look how much you can do now!"

---

### 1:35-1:40 | Wrap-Up & Transition to Exercise (5 min)

**Quick recap:**
- ✅ INNER JOIN - matching rows
- ✅ LEFT JOIN - all from left + matches
- ✅ Anti-join - finding unmatched (LEFT + IS NULL)
- ✅ CTEs - readable structure
- ✅ Duplicate inflation - use COUNT(DISTINCT)
- ✅ Aggregation grain - GROUP BY defines result level
- ✅ Synthesis - combining with window functions

**Critical warnings to repeat:**
- ⚠️ Check row counts after joins (did they explode?)
- ⚠️ Use COUNT(DISTINCT) across one-to-many relationships
- ⚠️ LEFT JOIN when you want "ALL of something"

**Transition to exercise:**
- "Now YOU practice with a real business scenario"
- "Paula Costa at Olist needs insights for a board meeting"
- "You'll write 3 queries in class (25 min)"
- "3 more queries for homework"

**Open exercise notebook:** `day2_exercise_joins.ipynb`

**Read the Paula Costa email aloud** (or have students read it)
- Sets the scene
- Creates urgency and business context
- Students should feel they're solving a REAL problem

---

### 1:40-2:05 | Student Work Time (25 min)

**Circulate the classroom:**
- Help with technical issues (can't connect to DuckDB, path problems)
- Answer conceptual questions ("Which join type should I use?")
- Encourage students who are stuck ("Start with the simplest part")
- Challenge students who finish early ("Try Query 4!")

**Common issues to watch for:**
- Confusion about which tables to join
- Forgetting table aliases
- Using INNER JOIN when they need LEFT JOIN
- Not using DISTINCT when counting

**Dos:**
- Ask guiding questions: "What are you trying to keep - all orders or only matched ones?"
- Point to teaching notebook: "Remember Example 6 - same pattern"
- Encourage peer help: "Check with your neighbor"

**Don'ts:**
- Don't write the query for them
- Don't let them get stuck for more than 5 minutes without intervening
- Don't expect everyone to finish all 3 queries (that's OK!)

---

### 2:05-2:10 | Wrap-Up & Homework (5 min)

**If time allows:**
- Quick show of hands: "Who got Query 1 working? Query 2? Query 3?"
- Celebrate progress: "You're writing multi-table analytical queries!"

**Homework instructions:**
- Complete Queries 1-3 if not done in class
- Attempt Queries 4-6 (less scaffolded, good practice)
- Write executive summary for Paula (8-10 sentences)
- Due: Start of next class
- Upload to Moodle

**Remind about solution:**
- Solution will be released after next class
- Don't look until you've tried!
- Learning happens in the struggle

**Preview next block:**
- "Next up: JSON normalization and API data ingestion"
- "We'll take messy nested JSON and transform it to clean relational tables"

---

## Materials Required

### For Teaching:
1. **Teaching notebook:** `notebooks/day2_block_a_joins.ipynb`
   - All examples pre-written and tested
   - Runs end-to-end without errors
   - Optimized for projection (clear visuals, good font sizes)

2. **Projector/screen setup:**
   - Test font size readability from back of room
   - Zoom browser if needed
   - Have backup: PDF export of notebook

3. **Data files** (already loaded in notebook):
   - All 7 Olist CSV files in `data/day2/block_a/`
   - Verified to load correctly with relative paths

### For Students:
4. **Exercise starter:** `notebooks/day2_exercise_joins.ipynb`
   - Paula Costa narrative
   - 3 scaffolded in-class queries
   - 3 homework queries
   - Validation cells

5. **Solution (encrypted):** `solutions/solutions-day2-blockA.zip`
   - Complete with explanations
   - Password released after homework due date
   - Listed in `solutions/PASSWORDS.md` (gitignored)

### Reference Materials:
6. **Quick reference card:** `references/sql_joins_quick_reference.md`
   - One-page cheat sheet
   - Students can reference during exercise
   - Also useful for homework

---

## Pedagogical Approach for Demonstration-Based Teaching

### Core Principles

**1. Students watch, don't code during teaching**
- They should focus on understanding concepts, not syntax
- Hands-on practice comes later (exercise)
- This is lecture + live demonstration, not workshop

**2. Run EVERY query, show REAL results**
- Don't just talk about queries - execute them!
- Let students see the data transform
- Point out interesting patterns in results

**3. Business framing throughout**
- Every query should answer a business question
- "Why would Paula need this?"
- Connect to real-world analytics work

**4. Build complexity incrementally**
- Start simple (basic INNER JOIN)
- Add complexity gradually (multi-table, aggregation, CTEs)
- End with synthesis (grand finale combines everything)

**5. Address mistakes proactively**
- Show the WRONG way, then the RIGHT way
- Example: Count after join (wrong) vs COUNT(DISTINCT) (right)
- Normalize errors: "Everyone makes this mistake at first"

---

## Common Student Struggles & Mitigation

| Struggle | What It Looks Like | Mitigation Strategy |
|----------|-------------------|---------------------|
| **"Too many tables!"** | Overwhelmed by ERD, unsure which tables to join | Focus on the FK arrows: "Follow the foreign key from table A to table B" |
| **"INNER vs LEFT - which one?"** | Students default to INNER for everything | Decision tree: "Do you want ALL of X? Use LEFT. Only matches? Use INNER." |
| **"My query returns no rows"** | Filter conditions too strict, or wrong join type | Check row counts at each step: "How many BEFORE join? How many AFTER?" |
| **"Row count exploded"** | Didn't realize one-to-many relationship | Show with specific example: "One order, three items = three rows in result" |
| **"Syntax errors"** | Missing commas, wrong aliases, typos | Encourage copy-paste from teaching notebook, then modify |
| **"Don't know where to start"** | Paralyzed by exercise complexity | "Start with Query 1 - just get TWO tables connected first" |

---

## Time Management & Pacing

**If running ahead:**
- Spend more time on questions during break (1:10)
- Add additional examples from teaching notebook
- Start exercise early (students get more work time)

**If running behind (likely!):**
- Skip Example 4 (implicit INNER JOIN) - nice-to-know, not critical
- Condense RIGHT/FULL JOIN section (0:50-0:55) to 2 minutes
- Shorten grand finale walkthrough to 7 minutes (still show it, just faster)
- Still give students full 25 minutes for exercise (this is non-negotiable)

**Critical sections (don't cut):**
- INNER JOIN examples (students must see this)
- LEFT JOIN + anti-join pattern (critical for analytics)
- Duplicate inflation danger (most common mistake)
- Exercise work time (students need hands-on practice)

**Timing checks:**
- 0:35 - Should be finishing INNER JOIN section
- 1:05 - Should be at break point
- 1:25 - Should be starting grand finale
- 1:40 - MUST transition to exercise (even if not done with teaching)

---

## Assessment (Formative)

**During teaching (observation):**
- Are students taking notes?
- Do they look confused or engaged?
- Are they asking questions?

**During exercise (circulation):**
- Can they identify which tables to join?
- Do they choose correct join types?
- Are they making progress or stuck?

**After class (review submissions):**
- Did they complete the 3 in-class queries?
- Are the queries correct or close?
- Do their interpretations show business thinking?

**Not assessed:**
- Speed (some students are slower, that's OK)
- Perfect syntax (syntax can be fixed)
- Completing all homework queries (Query 6 is bonus/challenging)

---

## Connection to Other Materials

**From Day 1 Block B:**
- Students already know SELECT, WHERE, GROUP BY, ORDER BY
- They've used window functions (ROW_NUMBER, PARTITION BY)
- CTEs are new, but build on familiar SELECT structure

**To Homework 1:**
- Homework will require multi-table joins
- They'll need LEFT JOIN for unmatched rows
- CTEs will make complex homework queries manageable

**To Day 3:**
- JSON normalization will CREATE the tables they're now joining
- Understanding table relationships is critical for normalization decisions

**To Rest of Program:**
- Joins are foundational for ALL future data work
- Every analytics project involves connecting data sources
- This skill transfers to any SQL database (Postgres, BigQuery, Snowflake)

---

## Instructor Reminders

**Before Class:**
- [ ] Test teaching notebook end-to-end (fresh kernel, Run All)
- [ ] Verify data files load correctly
- [ ] Check projector font size (readable from back?)
- [ ] Have exercise notebook ready to share
- [ ] Ensure solution is encrypted (check `solutions/` directory)

**During Class:**
- [ ] Start with energy - set the tone
- [ ] Run EVERY query (don't just show code)
- [ ] Point out business insights in results
- [ ] Take questions during break point
- [ ] Give students full 25 minutes for exercise
- [ ] Circulate actively during work time

**After Class:**
- [ ] Note timing (did you run over? which sections?)
- [ ] Note student questions (improve materials for next year)
- [ ] Identify students who struggled (offer office hours)
- [ ] Prepare for next block (JSON/API)

**Philosophy:**
> "You're teaching them to think relationally. The SQL syntax is just the tool. Focus on the concepts: how data connects, why join types matter, what business questions require multi-table analysis."

---

## Additional Teaching Tips

**For the anti-join pattern:**
- This is often an "aha!" moment for students
- Emphasize: "You'll use this ALL THE TIME in real work"
- Example framing: "Customers who haven't bought in 90 days", "Products with no sales", "Employees with no training records"

**For duplicate inflation:**
- Use strong visual language: "Your rows EXPLODED - why?"
- Show the specific example with multi-item order
- This mistake can cause serious business errors (over-counting revenue!)

**For CTEs:**
- Compare to Excel: "Like creating named ranges"
- Or cooking: "Like a recipe with steps"
- Students often love CTEs because they make queries readable

**For the grand finale:**
- This should feel like a big reveal: "Look what you can do now!"
- Point out: "This query would be VERY hard without CTEs and window functions"
- Connect back to Day 1: "Yesterday's window functions + today's joins = powerful analytics"

---

## Troubleshooting

**If DuckDB won't connect:**
- Check Python version (need 3.7+)
- Try re-running `uv sync` from the repo root
- Worst case: use pandas only (less elegant but works)

**If data files won't load:**
- Check working directory: should be repo root
- Verify relative paths: `../data/day2/block_a/...`
- Check file exists: `ls data/day2/block_a/`

**If students can't access exercise:**
- Share via Moodle (already done)
- Have USB backup
- Can display on screen and they can recreate

**If projector fails:**
- Have PDF backup of teaching notebook
- Can walk through concepts on whiteboard
- Students still have exercise to work through

---

## Success Metrics

**This session is successful if:**
- ✅ Students can explain when to use INNER vs LEFT JOIN
- ✅ Students recognize the anti-join pattern (LEFT + IS NULL)
- ✅ Students understand duplicate inflation danger
- ✅ Students complete at least 2 of 3 in-class queries
- ✅ Students connect concepts to business problems

**Red flags:**
- ❌ More than 50% of students can't finish Query 1
- ❌ No questions during break point (probably confused, not understanding)
- ❌ Students asking "Why do we need joins?" (missed the business framing)

---

**Good luck! You're teaching one of the most important skills in data analytics. Make it count!** 🎯
