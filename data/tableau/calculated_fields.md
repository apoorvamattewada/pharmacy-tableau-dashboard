# Tableau Calculated Fields Reference
## Pharmacy Sales Dashboard — `pharmacy_sales_clean.csv`

All formulas below are entered in Tableau Desktop via  
**Analysis → Create Calculated Field** (or right-click a dimension/measure in the Data pane).

---

## 1 · Core KPI Calculations

### [Total Net Sales]
```
SUM([Net_Sales])
```
**Type:** Measure (Aggregation)  
**Format:** Currency ($0.00)  
**Purpose:** Primary revenue KPI shown in the KPI banner.

---

### [Total Net Profit]
```
SUM([Net_Profit])
```
**Type:** Measure  
**Format:** Currency ($0.00)  
**Purpose:** Bottom-line profitability KPI.

---

### [Profit Margin %]
```
SUM([Net_Profit]) / SUM([Net_Sales])
```
**Type:** Measure  
**Format:** Percentage (0.00%)  
**Purpose:** Overall efficiency. Target benchmark: ≥ 35%.

---

### [Total COGS]
```
SUM([COGS])
```
**Type:** Measure  
**Format:** Currency  
**Purpose:** Cost visibility for procurement analysis.

---

### [Discount Impact $]
```
SUM([Discount_Amount])
```
**Type:** Measure  
**Format:** Currency  
**Purpose:** Total revenue lost to discounting.

---

### [Avg Revenue per Transaction]
```
SUM([Net_Sales]) / COUNTD([Transaction_Id])
```
**Type:** Measure  
**Format:** Currency  
**Purpose:** Basket-size metric — how much each visit is worth.

---

### [Refill Rate %]
```
COUNTD(IF [Is_Refill] = "Yes" THEN [Transaction_Id] END)
/ COUNTD([Transaction_Id])
```
**Type:** Measure  
**Format:** Percentage  
**Purpose:** Customer retention proxy. Higher = better loyalty.

---

## 2 · Year-over-Year (YoY) Growth

### [Current Year Sales]
```
IF YEAR([Date]) = {MAX(YEAR([Date]))} THEN [Net_Sales] END
```
> ℹ️ Uses an LOD expression to dynamically pick the latest year in the data.

---

### [Prior Year Sales]
```
IF YEAR([Date]) = {MAX(YEAR([Date]))} - 1 THEN [Net_Sales] END
```

---

### [YoY Sales Growth %]
```
(SUM([Current Year Sales]) - SUM([Prior Year Sales]))
/ ABS(SUM([Prior Year Sales]))
```
**Type:** Measure  
**Format:** Percentage (+/- arrows via custom color rules)  
**Purpose:** Headline growth story for executives.

---

### [YoY Profit Growth %]
```
(SUM(IF YEAR([Date]) = {MAX(YEAR([Date]))} THEN [Net_Profit] END)
 - SUM(IF YEAR([Date]) = {MAX(YEAR([Date]))} - 1 THEN [Net_Profit] END))
/ ABS(SUM(IF YEAR([Date]) = {MAX(YEAR([Date]))} - 1 THEN [Net_Profit] END))
```

---

## 3 · Trend & Time Intelligence

### [Month-Year Label]
```
STR(YEAR([Date])) + "-" + RIGHT("0" + STR(MONTH([Date])), 2)
```
**Purpose:** Ensures correct sort order on the X-axis of the trend line chart  
(avoids alphabetic month sorting).

---

### [Rolling 12-Month Sales]
```
WINDOW_SUM(SUM([Net_Sales]), -11, 0)
```
**Purpose:** Smoothed revenue trend line. Add as a Table Calculation on the trend chart.

---

### [Quarter Label]
```
"Q" + STR(DATEPART('quarter', [Date])) + " " + STR(YEAR([Date]))
```
**Purpose:** Readable quarter labels for quarterly comparison bar charts.

---

## 4 · Performance Tiers

### [Category Performance Tier]
```
IF SUM([Net_Sales]) >= 100000 THEN "🏆 Top Performer"
ELSEIF SUM([Net_Sales]) >= 50000 THEN "✅ On Target"
ELSEIF SUM([Net_Sales]) >= 20000 THEN "⚠️ Below Target"
ELSE "🔴 Needs Attention"
END
```
**Usage:** Color-code bar chart bars. Add to **Color** shelf.

---

### [Margin Health]
```
IF SUM([Net_Profit]) / SUM([Net_Sales]) >= 0.45 THEN "High Margin"
ELSEIF SUM([Net_Profit]) / SUM([Net_Sales]) >= 0.30 THEN "Acceptable"
ELSE "Low Margin"
END
```
**Usage:** Tooltip or secondary dimension for scatter plots.

---

## 5 · Geographic / Segment

### [Region Sales Rank]
```
RANK(SUM([Net_Sales]))
```
**Usage:** Add as Table Calculation. Shows which region ranks 1–5 by revenue.

---

### [Senior Share %]
```
COUNTD(IF [Customer_Segment] = "Senior (65+)" THEN [Transaction_Id] END)
/ COUNTD([Transaction_Id])
```
**Purpose:** Regulatory / compliance insight — senior patient volume.

---

### [Insurance vs Self-Pay Ratio]
```
COUNTD(IF [Payment_Type] != "Cash" THEN [Transaction_Id] END)
/ COUNTD([Transaction_Id])
```

---

## 6 · Parameters (create via right-click → Create Parameter)

| Parameter Name          | Data Type | Allowable Values         | Default     |
|-------------------------|-----------|--------------------------|-------------|
| `[P: Select Year]`      | Integer   | List: 2021, 2022, 2023, 2024 | 2024    |
| `[P: Select Region]`    | String    | List: All regions + "All" | "All"      |
| `[P: Top N Categories]` | Integer   | Range 1–10               | 5           |
| `[P: KPI Toggle]`       | String    | Net Sales, Profit, Margin | Net Sales  |

### [Parameter-Driven KPI]
```
IF [P: KPI Toggle] = "Net Sales" THEN SUM([Net_Sales])
ELSEIF [P: KPI Toggle] = "Profit"    THEN SUM([Net_Profit])
ELSE SUM([Net_Profit]) / SUM([Net_Sales])
END
```
**Usage:** Swap the measure displayed in View 3 without rebuilding the chart.

---

## 7 · Quick LOD Examples

### Sales per State (fixed LOD)
```
{ FIXED [State] : SUM([Net_Sales]) }
```
**Usage:** Place on the filled map to color by total state sales — avoids  
aggregation issues when other filters are active.

### Avg Transaction Value by Category (fixed LOD)
```
{ FIXED [Product_Category] : AVG([Net_Sales]) }
```

---

*Last updated: 2024 | Pharmacy Analytics Dashboard v1.0*
