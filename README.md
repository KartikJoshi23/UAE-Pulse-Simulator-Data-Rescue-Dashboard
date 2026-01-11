# 🛒 UAE Pulse - Retail Simulator & Data Rescue Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![Plotly](https://img.shields.io/badge/Plotly-5.0+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**A powerful retail analytics dashboard for UAE market with data cleaning, KPI tracking, and campaign simulation capabilities.**

[Live Demo](https://uae-pulse-simulator-data-rescue-dashboard.streamlit.app/) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Data Schema](#-data-schema)
- [Dashboard Views](#-dashboard-views)
- [Campaign Simulator](#-campaign-simulator)
- [Data Cleaning](#-data-cleaning)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

UAE Pulse is a comprehensive retail analytics platform designed for the UAE market. It combines:

- **Data Rescue**: Clean messy retail data with automated issue detection
- **Analytics Dashboard**: Executive and Manager views with interactive charts
- **Campaign Simulator**: Run what-if scenarios for promotional campaigns

Perfect for retail managers, data analysts, and business executives who need actionable insights from their sales, inventory, and store data.

---

## ✨ Features

### 📊 Dashboard Views

| View | Purpose | Key Metrics |
|------|---------|-------------|
| **Executive View** | Strategic financial overview | Revenue, Margins, Profit, Discounts |
| **Manager View** | Operational insights | Stockout Risk, Inventory, Data Quality |

### 📈 Interactive Charts

- **Waterfall Chart** - Profit bridge analysis (Revenue → COGS → Net Profit)
- **Revenue Trend** - Daily/Weekly/Monthly grouping options
- **Gross Margin by Category** - Top N selector with sorting
- **Sunburst Chart** - Drill-down: City → Channel → Category
- **Discount Impact Analysis** - Adjustable margin floor slider
- **Stockout Risk Gauge** - Real-time inventory risk assessment
- **Demand vs Stock** - Dual Y-axis comparison
- **Pareto Analysis** - Data quality issues (80/20 rule)

### 🎛️ Filtering System

| Filter Type | Description |
|-------------|-------------|
| **Global Filters** | City, Channel, Category - apply to all charts |
| **Local Filters** | Chart-specific controls (Top N, Sort, Time grouping) |

### 🧹 Data Cleaning

Automatic detection and fixing of:

- ❌ Missing values (unit cost, discount, timestamps)
- ❌ Invalid timestamps (out of range dates)
- ❌ Negative stock values
- ❌ Extreme outliers (quantity, price, stock)
- ❌ Duplicate order IDs

### 🎯 Campaign Simulator

Run what-if scenarios with:

- Discount percentage (0-50%)
- Promo budget allocation
- Margin floor constraints
- City/Channel/Category targeting
- Campaign duration

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive visualizations |
| **Plotly Express** | Quick chart creation |

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/uae-pulse-simulator-data-rescue-dashboard.git
cd uae-pulse-simulator-data-rescue-dashboard
