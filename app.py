import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="Executive Sales & Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# 2. Generate or Load E-Commerce Dataset
@st.cache_data
def load_data():
    np.random.seed(42)
    n_rows = 1500
    dates = pd.date_range(start="2024-01-01", periods=n_rows, freq="h")
    
    regions = ["North", "South", "East", "West"]
    categories = {
        "Technology": ["Laptops", "Phones", "Accessories"],
        "Furniture": ["Chairs", "Tables", "Bookcases"],
        "Office Supplies": ["Storage", "Binders", "Paper"]
    }
    
    data = []
    for i in range(n_rows):
        cat = np.random.choice(list(categories.keys()))
        sub_cat = np.random.choice(categories[cat])
        sales = np.round(np.random.uniform(20, 1200), 2)
        margin = np.random.uniform(-0.15, 0.40)
        profit = np.round(sales * margin, 2)
        region = np.random.choice(regions)
        customer_type = np.random.choice(["Consumer", "Corporate", "Home Office"])
        
        data.append([dates[i], region, cat, sub_cat, customer_type, sales, profit])
        
    df = pd.DataFrame(data, columns=["Date", "Region", "Category", "SubCategory", "Segment", "Sales", "Profit"])
    df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)
    return df

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🔍 Dashboard Filters")
selected_region = st.sidebar.multiselect(
    "Select Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Filter Data
filtered_df = df[(df["Region"].isin(selected_region)) & (df["Category"].isin(selected_category))]

# 4. Header & Top-Level KPIs
st.title("📊 Executive Sales & Profitability Analytics Dashboard")
st.markdown("Interactive commercial performance analytics tracking key operational metrics.")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Profit Margin", f"{profit_margin:.1f}%")
col4.metric("Transactions", f"{total_orders:,}")

st.markdown("---")

# 5. Visualizations Section
row1_col1, row1_col2 = st.columns([1, 1])

with row1_col1:
    st.subheader("Monthly Revenue Trajectory")
    monthly_sales = filtered_df.groupby("YearMonth")["Sales"].sum().reset_index()
    fig_trend = px.line(
        monthly_sales, 
        x="YearMonth", 
        y="Sales", 
        title="Revenue by Month", 
        markers=True,
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with row1_col2:
    st.subheader("Sales by Customer Segment")
    segment_sales = filtered_df.groupby("Segment")["Sales"].sum().reset_index()
    fig_pie = px.pie(
        segment_sales, 
        values="Sales", 
        names="Segment", 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_pie, use_container_width=True)

row2_col1, row2_col2 = st.columns([1, 1])

with row2_col1:
    st.subheader("Profitability by Sub-Category")
    subcat_perf = filtered_df.groupby("SubCategory")[["Sales", "Profit"]].sum().reset_index()
    fig_bar = px.bar(
        subcat_perf, 
        x="SubCategory", 
        y="Profit", 
        color="Profit",
        color_continuous_scale="RdBu",
        title="Net Profit by Product Line"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with row2_col2:
    st.subheader("Regional Performance Breakdown")
    region_perf = filtered_df.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
    fig_reg = px.bar(
        region_perf, 
        x="Region", 
        y="Sales", 
        color="Region",
        title="Regional Sales Volume"
    )
    st.plotly_chart(fig_reg, use_container_width=True)

# 6. Raw Data Table
with st.expander("📄 View Filtered Data Table"):
    st.dataframe(filtered_df)