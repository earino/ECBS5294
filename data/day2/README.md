# Day 2 Datasets

This directory contains datasets used in Day 2 teaching materials.

---

## Block A: Brazilian E-Commerce (Olist)

**Source:** Kaggle - Brazilian E-Commerce Public Dataset by Olist  
**URL:** https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce  
**License:** CC BY-NC-SA 4.0  
**Used in:** Day 2 Block A (SQL Joins and Multi-Table Queries)

---

## Dataset Description

This is a **real-world Brazilian e-commerce dataset** containing 100,000 orders made at the Olist Store between 2016 and 2018. Olist is the largest department store marketplace in Brazil, connecting small businesses to customers through a single contract.

This dataset is perfect for teaching SQL joins because it contains **multiple interconnected tables** with clear primary key/foreign key relationships. Students will learn to combine data from customers, orders, products, sellers, payments, and reviews to answer business questions.

**Why this dataset?**
- ✅ Real business data from actual e-commerce marketplace
- ✅ Multiple tables with clear relationships (like production databases)
- ✅ Complex enough to teach all join types (INNER, LEFT, RIGHT, FULL)
- ✅ Business-relevant questions: customer behavior, product performance, seller analysis
- ✅ Data quality issues to handle (nulls, missing relationships)

---

## Dataset Structure

### Core Tables (Primary Focus for Day 2)

#### 1. `olist_orders_dataset.csv` - Orders (Fact Table)
**99,441 orders** | Primary Key: `order_id`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Unique order identifier (PK) |
| `customer_id` | string | Foreign key to customers table |
| `order_status` | string | Order status (delivered, shipped, canceled, etc.) |
| `order_purchase_timestamp` | datetime | When order was placed |
| `order_approved_at` | datetime | When payment was approved |
| `order_delivered_carrier_date` | datetime | When order handed to carrier |
| `order_delivered_customer_date` | datetime | When order delivered to customer |
| `order_estimated_delivery_date` | datetime | Estimated delivery date shown to customer |

**Business value:** Central fact table connecting customers, order items, payments, and reviews.

---

#### 2. `olist_customers_dataset.csv` - Customers (Dimension Table)
**99,441 customers** | Primary Key: `customer_id`

| Column | Type | Description |
|--------|------|-------------|
| `customer_id` | string | Unique customer identifier (PK) |
| `customer_unique_id` | string | Unique identifier for customer (handles duplicates) |
| `customer_zip_code_prefix` | integer | First 5 digits of ZIP code |
| `customer_city` | string | Customer city |
| `customer_state` | string | Customer state (2-letter code) |

**Business value:** Who are our customers? Where do they live? Customer segmentation by location.

**Note:** `customer_id` is unique per order, but `customer_unique_id` identifies the same person across multiple orders.

---

#### 3. `olist_order_items_dataset.csv` - Order Line Items (Fact Table)
**112,650 order items** | Composite Key: `order_id` + `order_item_id`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Foreign key to orders table |
| `order_item_id` | integer | Sequential item number within order (1, 2, 3...) |
| `product_id` | string | Foreign key to products table |
| `seller_id` | string | Foreign key to sellers table |
| `shipping_limit_date` | datetime | Seller must ship by this date |
| `price` | float | Item price in BRL (Brazilian Real) |
| `freight_value` | float | Shipping cost in BRL |

**Business value:** What products were ordered? How much revenue per order? Which sellers fulfilled items?

**Important:** One order can contain multiple items. This creates a **one-to-many relationship** with orders.

---

#### 4. `olist_products_dataset.csv` - Products (Dimension Table)
**32,951 products** | Primary Key: `product_id`

| Column | Type | Description |
|--------|------|-------------|
| `product_id` | string | Unique product identifier (PK) |
| `product_category_name` | string | Product category (in Portuguese) |
| `product_name_lenght` | integer | Number of characters in product name |
| `product_description_lenght` | integer | Number of characters in description |
| `product_photos_qty` | integer | Number of product photos |
| `product_weight_g` | integer | Product weight in grams |
| `product_length_cm` | integer | Product length in cm |
| `product_height_cm` | integer | Product height in cm |
| `product_width_cm` | integer | Product width in cm |

**Business value:** What products do we sell? Product catalog analysis, category performance.

**Note:** Actual product names are anonymized. Category names are in Portuguese (use translation table).

---

#### 5. `olist_sellers_dataset.csv` - Sellers (Dimension Table)
**3,095 sellers** | Primary Key: `seller_id`

| Column | Type | Description |
|--------|------|-------------|
| `seller_id` | string | Unique seller identifier (PK) |
| `seller_zip_code_prefix` | integer | First 5 digits of ZIP code |
| `seller_city` | string | Seller city |
| `seller_state` | string | Seller state (2-letter code) |

**Business value:** Who are our sellers? Where are they located? Seller performance by region.

---

### Supporting Tables (For Advanced Exercises)

#### 6. `olist_order_payments_dataset.csv` - Payments
**103,886 payment transactions** | Composite Key: `order_id` + `payment_sequential`

| Column | Type | Description |
|--------|------|-------------|
| `order_id` | string | Foreign key to orders table |
| `payment_sequential` | integer | Payment number (1, 2, 3 if multiple payments) |
| `payment_type` | string | Payment method (credit_card, boleto, voucher, debit_card) |
| `payment_installments` | integer | Number of installments |
| `payment_value` | float | Payment amount in BRL |

**Business value:** How do customers pay? Are installments common? What's the total payment per order?

**Note:** One order can have multiple payment methods (e.g., 50% credit card, 50% voucher).

---

#### 7. `olist_order_reviews_dataset.csv` - Reviews
**99,224 reviews** | Primary Key: `review_id`

| Column | Type | Description |
|--------|------|-------------|
| `review_id` | string | Unique review identifier (PK) |
| `order_id` | string | Foreign key to orders table |
| `review_score` | integer | Rating from 1 (worst) to 5 (best) |
| `review_comment_title` | string | Review title (Portuguese) |
| `review_comment_message` | string | Review text (Portuguese) |
| `review_creation_date` | datetime | When review was created |
| `review_answer_timestamp` | datetime | When review was answered |

**Business value:** Customer satisfaction, sentiment analysis, product quality feedback.

---

#### 8. `product_category_name_translation.csv` - Category Translation
**71 categories** | Primary Key: `product_category_name`

| Column | Type | Description |
|--------|------|-------------|
| `product_category_name` | string | Category name in Portuguese (PK) |
| `product_category_name_english` | string | Category name in English |

**Business value:** Translate Portuguese category names to English for analysis.

**Examples:**
- `perfumaria` → `perfumery`
- `moveis_decoracao` → `furniture_decor`
- `informatica_acessorios` → `computers_accessories`

---

#### 9. `olist_geolocation_dataset.csv` - Geolocation (Optional)
**1,000,163 geolocation records** | Composite Key: `geolocation_zip_code_prefix` + `geolocation_lat` + `geolocation_lng`

| Column | Type | Description |
|--------|------|-------------|
| `geolocation_zip_code_prefix` | integer | First 5 digits of ZIP code |
| `geolocation_lat` | float | Latitude |
| `geolocation_lng` | float | Longitude |
| `geolocation_city` | string | City name |
| `geolocation_state` | string | State (2-letter code) |

**Business value:** Map customer and seller locations, calculate distances, logistics analysis.

**Note:** This table is LARGE (1M rows, 58 MB file size) and optional for Day 2. Use for advanced geospatial exercises only.

---

## Entity-Relationship Diagram

```
┌─────────────────┐
│   customers     │
│  (99,441)       │
│                 │
│ customer_id (PK)│───┐
└─────────────────┘   │
                      │
                      │
┌─────────────────┐   │    ┌──────────────────┐
│   orders        │   │    │  order_items     │
│  (99,441)       │   │    │  (112,650)       │
│                 │   │    │                  │
│ order_id (PK)   │◄──┼────│ order_id (FK)    │
│ customer_id(FK) │◄──┘    │ product_id (FK)  │───┐
└─────────────────┘        │ seller_id (FK)   │───┼───┐
       ▲                   └──────────────────┘   │   │
       │                                           │   │
       │                                           │   │
       │                   ┌──────────────────┐   │   │
       │                   │   products       │   │   │
       │                   │  (32,951)        │   │   │
       │                   │                  │   │   │
       │                   │ product_id (PK)  │◄──┘   │
       │                   └──────────────────┘       │
       │                                               │
       │                   ┌──────────────────┐       │
       │                   │   sellers        │       │
       │                   │  (3,095)         │       │
       │                   │                  │       │
       │                   │ seller_id (PK)   │◄──────┘
       │                   └──────────────────┘
       │
       │
       ├───────────────────┐
       │                   │
       │                   │
┌──────▼──────────┐  ┌─────▼────────────┐
│  payments       │  │   reviews        │
│  (103,886)      │  │  (104,719)       │
│                 │  │                  │
│ order_id (FK)   │  │ order_id (FK)    │
└─────────────────┘  └──────────────────┘
```

**Key Relationships:**
- One customer → Many orders (via `customer_id`)
- One order → Many order items (via `order_id`)
- One order → Many payments (via `order_id`)
- One order → One or more reviews (via `order_id`)
- One product → Many order items (via `product_id`)
- One seller → Many order items (via `seller_id`)

---

## Recommended Tables for Day 2 Teaching

**Start with these 4 core tables:**

1. **`olist_orders_dataset.csv`** - Central fact table
2. **`olist_customers_dataset.csv`** - Who placed orders?
3. **`olist_order_items_dataset.csv`** - What was ordered?
4. **`olist_products_dataset.csv`** - Product catalog

**Why these 4?**
- Clear primary key/foreign key relationships
- Teach INNER JOIN, LEFT JOIN (with actual examples), and FULL OUTER JOIN
- RIGHT JOIN taught conceptually (all products have orders, so no natural RIGHT JOIN examples)
- Answer real business questions
- Manageable size (combined ~250K rows)

**Add for advanced exercises:**
- `olist_sellers_dataset.csv` - Multi-table joins (orders → items → sellers)
- `olist_order_payments_dataset.csv` - Multiple payments per order
- `olist_order_reviews_dataset.csv` - Customer satisfaction analysis
- `product_category_name_translation.csv` - String joins

---

## Intentional Data Characteristics

### Good News (Clean Data)
- ✅ No duplicate primary keys
- ✅ Consistent data types
- ✅ Valid date ranges (2016-2018)
- ✅ Clear foreign key relationships

### Teaching Opportunities (Real-World Messiness)

**1. Unmatched Rows (Perfect for JOIN Teaching!)**
- ❓ **Do all products appear in order_items?** YES - All 32,951 products have been ordered at least once.
  - **Teaching implication:** No natural RIGHT JOIN examples (products without orders)
  - **How to teach RIGHT JOIN:** Demonstrate conceptually that `A RIGHT JOIN B` is equivalent to `B LEFT JOIN A` (just flip the tables)
  - **Industry note:** RIGHT JOIN is rarely used in practice; LEFT JOIN is the standard
- ❓ **Do all customers have orders?** YES (by design - customer_id created at order time)
- ❓ **Do all sellers have sales?** YES - All 3,095 sellers in the sellers table have at least one sale
- ❓ **Do all orders have reviews?** NO! 768 orders (0.77%) have no reviews overall.
  - **BETTER LEFT JOIN EXAMPLES:** Filter by order status for clearer teaching:
    - **Shipped orders:** 75 unreviewed (6.71% of 1,118 shipped orders)
    - **Canceled orders:** 20 unreviewed (3.18% of 629 canceled orders)
    - **Delivered orders:** 646 unreviewed (0.67% of 97,007 delivered orders)
  - **Use case:** Perfect for `LEFT JOIN` teaching - shows orders without matching reviews
  - **Query:** `orders LEFT JOIN reviews WHERE order_status IN ('shipped', 'canceled')` gives stronger examples than using all orders

**2. Null Values**
- `order_approved_at`: NULL if payment not approved yet
- `order_delivered_carrier_date`: NULL if not shipped
- `order_delivered_customer_date`: NULL if not delivered
- `product_category_name`: Some products have NULL categories
- `review_comment_title`, `review_comment_message`: Many reviews have no text (just score)

**3. One-to-Many Relationships**
- One order → Multiple items (avg ~1.13 items per order)
- One order → Multiple payments (some customers split payment)
- **Watch for duplicate rows!** Joining orders to order_items inflates row count.

**4. Data Quality Issues**
- **VERIFIED: No orphaned foreign keys** - All `product_id` and `seller_id` in order_items have matching records in products/sellers tables
- However, some products have NULL category names (good for NULL handling practice)
- **Pedagogical note:** While this dataset is clean, teach students to CHECK for orphaned FKs in real-world scenarios

---

## Learning Objectives

By working with this dataset, students will practice:

### Block A: SQL Joins (Day 2 Focus)

**Core Concepts:**
1. **INNER JOIN** - Only matching rows from both tables
   - Example: Orders with products (only completed orders with valid products)
2. **LEFT JOIN** - All rows from left table + matches from right
   - Example: All orders, even those without reviews (768 orders have no reviews overall)
   - **Better example:** Filter by status - 6.71% of shipped orders lack reviews (75 orders)
3. **RIGHT JOIN** - All rows from right table + matches from left
   - **Teaching approach:** Demonstrate that `A RIGHT JOIN B` = `B LEFT JOIN A` (just flip the tables!)
   - **This dataset:** No natural RIGHT JOIN examples (all products ordered, all sellers active)
   - **Real-world use case:** "Products never sold" or "Employees with no sales" - but we don't have these in Olist
   - **Industry note:** RIGHT JOIN rarely used in practice; LEFT JOIN is the standard pattern
4. **FULL OUTER JOIN** - All rows from both tables
   - Example: Complete view of orders and reviews (shows unmatched rows from both sides)

**Key Skills:**
- Understanding primary keys and foreign keys
- Recognizing one-to-many relationships
- Handling unmatched rows appropriately
- Avoiding duplicate row inflation
- Aggregating after joins (GROUP BY on the right grain)

**Business Questions:**
- What are the top 10 best-selling products?
- Which customers have placed the most orders?
- Which sellers have the highest average review scores?
- What percentage of orders are delivered on time?
- Which product categories generate the most revenue?

---

## Sample DuckDB Queries

### Load Tables

```sql
-- Load orders
CREATE TABLE orders AS
SELECT * FROM 'data/day2/block_a/olist_orders_dataset.csv';

-- Load customers
CREATE TABLE customers AS
SELECT * FROM 'data/day2/block_a/olist_customers_dataset.csv';

-- Load order items
CREATE TABLE order_items AS
SELECT * FROM 'data/day2/block_a/olist_order_items_dataset.csv';

-- Load products
CREATE TABLE products AS
SELECT * FROM 'data/day2/block_a/olist_products_dataset.csv';

-- Verify row counts
SELECT 'orders' as table_name, COUNT(*) as row_count FROM orders
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'products', COUNT(*) FROM products;
```

### Example Joins

**1. INNER JOIN: Orders with customer details**
```sql
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    c.customer_city,
    c.customer_state
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
LIMIT 10;
```

**2. LEFT JOIN: All orders, even those without reviews**
```sql
-- Load reviews first
CREATE TABLE reviews AS
SELECT * FROM 'data/day2/block_a/olist_order_reviews_dataset.csv';

-- Find orders without reviews
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    r.review_score
FROM orders o
LEFT JOIN reviews r ON o.order_id = r.order_id
WHERE r.review_id IS NULL;
```

**3. Aggregation after JOIN: Revenue by product category**
```sql
-- Join order_items → products → category translation
SELECT
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) as num_orders,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_item_price
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
WHERE p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 10;
```

**4. Multi-table JOIN: Orders → Items → Products → Sellers**
```sql
-- Load sellers
CREATE TABLE sellers AS
SELECT * FROM 'data/day2/block_a/olist_sellers_dataset.csv';

-- Top sellers by number of items sold
SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,
    COUNT(*) as items_sold,
    SUM(oi.price) as total_sales
FROM order_items oi
INNER JOIN sellers s ON oi.seller_id = s.seller_id
GROUP BY s.seller_id, s.seller_city, s.seller_state
ORDER BY total_sales DESC
LIMIT 10;
```

---

## Common Pitfalls & Teaching Notes

### 1. Row Count Explosion
**Problem:** Joining orders (99K rows) to order_items (112K rows) returns 112K rows, not 99K!

**Why:** One order can have multiple items (one-to-many relationship).

**Solution:** Always check row counts before/after joins. Aggregate at the correct grain.

```sql
-- ❌ Wrong: This counts orders multiple times if they have multiple items
SELECT COUNT(*) FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;
-- Returns 112,650 (number of items, not orders!)

-- ✅ Correct: Count distinct orders
SELECT COUNT(DISTINCT o.order_id) FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;
-- Returns 99,441 (actual number of orders)
```

### 2. Handling Unmatched Foreign Keys
**Problem:** Some `product_id` in order_items don't exist in products table.

**Decision points for students:**
- INNER JOIN: Exclude these rows (most conservative)
- LEFT JOIN: Keep order_items, show NULL for product info
- Document the issue and explain your choice!

### 3. NULL vs Missing Relationships
**Problem:** `review_score = NULL` could mean two things:
1. Order has no review (no matching row in reviews table)
2. Review exists but score is NULL (unlikely)

**Solution:** Use `IS NULL` checks on the foreign key (`review_id`), not the data columns.

---

## Attribution & License

**License:** CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0)

This means:
- ✅ Free to use for educational purposes
- ✅ Can modify and build upon
- ✅ Must give attribution
- ❌ Cannot use commercially
- ❌ Derivatives must use same license

**Required Attribution:**
> Brazilian E-Commerce Public Dataset by Olist. (2018). Retrieved from https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce. Licensed under CC BY-NC-SA 4.0.

**Original Source:** Olist (https://olist.com/pt-br/)

**Published by:** Olist on Kaggle (2018)

---

## Tips for Students

### Start Simple, Build Up
1. **First:** Explore individual tables (SELECT, WHERE, ORDER BY, GROUP BY)
2. **Then:** Join two tables (orders + customers)
3. **Then:** Join three tables (orders + order_items + products)
4. **Finally:** Complex multi-table joins with aggregations

### Validate Your Joins
Always check:
```sql
-- Before join: How many orders?
SELECT COUNT(*) FROM orders;  -- Should be 99,441

-- After join: How many rows?
SELECT COUNT(*) FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id;  -- Should be 112,650

-- Why the difference? One-to-many relationship!
```

### Use Table Aliases
```sql
-- ❌ Hard to read
SELECT order_id FROM orders WHERE order_id = '123';

-- ✅ Clear, especially with multiple tables
SELECT o.order_id, c.customer_city
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;
```

### Check for Unmatched Rows
```sql
-- Products never ordered (use this pattern for LEFT/RIGHT JOIN practice)
SELECT p.product_id, p.product_category_name
FROM products p
LEFT JOIN order_items oi ON p.product_id = oi.product_id
WHERE oi.order_id IS NULL;
```

---

## Need Help?

**Common issues:**

- **"Too many rows after join!"** → You have a one-to-many relationship. Use `COUNT(DISTINCT ...)` or aggregate at the correct grain.
- **"Some products show NULL"** → Foreign key doesn't exist in dimension table. Decide: INNER JOIN (exclude) or LEFT JOIN (keep with NULLs).
- **"Dates won't parse"** → DuckDB handles this automatically for ISO format. If issues, use `CAST(... AS TIMESTAMP)`.
- **"Category names are in Portuguese"** → Join with `product_category_name_translation.csv`.

**For more examples, see Day 2 teaching notebooks:**
- `notebooks/day2/day2_block_a_joins.ipynb`
- `notebooks/day2/day2_exercise_joins.ipynb`

---

## Advanced Exercises

Once comfortable with basic joins, try:

1. **Calculate seller performance:**
   - Join: order_items → sellers → reviews
   - Metric: Average review score per seller
   - Filter: Only sellers with 10+ orders

2. **Customer lifetime value:**
   - Join: customers → orders → order_items
   - Metric: Total revenue per customer
   - Rank: Top 100 customers by revenue

3. **Product category trends:**
   - Join: products → order_items → orders
   - Group by: Month and category
   - Visualize: Revenue trends over time

4. **Delivery performance:**
   - Compare `order_estimated_delivery_date` vs `order_delivered_customer_date`
   - Calculate: Percentage on-time delivery by seller
   - Insight: Which sellers consistently deliver on time?

5. **Geographic analysis (use geolocation table):**
   - Join: customers → geolocation
   - Calculate: Distance between customer and seller
   - Insight: How does distance affect delivery time?

---

**Ready to start? Open `notebooks/day2/day2_block_a_joins.ipynb` and let's join some tables!**

---
---

# Block B: DummyJSON Products API

**Source:** DummyJSON - Fake REST API for Testing and Prototyping
**URL:** https://dummyjson.com/docs/products
**License:** Public API, no authentication required
**Teaching Method:** Live API calls (primary) + offline backup (emergency only)
**Backup File:** `block_b/products_backup.json` (30 products)
**Used in:** Day 2 Block B (JSON Normalization and API Ingestion)

---

## Dataset Description

This is a **JSON dataset from DummyJSON**, a free fake REST API designed for testing and prototyping. Teaching notebooks fetch 30 products via live API calls, with an offline backup file available if the API is unavailable during class.

This dataset is perfect for teaching JSON normalization because it contains **multiple levels of nesting** that must be flattened and normalized into relational tables. Students will learn to parse complex JSON structures, extract nested data, and transform them into clean relational schemas.

**Why this dataset?**
- ✅ Rich nested structure (objects within objects, arrays of objects)
- ✅ Real-world API response format (like actual e-commerce APIs)
- ✅ Multiple normalization opportunities (one-to-many, many-to-many)
- ✅ No authentication required (students focus on data transformation, not API complexity)
- ✅ Business-relevant (product catalog with reviews - recognizable domain)
- ✅ Manageable size (30 products via API, ~90 reviews) - easy to inspect
- ✅ Live API teaching (shows real-world data fetching patterns)

---

## Dataset Structure

### Top-Level Response

```json
{
  "products": [ ... ],  // Array of 30 product objects (teaching uses limit=30)
  "total": 194,         // Total products available in API
  "skip": 0,            // Pagination offset
  "limit": 30           // Number of products requested (teaching default)
}
```

**Note:** Teaching notebooks fetch 30 products from the live API using `?limit=30`. The backup file (`products_backup.json`) contains the same 30 products for offline use.

### Product Object Structure

Each product in the `products` array has the following structure:

```json
{
  "id": 1,
  "title": "Essence Mascara Lash Princess",
  "description": "The Essence Mascara...",
  "category": "beauty",
  "price": 9.99,
  "discountPercentage": 7.17,
  "rating": 4.94,
  "stock": 5,
  "tags": ["beauty", "mascara"],
  "brand": "Essence",
  "sku": "RCH45Q1A",
  "weight": 2,
  "dimensions": {
    "width": 15.14,
    "height": 13.08,
    "depth": 22.99
  },
  "warrantyInformation": "1 month warranty",
  "shippingInformation": "Ships in 1 month",
  "availabilityStatus": "Low Stock",
  "reviews": [
    {
      "rating": 3,
      "comment": "Would not recommend!",
      "date": "2025-04-30T09:41:02.053Z",
      "reviewerName": "Eleanor Collins",
      "reviewerEmail": "eleanor.collins@x.dummyjson.com"
    },
    ...
  ],
  "returnPolicy": "30 days return policy",
  "minimumOrderQuantity": 24,
  "meta": {
    "createdAt": "2025-04-16T15:35:13.476Z",
    "updatedAt": "2025-04-16T15:35:13.476Z",
    "barcode": "9164035109868",
    "qrCode": "https://dummyjson.com/public/qr-code.png"
  },
  "thumbnail": "https://cdn.dummyjson.com/products/images/beauty/...",
  "images": [
    "https://cdn.dummyjson.com/products/images/beauty/..."
  ]
}
```

---

## Nested Structures (Normalization Opportunities!)

### 1. `dimensions` - Nested Object (Flatten to Columns)

**Structure:** Object with 3 keys
```json
"dimensions": {
  "width": 15.14,
  "height": 13.08,
  "depth": 22.99
}
```

**Normalization strategy:** Flatten to columns in products table
- `product_width`, `product_height`, `product_depth`

---

### 2. `reviews` - Nested Array of Objects (One-to-Many Relationship)

**Structure:** Array of review objects
```json
"reviews": [
  {
    "rating": 3,
    "comment": "Would not recommend!",
    "date": "2025-04-30T09:41:02.053Z",
    "reviewerName": "Eleanor Collins",
    "reviewerEmail": "eleanor.collins@x.dummyjson.com"
  },
  ...
]
```

**Statistics:**
- Total reviews across 30 products: **~90 reviews** (3 per product average)
- Average reviews per product: **3 reviews**

**Normalization strategy:** Create separate `reviews` table
- Primary key: Generate `review_id`
- Foreign key: `product_id` → `products.id`
- Columns: `rating`, `comment`, `date`, `reviewerName`, `reviewerEmail`

---

### 3. `tags` - Simple Array (Many-to-Many Relationship)

**Structure:** Array of strings
```json
"tags": ["beauty", "mascara"]
```

**Statistics:**
- Unique tags across all products: **81 tags**
- Tags per product: Varies (typically 2-3)

**Normalization strategy:** Two options:

**Option A: Bridge table (many-to-many)**
- `product_tags` table with (`product_id`, `tag`)
- Allows querying "all products with tag X"

**Option B: JSON column** (if database supports it)
- Keep as JSON array in DuckDB
- Use JSON functions to query

---

### 4. `meta` - Nested Object (Flatten to Columns)

**Structure:** Object with metadata
```json
"meta": {
  "createdAt": "2025-04-16T15:35:13.476Z",
  "updatedAt": "2025-04-16T15:35:13.476Z",
  "barcode": "9164035109868",
  "qrCode": "https://dummyjson.com/public/qr-code.png"
}
```

**Normalization strategy:** Flatten to columns in products table
- `created_at`, `updated_at`, `barcode`, `qr_code`

---

### 5. `images` - Array of URLs (One-to-Many Relationship)

**Structure:** Array of image URLs
```json
"images": [
  "https://cdn.dummyjson.com/products/images/beauty/...",
  ...
]
```

**Normalization strategy:** Two options:

**Option A: Separate table**
- `product_images` table with (`image_id`, `product_id`, `image_url`)

**Option B: JSON column or comma-separated**
- Simpler for this use case (typically 1-2 images)

---

## Normalized Schema Design

After normalization, the JSON should be transformed into these tables:

### Table 1: `products` (Main Table)

| Column | Type | Source |
|--------|------|--------|
| `id` | INTEGER | `id` (PK) |
| `title` | VARCHAR | `title` |
| `description` | TEXT | `description` |
| `category` | VARCHAR | `category` |
| `price` | DECIMAL | `price` |
| `discount_percentage` | DECIMAL | `discountPercentage` |
| `rating` | DECIMAL | `rating` |
| `stock` | INTEGER | `stock` |
| `brand` | VARCHAR | `brand` |
| `sku` | VARCHAR | `sku` |
| `weight` | INTEGER | `weight` |
| `width` | DECIMAL | `dimensions.width` (flattened) |
| `height` | DECIMAL | `dimensions.height` (flattened) |
| `depth` | DECIMAL | `dimensions.depth` (flattened) |
| `warranty_info` | VARCHAR | `warrantyInformation` |
| `shipping_info` | VARCHAR | `shippingInformation` |
| `availability` | VARCHAR | `availabilityStatus` |
| `return_policy` | VARCHAR | `returnPolicy` |
| `min_order_qty` | INTEGER | `minimumOrderQuantity` |
| `barcode` | VARCHAR | `meta.barcode` (flattened) |
| `qr_code` | VARCHAR | `meta.qrCode` (flattened) |
| `created_at` | TIMESTAMP | `meta.createdAt` (flattened) |
| `updated_at` | TIMESTAMP | `meta.updatedAt` (flattened) |
| `thumbnail` | VARCHAR | `thumbnail` |

---

### Table 2: `reviews` (One-to-Many from Products)

| Column | Type | Source |
|--------|------|--------|
| `review_id` | INTEGER | Generated (PK) |
| `product_id` | INTEGER | Parent product `id` (FK) |
| `rating` | INTEGER | `reviews[].rating` |
| `comment` | TEXT | `reviews[].comment` |
| `date` | TIMESTAMP | `reviews[].date` |
| `reviewer_name` | VARCHAR | `reviews[].reviewerName` |
| `reviewer_email` | VARCHAR | `reviews[].reviewerEmail` |

**Expected rows:** ~90 reviews (from 30 products, ~3 reviews per product)

---

### Table 3: `product_tags` (Many-to-Many Bridge)

| Column | Type | Source |
|--------|------|--------|
| `product_id` | INTEGER | Parent product `id` (FK) |
| `tag` | VARCHAR | `tags[]` (exploded) |

**Expected rows:** ~60-90 rows (30 products × 2-3 tags each)

---

### Table 4: `product_images` (One-to-Many - Optional)

| Column | Type | Source |
|--------|------|--------|
| `image_id` | INTEGER | Generated (PK) |
| `product_id` | INTEGER | Parent product `id` (FK) |
| `image_url` | VARCHAR | `images[]` (exploded) |

**Expected rows:** ~100-150 rows (most products have 1-2 images)

---

## Sample Python Code

### Load and Parse JSON

**Primary Method: Live API (used in teaching notebooks)**
```python
import requests
import json

# Fetch from live API (preferred method)
response = requests.get("https://dummyjson.com/products", params={'limit': 30}, timeout=10)
data = response.json()

# Extract products array
products = data['products']
print(f"Loaded {len(products)} products from API")

# Inspect first product
print(products[0].keys())
```

**Backup Method: Offline File (emergency only)**
```python
import json

# Load backup file if API is unavailable
with open('data/day2/block_b/products_backup.json', 'r') as f:
    data = json.load(f)

products = data['products']
print(f"Loaded {len(products)} products from backup file")
```

### Normalize `products` Table (Flatten Nested Objects)

```python
import pandas as pd

# Create base products dataframe
products_df = pd.DataFrame(products)

# Flatten dimensions
products_df['width'] = products_df['dimensions'].apply(lambda x: x['width'])
products_df['height'] = products_df['dimensions'].apply(lambda x: x['height'])
products_df['depth'] = products_df['dimensions'].apply(lambda x: x['depth'])

# Flatten meta
products_df['barcode'] = products_df['meta'].apply(lambda x: x['barcode'])
products_df['qr_code'] = products_df['meta'].apply(lambda x: x['qrCode'])
products_df['created_at'] = products_df['meta'].apply(lambda x: x['createdAt'])
products_df['updated_at'] = products_df['meta'].apply(lambda x: x['updatedAt'])

# Drop original nested columns
products_df = products_df.drop(columns=['dimensions', 'meta', 'reviews', 'tags', 'images'])

print(products_df.head())
```

### Normalize `reviews` Table (Explode Nested Array)

```python
# Extract reviews from all products
reviews_list = []

for product in products:
    product_id = product['id']
    for review in product['reviews']:
        review_row = {
            'product_id': product_id,
            'rating': review['rating'],
            'comment': review['comment'],
            'date': review['date'],
            'reviewer_name': review['reviewerName'],
            'reviewer_email': review['reviewerEmail']
        }
        reviews_list.append(review_row)

reviews_df = pd.DataFrame(reviews_list)
reviews_df['review_id'] = range(1, len(reviews_df) + 1)  # Generate PK

print(f"Total reviews: {len(reviews_df)}")
print(reviews_df.head())
```

### Normalize `product_tags` Table (Explode Simple Array)

```python
# Extract tags from all products
tags_list = []

for product in products:
    product_id = product['id']
    for tag in product['tags']:
        tags_list.append({
            'product_id': product_id,
            'tag': tag
        })

tags_df = pd.DataFrame(tags_list)
print(f"Total product-tag relationships: {len(tags_df)}")
print(f"Unique tags: {tags_df['tag'].nunique()}")
print(tags_df.head())
```

### Load into DuckDB

```python
import duckdb

con = duckdb.connect(':memory:')

# Create tables from dataframes
con.register('products', products_df)
con.register('reviews', reviews_df)
con.register('product_tags', tags_df)

# Query: Average rating by category
result = con.execute("""
    SELECT
        p.category,
        COUNT(DISTINCT p.id) as num_products,
        AVG(r.rating) as avg_review_rating
    FROM products p
    INNER JOIN reviews r ON p.id = r.product_id
    GROUP BY p.category
    ORDER BY avg_review_rating DESC
""").fetchdf()

print(result)
```

---

## Learning Objectives

By working with this dataset, students will practice:

### Block B: JSON Normalization (Day 2 Focus)

**Core Concepts:**
1. **JSON structure** - Nested objects, arrays of objects, simple arrays
2. **Flattening nested objects** - Extract keys to columns (dimensions, meta)
3. **Exploding nested arrays** - Transform one-to-many into separate table (reviews)
4. **Many-to-many relationships** - Bridge tables for tags
5. **Type handling** - Converting JSON strings to proper types (dates, decimals)
6. **Primary key generation** - Creating surrogate keys for child tables
7. **Foreign key relationships** - Maintaining relationships after normalization

**Key Skills:**
- Parsing JSON from file or API
- Identifying nested structures
- Deciding when to flatten vs create new table
- Writing Python loops to extract nested data
- Using pandas to structure normalized data
- Loading normalized data into DuckDB
- Querying across normalized tables

**Business Questions:**
- What's the average review rating by product category?
- Which products have the highest ratings?
- What are the most common tags?
- Which products have the most reviews?
- What percentage of products are low stock?

---

## Data Characteristics

### Size
- **Products:** 100
- **Reviews:** 300 (3 per product average)
- **Tags:** 81 unique tags, ~200 product-tag relationships
- **Images:** ~100 image URLs
- **File size:** 203 KB

### Categories
The 30 products span multiple categories including:
- beauty
- fragrances
- furniture
- groceries
- home-decoration
- kitchen-accessories
- laptops
- mens-shirts
- mens-shoes
- mens-watches
- mobile-accessories
- smartphones
- sports-accessories
- sunglasses
- tablets
- tops
- vehicle
- womens-bags
- womens-dresses
- womens-jewellery
- womens-shoes
- womens-watches

### Data Quality
- ✅ No missing values in core fields (id, title, price, category)
- ✅ All products have at least one review
- ✅ All products have at least one tag
- ✅ Consistent date formats (ISO 8601)
- ✅ Realistic e-commerce data (prices, stock levels, ratings)

---

## Teaching Notes

### Why DummyJSON for Day 2?

**Separation of concerns:**
- **Day 2 Block B:** Focus on JSON normalization (data transformation complexity)
- **Day 3:** Focus on API complexity (auth, rate limits, error handling, multi-source)

By using a simple API on Day 2, students can focus entirely on:
- Understanding nested JSON structures
- Deciding how to normalize (flatten vs separate table)
- Writing transformation code
- Validating results

**No authentication required** - Students don't need API keys, can run locally from cached JSON.

### Comparison to Real-World APIs

This structure mirrors real e-commerce APIs:
- **Shopify API:** Similar product + variants + reviews structure
- **Amazon API:** Similar nested product attributes
- **E-commerce platforms:** Commonly return nested data requiring normalization

Students who master this dataset will be able to work with real production APIs.

---

## Common Pitfalls

### 1. Forgetting to Generate Primary Keys
**Problem:** Reviews table needs a `review_id` but JSON doesn't provide one.

**Solution:** Generate using `range()` or `row_number()`
```python
reviews_df['review_id'] = range(1, len(reviews_df) + 1)
```

### 2. Losing Foreign Key Relationship
**Problem:** When extracting reviews, forgetting to include `product_id`.

**Solution:** Always capture parent ID when iterating:
```python
for product in products:
    product_id = product['id']  # ← Capture this!
    for review in product['reviews']:
        review_row = {'product_id': product_id, ...}
```

### 3. Not Handling NULL/Missing Values
**Problem:** Some products might not have all nested fields.

**Solution:** Use `.get()` with defaults:
```python
width = product.get('dimensions', {}).get('width', None)
```

### 4. Type Confusion
**Problem:** Dates are strings, not datetime objects.

**Solution:** Convert types explicitly:
```python
reviews_df['date'] = pd.to_datetime(reviews_df['date'])
```

---

## Advanced Exercises

Once comfortable with basic normalization, try:

1. **Category hierarchy:**
   - Some categories have parent-child relationships (e.g., "beauty" → "mascara")
   - Create a category dimension table

2. **Review sentiment analysis:**
   - Analyze review comments for positive/negative sentiment
   - Compare sentiment score to numeric rating

3. **Price analytics:**
   - Calculate actual price after discount
   - Find products with highest discount percentage
   - Group by category and compare pricing

4. **Inventory analysis:**
   - Identify low-stock products (stock < minimum order quantity)
   - Calculate total inventory value (stock × price)

5. **Tag analysis:**
   - Find most common tags
   - Products with most tags
   - Tag co-occurrence analysis (which tags appear together?)

---

## Attribution & License

**Source:** DummyJSON (https://dummyjson.com)  
**License:** Public API - Free to use for testing and prototyping  
**No authentication required:** Data is publicly accessible  
**Attribution:** Not required, but good practice

**Recommended attribution:**
> DummyJSON Products API. (2024). Retrieved from https://dummyjson.com/docs/products. Free public API for testing and prototyping.

---

**Ready to normalize? Open `notebooks/day2/day2_block_b_01_api_json_basics.ipynb` and let's flatten some JSON!**
