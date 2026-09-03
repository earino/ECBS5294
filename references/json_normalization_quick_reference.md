# JSON Normalization Quick Reference Card

**ECBS5294 - Data Science 2: Working with Data**
**Day 2, Block B**

---

## JSON Structure Fundamentals

### Basic Types

```json
{
  "string": "Hello",
  "number": 42,
  "boolean": true,
  "null": null,
  "array": [1, 2, 3],
  "object": {"nested": "value"}
}
```

### Common Patterns

**Simple Object (one product):**
```json
{
  "id": 1,
  "name": "Widget",
  "price": 29.99,
  "in_stock": true
}
```

**Array of Objects (multiple products):**
```json
[
  {"id": 1, "name": "Widget", "price": 29.99},
  {"id": 2, "name": "Gadget", "price": 49.99}
]
```

**Nested Object (one-to-one relationship):**
```json
{
  "product": "Widget",
  "supplier": {
    "name": "ACME Corp",
    "country": "USA"
  }
}
```

**Nested Array (one-to-many relationship):**
```json
{
  "product": "Widget",
  "reviews": [
    {"rating": 5, "comment": "Great!"},
    {"rating": 4, "comment": "Good"}
  ]
}
```

---

## Python Navigation Patterns

### Accessing Simple Values

```python
import json

# Load JSON from file
with open('data/products.json') as f:
    data = json.load(f)

# Access by key
product_name = data['name']
price = data['price']

# Access nested object
supplier_name = data['supplier']['name']
city = data['supplier']['address']['city']
```

### Accessing Arrays

```python
# First item in array
first_product = data['products'][0]
first_product_name = data['products'][0]['name']

# Loop through array
for product in data['products']:
    print(product['name'], product['price'])

# List comprehension
names = [p['name'] for p in data['products']]
```

### Safe Access (Avoiding KeyError)

```python
# ❌ WRONG: Crashes if key doesn't exist
price = data['price']  # KeyError if missing!

# ✅ CORRECT: Use .get() with default
price = data.get('price', 0.0)

# ✅ CORRECT: Check if key exists
if 'price' in data:
    price = data['price']
else:
    price = 0.0

# Nested safe access
supplier_name = data.get('supplier', {}).get('name', 'Unknown')
```

### Checking Data Types

```python
# Check if value is a list
if isinstance(data['reviews'], list):
    print(f"Found {len(data['reviews'])} reviews")

# Check if key exists and is not None
if data.get('description') is not None:
    print(data['description'])
```

---

## Pandas Normalization Recipes

### Recipe 1: Simple JSON to DataFrame

**For: Array of flat objects**

```python
import pandas as pd

# Simple list of products
products = [
    {"id": 1, "name": "Widget", "price": 29.99},
    {"id": 2, "name": "Gadget", "price": 49.99}
]

# Convert to DataFrame
df = pd.DataFrame(products)
```

### Recipe 2: Flatten Nested Objects

**For: One-to-one relationships (nested objects)**

```python
import pandas as pd

# Products with nested supplier info
data = {
    "products": [
        {"id": 1, "name": "Widget", "supplier": {"name": "ACME", "country": "USA"}},
        {"id": 2, "name": "Gadget", "supplier": {"name": "TechCo", "country": "UK"}}
    ]
}

# Flatten nested objects
df = pd.json_normalize(data['products'])
# Result columns: id, name, supplier.name, supplier.country

# Rename flattened columns
df.columns = ['id', 'name', 'supplier_name', 'supplier_country']
```

**What pd.json_normalize() does:**
- Flattens nested objects into separate columns
- Uses dot notation for nested keys (`supplier.name`)
- Keeps array relationships intact (use with `record_path`)

### Recipe 3: Explode One-to-Many Arrays

**For: Simple arrays in a column**

```python
import pandas as pd

# Products with tags array
products = [
    {"id": 1, "name": "Widget", "tags": ["electronics", "sale"]},
    {"id": 2, "name": "Gadget", "tags": ["electronics"]}
]

df = pd.DataFrame(products)
# df has a 'tags' column with list values

# Explode array into separate rows
df_exploded = df.explode('tags')
# Result:
# id | name   | tags
# 1  | Widget | electronics
# 1  | Widget | sale
# 2  | Gadget | electronics
```

**Use .explode() when:**
- You have a column with list values
- You want one row per array item
- You're creating a many-to-many relationship table

### Recipe 4: Normalize Nested Arrays (Advanced)

**For: One-to-many relationships (nested arrays of objects)**

```python
import pandas as pd

# Products with nested reviews array
data = {
    "products": [
        {
            "id": 1,
            "name": "Widget",
            "reviews": [
                {"rating": 5, "comment": "Great!"},
                {"rating": 4, "comment": "Good"}
            ]
        },
        {
            "id": 2,
            "name": "Gadget",
            "reviews": [
                {"rating": 3, "comment": "OK"}
            ]
        }
    ]
}

# Normalize nested array into separate DataFrame
reviews_df = pd.json_normalize(
    data['products'],
    record_path='reviews',        # Path to array
    meta=['id', 'name']           # Include parent fields
)

# Result:
# id | name   | rating | comment
# 1  | Widget | 5      | Great!
# 1  | Widget | 4      | Good
# 2  | Gadget | 3      | OK
```

**Key parameters for json_normalize():**
- `record_path`: Path to the array you want to normalize
- `meta`: Parent fields to include in each row
- `meta_prefix`: Add prefix to meta columns (optional)

---

## DuckDB Integration Patterns

### Load DataFrame to DuckDB

```python
import duckdb
import pandas as pd

# Create connection
con = duckdb.connect('database.db')

# Load DataFrame to table
products_df = pd.DataFrame([...])
con.execute("CREATE TABLE products AS SELECT * FROM products_df")

# Verify it worked
con.execute("SELECT COUNT(*) FROM products").df()
```

### Common Patterns

```python
# Create table from DataFrame
con.execute("CREATE TABLE products AS SELECT * FROM products_df")

# Append to existing table
con.execute("INSERT INTO products SELECT * FROM new_products_df")

# Replace table
con.execute("DROP TABLE IF EXISTS products")
con.execute("CREATE TABLE products AS SELECT * FROM products_df")

# Query DataFrame directly (without creating table)
con.execute("SELECT * FROM products_df WHERE price > 50").df()
```

### Type Handling

```python
import pandas as pd

# Ensure correct types before loading
df['id'] = df['id'].astype(int)
df['price'] = df['price'].astype(float)
df['created_at'] = pd.to_datetime(df['created_at'])
df['in_stock'] = df['in_stock'].astype(bool)

# Load to DuckDB
con.execute("CREATE TABLE products AS SELECT * FROM df")
```

---

## Common Gotchas Checklist

### Before You Start

- [ ] **Inspect the JSON structure** - Use `json.load()` and print first item
- [ ] **Identify relationships** - What's one-to-one? What's one-to-many?
- [ ] **Plan your tables** - What tables will you create?
- [ ] **Check for missing keys** - Are all fields present in all records?

### While Parsing JSON

- [ ] **Use .get() for optional fields** - Avoid KeyError
  ```python
  # ❌ data['optional_field']
  # ✅ data.get('optional_field', 'default')
  ```

- [ ] **Check for None vs missing key**
  ```python
  if data.get('field') is not None:  # Field exists and not null
  if 'field' in data:                # Field exists (might be null)
  ```

- [ ] **Handle nested arrays carefully** - Use `json_normalize()` with `record_path`

- [ ] **Test with small sample first** - Don't process all 194 products immediately

### After Creating DataFrames

- [ ] **Check for duplicates** - Especially in ID columns
  ```python
  assert df['id'].is_unique, "Duplicate IDs found!"
  ```

- [ ] **Verify row counts** - Does math make sense?
  ```python
  print(f"Products: {len(products_df)}")
  print(f"Reviews: {len(reviews_df)}")
  ```

- [ ] **Check for NULL values** - Are they expected?
  ```python
  print(df.isnull().sum())
  ```

- [ ] **Verify data types** - Convert before loading to DuckDB
  ```python
  print(df.dtypes)
  ```

### Before Loading to DuckDB

- [ ] **Foreign keys exist** - Can you join back?
  ```python
  assert reviews_df['product_id'].isin(products_df['id']).all()
  ```

- [ ] **Column names are clean** - No spaces, special characters
  ```python
  df.columns = df.columns.str.replace(' ', '_').str.lower()
  ```

- [ ] **Types are correct** - Dates are dates, ints are ints

---

## Quick Troubleshooting

### "KeyError: 'field_name'"

**Problem:** Trying to access a key that doesn't exist

**Solution:** Use `.get()` with a default value
```python
# ❌ price = data['price']
# ✅ price = data.get('price', 0.0)
```

### "Can't join on column with list values"

**Problem:** Column contains arrays/lists

**Solution:** Use `.explode()` to create one row per item
```python
df_exploded = df.explode('tags')
```

### "More rows than expected after normalization"

**Problem:** One-to-many relationship created duplicate parent data

**Solution:** This is normal! Verify with counts:
```python
print(f"Products: {len(products_df)}")
print(f"Reviews: {len(reviews_df)}")
# Reviews should be >= Products
```

### "TypeError: Object of type 'X' is not JSON serializable"

**Problem:** Trying to write Python object to JSON

**Solution:** Convert to JSON-compatible types first
```python
# Convert dates
df['date'] = df['date'].astype(str)

# Convert numpy types
df['value'] = df['value'].astype(float)
```

### "Empty DataFrame / No data loaded"

**Problem:** Wrong path in `json_normalize()` or wrong key

**Solution:** Inspect JSON structure first
```python
print(data.keys())  # See top-level keys
print(type(data['products']))  # Verify it's a list
print(data['products'][0].keys())  # See fields
```

### "ValueError: If using all scalar values, must pass an index"

**Problem:** Trying to create DataFrame from single dict

**Solution:** Wrap in a list or specify index
```python
# ❌ df = pd.DataFrame({"a": 1, "b": 2})
# ✅ df = pd.DataFrame([{"a": 1, "b": 2}])
# ✅ df = pd.DataFrame({"a": 1, "b": 2}, index=[0])
```

---

## Common Normalization Patterns

### Pattern 1: Flat Product Catalog

**JSON:**
```json
[
  {"id": 1, "name": "Widget", "price": 29.99},
  {"id": 2, "name": "Gadget", "price": 49.99}
]
```

**Code:**
```python
products_df = pd.DataFrame(data)
con.execute("CREATE TABLE products AS SELECT * FROM products_df")
```

### Pattern 2: Products with Nested Supplier (One-to-One)

**JSON:**
```json
[
  {"id": 1, "name": "Widget", "supplier": {"name": "ACME", "country": "USA"}},
  ...
]
```

**Code:**
```python
# Option A: Flatten into products table
products_df = pd.json_normalize(data)
products_df.columns = ['id', 'name', 'supplier_name', 'supplier_country']

# Option B: Separate suppliers table (if many products per supplier)
products_df = pd.DataFrame([
    {"id": p['id'], "name": p['name'], "supplier_name": p['supplier']['name']}
    for p in data
])

suppliers_df = pd.json_normalize([p['supplier'] for p in data]).drop_duplicates()
```

### Pattern 3: Products with Reviews (One-to-Many)

**JSON:**
```json
[
  {
    "id": 1,
    "name": "Widget",
    "reviews": [
      {"rating": 5, "comment": "Great!"},
      {"rating": 4, "comment": "Good"}
    ]
  },
  ...
]
```

**Code:**
```python
# Products table (just product info)
products_df = pd.DataFrame([
    {"id": p['id'], "name": p['name']}
    for p in data
])

# Reviews table (normalized from nested array)
reviews_df = pd.json_normalize(
    data,
    record_path='reviews',
    meta=['id'],
    meta_prefix='product_'
)

# Load both tables
con.execute("CREATE TABLE products AS SELECT * FROM products_df")
con.execute("CREATE TABLE reviews AS SELECT * FROM reviews_df")

# Verify relationship
con.execute("""
    SELECT p.name, AVG(r.rating) AS avg_rating
    FROM products p
    LEFT JOIN reviews r ON p.id = r.product_id
    GROUP BY p.name
""").df()
```

### Pattern 4: Products with Tags (Many-to-Many)

**JSON:**
```json
[
  {"id": 1, "name": "Widget", "tags": ["electronics", "sale"]},
  {"id": 2, "name": "Gadget", "tags": ["electronics"]}
]
```

**Code:**
```python
# Products table
products_df = pd.DataFrame([
    {"id": p['id'], "name": p['name']}
    for p in data
])

# Product-tags junction table
df_with_tags = pd.DataFrame(data)
product_tags_df = df_with_tags[['id', 'tags']].explode('tags')
product_tags_df.columns = ['product_id', 'tag']

# Optional: Separate tags table
tags_df = pd.DataFrame({'tag': product_tags_df['tag'].unique()})

# Load all tables
con.execute("CREATE TABLE products AS SELECT * FROM products_df")
con.execute("CREATE TABLE product_tags AS SELECT * FROM product_tags_df")
con.execute("CREATE TABLE tags AS SELECT * FROM tags_df")
```

---

## Decision Framework

**Ask yourself:**

1. **What's the structure?**
   - Flat array of objects → Use `pd.DataFrame()`
   - Nested objects (one-to-one) → Use `json_normalize()`
   - Nested arrays (one-to-many) → Use `json_normalize()` with `record_path`

2. **How many tables do I need?**
   - One entity type → One table
   - Multiple entity types → Multiple tables
   - Many-to-many relationship → Junction table

3. **Are there optional fields?**
   - Yes → Use `.get()` with defaults
   - No → Direct access with `[]` is fine

4. **Do I need to preserve relationships?**
   - Yes → Include foreign keys (`product_id`, etc.)
   - No → Flatten everything into one wide table

---

## Best Practices

### DO

✅ **Inspect JSON structure first** - Print first item, understand nesting
✅ **Start with small sample** - Test on 5 records before processing all
✅ **Use .get() for optional fields** - Prevent KeyError
✅ **Verify row counts** - Ensure normalization worked correctly
✅ **Check for duplicates** - Especially in ID columns
✅ **Convert types before DuckDB** - Dates, booleans, integers
✅ **Add assertions** - Validate data quality with code
✅ **Document your schema** - What does each table represent?

### DON'T

❌ **Assume all records have same fields** - Use .get()
❌ **Forget foreign keys** - You need them to join tables
❌ **Skip type checking** - DuckDB needs correct types
❌ **Process all data at once** - Test on sample first
❌ **Ignore NULL values** - Check if they're expected
❌ **Use spaces in column names** - Use underscores
❌ **Skip validation** - Always verify your work

---

## Additional Resources

**Teaching Notebooks:**
- `notebooks/day2/day2_block_b_01_api_json_basics.ipynb` - JSON fundamentals and API calls
- `notebooks/day2/day2_block_b_02_json_to_duckdb.ipynb` - Complete normalization pipeline

**Data Documentation:**
- `data/day2/README.md` - Dataset descriptions and sources

**Related Quick References:**
- `sql_joins_quick_reference.md` - Joining your normalized tables
- `api_pipeline_quick_reference.md` - Production API patterns (advanced)

**Python Documentation:**
- Pandas json_normalize: https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html
- Python json module: https://docs.python.org/3/library/json.html
- DuckDB Python API: https://duckdb.org/docs/api/python/overview

---

**Remember:** JSON normalization is about transforming nested data into tidy relational tables. Focus on the relationships, verify your work, and you'll be fine!

**Good luck!**
