# Day 2, Block B: Backup Data

This directory contains **backup JSON files** fetched from the DummyJSON API.

## ⚠️ Important: Teaching Data Source

**Day 2 teaching notebooks use:**
1. **PRIMARY:** Live API calls to `https://dummyjson.com/products?limit=30`
2. **BACKUP:** `products_backup.json` (30 products) - emergency fallback only

**This directory does NOT contain data for homework assignments.** Homework datasets are located in `assignments/hwN/data/` folders.

## Purpose

These files serve as **emergency fallback data** for teaching notebooks if the live DummyJSON API is unavailable during class.

## Files

### `products_backup.json`

**Source:** https://dummyjson.com/products?limit=30
**Fetched:** October 2025
**Records:** 30 products
**Size:** ~46 KB

Contains e-commerce product data including:
- Product details (id, title, description, price, category, brand)
- Nested dimensions object (width, height, depth)
- Reviews array (one-to-many relationship)
- Tags array (product categories)
- Stock and availability information

## Usage in Teaching Notebooks

**Normal operation (live API):**
```python
# OPTION 1: Use live API (DEFAULT)
import requests
response = requests.get("https://dummyjson.com/products", params={'limit': 30})
products_data = response.json()
```

**Fallback (if API is down):**
```python
# OPTION 2: Use backup file (if API is down)
import json
with open('../../data/day2/block_b/products_backup.json') as f:
    products_data = json.load(f)
```

**Instructor:** Simply comment/uncomment the appropriate cell at the top of the notebook.

## When to Update

Update these backup files if:
- DummyJSON API structure changes significantly
- Teaching content needs different data
- Current backup data becomes outdated

**To update:**
```bash
python3 -c "
import requests
import json

response = requests.get('https://dummyjson.com/products', params={'limit': 30})
with open('data/day2/block_b/products_backup.json', 'w') as f:
    json.dump(response.json(), f, indent=2)
"
```

## License

Data sourced from [DummyJSON](https://dummyjson.com/), a free fake REST API for testing and prototyping.
