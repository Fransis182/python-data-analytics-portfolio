import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


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
# 6. VISUALIZATIONS
# ============================================================

def plot_daily_revenue(df, output_folder="visualizations"):
    """
    Creates and saves a line chart of daily revenue.
    """

    daily = get_daily_revenue(df)

    base_path = Path(__file__).resolve().parent
    out_dir = base_path / output_folder
    out_dir.mkdir(exist_ok=True)

    output_path = out_dir / "daily_revenue.png"

    plt.figure(figsize=(8, 4))
    plt.plot(daily["date"], daily["revenue"], marker="o")
    plt.title("Daily Revenue")
    plt.xlabel("Date")
    plt.ylabel("Revenue (€)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[✔] Daily revenue chart saved to: {output_path}")


def plot_revenue_by_product(df, output_folder="visualizations"):
    """
    Creates and saves a bar chart of revenue by product.
    """

    product_summary = (
        df.groupby("product")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    base_path = Path(__file__).resolve().parent
    out_dir = base_path / output_folder
    out_dir.mkdir(exist_ok=True)

    output_path = out_dir / "revenue_by_product.png"

    plt.figure(figsize=(6, 4))
    plt.bar(product_summary["product"], product_summary["revenue"])
    plt.title("Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue (€)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[✔] Revenue by product chart saved to: {output_path}")


def plot_revenue_by_region(df, output_folder="visualizations"):
    """
    Creates and saves a bar chart of revenue by region.
    """

    region_summary = (
        df.groupby("region")["revenue"]
        .sum()
        .reset_index()
        .sort_values("revenue", ascending=False)
    )

    base_path = Path(__file__).resolve().parent
    out_dir = base_path / output_folder
    out_dir.mkdir(exist_ok=True)

    output_path = out_dir / "revenue_by_region.png"

    plt.figure(figsize=(6, 4))
    plt.bar(region_summary["region"], region_summary["revenue"])
    plt.title("Revenue by Region")
    plt.xlabel("Region")
    plt.ylabel("Revenue (€)")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"[✔] Revenue by region chart saved to: {output_path}")


def print_dashboard(df):
    """
    Print a concise dashboard to the console: KPIs, top products and top regions.
    """
    kpis = calculate_kpis(df)

    print("\n" + "="*60)
    print("SALES DASHBOARD - SUMMARY")
    print("="*60)

    for key, value in kpis.items():
        print(f" - {key}: {value}")

    # Top products
    prod_summary = get_product_summary(df).head(5)
    print("\nTop 5 products by revenue:")
    print(prod_summary.to_string(index=False))

    # Top regions
    region_summary = get_region_summary(df).head(5)
    print("\nTop regions by revenue:")
    print(region_summary.to_string(index=False))

    print("="*60)





# ============================================================
# 7. RUN SCRIPT
# ============================================================

if __name__ == "__main__":
    df = load_sales_data()

    if df is not None:
        print_dashboard(df)
        # Generate charts
        plot_daily_revenue(df)
        plot_revenue_by_product(df)
        plot_revenue_by_region(df)
    else:
        print("Failed to load dataset.")