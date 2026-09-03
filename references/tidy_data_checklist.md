# Tidy Data Quick Reference Card

**ECBS5294 - Data Science 2: Working with Data**

---

## The Three Rules of Tidy Data

A dataset is **tidy** if:

1. ✅ **Each variable is a column**
2. ✅ **Each observation is a row**
3. ✅ **Each value is a cell**

> "Tidy datasets are all alike, but every messy dataset is messy in its own way." – Hadley Wickham

---

## Five Common Problems (and Solutions)

| Problem | Example | Solution |
|---------|---------|----------|
| **1. Column headers are values** | Columns: `2021`, `2022`, `2023` | Make `year` a variable with values 2021, 2022, 2023 |
| **2. Multiple variables in one column** | Column: `male_under_18` | Split into `gender` and `age_group` columns |
| **3. Variables in rows AND columns** | Matrix/pivot table layout | Reshape (use `melt` + `pivot`) |
| **4. Multiple observational units in one table** | Customer info repeated on every transaction | Split into `customers` and `transactions` tables |
| **5. Single unit across multiple tables** | `sales_jan.csv`, `sales_feb.csv` | Combine into one table with `month` column |

---

## Primary Key Checklist

A valid primary key must be:

- ✅ **Unique** - No duplicate values
- ✅ **Non-null** - Every row has a value
- ✅ **Stable** - Doesn't change over time
- ✅ **Single-purpose** - Identifies, doesn't describe

### Validation Code

```python
# Check primary key validity
assert df['transaction_id'].is_unique, "Duplicate IDs found"
assert df['transaction_id'].notna().all(), "NULL IDs found"
```

### Types of Keys

- **Natural key:** Inherent to entity (email, ISBN, SSN)
- **Surrogate key:** Made up (customer_id: 1, 2, 3...)
- **Composite key:** Multiple columns (store_id + date)

---

## Type Conversion Patterns

### Dates

```python
# Always parse explicitly
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Handle mixed formats (requires manual inspection first)
df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True, errors='coerce')
```

### Numbers Stored as Strings

```python
# Remove currency symbols and commas
df['price'] = df['price'].str.replace('$', '', regex=False)
df['price'] = df['price'].str.replace(',', '', regex=False)
df['price'] = df['price'].astype(float)

# Or in one step with regex
df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float)
```

### Booleans

```python
# Map various representations to True/False
df['is_active'] = df['is_active'].map({
    'Yes': True, 'Y': True, '1': True, 1: True,
    'No': False, 'N': False, '0': False, 0: False
})
```

---

## Missing Value Handling

### Common Representations

| Representation | pandas detects as missing? |
|---------------|---------------------------|
| `NaN`, `None` | ✅ Yes |
| Empty string `""` | ❌ No |
| `"N/A"`, `"Unknown"` | ❌ No |
| `-999`, `-1` | ❌ No |
| `"ERROR"` | ❌ No |

### Standardize to NULL

```python
# Replace sentinel values with NaN
df = df.replace(['N/A', 'Unknown', 'ERROR', '', -999], np.nan)
```

### Handling Strategies

```python
# 1. Drop rows with missing values
df_clean = df.dropna(subset=['important_column'])

# 2. Drop columns with too many missing
df_clean = df.dropna(axis=1, thresh=len(df)*0.5)  # Keep if >50% non-null

# 3. Fill with default
df['payment_method'] = df['payment_method'].fillna('Unknown')

# 4. Fill with statistic
df['age'] = df['age'].fillna(df['age'].median())

# 5. Leave as NULL (affects aggregations!)
# COUNT excludes NULLs
# SUM, AVG, etc. exclude NULLs
```

### Impact on Aggregations

```python
# NULL is excluded from aggregations
[10, 20, NULL].mean()  # → 15
[10, 20, 0].mean()     # → 10

# Be aware!
df['amount'].sum()     # Excludes NULLs
df['amount'].count()   # Counts non-NULL values
len(df)                # Counts all rows
```

---

## Data Cleaning Workflow

### 1. Load and Explore

```python
import pandas as pd
import numpy as np

df = pd.read_csv('data/dataset.csv')

# Initial exploration
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.info())
print(df.describe())
```

### 2. Check for Messiness

```python
# Check for missing values
print(df.isnull().sum())

# Check for sentinel values
for col in df.select_dtypes(include='object').columns:
    print(f"{col}: {df[col].unique()}")

# Check for type issues
print(df.dtypes)  # Everything should have proper type
```

### 3. Identify Primary Key

```python
# Look for unique identifier
potential_keys = ['id', 'transaction_id', 'customer_id']
for col in potential_keys:
    if col in df.columns:
        print(f"{col}: {df[col].nunique()} unique, {len(df)} rows")
        print(f"  Unique? {df[col].is_unique}")
```

### 4. Clean Types

```python
# Dates
df['date'] = pd.to_datetime(df['date'])

# Numbers
df['price'] = df['price'].str.replace('[\$,]', '', regex=True).astype(float)

# Categories
df['category'] = df['category'].astype('category')
```

### 5. Handle Missing Values

```python
# Standardize
df = df.replace(['N/A', 'Unknown', 'ERROR', ''], np.nan)

# Handle based on column meaning
df['required_field'] = df['required_field'].dropna()  # or assert .notna().all()
df['optional_field'] = df['optional_field'].fillna('Not provided')
```

### 6. Validate

```python
# Primary key
assert df['id'].is_unique
assert df['id'].notna().all()

# Required fields
assert df['transaction_date'].notna().all()

# Data integrity
assert (df['quantity'] > 0).all()
assert (df['price'] >= 0).all()

# Calculated fields
# assert (df['total'] == df['quantity'] * df['price']).all()  # May need tolerance
```

### 7. Document

```markdown
## Data Cleaning Log

### Issues Found
1. 2,579 missing payment methods (25.8% of data)
2. 164 rows with "ERROR" in total_spent
3. Dates in mixed formats

### Actions Taken
1. Converted all sentinel values to NaN
2. Parsed dates to datetime
3. Removed $ and , from prices, converted to float

### Assumptions
- "Unknown" payment method treated as missing (excluded from analysis)
- Negative prices indicate refunds (kept as-is)
```

---

## Common pandas Functions

```python
# Reshaping
df.melt(id_vars=['key'], var_name='variable', value_name='value')
df.pivot(index='row', columns='col', values='value')

# Combining
pd.concat([df1, df2], ignore_index=True)
df.merge(other, on='key', how='inner')  # 'left', 'right', 'outer'

# Cleaning
df.drop(columns=['col1', 'col2'])
df.drop_duplicates(subset=['id'])
df.dropna(subset=['important'])
df.fillna(value)
df.replace(old, new)

# Type conversion
df['col'].astype('int64')
pd.to_datetime(df['col'])
df['col'].astype('category')

# String operations
df['col'].str.upper()
df['col'].str.strip()
df['col'].str.replace(pattern, replacement)
df['col'].str.split(delimiter, expand=True)
```

---

## Decision Framework

### Is my data tidy?

Ask yourself:
1. What is my unit of observation?
2. Is each observation a row?
3. Is each measurement/attribute a column?

If unsure → Think about what question you need to answer, and work backwards.

### How should I handle missing values?

Ask yourself:
1. What does "missing" mean for this column?
   - Not applicable?
   - Unknown?
   - Not collected yet?
2. How does it affect my analysis?
3. What would stakeholders expect?

Document your choice!

### What should be my primary key?

Ask yourself:
1. What uniquely identifies each observation?
2. Is it stable over time?
3. Could there be duplicates (data quality issue)?
4. Do I need to create a surrogate key?

Validate with assertions!

---

## Remember

✅ **Tidy data makes analysis easier**
✅ **Validate your primary key**
✅ **Handle types correctly**
✅ **Standardize missing values**
✅ **Document your choices**
✅ **Use assertions to prove data quality**

> "When you're defining the data, you're defining the nouns and verbs the business will use."

---

**More resources:**
- Hadley Wickham's "Tidy Data" paper: `references/papers/tidy_data_summary.md`
- Teaching notebook: `notebooks/day1/day1_block_a_tidy_foundations.ipynb`
- Exercise dataset: `data/day1/dirty_cafe_sales.csv`
