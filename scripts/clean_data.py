"""
Task 1 - Data Cleaning in Python (Pandas)
Run from the project folder:
    python scripts/clean_data.py
"""
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = BASE_DIR / "data" / "raw_sales_data.csv"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "cleaned_sales_data.csv"

PRODUCT_CATEGORY = {
    "Laptop": "Electronics", "Smartphone": "Electronics",
    "Headphones": "Electronics", "Office Chair": "Furniture",
    "Desk": "Furniture", "Notebook": "Stationery",
    "Pen Pack": "Stationery", "Backpack": "Accessories"
}
PRODUCT_PRICE = {
    "Laptop": 52000, "Smartphone": 22000, "Headphones": 1800,
    "Office Chair": 6500, "Desk": 9000, "Notebook": 80,
    "Pen Pack": 120, "Backpack": 1400
}

def parse_money(value):
    if pd.isna(value):
        return pd.NA
    value = str(value).replace("₹", "").replace(",", "").replace(" ", "")
    return pd.to_numeric(value, errors="coerce")

def parse_discount(value):
    if pd.isna(value):
        return pd.NA
    value = str(value).strip()
    if value.endswith("%"):
        return pd.to_numeric(value[:-1], errors="coerce") / 100
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return pd.NA
    return number / 100 if number > 1 else number

def main():
    df = pd.read_csv(INPUT_FILE)
    original_rows = len(df)
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Standardize text fields
    for col in ["product", "category", "customer_name", "region", "payment_method"]:
        df[col] = df[col].astype("string").str.strip().str.title()
        df[col] = df[col].replace({"<NA>": pd.NA, "Nan": pd.NA})

    df["order_id"] = df["order_id"].astype(str).str.strip().str.upper()

    # Convert mixed date, quantity, price and discount formats
    try:
        df["order_date"] = pd.to_datetime(
            df["order_date"], format="mixed", dayfirst=True, errors="coerce"
        )
    except TypeError:  # fallback for older pandas versions
        df["order_date"] = pd.to_datetime(
            df["order_date"], dayfirst=True, errors="coerce"
        )

    df["quantity"] = pd.to_numeric(
        df["quantity"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
        errors="coerce"
    )
    df["unit_price"] = df["unit_price"].apply(parse_money)
    df["discount"] = df["discount"].apply(parse_discount)

    # Remove duplicate orders (keep the first record for each Order ID)
    before_dedup = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    duplicates_removed = before_dedup - len(df)

    # Use product reference values to fill missing category/price
    df["category"] = df["category"].fillna(df["product"].map(PRODUCT_CATEGORY))
    df["unit_price"] = df["unit_price"].fillna(df["product"].map(PRODUCT_PRICE))

    # Fill remaining missing fields using clear rules
    df["customer_name"] = df["customer_name"].fillna("Unknown")
    df["region"] = df["region"].fillna("Unknown")
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    df["discount"] = df["discount"].fillna(0).clip(0, 1)
    df["quantity"] = df["quantity"].fillna(
        df.groupby("product")["quantity"].transform("median")
    )
    df["quantity"] = df["quantity"].fillna(1).round().astype(int)

    invalid_dates = int(df["order_date"].isna().sum())
    df = df.dropna(subset=["order_date", "product", "unit_price"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]

    # Add calculated sales columns
    df["gross_sales"] = df["quantity"] * df["unit_price"]
    df["net_sales"] = df["gross_sales"] * (1 - df["discount"])
    df["order_date"] = df["order_date"].dt.strftime("%Y-%m-%d")
    df = df.sort_values("order_date").reset_index(drop=True)
    df.to_csv(OUTPUT_FILE, index=False)

    report = [
        "TASK 1 - DATA CLEANING REPORT",
        "-----------------------------",
        f"Rows before cleaning: {original_rows}",
        f"Duplicate orders removed: {duplicates_removed}",
        f"Rows after cleaning: {len(df)}",
        f"Invalid/missing dates removed: {invalid_dates}",
        "",
        "Cleaning steps:",
        "1. Standardized column names and text formatting.",
        "2. Converted mixed date formats into YYYY-MM-DD.",
        "3. Converted quantity, unit price and discount to numeric values.",
        "4. Removed duplicate Order IDs, keeping the first record.",
        "5. Filled missing category and unit price using the product reference.",
        "6. Filled missing customer, region and payment method with 'Unknown'.",
        "7. Filled missing discount with 0 and quantity with product median (or 1).",
        "8. Removed rows with invalid dates, missing product/price, or non-positive values.",
        "9. Added gross_sales and net_sales columns.",
        f"",
        f"Cleaned file: {OUTPUT_FILE}"
    ]
    (OUTPUT_DIR / "cleaning_report.txt").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))

if __name__ == "__main__":
    main()
