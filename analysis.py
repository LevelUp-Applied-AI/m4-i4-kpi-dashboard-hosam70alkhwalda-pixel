"""Integration 4 — KPI Dashboard: Amman Digital Market Analytics

Extract data from PostgreSQL, compute KPIs, run statistical tests,
and create visualizations for the executive summary.

Usage:
    python analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sqlalchemy import create_engine, engine


def connect_db():
    """Create a SQLAlchemy engine connected to the amman_market database.

    Returns:
        engine: SQLAlchemy engine instance

    Notes:
        Use DATABASE_URL environment variable if set, otherwise default to:
        postgresql://postgres:postgres@localhost:5432/amman_market
    """
    engine = create_engine(
        "postgresql+psycopg://postgres:postgres@localhost:5432/amman_market"
    )
    return engine   


def extract_data(engine):
    """Extract all required tables from the database into DataFrames.

    Args:
        engine: SQLAlchemy engine connected to amman_market

    Returns:
        dict: mapping of table names to DataFrames
    """
    customers = pd.read_sql("SELECT * FROM customers", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    orders = pd.read_sql("SELECT * FROM orders", engine)
    order_items = pd.read_sql("SELECT * FROM order_items", engine)

    orders = orders[orders['status'] != 'cancelled']
    order_items = order_items[order_items['quantity'] <= 100]
    customers['city'] = customers['city'].fillna('Unknown')

    return {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items
    }


def compute_kpis(data_dict):
    """Compute the 5 KPIs defined in kpi_framework.md."""
    customers = data_dict['customers']
    products = data_dict['products']
    orders = data_dict['orders']
    order_items = data_dict['order_items']

    orders = orders[orders['status'] != 'cancelled']
    order_items = order_items[order_items['quantity'] <= 100]

    df = orders.merge(order_items, on='order_id') \
               .merge(products, on='product_id') \
               .merge(customers, on='customer_id')

    df['revenue'] = df['quantity'] * df['unit_price']
    df['city'] = df['city'].fillna('Unknown')

    monthly_revenue = (
        df.groupby(pd.to_datetime(df['order_date']).dt.to_period('M'))['revenue']
        .sum()
        .reset_index()
    )
    monthly_revenue['order_date'] = monthly_revenue['order_date'].astype(str)

    weekly_orders = (
        orders.groupby(pd.to_datetime(orders['order_date']).dt.to_period('W'))['order_id']
        .count()
        .reset_index(name='order_count')
    )
    weekly_orders['order_date'] = weekly_orders['order_date'].astype(str)

    revenue_by_city = (
        df.groupby('city')['revenue']
        .sum()
        .reset_index()
        .sort_values(by='revenue', ascending=False)
    )

    order_category = (
        df.groupby(['order_id', 'category'])['revenue']
        .sum()
        .reset_index()
    )

    aov_by_category = (
        order_category.groupby('category')['revenue']
        .mean()
        .reset_index(name='avg_order_value')
        .sort_values(by='avg_order_value', ascending=False)
    )

    orders_per_customer = (
        orders.groupby('customer_id')['order_id']
        .count()
        .reset_index(name='order_count')
    )

    avg_orders_per_customer = orders_per_customer['order_count'].mean()

    return {
        "monthly_revenue": monthly_revenue,
        "weekly_orders": weekly_orders,
        "revenue_by_city": revenue_by_city,
        "aov_by_category": aov_by_category,
        "customer_purchase_frequency": avg_orders_per_customer
    }


def run_statistical_tests(data_dict):
    """Run hypothesis tests to validate patterns in the data."""
    
    customers = data_dict['customers']
    products = data_dict['products']
    orders = data_dict['orders']
    order_items = data_dict['order_items']

    df = orders.merge(order_items, on='order_id') \
               .merge(products, on='product_id') \
               .merge(customers, on='customer_id')

    df = df[df['status'] != 'cancelled']
    df = df[df['quantity'] <= 100]

    df['revenue'] = df['quantity'] * df['unit_price']
    df['city'] = df['city'].fillna('Unknown')

    # Test 1
    order_city = df.groupby(['order_id', 'city'])['revenue'].sum().reset_index()
    amman = order_city[order_city['city'] == 'Amman']['revenue']
    irbid = order_city[order_city['city'] == 'Irbid']['revenue']

    t_stat, p_value = stats.ttest_ind(amman, irbid, equal_var=False)

    mean_diff = amman.mean() - irbid.mean()
    pooled_std = np.sqrt((amman.std()**2 + irbid.std()**2) / 2)
    cohen_d = mean_diff / pooled_std

    # Test 2
    order_cat = df.groupby(['order_id', 'category'])['revenue'].sum().reset_index()
    groups = [group['revenue'].values for name, group in order_cat.groupby('category')]

    f_stat, p_value_anova = stats.f_oneway(*groups)

    ss_between = sum([len(g) * (g.mean() - order_cat['revenue'].mean())**2 for g in groups])
    ss_total = sum((order_cat['revenue'] - order_cat['revenue'].mean())**2)
    eta_squared = ss_between / ss_total

    return {
        "t_test": {
            "t_stat": t_stat,
            "p_value": p_value,
            "cohen_d": cohen_d
        },
        "anova": {
            "f_stat": f_stat,
            "p_value": p_value_anova,
            "eta_squared": eta_squared
        }
    }

def create_visualizations(kpi_results, stat_results, data_dict):
    os.makedirs("output", exist_ok=True)

  
    sns.set_theme(style="whitegrid", palette="colorblind")

    # -----------------------------
    # KPI 1 — Monthly Revenue
    # -----------------------------
    df = kpi_results["monthly_revenue"]

    plt.figure(figsize=(12,6))
    plt.plot(df["order_date"], df["revenue"], marker='o', linewidth=2)

    plt.xticks(df["order_date"][::2], rotation=45)

    plt.title("Monthly Revenue Trend with Noticeable Growth Spikes", fontsize=14, weight='bold')
    plt.xlabel("Month")
    plt.ylabel("Revenue (JOD)")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("output/monthly_revenue.png", dpi=300)
    plt.close()

    # -----------------------------
    # KPI 2 — Weekly Orders
    # -----------------------------
    df = kpi_results["weekly_orders"]

    plt.figure(figsize=(14,6))
    plt.plot(df["order_date"], df["order_count"], marker='o', linewidth=2)


    plt.xticks(df["order_date"][::4], rotation=45)

    plt.title("Weekly Orders Highlight Sudden Demand Spikes", fontsize=14, weight='bold')
    plt.xlabel("Week")
    plt.ylabel("Orders")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("output/weekly_orders.png", dpi=300)
    plt.close()

    # -----------------------------
    # KPI 3 — Revenue by City
    # -----------------------------
    df = kpi_results["revenue_by_city"]

    plt.figure(figsize=(10,6))
    bars = plt.bar(df["city"], df["revenue"])


    for bar in bars:
        bar.set_alpha(0.8)

    plt.title("Revenue is Highly Concentrated in Amman", fontsize=14, weight='bold')
    plt.xlabel("City")
    plt.ylabel("Revenue (JOD)")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig("output/revenue_by_city.png", dpi=300)
    plt.close()

    # -----------------------------
    # KPI 4 — AOV by Category
    # -----------------------------
    df = kpi_results["aov_by_category"]

    plt.figure(figsize=(10,6))
    bars = plt.bar(df["category"], df["avg_order_value"])

    for bar in bars:
        bar.set_alpha(0.8)

    plt.title("Average Order Value Varies Across Product Categories", fontsize=14, weight='bold')
    plt.xlabel("Category")
    plt.ylabel("Average Order Value")
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig("output/aov_by_category.png", dpi=300)
    plt.close()



   
    customers = data_dict['customers']
    products = data_dict['products']
    orders = data_dict['orders']
    order_items = data_dict['order_items']

    df_full = orders.merge(order_items, on='order_id') \
                    .merge(products, on='product_id') \
                    .merge(customers, on='customer_id')

    df_full = df_full[df_full['status'] != 'cancelled']
    df_full = df_full[df_full['quantity'] <= 100]

    df_full['revenue'] = df_full['quantity'] * df_full['unit_price']

    order_cat = df_full.groupby(['order_id', 'category'])['revenue'].sum().reset_index()

    plt.figure(figsize=(10,6))
    sns.boxplot(data=order_cat, x="category", y="revenue")

    plt.title("Distribution of Order Values by Category", fontsize=14, weight='bold')
    plt.xticks(rotation=30)

    plt.tight_layout()
    plt.savefig("output/aov_boxplot.png", dpi=300)
    plt.close()

    # -----------------------------
    # KPI 5 — Customer Frequency
    # -----------------------------
    value = kpi_results["customer_purchase_frequency"]

    plt.figure(figsize=(6,5))
    plt.bar(["Avg Orders per Customer"], [value])

    plt.title("Customers Show Strong Repeat Purchase Behavior (~4.4 Orders)", fontsize=13, weight='bold')
    plt.ylabel("Orders")

    plt.tight_layout()
    plt.savefig("output/customer_frequency.png", dpi=300)
    plt.close()
    
def main():
    """Orchestrate the full analysis pipeline."""
    os.makedirs("output", exist_ok=True)

    engine = connect_db()  
    data_dict = extract_data(engine)

    kpi_results = compute_kpis(data_dict)

    stat_results = run_statistical_tests(data_dict)  

    create_visualizations(kpi_results, stat_results, data_dict)

    print("\n=== KPI SUMMARY ===")
    print("Avg Orders per Customer:", kpi_results["customer_purchase_frequency"])

    print("\n=== STATISTICAL TESTS ===")
    print(stat_results)



if __name__ == "__main__":
    main()
