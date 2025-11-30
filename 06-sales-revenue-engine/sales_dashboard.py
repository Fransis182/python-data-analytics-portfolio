import pandas as pd
from pathlib import Path


# ============================================================
# 1. LOAD DATA
# ============================================================

def load_sales_data(file_name="sales_data.csv"):
    """
    Loads sales data from CSV file located in the same folder as this script.
    Returns a pandas DataFrame.
    """
    try:
        # Ruta de la carpeta donde está este archivo .py
        base_path = Path(__file__).resolve().parent
        file_path = base_path / file_name

        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        df['revenue'] = df['units_sold'] * df['unit_price']
        return df
    except Exception as e:
        print("ERROR loading file:", e)
        return None


# ============================================================
# 2. KPI CALCULATIONS
# ============================================================

def calculate_kpis(df):
    """
    Computes overall KPIs:
    - Total revenue
    - Total units sold
    - Average order value
    - Best-selling product
    - Top region by revenue
    """

    total_revenue = df['revenue'].sum()
    total_units = df['units_sold'].sum()
    avg_order_value = df['revenue'].mean()

    best_product = (
        df.groupby("product")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )

    best_region = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .idxmax()
    )

    return {
        "Total Revenue (€)": round(total_revenue, 2),
        "Total Units Sold": int(total_units),
        "Average Order Value (€)": round(avg_order_value, 2),
        "Best-Selling Product": best_product,
        "Top Region by Revenue": best_region,
    }


# ============================================================
# 3. DAILY REVENUE REPORT
# ============================================================

def get_daily_revenue(df):
    """
    Returns daily revenue totals.
    """
    return (
        df.groupby("date")["revenue"]
        .sum()
        .reset_index()
        .sort_values("date")
    )


# ============================================================
# 4. PRODUCT PERFORMANCE REPORT
# ============================================================

def get_product_summary(df):
    """
    Returns revenue and units sold by product.
    """
    return (
        df.groupby("product")
        .agg(
            total_units=("units_sold", "sum"),
            total_revenue=("revenue", "sum"),
            avg_unit_price=("unit_price", "mean")
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )


# ============================================================
# 5. REGIONAL PERFORMANCE REPORT
# ============================================================

def get_region_summary(df):
    """
    Returns revenue and performance per region.
    """
    return (
        df.groupby("region")
        .agg(
            total_units=("units_sold", "sum"),
            total_revenue=("revenue", "sum")
        )
        .sort_values("total_revenue", ascending=False)
        .reset_index()
    )


# ============================================================
# 6. PRINT DASHBOARD
# ============================================================

def print_dashboard(df):
    """
    Prints all reports in a clear BI-style dashboard.
    """

    print("\n")
    print("==========================================================")
    print(" 📊  SALES PERFORMANCE DASHBOARD (Python CLI Version)")
    print("==========================================================\n")

    # KPI SECTION
    kpis = calculate_kpis(df)
    print("🔹 KEY PERFORMANCE INDICATORS:\n")
    for k, v in kpis.items():
        print(f"{k}: {v}")
    print("\n----------------------------------------------------------\n")

    # DAILY REVENUE
    print("📅 DAILY REVENUE:\n")
    print(get_daily_revenue(df).to_string(index=False))
    print("\n----------------------------------------------------------\n")

    # PRODUCT SUMMARY
    print("📦 PRODUCT PERFORMANCE SUMMARY:\n")
    print(get_product_summary(df).to_string(index=False))
    print("\n----------------------------------------------------------\n")

    # REGION SUMMARY
    print("🌍 REGIONAL PERFORMANCE SUMMARY:\n")
    print(get_region_summary(df).to_string(index=False))
    print("\n==========================================================")
    print(" END OF DASHBOARD ")
    print("==========================================================\n")


# ============================================================
# 7. RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    df = load_sales_data()

    if df is not None:
        print_dashboard(df)
    else:
        print("Failed to load dataset.")
