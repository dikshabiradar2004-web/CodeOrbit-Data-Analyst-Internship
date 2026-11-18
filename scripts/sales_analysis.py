"""
Task 2 - Sales Data Analysis using Pandas
Run from the project folder:
    python scripts/sales_analysis.py
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "output" / "cleaned_sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(INPUT_FILE, parse_dates=["order_date"])

    total_sales = df["net_sales"].sum()
    total_orders = df["order_id"].nunique()
    average_order_value = total_sales / total_orders if total_orders else 0
    total_units = df["quantity"].sum()

    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month", as_index=False)["net_sales"].sum()
    by_region = df.groupby("region", as_index=False)["net_sales"].sum()
    by_category = df.groupby("category", as_index=False)["net_sales"].sum()
    top_products = (
        df.groupby("product", as_index=False)
          .agg(total_sales=("net_sales", "sum"),
               units_sold=("quantity", "sum"),
               orders=("order_id", "nunique"))
          .sort_values("total_sales", ascending=False)
          .head(5)
    )

    monthly.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)
    by_region.sort_values("net_sales", ascending=False).to_csv(
        OUTPUT_DIR / "sales_by_region.csv", index=False
    )
    by_category.sort_values("net_sales", ascending=False).to_csv(
        OUTPUT_DIR / "sales_by_category.csv", index=False
    )
    top_products.to_csv(OUTPUT_DIR / "top_5_products.csv", index=False)

    best_product = top_products.iloc[0]["product"] if not top_products.empty else "N/A"
    best_region = by_region.sort_values("net_sales", ascending=False).iloc[0]["region"] if not by_region.empty else "N/A"

    report = f"""
TASK 2 - SALES DATA ANALYSIS REPORT
----------------------------------
Total sales: ₹{total_sales:,.2f}
Total orders: {total_orders}
Average order value: ₹{average_order_value:,.2f}
Total units sold: {total_units}

Top product by sales: {best_product}
Highest-sales region: {best_region}

Files created:
- monthly_sales.csv
- sales_by_region.csv
- sales_by_category.csv
- top_5_products.csv

Interpretation:
The report summarizes sales by month, region, category and product.
Use the output tables to identify high-performing products and regions,
and to compare sales performance over time.
"""
    (OUTPUT_DIR / "sales_analysis_report.txt").write_text(report.strip(), encoding="utf-8")
    print(report)

if __name__ == "__main__":
    main()
