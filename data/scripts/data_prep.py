"""
Pharmacy Data Preparation & Validation Script
==============================================
Cleans the raw dataset, validates types, checks for nulls,
and outputs a Tableau-ready CSV with pre-computed helper columns.

Usage:
    python scripts/data_prep.py
"""

import csv
import os
from datetime import datetime
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH  = os.path.join(script_dir, "..", "data", "pharmacy_sales.csv")
OUTPUT_PATH = os.path.join(script_dir, "..", "data", "pharmacy_sales_clean.csv")

# ── Load ───────────────────────────────────────────────────────────────────────
with open(INPUT_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    raw_rows = list(reader)

print(f"Loaded {len(raw_rows):,} rows from {INPUT_PATH}")

# ── Step 1 – Null / blank check ────────────────────────────────────────────────
REQUIRED_COLS = [
    "Transaction_ID", "Date", "Year", "Region", "State",
    "Product_Category", "Net_Sales", "Net_Profit", "COGS",
]
null_issues = 0
clean_rows  = []

for i, row in enumerate(raw_rows, start=2):  # row 1 = header
    skip = False
    for col in REQUIRED_COLS:
        if row.get(col, "").strip() == "":
            print(f"  [WARN] Row {i}: null in required column '{col}' – row dropped")
            null_issues += 1
            skip = True
            break
    if not skip:
        clean_rows.append(row)

print(f"Null-check: dropped {null_issues} rows → {len(clean_rows):,} remain")

# ── Step 2 – Type coercion & validation ────────────────────────────────────────
NUMERIC_COLS = [
    "Quantity", "Unit_Price", "Gross_Sales", "Discount_Pct",
    "Discount_Amount", "Net_Sales", "COGS", "Gross_Profit", "Net_Profit",
]
type_issues = 0
valid_rows  = []

for i, row in enumerate(clean_rows, start=2):
    skip = False
    # Date
    try:
        d = datetime.strptime(row["Date"], "%Y-%m-%d")
        row["Date"] = d.strftime("%Y-%m-%d")
    except ValueError:
        print(f"  [WARN] Row {i}: bad date '{row['Date']}' – row dropped")
        type_issues += 1
        continue
    # Numerics
    for col in NUMERIC_COLS:
        try:
            row[col] = float(row[col])
        except (ValueError, KeyError):
            print(f"  [WARN] Row {i}: non-numeric '{col}' – set to 0")
            row[col] = 0.0
            type_issues += 1
    # Negative net sales sanity check
    if row["Net_Sales"] < 0:
        row["Net_Sales"] = 0.0
    valid_rows.append(row)

print(f"Type-check: {type_issues} coercions → {len(valid_rows):,} valid rows")

# ── Step 3 – Add helper columns for Tableau ────────────────────────────────────
# Pre-compute Profit Margin % to avoid Tableau LOD complexity for new users.
# Tableau calculated fields (see tableau/calculated_fields.md) are still
# the primary KPI source; these columns are convenience copies.

for row in valid_rows:
    ns = row["Net_Sales"]
    np_ = row["Net_Profit"]

    # Profit Margin %
    row["Profit_Margin_Pct"] = round((np_ / ns * 100) if ns != 0 else 0.0, 2)

    # Revenue per unit
    qty = row["Quantity"] if row["Quantity"] else 1
    row["Revenue_Per_Unit"] = round(ns / qty, 2)

    # Fiscal Quarter label
    row["Fiscal_Period"] = f"{row['Year']}-{row['Quarter']}"

print(f"Added helper columns: Profit_Margin_Pct, Revenue_Per_Unit, Fiscal_Period")

# ── Step 4 – Summary statistics (console only) ────────────────────────────────
total_sales  = sum(r["Net_Sales"]   for r in valid_rows)
total_profit = sum(r["Net_Profit"]  for r in valid_rows)
overall_margin = total_profit / total_sales * 100 if total_sales else 0

print("\n── Summary Statistics ─────────────────────────────")
print(f"  Total Net Sales : ${total_sales:>12,.2f}")
print(f"  Total Net Profit: ${total_profit:>12,.2f}")
print(f"  Overall Margin  : {overall_margin:>8.1f}%")
print(f"  Date Range      : {min(r['Date'] for r in valid_rows)} → {max(r['Date'] for r in valid_rows)}")

sales_by_cat = defaultdict(float)
for r in valid_rows:
    sales_by_cat[r["Product_Category"]] += r["Net_Sales"]
print("\n  Net Sales by Category:")
for cat, val in sorted(sales_by_cat.items(), key=lambda x: -x[1]):
    print(f"    {cat:<30} ${val:>10,.2f}")

# ── Step 5 – Write clean output ────────────────────────────────────────────────
fieldnames = list(valid_rows[0].keys())

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(valid_rows)

print(f"\n✅  Clean data written → {OUTPUT_PATH}")
print(f"    Rows: {len(valid_rows):,}  |  Columns: {len(fieldnames)}")
