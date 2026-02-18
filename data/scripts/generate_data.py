"""
Pharmacy Sales Data Generator
==============================
Generates a realistic synthetic pharmacy dataset for Tableau dashboard analysis.
Run this script to produce `data/pharmacy_sales.csv`.

Usage:
    python scripts/generate_data.py
"""

import csv
import random
import math
from datetime import date, timedelta

random.seed(42)

# ── Configuration ──────────────────────────────────────────────────────────────
ROWS = 5000
START_DATE = date(2021, 1, 1)
END_DATE   = date(2024, 12, 31)

REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]

STATES = {
    "Northeast": ["NY", "NJ", "PA", "CT", "MA"],
    "Southeast": ["FL", "GA", "NC", "SC", "VA"],
    "Midwest":   ["IL", "OH", "MI", "IN", "WI"],
    "Southwest": ["TX", "AZ", "NM", "OK", "CO"],
    "West":      ["CA", "WA", "OR", "NV", "UT"],
}

PRODUCT_CATEGORIES = {
    "Pain Relief":        {"brands": ["Ibuprofen 200mg", "Acetaminophen 500mg", "Naproxen 220mg", "Aspirin 325mg"], "margin_base": 0.42},
    "Antibiotics":        {"brands": ["Amoxicillin 500mg", "Azithromycin 250mg", "Ciprofloxacin 500mg"],            "margin_base": 0.35},
    "Cardiovascular":     {"brands": ["Lisinopril 10mg", "Atorvastatin 20mg", "Metoprolol 50mg", "Amlodipine 5mg"],"margin_base": 0.38},
    "Diabetes Care":      {"brands": ["Metformin 500mg", "Glipizide 5mg", "Insulin Glargine", "Januvia 100mg"],     "margin_base": 0.31},
    "Mental Health":      {"brands": ["Sertraline 50mg", "Escitalopram 10mg", "Bupropion 150mg"],                   "margin_base": 0.44},
    "Vitamins & Supplements": {"brands": ["Vitamin D3 2000IU", "Omega-3 Fish Oil", "Multivitamin Daily", "Zinc 50mg"], "margin_base": 0.55},
    "Allergy & Sinus":    {"brands": ["Cetirizine 10mg", "Loratadine 10mg", "Fluticasone Nasal Spray"],             "margin_base": 0.48},
    "Gastrointestinal":   {"brands": ["Omeprazole 20mg", "Loperamide 2mg", "Famotidine 20mg"],                      "margin_base": 0.40},
    "Dermatology":        {"brands": ["Hydrocortisone 1%", "Clotrimazole Cream", "Tretinoin 0.025%"],               "margin_base": 0.52},
    "Cold & Flu":         {"brands": ["DayQuil LiquidCaps", "NyQuil Severe", "Mucinex DM", "Theraflu"],             "margin_base": 0.46},
}

PAYMENT_TYPES = ["Insurance", "Cash", "Medicare", "Medicaid", "HSA/FSA"]
CUSTOMER_SEGMENTS = ["Senior (65+)", "Adult (26-64)", "Young Adult (18-25)"]

INSURANCE_PROVIDERS = ["BlueCross", "Aetna", "Cigna", "UnitedHealth", "Humana", "Self-Pay"]

# Price ranges by category (unit price in USD)
PRICE_RANGE = {
    "Pain Relief":            (4.99,  24.99),
    "Antibiotics":            (12.99, 89.99),
    "Cardiovascular":         (18.99, 149.99),
    "Diabetes Care":          (22.99, 299.99),
    "Mental Health":          (15.99, 129.99),
    "Vitamins & Supplements": (6.99,  49.99),
    "Allergy & Sinus":        (8.99,  39.99),
    "Gastrointestinal":       (9.99,  54.99),
    "Dermatology":            (11.99, 79.99),
    "Cold & Flu":             (6.99,  22.99),
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def random_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def seasonal_multiplier(d):
    """Cold & Flu spikes in winter; Allergy spikes in spring."""
    m = d.month
    if m in (12, 1, 2):   return 1.30   # winter
    if m in (3, 4, 5):    return 1.15   # spring
    if m in (6, 7, 8):    return 0.90   # summer
    return 1.05                          # fall

def yoy_growth_factor(d):
    """Simulate ~8% YoY revenue growth."""
    years_from_base = d.year - 2021
    return 1.0 + (0.08 * years_from_base) + random.uniform(-0.03, 0.03)

# ── Generate rows ──────────────────────────────────────────────────────────────

rows = []
transaction_id = 1000

for _ in range(ROWS):
    txn_date   = random_date(START_DATE, END_DATE)
    region     = random.choice(REGIONS)
    state      = random.choice(STATES[region])
    category   = random.choices(
        list(PRODUCT_CATEGORIES.keys()),
        weights=[15, 8, 12, 10, 9, 18, 10, 8, 5, 14],  # realistic demand weights
        k=1
    )[0]
    cat_info   = PRODUCT_CATEGORIES[category]
    product    = random.choice(cat_info["brands"])
    segment    = random.choices(CUSTOMER_SEGMENTS, weights=[35, 50, 15], k=1)[0]
    insurance  = random.choice(INSURANCE_PROVIDERS)
    payment    = random.choice(PAYMENT_TYPES)

    # Price & quantity
    lo, hi     = PRICE_RANGE[category]
    unit_price = round(random.uniform(lo, hi), 2)
    quantity   = random.choices([1, 2, 3, 4, 5, 6], weights=[40, 25, 15, 10, 6, 4], k=1)[0]

    # Apply seasonality and YoY growth to effective revenue
    base_revenue = unit_price * quantity
    adj_revenue  = base_revenue * seasonal_multiplier(txn_date) * yoy_growth_factor(txn_date)
    sales        = round(adj_revenue, 2)

    # Cost & profit
    margin_pct   = cat_info["margin_base"] + random.uniform(-0.08, 0.08)
    margin_pct   = max(0.10, min(0.65, margin_pct))
    cogs         = round(sales * (1 - margin_pct), 2)
    profit       = round(sales - cogs, 2)

    # Discount (some transactions)
    discount_pct = 0.0
    if random.random() < 0.18:   # 18% of transactions have a discount
        discount_pct = random.choice([0.05, 0.10, 0.15, 0.20])
    discount_amt = round(sales * discount_pct, 2)
    net_sales    = round(sales - discount_amt, 2)
    net_profit   = round(profit - discount_amt, 2)

    # Refill flag
    is_refill = "Yes" if random.random() < 0.45 else "No"

    rows.append({
        "Transaction_ID":     transaction_id,
        "Date":               txn_date.strftime("%Y-%m-%d"),
        "Year":               txn_date.year,
        "Month":              txn_date.strftime("%B"),
        "Month_Num":          txn_date.month,
        "Quarter":            f"Q{math.ceil(txn_date.month / 3)}",
        "Region":             region,
        "State":              state,
        "Product_Category":   category,
        "Product_Name":       product,
        "Customer_Segment":   segment,
        "Insurance_Provider": insurance,
        "Payment_Type":       payment,
        "Quantity":           quantity,
        "Unit_Price":         unit_price,
        "Gross_Sales":        sales,
        "Discount_Pct":       discount_pct,
        "Discount_Amount":    discount_amt,
        "Net_Sales":          net_sales,
        "COGS":               cogs,
        "Gross_Profit":       profit,
        "Net_Profit":         net_profit,
        "Is_Refill":          is_refill,
    })
    transaction_id += 1

# ── Write CSV ──────────────────────────────────────────────────────────────────

import os
script_dir  = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "..", "data", "pharmacy_sales.csv")
fieldnames  = list(rows[0].keys())

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"✅  Generated {len(rows):,} rows → {output_path}")
