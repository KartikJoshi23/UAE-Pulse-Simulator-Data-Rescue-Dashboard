<div align="center">

# 🇦🇪 UAE Pulse Simulator + Data Rescue Dashboard

### Transform Messy E-Commerce Data into Actionable Insights

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Click_Here-brightgreen?style=for-the-badge)](https://uae-pulse-simulator-data-rescue-dashboard.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<p align="center">
  <img src="https://img.shields.io/badge/Data_Issues_Detected-15+-purple?style=flat-square" alt="Issues">
  <img src="https://img.shields.io/badge/Campaign_Simulator-✓-blue?style=flat-square" alt="Simulator">
  <img src="https://img.shields.io/badge/Real--time_Analytics-✓-green?style=flat-square" alt="Analytics">
  <img src="https://img.shields.io/badge/UAE_Focused-🇦🇪-red?style=flat-square" alt="UAE">
</p>

---

**[Explore Demo](https://uae-pulse-simulator-data-rescue-dashboard.streamlit.app/)**

---

</div>

## 📸 Dashboard Preview

<div align="center">
<table>
<tr>
<td width="50%">

### 🧹 Data Rescue View

*Detect and fix 15+ types of data quality issues*

</td>
<td width="50%">

### 📊 Executive & Manager Analytics

*Financial, Strategic, Operations, Execution*

</td>
</tr>
<tr>
<td width="50%">

### 🎯 Campaign Simulator

*What-if scenarios for promotions*

</td>
<td width="50%">

### 📈 Performance KPIs

*Real-time business metrics*

</td>
</tr>
</table>
</div>

---

## 📋 Table of Contents

<details>
<summary>Click to expand</summary>

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🧹 Data Cleaning Rules](#-data-cleaning-rules)
- [🎯 Campaign Simulator](#-campaign-simulator)
- [🧠 Critical Thinking](#-critical-thinking)
- [⚠️ Limitations](#️-limitations)
- [🗺️ Roadmap](#️-roadmap)
- [👥 Team](#-team)
- [📄 License](#-license)

</details>

---

## ✨ Features

<table>
<tr>
<td>

### 📂 Data Management
- Upload CSV/Excel files
- Generate random sample data
- Preview & validate datasets
- Export cleaned data

</td>
<td>

### 🧹 Data Rescue
- Detect 15+ issue types
- One-click auto-fix
- Before/after comparison
- Detailed issue reports

</td>
</tr>
<tr>
<td>

### 🎯 Campaign Simulator
- Demand lift modeling
- ROI forecasting
- What-if scenarios
- Risk warnings

</td>
<td>

### 📊 Analytics
- Revenue trends
- City/Channel breakdown
- Inventory health
- Pareto analysis

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Option 1: Use Live Demo (Recommended)

👉 **[Launch Dashboard](https://uae-pulse-simulator-data-rescue-dashboard.streamlit.app/)** — No installation required!

### Option 2: Run Locally

**Step 1: Clone the repository**
```bash
git clone https://github.com/yourusername/UAE-Pulse-Simulator-Data-Rescue-Dashboard.git
cd UAE-Pulse-Simulator-Data-Rescue-Dashboard
```

**Step 2: Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate
```
> On Windows use: `venv\Scripts\activate`

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the dashboard**
```bash
streamlit run app.py
```

### Option 3: Docker

```bash
docker build -t uae-pulse-dashboard .
docker run -p 8501:8501 uae-pulse-dashboard
```

---

## 🛠️ Tech Stack

| Category | Technologies |
|:--------:|:-------------|
| **Frontend** | Streamlit |
| **Backend** | Python, Pandas, NumPy |
| **Visualization** | Plotly |
| **Data Source** | Google Sheets, CSV |
| **Deployment** | Streamlit Cloud |

---

## 📂 Project Structure

```
UAE-Pulse-Simulator-Data-Rescue-Dashboard/
│
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # Documentation
│
├── data/                     # Sample datasets
│   ├── products.csv
│   ├── stores.csv
│   ├── sales_raw.csv
│   └── inventory_snapshot.csv
│
├── assets/                   # Images and static files
│   └── logo.png
│
└── .streamlit/               # Streamlit configuration
    └── config.toml
```

---

## 🧹 Data Cleaning Rules

The dashboard detects and fixes **15+ types** of data quality issues:

<details>
<summary><b>Click to see all issue types</b></summary>

| # | Issue Type | Description | Auto-Fix Action |
|:-:|:-----------|:------------|:----------------|
| 1 | MISSING_VALUES | NULL/NaN in required fields | Flag or fill with default |
| 2 | NULL_REPRESENTATIONS | Strings like 'N/A', 'null', '-' | Convert to NULL |
| 3 | DUPLICATE_ORDER_ID | Duplicate transaction records | Remove duplicates |
| 4 | INVALID_TIMESTAMP | Unparseable date formats | Flag for review |
| 5 | FUTURE_DATE_OUTLIER | Dates in the future | Cap to current date |
| 6 | WHITESPACE | Leading/trailing spaces | Trim whitespace |
| 7 | MIXED_CASE | Inconsistent capitalization | Standardize case |
| 8 | INVALID_SKU_FK | SKU not in products table | Flag violation |
| 9 | INVALID_STORE_FK | Store ID not in stores table | Flag violation |
| 10 | OUTLIER_PRICE | Prices beyond 3 std deviations | Cap to threshold |
| 11 | OUTLIER_QTY | Quantities beyond normal range | Cap to threshold |
| 12 | NEGATIVE_PRICE | Negative price values | Convert to zero |
| 13 | NEGATIVE_QTY | Negative quantities | Convert to zero |
| 14 | COST_EXCEEDS_PRICE | Unit cost > selling price | Flag for review |
| 15 | BOOLEAN_STRINGS | 'Yes'/'No' instead of True/False | Convert to boolean |

</details>

---

## 🎯 Campaign Simulator

### How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   INPUT         │    │   CALCULATION   │    │   OUTPUT        │
│                 │    │                 │    │                 │
│ • Discount %    │───▶│ • Demand Lift   │───▶│ • Expected Rev  │
│ • Category      │    │ • Elasticity    │    │ • Profit/Loss   │
│ • Channel       │    │ • Cannibtic.    │    │ • ROI %         │
│ • Duration      │    │                 │    │ • Warnings      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Formulas

| Metric | Formula |
|:-------|:--------|
| **Demand Lift** | Base Sales × Uplift Multiplier × Channel Efficiency |
| **Cannibalization** | Lifted Sales × 0.20 (20% would buy anyway) |
| **Net Incremental** | Lifted Sales - Cannibalized Sales |
| **ROI** | (Incremental Profit - Promo Cost) / Promo Cost × 100% |

---

## 🧠 Critical Thinking

<details>
<summary><b>Q1: Which cleaning rules could change business decisions the most?</b></summary>

### Top 3 High-Impact Cleaning Rules

**1. Payment Status Filtering (Highest Impact)**
- Keeping only "Paid" orders vs including "Pending"
- Could swing revenue calculations by 10-30%
- Risk: CEO approves expansion based on inflated numbers

**2. Negative/Zero Price Handling**
- Negatives often represent returns or adjustments
- Zeroing them out inflates margins artificially
- Risk: Pricing manager sees false profitability

**3. Duplicate Order Handling**
- System glitches create duplicate records
- Inflates demand signals for inventory planning
- Risk: Ordering 2x inventory needed

**Our Decision:** Conservative approach — filter to Paid only, cap negatives at zero. Understating revenue is safer for cash flow planning.

</details>

<details>
<summary><b>Q2: What uplift assumptions did you choose, and how could they be wrong?</b></summary>

### Our Assumptions

| Parameter | Value | Rationale |
|:----------|:------|:----------|
| Baseline Conversion | 2% | Industry average |
| Small Discount Uplift (<20%) | 1.5x | Conservative |
| Deep Discount Uplift (>40%) | 2.5x | Aggressive |
| Cannibalization Rate | 20% | Standard assumption |
| Margin Floor | 15% | Below = unprofitable |

### How They Could Be Wrong

| Assumption | Reality | Impact |
|:-----------|:--------|:-------|
| Uniform 1.5-2.5x uplift | Fashion: 3-4x, Grocery: 1.2x | Over/undervalue promos |
| Flat 20% cannibalization | Timing-dependent (20-40%) | Misstate incremental value |
| Ignore halo effects | Accessories bought with discounted TV | Undervalue promos by 20-30% |
| Past = Future | Novelty effect fades with repetition | Overestimate repeat promos |

**If we had more time:** Segment by category, seasonality, and promo frequency.

</details>

<details>
<summary><b>Q3: Fixed budget — margin floor vs stockout risk?</b></summary>

### Our Tiered Strategy

**Budget Allocation:**
- **Top 20% Products (Revenue Drivers):** 60% budget → Prevent Stockouts
  - Why? Lost sale = lost basket + lost customer
- **Mid-tier Products:** 30% budget → Protect Margins
  - Why? Don't need traffic, need profit
- **Long-tail Products:** 10% budget → Minimal investment
  - Why? Low volume, low impact either way

### Math Example

| Scenario | Calculation | Cost |
|:---------|:------------|:-----|
| Stockout (3 days) | 30 sales × \$25 profit × 1.3 (customer loss) | **\$975** |
| Unnecessary 10% discount | 30 units × \$5 discount | **\$150** |

**Conclusion:** For high-velocity items, stockout prevention wins.

</details>

<details>
<summary><b>Q4: What did you exclude for scope control (2-hour limit)?</b></summary>

### ❌ Excluded Features

| Feature | Time Required | Why Excluded |
|:--------|:--------------|:-------------|
| User Authentication | 2+ hours | Not critical for demo |
| Write-back to Sheets | 1.5 hours | Read-only sufficient |
| ML Forecasting | 4+ hours | Complex pipeline |
| Email Alerts | 2+ hours | Infrastructure needed |
| Multi-currency | 1 hour | AED only for UAE focus |
| PDF Export | 1.5 hours | Interactive view enough |
| Mobile Optimization | 2+ hours | Desktop analysts |

### ⚡ Technical Shortcuts
- Hardcoded sheet names
- No caching layer
- Generic error messages
- Manual testing only
- Sequential data loading

### 🎯 If We Had 2 More Hours

| Addition | Time | Value |
|:---------|:-----|:------|
| Data caching | 30 min | Performance |
| CSV export buttons | 30 min | User convenience |
| Global date filter | 45 min | Better UX |
| Error logging | 15 min | Debugging |

</details>

---

## ⚠️ Limitations

| Limitation | Impact | Workaround |
|:-----------|:-------|:-----------|
| Batch refresh only | No real-time updates | Manual refresh |
| Google Sheets source | Size limits | Use CSV for large data |
| No access control | Single user | Deploy privately |
| Performance >100K rows | Charts slow down | Filter data first |

---

## 🗺️ Roadmap

- [x] Core dashboard functionality
- [x] 15+ data cleaning rules
- [x] Campaign simulator
- [x] Manager analytics view
- [ ] BigQuery connector
- [ ] Redis caching
- [ ] Anomaly detection (ML)
- [ ] Mobile responsive
- [ ] Slack/Teams alerts
- [ ] Multi-language support

---

## 👥 Team

<div align="center">
<table>
<tr>
<td align="center">
<img src="https://via.placeholder.com/100/6c5ce7/ffffff?text=GS" width="100px;" alt=""/><br />
<sub><b>Gagandeep Singh</b></sub><br />
<sub>Data Engineering</sub>
</td>
<td align="center">
<img src="https://via.placeholder.com/100/00b894/ffffff?text=KJ" width="100px;" alt=""/><br />
<sub><b>Kartik Joshi</b></sub><br />
<sub>Analytics</sub>
</td>
<td align="center">
<img src="https://via.placeholder.com/100/0984e3/ffffff?text=SA" width="100px;" alt=""/><br />
<sub><b>Samuel Alex</b></sub><br />
<sub>Visualization</sub>
</td>
<td align="center">
<img src="https://via.placeholder.com/100/e17055/ffffff?text=PK" width="100px;" alt=""/><br />
<sub><b>Prem Kukreja</b></sub><br />
<sub>Business Logic</sub>
</td>
</tr>
</table>

**Course:** MAIB | **Date:** January 2025 | **Development Time:** ~2 hours

</div>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) — Amazing framework for data apps
- [Plotly](https://plotly.com) — Beautiful interactive visualizations
- Course instructors — For the challenge prompt

---

<div align="center">

### ⭐ Star this repo if you found it helpful!

**Made with ❤️ in UAE**

</div>
