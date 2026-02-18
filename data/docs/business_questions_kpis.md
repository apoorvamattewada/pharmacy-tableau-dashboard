# Business Questions & KPI Definitions
## Pharmacy Sales Analytics Dashboard

---

## Business Context

A regional pharmacy chain operates across 5 US regions (Northeast, Southeast, Midwest, Southwest, West) selling 10 product categories spanning prescription and OTC medications. The analytics team needs a self-service dashboard that lets operations managers, regional directors, and the CFO answer strategic questions from a single screen without relying on ad-hoc SQL queries.

---

## Key Business Questions

### Revenue & Growth
| # | Question | Visualization | KPI Used |
|---|----------|---------------|----------|
| Q1 | Are total pharmacy revenues growing year-over-year? | Trend line chart | YoY Sales Growth % |
| Q2 | Which months show seasonal revenue spikes? | Monthly trend chart | Net Sales by Month |
| Q3 | What is this year's revenue vs. last year for each quarter? | Bar chart | Current vs. Prior Year Sales |

### Profitability
| # | Question | Visualization | KPI Used |
|---|----------|---------------|----------|
| Q4 | Which product categories generate the highest profit margins? | Sorted bar chart | Profit Margin % by Category |
| Q5 | Are high-revenue categories also high-margin? | Dual-axis bar | Net Sales + Profit Margin % |
| Q6 | How much revenue are we losing to discounts? | KPI tile + tooltip | Discount Impact $ |

### Geographic Performance
| # | Question | Visualization | KPI Used |
|---|----------|---------------|----------|
| Q7 | Which states and regions drive the most sales? | Filled state map | Net Sales (LOD) by State |
| Q8 | Are there underperforming regions we should investigate? | Map + Region filter | Region Sales Rank |
| Q9 | How does profitability vary by geography? | Map color + tooltip | Margin % by State |

### Customer & Product Insights
| # | Question | Visualization | KPI Used |
|---|----------|---------------|----------|
| Q10 | What percentage of transactions are refills (retention proxy)? | KPI tile | Refill Rate % |
| Q11 | Which customer segments (Senior/Adult/Young Adult) generate most revenue? | Segment filter | Net Sales by Segment |
| Q12 | Which insurance/payment types are most common in high-profit categories? | Tooltip drill-down | Count by Payment Type |

---

## KPI Definitions

### 1 — Total Net Sales
**Definition:** Sum of all net sales after discounts, across the selected period and filters.  
**Formula:** `SUM(Net_Sales)` = Gross Sales − Discount Amount  
**Unit:** USD  
**Target:** > $170,000 per year (based on 2021 baseline)  
**Alert threshold:** < $140,000 = underperformance flag  

---

### 2 — Total Net Profit
**Definition:** Revenue remaining after Cost of Goods Sold (COGS) and discounts.  
**Formula:** `SUM(Net_Profit)` = Net Sales − COGS  
**Unit:** USD  
**Target:** > $65,000 per year  

---

### 3 — Profit Margin %
**Definition:** Percentage of net sales retained as profit; measures operational efficiency.  
**Formula:** `SUM(Net_Profit) / SUM(Net_Sales) × 100`  
**Unit:** Percentage  
**Industry benchmark:** Retail pharmacy typically 20–35%; specialty categories can reach 50%+  
**Dashboard target:** ≥ 35% overall  

---

### 4 — YoY Sales Growth %
**Definition:** Percentage change in net sales compared to the same period last year.  
**Formula:** `(Current Year Sales − Prior Year Sales) / |Prior Year Sales|`  
**Unit:** Percentage  
**Target:** ≥ 8% YoY growth  
**Interpretation:** Positive = growing; negative = declining; 0–5% = flat/stagnant  

---

### 5 — Refill Rate %
**Definition:** Proportion of transactions flagged as prescription refills — a proxy for patient loyalty and recurring revenue.  
**Formula:** `COUNT(Is_Refill = "Yes") / COUNT(All Transactions)`  
**Unit:** Percentage  
**Target:** ≥ 45%  
**Why it matters:** Refills are lower acquisition-cost revenue and indicate chronic condition management revenue streams.  

---

### 6 — Avg Revenue per Transaction
**Definition:** Mean net sales value per individual pharmacy visit / transaction.  
**Formula:** `SUM(Net_Sales) / COUNTD(Transaction_ID)`  
**Unit:** USD  
**Target:** > $140 per transaction  
**Use case:** Track basket-size changes over time; spikes may indicate new high-value products.  

---

### 7 — Discount Impact $
**Definition:** Total dollar value of revenue forgone through discounts.  
**Formula:** `SUM(Discount_Amount)`  
**Unit:** USD  
**Use case:** Evaluate if discount programs are growing revenue (compare with sales growth) or just eroding margin.  

---

### 8 — Region Sales Rank
**Definition:** Ordinal rank of each region (1 = highest sales, 5 = lowest) within the selected time period.  
**Formula:** `RANK(SUM(Net_Sales))`  (Tableau table calculation)  
**Unit:** Rank (1–5)  
**Use case:** Instantly identify which region needs support or additional investment.  

---

### 9 — Senior Share %
**Definition:** Proportion of transactions from the Senior (65+) customer segment.  
**Formula:** `COUNTD(IF Segment = "Senior" THEN Transaction_ID END) / COUNTD(Transaction_ID)`  
**Unit:** Percentage  
**Regulatory note:** High senior share elevates Medicare/Medicaid reimbursement relevance.  

---

## Data Dictionary

| Column              | Type    | Description                                          |
|---------------------|---------|------------------------------------------------------|
| Transaction_ID      | String  | Unique identifier per pharmacy transaction           |
| Date                | Date    | Transaction date (YYYY-MM-DD)                        |
| Year                | Integer | Calendar year                                        |
| Month               | String  | Month name (January–December)                        |
| Month_Num           | Integer | Month number (1–12) for sorting                      |
| Quarter             | String  | Q1–Q4                                                |
| Region              | String  | US Census region (5 values)                          |
| State               | String  | 2-letter state abbreviation                          |
| Product_Category    | String  | Drug/product category (10 values)                    |
| Product_Name        | String  | Specific brand/generic product name                  |
| Customer_Segment    | String  | Age-based segment (Senior, Adult, Young Adult)       |
| Insurance_Provider  | String  | Payer or "Self-Pay"                                  |
| Payment_Type        | String  | Payment method (Insurance, Cash, Medicare, etc.)     |
| Quantity            | Integer | Units dispensed per transaction                      |
| Unit_Price          | Decimal | Price per unit (USD)                                 |
| Gross_Sales         | Decimal | Revenue before discounts (USD)                       |
| Discount_Pct        | Decimal | Discount percentage applied (0.0–0.20)               |
| Discount_Amount     | Decimal | Dollar value of discount (USD)                       |
| Net_Sales           | Decimal | Revenue after discounts (USD)                        |
| COGS                | Decimal | Cost of goods sold (USD)                             |
| Gross_Profit        | Decimal | Gross Sales − COGS (USD)                             |
| Net_Profit          | Decimal | Net Sales − COGS (USD)                               |
| Is_Refill           | String  | "Yes" / "No" — prescription refill indicator         |
| Profit_Margin_Pct   | Decimal | Net Profit / Net Sales × 100 (pre-computed helper)   |
| Revenue_Per_Unit    | Decimal | Net Sales / Quantity (pre-computed helper)           |
| Fiscal_Period       | String  | "YYYY-Qn" label (e.g., "2024-Q3")                   |

---

*Document version 1.0 — Pharmacy Analytics Dashboard*
