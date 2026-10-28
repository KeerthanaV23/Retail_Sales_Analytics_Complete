```python
import os
import pandas as pd
import streamlit as st
import plotly.express as px


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, "data", "sales_data.csv")

    df = pd.read_csv(data_path)

    return df


df = load_data()


# -----------------------------
# Title
# -----------------------------
st.title("📊 Retail Sales & Customer Analytics Dashboard")
st.caption("Data-driven insights for sales, customers, products and regions")


# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔎 Filters")

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox(
    "Select Region",
    regions
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)


# -----------------------------
# Apply Filters
# -----------------------------
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]


# -----------------------------
# KPI Calculations
# -----------------------------
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["Order_ID"].nunique()
units_sold = filtered_df["Quantity"].sum()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

unique_customers = filtered_df["Customer_ID"].nunique()

customer_orders = (
    filtered_df.groupby("Customer_ID")["Order_ID"]
    .nunique()
)

repeat_customers = (customer_orders > 1).sum()


# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(
    "Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Units Sold",
    f"{units_sold:,}"
)

col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)

col5.metric(
    "Unique Customers",
    f"{unique_customers:,}"
)

col6.metric(
    "Repeat Customers",
    f"{repeat_customers:,}"
)


st.divider()


# -----------------------------
# Monthly Revenue Trend
# -----------------------------
st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df.groupby("Month", as_index=False)["Revenue"]
    .sum()
)

fig_monthly = px.line(
    monthly_revenue,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# -----------------------------
# Product & Category Analysis
# -----------------------------
col1, col2 = st.columns(2)


with col1:
    st.subheader("🏆 Top Products")

    top_products = (
        filtered_df.groupby("Product", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="Revenue",
        y="Product",
        orientation="h",
        title="Top Products by Revenue"
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


with col2:
    st.subheader("📦 Category Performance")

    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Revenue",
        title="Revenue by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# -----------------------------
# Regional Analysis
# -----------------------------
st.subheader("🌍 Regional Performance")

regional_sales = (
    filtered_df.groupby("Region", as_index=False)["Revenue"]
    .sum()
    .sort_values("Revenue", ascending=False)
)

fig_region = px.bar(
    regional_sales,
    x="Region",
    y="Revenue",
    title="Revenue by Region"
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)


# -----------------------------
# Customer Insights
# -----------------------------
st.subheader("👥 Customer Insights")

customer_summary = (
    filtered_df.groupby("Customer_ID")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Revenue", "sum")
    )
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

st.dataframe(
    customer_summary.head(10),
    use_container_width=True
)


# -----------------------------
```python
# -----------------------------
# Business Insights
# -----------------------------
st.subheader("💡 Business Insights")

if not filtered_df.empty:

    best_category = (
        filtered_df.groupby("Category")["Revenue"]
        .sum()
        .idxmax()
    )

    best_region = (
        filtered_df.groupby("Region")["Revenue"]
        .sum()
        .idxmax()
    )

    top_product = (
        filtered_df.groupby("Product")["Revenue"]
        .sum()
        .idxmax()
    )

    st.success(
        f"Best-performing category: **{best_category}**"
    )

    st.info(
        f"Best-performing region: **{best_region}**"
    )

    st.warning(
        f"Top product by revenue: **{top_product}**"
    )

else:
    st.warning("No data available for the selected filters.")


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Retail Sales Analytics Dashboard | "
    "Built with Python, Pandas, Plotly and Streamlit"
)
```