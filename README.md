# CodeOrbit Tech - Data Analyst Internship Projects

This folder contains completed practice versions of all 3 tasks from the internship instructions.

## Important
The supplied dataset is **synthetic practice data** created for learning. It is not CodeOrbit Tech's internal or customer data. Replace it with an official dataset if your internship coordinator provides one.

## Project structure

- `data/raw_sales_data.csv` - intentionally messy source dataset for Task 1
- `output/cleaned_sales_data.csv` - cleaned dataset
- `output/cleaning_report.txt` - Task 1 cleaning documentation
- `output/sales_analysis_report.txt` - Task 2 written findings
- `output/monthly_sales.csv` - monthly summary
- `output/sales_by_region.csv` - region summary
- `output/sales_by_category.csv` - category summary
- `output/top_5_products.csv` - top products
- `output/CodeOrbit_Data_Analyst_Dashboard.xlsx` - Task 3 Excel dashboard
- `scripts/clean_data.py` - Task 1 code
- `scripts/sales_analysis.py` - Task 2 code
- `scripts/create_dashboard.py` - Task 3 code

## Requirements

Python 3.10 or newer is recommended.

Install packages in VS Code terminal:

```bash
python -m pip install pandas openpyxl
```

## Run the projects

Open this folder in VS Code. Open Terminal > New Terminal and run these commands one by one:

```bash
python scripts/clean_data.py
python scripts/sales_analysis.py
python scripts/create_dashboard.py
```

If `python` does not work on Windows, try `py` instead:

```bash
py scripts/clean_data.py
py scripts/sales_analysis.py
py scripts/create_dashboard.py
```

Run Task 1 first, then Task 2, then Task 3 because the later tasks use the cleaned dataset.

## Task 1 - Data Cleaning

- Standardizes text and column names.
- Converts dates, quantity, price and discount into consistent formats.
- Removes duplicate Order IDs.
- Fills missing category/price from a product reference.
- Fills other missing values using documented rules.
- Removes unusable rows and calculates gross and net sales.

## Task 2 - Sales Analysis

Calculates:
- Total sales
- Total orders
- Average order value (AOV)
- Total units sold
- Sales by month, region and category
- Top 5 products by sales

## Task 3 - Dashboard

The Excel dashboard includes:
- KPI cards for total sales, orders, average order value and units sold
- Monthly sales trend line chart
- Sales by region bar chart
- Sales share by category doughnut chart
- Top 5 products table

## Before submitting

1. Open the Excel dashboard and check that the charts display correctly.
2. Keep the raw data, cleaned data, reports, scripts and dashboard together.
3. Follow the submission form instructions provided by your internship coordinator.
4. Do not claim the sample data is real company data.
