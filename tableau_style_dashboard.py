
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Skyline Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("May Cohort Sales_data.xlsx", sheet_name="sales_data")
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    df.dropna(subset=['price', 'quantity'], inplace=True)
    df['revenue'] = df['price'] * df['quantity']
    df['month'] = df['sale_date'].dt.to_period("M").astype(str)
    return df

df = load_data()

st.title("📊 Skyline Sales Dashboard")

# Inline Filters (no sidebar)
cols = st.columns(3)
with cols[0]:
    selected_category = st.multiselect("Category", options=df['category'].unique(), default=list(df['category'].unique()))
with cols[1]:
    selected_product = st.multiselect("Product", options=df['product'].unique(), default=list(df['product'].unique()))
with cols[2]:
    selected_month = st.multiselect("Month", options=sorted(df['month'].unique()), default=sorted(df['month'].unique()))

# Filtered Data
filtered_df = df[
    (df['category'].isin(selected_category)) &
    (df['product'].isin(selected_product)) &
    (df['month'].isin(selected_month))
]

# KPIs
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("💰 Total Revenue", f"${filtered_df['revenue'].sum():,.2f}")
kpi2.metric("📦 Units Sold", int(filtered_df['quantity'].sum()))
kpi3.metric("🧾 Orders", filtered_df.shape[0])

st.markdown("---")

# Revenue Over Time
st.subheader("📆 Monthly Revenue Trend")
monthly = filtered_df.groupby('month')['revenue'].sum().reset_index()
fig_monthly = px.line(monthly, x='month', y='revenue', markers=True)
st.plotly_chart(fig_monthly, use_container_width=True)

# 2-Column Charts (Top Products & Category Pie)
col4, col5 = st.columns(2)

with col4:
    st.subheader("🏆 Top 5 Products")
    top_products = filtered_df.groupby('product')['revenue'].sum().nlargest(5).reset_index()
    fig_top = px.bar(top_products, x='product', y='revenue', title="Top 5 Products by Revenue")
    st.plotly_chart(fig_top, use_container_width=True)

with col5:
    st.subheader("📂 Category Revenue Share")
    cat_revenue = filtered_df.groupby('category')['revenue'].sum().reset_index()
    fig_cat = px.pie(cat_revenue, names='category', values='revenue')
    st.plotly_chart(fig_cat, use_container_width=True)

# 2-Column Charts (Heatmap & Pareto)
col6, col7 = st.columns(2)

with col6:
    st.subheader("🌡️ Category vs. Month Heatmap")
    heatmap_data = filtered_df.groupby(['category', 'month'])['revenue'].sum().reset_index()
    pivot = heatmap_data.pivot(index='category', columns='month', values='revenue').fillna(0)
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Viridis'
    ))
    fig_heatmap.update_layout(xaxis_title="Month", yaxis_title="Category")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col7:
    st.subheader("📊 Pareto Analysis")
    pareto = filtered_df.groupby('product')['revenue'].sum().sort_values(ascending=False).reset_index()
    pareto['cumulative_pct'] = pareto['revenue'].cumsum() / pareto['revenue'].sum() * 100
    fig_pareto = px.line(pareto, x='product', y='cumulative_pct')
    fig_pareto.add_bar(x=pareto['product'], y=pareto['revenue'], name="Revenue")
    fig_pareto.update_layout(yaxis_title="Cumulative % / Revenue", xaxis_title="Product")
    st.plotly_chart(fig_pareto, use_container_width=True)

# Data Quality + Raw
with st.expander("📋 View Raw Data & Missing Summary"):
    st.write("Missing Data:")
    st.write(df.isnull().sum()[df.isnull().sum() > 0])
    st.dataframe(filtered_df)
