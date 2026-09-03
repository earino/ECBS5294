# HW3 Data Pack: Multi-City Business & Permitting Data

**Course:** ECBS5294 - Data Science 2: Working with Data
**Assignment:** Homework 3 - End-to-End Data Integration Project
**Data Sources:** Chicago Data Portal + NYC Open Data

---

## 📋 Overview

This data pack contains **real government data** from two major US cities' open data portals. Your mission: integrate these datasets into a unified analytical database to understand business licensing and permitting patterns across jurisdictions.

**Total Records:** ~70,000 records across 2 datasets
**Formats:** CSV + JSON (demonstrating multi-format integration)
**Time Period:** Chicago: predominantly 2020s. NYC: bulk of filings in the 2020s with a legitimate tail back to 1989 — and at least one obviously erroneous future date (a `job_start_date` in the year 2222). Profile before you assert!
**Use Case:** Policy analysis, regulatory compliance, business intelligence

---

## 📊 Dataset 1: Chicago Business Licenses

**Source:** City of Chicago Data Portal
**URL:** https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr
**File:** `chicago_business_licenses.csv`
**License:** Public Domain (U.S. Government Work)
**Format:** CSV
**Records:** 50,000 business licenses

### Description

Business licenses issued by the Chicago Department of Business Affairs and Consumer Protection. This dataset contains all types of business licenses from various industries operating in Chicago.

### Key Columns

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Unique record identifier |
| `license_id` | Integer | License identifier (may have multiple records per license) |
| `account_number` | Integer | Business account number |
| `legal_name` | String | Legal name of business |
| `doing_business_as_name` | String | DBA (doing business as) name |
| `address` | String | Business address |
| `city` | String | City (mostly Chicago) |
| `state` | String | State (mostly IL) |
| `zip_code` | String | ZIP code |
| `ward` | Integer | Chicago ward number |
| `license_code` | Integer | License type code |
| `license_description` | String | Description of license type |
| `business_activity` | String | Type of business activity |
| `application_type` | String | ISSUE, RENEW, C_LOC (change location), C_CAPA (change capacity) |
| `application_created_date` | Datetime | When application was created |
| `payment_date` | Datetime | When license fee was paid |
| `license_start_date` | Datetime | License effective date |
| `expiration_date` | Datetime | License expiration date |
| `license_status` | String | Current license status (AAC=active, REV=revoked, etc.) |
| `latitude` | Float | Latitude coordinate |
| `longitude` | Float | Longitude coordinate |

### Data Quality Notes

**Natural Messiness (Real-World Data):**
- **Missing values:** Some addresses incomplete, lat/lon occasionally null
- **Date formats:** Mostly consistent ISO 8601, but check for edge cases
- **Status changes:** Some licenses have multiple records (renewals, relocations)
- **ZIP codes:** Stored as strings (may have leading zeros)

**Expected Issues:**
- Some businesses have multiple licenses (same business, different activities)
- Application type codes require understanding (ISSUE vs RENEW vs C_LOC)
- License status changes tracked via `license_status_change_date`
- Not all licenses have payment dates (some grandfathered/exempt)

---

## 📊 Dataset 2: NYC DOB Permit Issuance

**Source:** NYC Open Data
**URL:** https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a
**File:** `nyc_building_permits.json`
**License:** Public Domain (U.S. Government Work)
**Format:** JSON (nested structure)
**Records:** 20,000 building permits

### Description

Department of Buildings (DOB) permit issuance records for construction, renovation, and demolition activities in New York City. Each record represents the lifecycle of one permit.

### JSON Structure

```json
[
  {
    "borough": "MANHATTAN",
    "bin__": "1001831",
    "house__": "123",
    "street_name": "MAIN ST",
    "job__": "123456789",
    "job_doc___": "01",
    "job_type": "A1",
    "block": "1234",
    "lot": "1",
    "community_board": "101",
    "zip_code": "10001",
    "bldg_type": "1",
    "issuance_date": "2024-01-15T00:00:00.000",
    "expiration_date": "2025-01-15T00:00:00.000",
    "filing_date": "2023-12-01T00:00:00.000",
    "job_start_date": "2024-01-20T00:00:00.000",
    "permit_status": "ISSUED",
    "filing_status": "RENEWAL",
    "permit_type": "NB",
    "permit_sequence__": "01",
    "owner_s_business_name": "ACME PROPERTIES LLC",
    "owner_s_first_name": "JOHN",
    "owner_s_last_name": "DOE",
    "owner_s_house__": "456",
    "owner_s_house_street_name": "ELM ST",
    "owner_s_zip_code": "10002",
    "superintendent_business_name": "BUILD IT RIGHT INC",
    "gis_latitude": "40.7589",
    "gis_longitude": "-73.9851",
    ...
  }
]
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `borough` | String | NYC borough (MANHATTAN, BROOKLYN, QUEENS, BRONX, STATEN ISLAND) |
| `bin__` | String | Building Identification Number |
| `house__` | String | House number |
| `street_name` | String | Street name |
| `permit_si_no` | String | Permit sequence ID — the UNIQUE identifier of each permit row [PK] |
| `job__` | String | Job number — NOT unique: one job can have many permits (see `permit_si_no` for the unique per-permit key) |
| `job_type` | String | Type of work (A1=major alteration, NB=new building, etc.) |
| `block` | String | Tax block |
| `lot` | String | Tax lot |
| `zip_code` | String | ZIP code |
| `issuance_date` | Datetime | When permit was issued |
| `expiration_date` | Datetime | When permit expires |
| `filing_date` | Datetime | When application was filed |
| `permit_status` | String | Current status (ISSUED, EXPIRED, etc.) |
| `permit_type` | String | Type of permit |
| `owner_s_business_name` | String | Property owner business name |
| `owner_s_first_name` | String | Property owner first name |
| `owner_s_last_name` | String | Property owner last name |
| `gis_latitude` | String | Latitude (as string!) |
| `gis_longitude` | String | Longitude (as string!) |

### Data Quality Notes

**Natural Messiness (Real-World Data):**
- **JSON structure:** Flat structure (no nested objects), but many optional fields
- **Type inconsistencies:** Lat/lon stored as strings, not floats
- **Missing values:** Owner info, geo coordinates often missing
- **Field naming:** Trailing underscores (`bin__`, `house__`, `job__`) from database export
- **Date formats:** ISO 8601 strings, need conversion to datetime

**Expected Issues:**
- Some permits missing geo coordinates
- Owner names split across multiple fields (business name vs person name)
- Permit types require code lookup (A1, NB, DM, etc.)
- Multiple permits per job (one job can have multiple permit types)

---

## 🎯 Integration Challenges

Your HW3 task is to handle these **realistic integration scenarios**:

### 1. Multi-Format Sources
- Chicago: CSV (rectangular, easy to load)
- NYC: JSON (needs parsing, type conversion)

### 2. Different Schemas
- Chicago: Business licenses (ongoing operations)
- NYC: Building permits (time-limited projects)
- No direct relationship, but can analyze by geography

### 3. Real-World Data Quality
- **Missing values:** Both datasets have nulls in various fields
- **Type issues:** Numbers as strings, dates as strings
- **Inconsistent naming:** Different conventions (snake_case vs mixed)
- **Duplicate handling:** Chicago has renewal records, NYC has multi-permit jobs

### 4. Geographic Analysis
- Both have lat/lon (but NYC stores as strings!)
- Both have ZIP codes (but formatting differs)
- Opportunity for cross-city comparisons

---

## 💡 Analysis Opportunities

### Business Questions You Can Answer:

**Chicago Focus:**
- Which wards have the most business licenses?
- What are the most common business types?
- How long do businesses typically hold licenses before renewal?
- Which license types have the highest revocation rates?

**NYC Focus:**
- Which boroughs have the most construction activity?
- What's the average time from filing to issuance?
- How many permits expire unused?
- Which job types take longest to get approved?

**Cross-City:**
- Business activity density (licenses/permits per capita by area)
- Geographic distribution patterns
- Regulatory timeline comparisons (if you normalize concepts)

---

## 📚 Attribution & License

### Chicago Business Licenses
**Source:** City of Chicago Data Portal
**Publisher:** Chicago Department of Business Affairs and Consumer Protection
**URL:** https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr
**License:** Public Domain - U.S. Government Work
**Attribution:** "Business Licenses dataset from City of Chicago Data Portal (data.cityofchicago.org), accessed October 2025."

**Terms of Use:** This data is in the public domain and made available without restrictions. No attribution legally required, but appreciated for academic integrity.

### NYC DOB Permit Issuance
**Source:** NYC Open Data
**Publisher:** NYC Department of Buildings
**URL:** https://data.cityofnewyork.us/Housing-Development/DOB-Permit-Issuance/ipu4-2q9a
**License:** Public Domain - U.S. Government Work
**Attribution:** "DOB Permit Issuance dataset from NYC Open Data (data.cityofnewyork.us), accessed October 2025."

**Terms of Use:** This data is in the public domain and made available without restrictions. NYC encourages use and republication of public data.

---

## 🔍 Getting Started

### Load Chicago Data (CSV)
```python
import pandas as pd
import duckdb

# Pandas
chicago = pd.read_csv('data/day3/hw3_data_pack/chicago_business_licenses.csv')

# DuckDB
con = duckdb.connect(':memory:')
con.execute("CREATE TABLE chicago_licenses AS SELECT * FROM 'data/day3/hw3_data_pack/chicago_business_licenses.csv'")
```

### Load NYC Data (JSON)
```python
import json

# Load JSON
with open('data/day3/hw3_data_pack/nyc_building_permits.json', 'r') as f:
    nyc_data = json.load(f)

# Convert to DataFrame
nyc = pd.DataFrame(nyc_data)

# Load to DuckDB
con.execute("CREATE TABLE nyc_permits AS SELECT * FROM nyc")
```

---

## ⚠️ Important Notes

### What This Data Is
- ✅ Real government data from official sources
- ✅ Authentic messiness (natural data quality issues)
- ✅ Suitable for learning data integration skills
- ✅ Public domain (no usage restrictions)

### What This Data Is NOT
- ❌ Not complete (we've subsetted to 50K+20K records)
- ❌ Not current (snapshot from time of download)
- ❌ Not guaranteed accurate (use for learning, not policy decisions)
- ❌ Not synthetic (these are real businesses and permits)

### Ethical Use
- This data contains information about real businesses and properties
- Use for educational purposes only
- Do not republish personally identifiable information
- Do not use for commercial purposes without verifying current licensing

---

## 📖 Learning Objectives

By working with this data pack, you will practice:
1. **Multi-format ingestion** (CSV + JSON)
2. **Real-world data quality** (missing values, type issues)
3. **Schema understanding** (interpreting unfamiliar column names)
4. **Type conversion** (strings to dates, strings to numbers)
5. **Data validation** (checking for expected issues)
6. **Cross-dataset analysis** (even without direct joins)
7. **Documentation** (explaining what you found and can't find)
8. **Stakeholder communication** (translating technical findings)

---

## 🆘 Common Issues

**"Too many columns! I'm overwhelmed"**
- You don't need to use all columns
- Focus on key fields for your analysis
- Document which columns you excluded and why

**"Missing values everywhere"**
- This is normal for government data
- Document your strategy (drop? fill? flag?)
- Explain how it affects your analysis

**"Can't join Chicago and NYC"**
- Correct! No direct relationship
- Analyze each separately, then compare findings
- Or get creative: geographic analysis by ZIP/coordinates

**"JSON won't load properly"**
- Use `json.load()`, not `pd.read_json()` initially
- Inspect structure first: `print(data[0].keys())`
- Then convert to DataFrame: `pd.DataFrame(data)`

---

**Ready to integrate? Good luck! 🚀**
