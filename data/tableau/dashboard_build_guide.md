# Tableau Dashboard Build Guide
## Pharmacy Sales Analytics — Step-by-Step Instructions

**Prerequisite:** Tableau Desktop 2023.1+ (or Tableau Public 2023.1+)  
**Data file:** `data/pharmacy_sales_clean.csv`

---

## Step 1 — Connect to Data

1. Open Tableau Desktop.  
2. In the **Start** screen, under *Connect*, click **Text File**.  
3. Navigate to `data/pharmacy_sales_clean.csv` and click **Open**.  
4. Tableau loads the Data Source screen. Verify the preview shows 26 columns and 5,000 rows.

### Set Data Types
Click the column-type icon above each field and confirm:

| Column              | Required Type |
|---------------------|---------------|
| Date                | Date          |
| Year                | Number (Whole)|
| Month_Num           | Number (Whole)|
| Quantity            | Number (Whole)|
| Net_Sales           | Number (Decimal)|
| Net_Profit          | Number (Decimal)|
| COGS                | Number (Decimal)|
| Profit_Margin_Pct   | Number (Decimal)|
| Transaction_ID      | String (convert to dimension) |

5. Click the **Sheet 1** tab at the bottom to begin building.

---

## Step 2 — Create All Calculated Fields

> Open each formula from `tableau/calculated_fields.md` and create them via  
> **Analysis → Create Calculated Field** in the menu bar.

**Priority order (create these first):**
1. `[Profit Margin %]`  
2. `[YoY Sales Growth %]`  
3. `[Month-Year Label]`  
4. `[Category Performance Tier]`  
5. `[Parameter-Driven KPI]` (after creating the 4 parameters)

---

## Step 3 — View 1: Monthly Revenue Trend (Line Chart)

**Sheet name:** `Trend Analysis`

1. Drag `[Month-Year Label]` → **Columns** shelf.  
2. Drag `[Net_Sales]` → **Rows** shelf.  
3. Right-click the Y-axis → **Edit Axis** → rename to *Net Sales ($)*.  
4. Drag `[Year]` → **Color** shelf (Marks card). This creates one line per year.  
5. Right-click `[Year]` on Color → **Convert to Discrete**.  
6. In **Marks**, change the mark type dropdown from *Automatic* to **Line**.  
7. Add a **[Rolling 12-Month Sales]** reference:  
   - Drag `[Net_Sales]` to the view again (dual axis).  
   - Right-click new axis → **Add Table Calculation** → **Moving Average** (12 periods).  
   - Right-click → **Dual Axis** → synchronize axes.  
   - Change this second mark type to **Line**, reduce opacity to 40%, dash the line.  
8. Add **[YoY Sales Growth %]** as a **Tooltip** field.  
9. Title the sheet: *"Monthly Net Sales Trend (2021–2024)"*.

**Business Question Answered:** *Are pharmacy revenues growing year-over-year, and are there seasonal spikes?*

---

## Step 4 — View 2: Geographic Analysis (Filled Map)

**Sheet name:** `Geographic Analysis`

1. Double-click `[State]` in the Data pane — Tableau auto-generates a map.  
2. If prompted, set geographic role: right-click `[State]` → **Geographic Role → State/Province**.  
3. Drag `{ FIXED [State] : SUM([Net_Sales]) }` (the LOD field) → **Color** shelf.  
4. Click **Color** → **Edit Colors** → choose a **Sequential** palette (e.g., Blue).  
5. Drag `[Net_Profit]` → **Size** shelf (bubble size reflects profitability).  
6. Drag `[Profit Margin %]` → **Tooltip**.  
7. Drag `[Region]` → **Tooltip**.  
8. Change the map style: **Map → Map Layers** → select *Light* background.  
9. Add a **Region filter**:  
   - Drag `[Region]` → **Filters** shelf → check all → **Show Filter**.  
   - Right-click the filter → *Single Value (List)*.  
10. Title: *"Net Sales by State — Geographic Heatmap"*.

**Business Question Answered:** *Which states and regions generate the most revenue? Where should we expand?*

---

## Step 5 — View 3: Category Performance Breakdown (Bar Chart)

**Sheet name:** `Category Performance`

1. Drag `[Product_Category]` → **Rows**.  
2. Drag `[Net_Sales]` → **Columns**.  
3. Sort descending: click the sort icon on the `[Net_Sales]` axis.  
4. Drag `[Category Performance Tier]` → **Color** shelf.  
   - Set colors: Top Performer = Green, On Target = Blue, Below Target = Orange, Needs Attention = Red.  
5. Drag `[Profit Margin %]` → **Label** shelf. Format as *percentage*.  
6. Add a **Reference Line**:  
   - Right-click the X-axis → **Add Reference Line** → Average → dashed, grey.  
   - Label: *"Avg Category Sales"*.  
7. Drag `[P: Top N Categories]` parameter into a **Top N filter**:  
   - Right-click `[Product_Category]` → **Create Set** → **By field** → Top → By `[Net_Sales]` → link to parameter.  
8. Add dual measure: right-click `[Net_Profit]` → **Add to Rows** → right-click axis → **Dual Axis** → Synchronize.  
   - Change second mark to **Circle** (scatter) to show profit vs. sales simultaneously.  
9. Title: *"Product Category Performance — Sales & Profit Margin"*.

**Business Question Answered:** *Which categories drive the most profit? Are high-revenue categories also high-margin?*

---

## Step 6 — KPI Banner Sheet

**Sheet name:** `KPI Banner`

Create 4 individual **BAN (Big Ass Number)** sheets, then tile them side by side on the dashboard:

| Sheet Name     | Measure                 | Format       |
|----------------|-------------------------|--------------|
| `KPI - Sales`  | `SUM([Net_Sales])`      | `$#,##0.0K`  |
| `KPI - Profit` | `SUM([Net_Profit])`     | `$#,##0.0K`  |
| `KPI - Margin` | `[Profit Margin %]`     | `0.0%`       |
| `KPI - YoY`    | `[YoY Sales Growth %]`  | `+0.0%;-0.0%` |

For each:
1. Drag the measure to the **Text** shelf only.  
2. Go to **Format → Shading** → set background color (dark navy: `#1B2A4A`).  
3. Format text to white, 28pt bold.  
4. Add a subtitle label below in 12pt describing the KPI name.

---

## Step 7 — Assemble the Dashboard

1. Click the **New Dashboard** icon (grid icon at sheet tab bar).  
2. Set size: **Fixed → 1400 × 900 px** (standard widescreen).  
3. Layout structure:

```
┌─────────────────────────────────────────────────────────┐
│  HEADER: Pharmacy Analytics Dashboard   [Logo Placeholder]│
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ KPI      │ KPI      │ KPI      │ KPI      │             │
│ Net Sales│ Net Prof.│ Margin % │ YoY Grwth│  FILTER     │
│          │          │          │          │  PANEL      │
├──────────┴──────────┴──────────┴──────────┤  (Region,   │
│                                           │  Year,      │
│      Trend Analysis (Line Chart)          │  Category,  │
│                                           │  Segment)   │
├───────────────────────┬───────────────────┤             │
│                       │                   │             │
│  Geographic Analysis  │ Category          │             │
│  (Filled Map)         │ Performance       │             │
│                       │ (Bar Chart)       │             │
└───────────────────────┴───────────────────┴─────────────┘
```

4. Drag sheets from the left panel into positions above.  
5. Set all sheets to **Fit Width** (right-click sheet on dashboard → Fit).

---

## Step 8 — Dashboard Actions (Interactivity)

Go to **Dashboard → Actions → Add Action:**

### Action 1 — Region Filter (Map → Bar Chart)
- **Name:** Filter by Region  
- **Source:** Geographic Analysis  
- **Run on:** Select  
- **Target:** Category Performance  
- **Clearing selection:** Show All Values  
- **Filter:** Region field  

### Action 2 — Category Highlight (Bar → Trend)
- **Name:** Highlight Category in Trend  
- **Type:** Highlight  
- **Source:** Category Performance  
- **Target:** Trend Analysis  
- **Run on:** Hover  

### Action 3 — URL Drill-Down (optional)
- **Name:** Open Drug Info  
- **Type:** URL  
- **Source:** Category Performance  
- **URL:** `https://www.drugs.com/search.php?searchterm=<Product_Name>`  
- **Run on:** Menu  

### Action 4 — Filter: Year Selector → All Views
- **Name:** Global Year Filter  
- **Source:** KPI Banner  
- **Run on:** Select  
- **Target:** All Sheets  
- **Filter:** Year  

---

## Step 9 — Formatting & Polish

1. **Dashboard Title:** Insert → Text → "💊 Pharmacy Analytics Dashboard" | font: Georgia 22pt bold, navy `#1B2A4A`.  
2. **Color Palette:** Use a consistent 5-color palette across all sheets:  
   `#1B2A4A` (navy), `#2E8B57` (green), `#E07B39` (amber), `#DC3545` (red), `#6C757D` (grey).  
3. **Borders:** Set sheet padding to 8px. Add a thin border around each chart area.  
4. **Tooltips:** Ensure every view has a well-formatted tooltip:  
   *Category: <Product_Category> | Net Sales: $<Net_Sales> | Margin: <Profit_Margin_Pct>%*  
5. **Legend placement:** Move all legends to the filter panel on the right.  
6. **Grid lines:** Remove most grid lines (Format → Lines → set to None for minor gridlines).

---

## Step 10 — Save & Publish

### Save as Packaged Workbook
- **File → Save As → Tableau Packaged Workbook (.twbx)**  
- Filename: `pharmacy_dashboard.twbx`  
- Save to the `tableau/` folder of this project.

### Publish to Tableau Public (Free)
1. **Server → Tableau Public → Save to Tableau Public As...**  
2. Sign in to your Tableau Public account.  
3. Name the workbook: *"Pharmacy Sales Analytics Dashboard"*  
4. Copy the public URL — paste it into the **README.md** live demo section.

---

## Definition of Done ✅

| Criterion                                              | Status |
|--------------------------------------------------------|--------|
| Dataset loaded with correct data types                | ☐      |
| All 6 calculated fields created and validated          | ☐      |
| Trend line chart with year-over-year color encoding    | ☐      |
| Filled map with state-level sales heatmap             | ☐      |
| Category bar chart with performance tier color coding  | ☐      |
| 4 KPI banners displaying correct aggregations         | ☐      |
| 4 dashboard actions configured and tested             | ☐      |
| Global filters (Region, Year, Segment) functional     | ☐      |
| Dashboard fits 1400×900px without scrolling           | ☐      |
| `.twbx` file saved to `tableau/` folder               | ☐      |
| README updated with Tableau Public link               | ☐      |

---

*Pharmacy Analytics Dashboard v1.0 | Built with Tableau Desktop 2023.3+*
