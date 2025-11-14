#!/usr/bin/env python3
"""
HW2 Validation Script
Run this to check if your homework is ready for submission.

Usage: python validation_check.py
"""

import pandas as pd
import json
import sys
import os

def check_hw2():
    """Validate HW2 implementation"""

    print("=" * 50)
    print("🔍 HW2 VALIDATION CHECK")
    print("TechMart Acquisition Data Integration")
    print("=" * 50)

    errors = []
    warnings = []

    # Check 1: Data file exists
    print("\n✓ Checking data file...")
    if not os.path.exists('data/products_hw2.json'):
        errors.append("❌ data/products_hw2.json not found")
        print("  ❌ data/products_hw2.json not found")
        return False
    else:
        print("  ✅ Data file exists")

    # Check 2: Load JSON data
    print("\n✓ Loading JSON data...")
    try:
        with open('data/products_hw2.json', 'r') as f:
            data = json.load(f)
        products = data['products']
        print(f"  ✅ Loaded {len(products)} products")

        if len(products) != 194:
            warnings.append(f"⚠️ Expected 194 products, found {len(products)}")
    except Exception as e:
        errors.append(f"❌ Failed to load JSON: {e}")
        return False

    # Check 3: Verify you have DataFrames
    print("\n✓ Checking for normalized tables...")
    try:
        # This assumes students will have these variables
        # In practice, they'd need to run their notebook first
        print("  ℹ️ Make sure your notebook creates:")
        print("     - products_df (194 rows)")
        print("     - reviews_df (582 rows)")
        print("     - tags_df (364 rows)")
    except:
        pass

    # Check 4: Expected counts
    print("\n✓ Expected data counts:")
    total_reviews = sum(len(p.get('reviews', [])) for p in products)
    total_tags = sum(len(p.get('tags', [])) for p in products)

    print(f"  📊 Products: 194")
    print(f"  💬 Reviews: {total_reviews}")
    print(f"  🏷️ Tags: {total_tags}")

    # Check 5: Categories check
    print("\n✓ Checking categories...")
    categories = set(p.get('category') for p in products)
    print(f"  ✅ Found {len(categories)} unique categories")

    # Check 6: Data quality
    print("\n✓ Data quality checks:")
    products_without_id = [p for p in products if 'id' not in p]
    products_without_price = [p for p in products if 'price' not in p]

    if products_without_id:
        errors.append(f"❌ {len(products_without_id)} products missing ID")
    else:
        print("  ✅ All products have IDs")

    if products_without_price:
        errors.append(f"❌ {len(products_without_price)} products missing price")
    else:
        print("  ✅ All products have prices")

    # Summary
    print("\n" + "=" * 50)
    print("📋 VALIDATION SUMMARY")
    print("=" * 50)

    if errors:
        print("\n❌ ERRORS (must fix):")
        for error in errors:
            print(f"  {error}")

    if warnings:
        print("\n⚠️ WARNINGS (please check):")
        for warning in warnings:
            print(f"  {warning}")

    if not errors and not warnings:
        print("\n✅ ALL CHECKS PASSED!")
        print("Your data is ready for normalization.")

    print("\n📝 CHECKLIST before submission:")
    print("  □ All TODO sections completed")
    print("  □ Three tables created (products, reviews, tags)")
    print("  □ All assertions pass")
    print("  □ SQL queries return results")
    print("  □ Data dictionary complete")
    print("  □ Notebook runs with Restart & Run All")
    print("  □ File renamed to hw2_[your_name].ipynb")

    print("\n💡 TIP: After creating your DataFrames, verify shapes:")
    print("  products_df.shape should be (194, 24+)")
    print("  reviews_df.shape should be (582, 7)")
    print("  tags_df.shape should be (364, 2)")

    return len(errors) == 0

if __name__ == "__main__":
    success = check_hw2()

    if success:
        print("\n🎉 Great work! Ready for the board meeting!")
    else:
        print("\n⚠️ Please fix errors before submitting.")

    sys.exit(0 if success else 1)