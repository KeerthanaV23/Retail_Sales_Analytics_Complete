import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Retail Sales Analytics", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Revenue"] = df["Quantity"] * df["Unit_Price"]
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

st.title("📊 Retail Sales & Customer Analytics Dashboard")
st.caption("Data-driven insights for sales, customers, products and regions")

# Filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))

filtered = df[df["Region"].isin(regions) & df["Category"].isin(categories)]

total_revenue = filtered["Revenue"].sum()
total_orders = filtered["Order_ID"].nunique()
total_units = filtered["Quantity"].sum()
avg_order = total_revenue / total_orders if total_orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Orders", f"{total_orders:,}")
c3.metric("Units Sold", f"{total_units:,}")
c4.metric("Average Order Value", f"₹{avg_order:,.0f}")

st.divider()

monthly = filtered.groupby("Month", as_index=False)["Revenue"].sum()
fig_month = px.line(monthly, x="Month", y="Revenue", markers=True, title="Monthly Revenue Trend")
st.plotly_chart(fig_month, use_container_width=True)

col1, col2 = st.columns(2)

category = filtered.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
fig_cat = px.bar(category, x="Category", y="Revenue", title="Revenue by Category", text_auto=".2s")
col1.plotly_chart(fig_cat, use_container_width=True)

region = filtered.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
fig_region = px.bar(region, x="Region", y="Revenue", title="Revenue by Region", text_auto=".2s")
col2.plotly_chart(fig_region, use_container_width=True)

st.subheader("🏆 Top Products")
products = (
    filtered.groupby("Product", as_index=False)
    .agg(Revenue=("Revenue", "sum"), Units_Sold=("Quantity", "sum"))
    .sort_values("Revenue", ascending=False)
    .head(10)
)
st.dataframe(products, use_container_width=True, hide_index=True)

st.subheader("👥 Customer Insights")
customer_count = filtered["Customer_ID"].nunique()
repeat_customers = filtered.groupby("Customer_ID")["Order_ID"].nunique().gt(1).sum()
a, b = st.columns(2)
a.metric("Unique Customers", f"{customer_count:,}")
b.metric("Repeat Customers", f"{repeat_customers:,}")

st.subheader("📌 Business Insights")
if not filtered.empty:
    best_category = category.iloc[0]["Category"]
    best_region = region.iloc[0]["Region"]
    best_product = products.iloc[0]["Product"]
    st.write(f"- **Best category:** {best_category}")
    st.write(f"- **Best-performing region:** {best_region}")
    st.write(f"- **Top product by revenue:** {best_product}")
    st.write("- The dashboard can be used to compare sales performance and identify areas needing attention.")

with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)
