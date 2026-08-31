# HW2 Instructor Grading Notes

**Assignment:** Homework 2 - TechMart QuickBuy Acquisition
**Total Points:** 100
**New Focus:** Stakeholder Communication (added ~12 communication points)

---

## 📊 Updated Point Distribution

### Original Technical Points (85 points)
- Part 1: Data Ingestion & Exploration (15 points)
- Part 2: Data Normalization (35 points)
- Part 3: Data Validation (20 points)
- Part 4: Database Persistence (10 points)
- Part 5: SQL Analysis (15 points - technical queries only)
- Part 6: Data Dictionary (5 points)

### New Communication Points (15 points)
- Part 1: Initial Assessment (2 points)
- Part 2: Normalization Summary (2 points)
- Part 3: Data Quality Report (2 points)
- Part 4: Technical Handoff (2 points)
- Part 5.1: Category Strategy (1.5 points)
- Part 5.2: Marketing Strategy (1.5 points)
- Part 5.3: Product Development (1.5 points)
- Part 5.4: Integration Timing (1.5 points)
- Executive Summary (2 points)

**Note:** Adjust technical points slightly if needed to maintain 100 total.

---

## 🎯 Grading Rubric for Communication Sections

### A-Level Communication (90-100% of points)

**Characteristics:**
- **Specific metrics** (not "good" but "4.2 average rating")
- **Actionable recommendations** (what to do, not just observations)
- **Appropriate audience focus** (CEO gets strategy, not SQL details)
- **Business value quantified** ($800K savings, 35% margin improvement)
- **Comparison/context** provided (vs. other acquisitions, benchmarks)
- **Clear next steps** stated
- **Unexpected insights** highlighted
- **Professional tone** throughout

**Example snippet:**
"QuickBuy's data quality exceeds expectations with 100% field completeness, significantly outperforming our SpringCo acquisition (12% missing). Recommend accelerating integration by 2 weeks to capture Q4 sales."

### B-Level Communication (80-89% of points)

**Characteristics:**
- Good insights but less specific numbers
- Some recommendations but not always actionable
- Generally appropriate for audience
- Some business context
- Professional writing
- Main concerns addressed

**Example snippet:**
"The data quality is very good with no major issues found. We should proceed with integration soon to take advantage of the holiday season."

### C-Level Communication (70-79% of points)

**Characteristics:**
- Basic observations without depth
- Few specific numbers
- Generic recommendations
- May miss audience needs
- Adequate writing
- Some stakeholder concerns unaddressed

**Example snippet:**
"Data has been processed successfully. Quality checks passed. Ready for next steps."

### Below C (<70% of points)

**Characteristics:**
- Vague or missing communications
- No actionable recommendations
- Wrong audience focus (technical details to CEO)
- Poor writing or formatting
- Misses business context entirely
- Copy-paste generic responses

**Example snippet:**
"Data is fine. No problems."

---

## 📝 Specific Grading Guidelines by Section

### Part 1: Initial Assessment (2 points)

**Look for:**
- Quantification of data scope (194 products, 710 reviews)
- Quality assessment (missing values, completeness)
- Effort estimation for normalization
- Comparison to other data sources
- Clear recommendation (proceed/delay/investigate)

**Deductions:**
- -0.5: No specific numbers
- -0.5: No effort estimation
- -0.5: No clear recommendation
- -0.5: Inappropriate technical depth

### Part 2: Normalization Summary (2 points)

**Look for:**
- Confirmation of table creation with row counts
- Schema compatibility mention (Tableau, existing systems)
- Technical notes relevant to BI team
- Foreign key relationship confirmation

**Deductions:**
- -0.5: Missing row/column counts
- -0.5: No mention of compatibility
- -0.5: No relationship verification
- -0.5: Too technical or too vague

### Part 3: Data Quality Report (2 points)

**Look for:**
- Specific quality metrics (% complete, duplicates, orphans)
- Risk assessment (minimal/moderate/high)
- Comparison to other acquisitions or benchmarks
- Monitoring recommendations

**Deductions:**
- -0.5: No specific metrics
- -0.5: Missing risk assessment
- -0.5: No comparisons
- -0.5: No forward-looking recommendations

### Part 4: Technical Handoff (2 points)

**Look for:**
- Schema pattern description
- Performance considerations
- Technical specifications (data types, indexes)
- Integration readiness statement

**Deductions:**
- -0.5: Missing technical specs
- -0.5: No performance mention
- -0.5: Unclear handoff point
- -0.5: Wrong audience (too business-focused)

### Part 5: SQL Analysis Communications (6 points total)

**Each subsection (1.5 points) should include:**
- Key finding from the query
- Business interpretation
- Specific recommendation
- Relevant metrics

**Common deductions per subsection:**
- -0.5: Just restating query results
- -0.5: No actionable recommendation
- -0.5: Missing business impact

### Executive Summary (2 points)

**Must include:**
- Total scope quantified
- Key insight highlighted
- Primary recommendation
- Risk assessment
- Timeline suggestion
- ROI or value statement

**Deductions:**
- -0.5: Too short (less than 4 sentences)
- -0.5: No quantification
- -0.5: Missing recommendations
- -0.5: No business value stated

---

## 🚨 Common Issues to Watch For

### 1. **Generic Copy-Paste Responses**
Students might use the same template for all communications. Look for:
- Identical structure across all sections
- No specific references to the analysis
- Generic business language without data

**Grading:** Maximum C-level if detected

### 2. **Wrong Audience Focus**
- Giving CEOs SQL details
- Giving engineers business strategy
- Not adapting tone/content

**Grading:** -0.5 points per occurrence

### 3. **No Quantification**
Using vague terms like "many," "several," "good," "bad" instead of specific numbers.

**Grading:** -0.5 points per section

### 4. **Missing Business Context**
Pure technical reporting without business implications.

**Grading:** -0.5 to -1 point depending on severity

### 5. **No Actionable Recommendations**
Just describing what they found without saying what to do about it.

**Grading:** -0.5 points per section

---

## 📈 Quick Grading Checklist

For each communication section, ask:

- [ ] **Specific?** Are there numbers, not generalizations?
- [ ] **Actionable?** Is there a clear next step?
- [ ] **Appropriate?** Is it written for the right audience?
- [ ] **Valuable?** Does it add business insight?
- [ ] **Professional?** Is it well-written and clear?

**Scoring guide:**
- 5/5 checks = A-level (90-100%)
- 4/5 checks = B-level (80-89%)
- 3/5 checks = C-level (70-79%)
- <3 checks = Below C

---

## 💡 Positive Feedback Examples

When students excel, acknowledge:

**Great specificity:**
"Excellent use of specific metrics (100% completeness, $800K savings) - this builds stakeholder confidence."

**Strong audience adaptation:**
"Perfect audience focus - your CEO summary focuses on strategy while your engineering brief provides technical specs."

**Valuable insights:**
"Great unexpected insight about furniture engagement - this kind of finding drives real business value."

**Clear recommendations:**
"Your recommendation to accelerate by 2 weeks with specific reasoning shows strong business judgment."

---

## 📝 Constructive Feedback Examples

When improvements needed:

**Too vague:**
"Your assessment mentions 'good quality' - quantify this. How many missing values? What % complete? Specifics build credibility."

**Wrong audience:**
"Your CEO brief includes SQL details they won't care about. Focus on strategic implications instead."

**No action:**
"You've identified that vehicle category underperforms, but what should we DO about it? Add a specific recommendation."

**Missing context:**
"You state '710 reviews' - is this good or bad? State the evidence base (time span, per-product spread) rather than inventing a benchmark."

---

## 🎯 Grade Distribution Guidance

Based on communication quality:

### A/A- (15-20% of class)
- All communications present and excellent
- Strong technical work
- Clear business value demonstrated
- Professional throughout

### B+/B (40-50% of class)
- Most communications good
- Solid technical work
- Some business insights
- Generally professional

### B-/C+ (25-35% of class)
- Communications present but basic
- Technical work acceptable
- Limited business insight
- Some professionalism issues

### C or below (5-10% of class)
- Missing communications
- Weak technical work
- No business context
- Poor presentation

---

## 📊 Sample Grading Sheet

```
Student: ________________
Technical (85 pts): ______
Communications (15 pts):
  - Initial Assessment (2): ___
  - Normalization (2): ___
  - Quality Report (2): ___
  - Technical Handoff (2): ___
  - Category Strategy (1.5): ___
  - Marketing (1.5): ___
  - Product Dev (1.5): ___
  - Timing (1.5): ___
  - Executive Summary (2): ___
Total: ___/100

Comments:
- Strengths:
- Improvements needed:
- Overall impression:
```

---

## 🔑 Key Takeaway for Grading

The new communication requirements transform this from a technical exercise into a professional data analyst simulation. Students who excel will:

1. Complete the technical work correctly
2. Communicate findings appropriately for each audience
3. Provide actionable business recommendations
4. Demonstrate they understand the business context

This better prepares them for real-world analyst roles where communication is as important as technical skills.

---

## 📚 Resources for Students

Point struggling students to:
- `HW2_Communication_Excellence_Guide.md`
- The complete solution (after deadline)
- Office hours for communication coaching
- Peer review exercises

Remember: We're teaching them to be analysts who can influence business decisions, not just process data.

---

**Note:** Consider sharing the Communication Excellence Guide with students BEFORE the assignment (minus the specific HW2 examples) to set expectations clearly.