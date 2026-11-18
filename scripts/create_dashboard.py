"""
Task 3 - Excel Dashboard
Run after Task 1 and Task 2:
    python scripts/create_dashboard.py
"""
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import LineChart, BarChart, DoughnutChart, Reference
from openpyxl.utils import get_column_letter

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = BASE_DIR / "output"
DATA_FILE = OUTPUT_DIR / "cleaned_sales_data.csv"
DASHBOARD_FILE = OUTPUT_DIR / "CodeOrbit_Data_Analyst_Dashboard.xlsx"

def main():
    df = pd.read_csv(DATA_FILE, parse_dates=["order_date"])
    total_sales = df["net_sales"].sum()
    total_orders = df["order_id"].nunique()
    aov = total_sales / total_orders if total_orders else 0
    units = df["quantity"].sum()

    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    monthly = df.groupby("month", as_index=False)["net_sales"].sum()
    region = df.groupby("region", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False)
    category = df.groupby("category", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False)
    top = (df.groupby("product", as_index=False)
             .agg(total_sales=("net_sales", "sum"), units_sold=("quantity", "sum"))
             .sort_values("total_sales", ascending=False).head(5))

    with pd.ExcelWriter(DASHBOARD_FILE, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)
        monthly.to_excel(writer, sheet_name="Monthly Sales", index=False)
        region.to_excel(writer, sheet_name="Region Sales", index=False)
        category.to_excel(writer, sheet_name="Category Sales", index=False)
        top.to_excel(writer, sheet_name="Top Products", index=False)

    wb = load_workbook(DASHBOARD_FILE)
    ws = wb.create_sheet("Dashboard", 0)
    ws.sheet_view.showGridLines = False
    ws.merge_cells("A1:L1")
    ws["A1"] = "CODEORBIT TECH | DATA ANALYST INTERNSHIP"
    ws["A1"].font = Font(bold=True, size=16, color="FFFFFF")
    ws["A1"].fill = PatternFill("solid", fgColor="17324D")
    ws["A1"].alignment = Alignment(horizontal="center")
    ws.merge_cells("A2:L2")
    ws["A2"] = "Sales Performance Dashboard (Practice Dataset | INR)"
    ws["A2"].alignment = Alignment(horizontal="center")

    for start_col, label, value in [
        (1, "TOTAL SALES", f"₹{total_sales:,.0f}"),
        (4, "TOTAL ORDERS", f"{total_orders:,}"),
        (7, "AVERAGE ORDER VALUE", f"₹{aov:,.0f}"),
        (10, "UNITS SOLD", f"{units:,}")
    ]:
        ws.merge_cells(start_row=4, start_column=start_col, end_row=4, end_column=start_col+1)
        ws.cell(4, start_col, label)
        ws.cell(4, start_col).font = Font(bold=True, color="FFFFFF")
        ws.cell(4, start_col).fill = PatternFill("solid", fgColor="0F766E")
        ws.cell(4, start_col).alignment = Alignment(horizontal="center")
        ws.merge_cells(start_row=5, start_column=start_col, end_row=5, end_column=start_col+1)
        ws.cell(5, start_col, value)
        ws.cell(5, start_col).font = Font(bold=True, size=15, color="17324D")
        ws.cell(5, start_col).fill = PatternFill("solid", fgColor="E6F4F1")
        ws.cell(5, start_col).alignment = Alignment(horizontal="center")

    ws.merge_cells("A8:C8")
    ws["A8"] = "TOP 5 PRODUCTS BY SALES"
    ws["A8"].font = Font(bold=True, color="FFFFFF")
    ws["A8"].fill = PatternFill("solid", fgColor="17324D")
    for col, header in enumerate(["Product", "Sales (₹)", "Units Sold"], 1):
        ws.cell(9, col, header).font = Font(bold=True, color="FFFFFF")
        ws.cell(9, col).fill = PatternFill("solid", fgColor="0F766E")
    for row_num, row in enumerate(top.itertuples(index=False), 10):
        ws.cell(row_num, 1, row.product)
        ws.cell(row_num, 2, float(row.total_sales)).number_format = '₹#,##0.00'
        ws.cell(row_num, 3, int(row.units_sold))

    for sheet_name in ["Monthly Sales", "Region Sales", "Category Sales", "Top Products", "Cleaned Data"]:
        sh = wb[sheet_name]
        sh.freeze_panes = "A2"
        sh.auto_filter.ref = sh.dimensions
        for cell in sh[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="17324D")
        for cells in sh.columns:
            width = min(max(max(len(str(c.value or "")) for c in cells) + 2, 12), 28)
            sh.column_dimensions[get_column_letter(cells[0].column)].width = width

    # Monthly sales line chart
    sh = wb["Monthly Sales"]
    chart = LineChart()
    chart.title = "Monthly Sales Trend"
    chart.y_axis.title = "Sales (₹)"
    chart.x_axis.title = "Month"
    chart.height, chart.width = 7, 13
    chart.add_data(Reference(sh, min_col=2, min_row=1, max_row=len(monthly)+1), titles_from_data=True)
    chart.set_categories(Reference(sh, min_col=1, min_row=2, max_row=len(monthly)+1))
    chart.legend = None
    ws.add_chart(chart, "E8")

    # Regional sales bar chart
    sh = wb["Region Sales"]
    chart = BarChart()
    chart.type = "bar"
    chart.title = "Sales by Region"
    chart.x_axis.title = "Sales (₹)"
    chart.y_axis.title = "Region"
    chart.height, chart.width = 7, 12
    chart.add_data(Reference(sh, min_col=2, min_row=1, max_row=len(region)+1), titles_from_data=True)
    chart.set_categories(Reference(sh, min_col=1, min_row=2, max_row=len(region)+1))
    chart.legend = None
    ws.add_chart(chart, "A19")

    # Category share doughnut chart
    sh = wb["Category Sales"]
    chart = DoughnutChart()
    chart.title = "Sales Share by Category"
    chart.height, chart.width = 7, 11
    chart.add_data(Reference(sh, min_col=2, min_row=1, max_row=len(category)+1), titles_from_data=True)
    chart.set_categories(Reference(sh, min_col=1, min_row=2, max_row=len(category)+1))
    chart.holeSize = 55
    ws.add_chart(chart, "G19")

    for col in range(1, 13):
        ws.column_dimensions[get_column_letter(col)].width = 15
    ws.freeze_panes = "A4"
    wb.save(DASHBOARD_FILE)
    print(f"Dashboard created: {DASHBOARD_FILE}")

if __name__ == "__main__":
    main()
