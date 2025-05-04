# starbucks_dashboard.py

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# Load data
#df = pd.read_csv("C:/Uni_Work/ALY 6040/Module 4/Starbucks_Business_Performance_Data.csv")
df = pd.read_csv("Starbucks_Business_Performance_Data.csv")


# --- Dashboard Planning ---
st.set_page_config(page_title="Starbucks Dashboard", layout="wide")
st.title("Starbucks Business Performance Dashboard")
st.markdown("""
This dashboard analyzes Starbucks' monthly revenue trends, customer engagement, and loyalty program usage across regions.
It helps decision-makers identify performance gaps and drive region-specific strategies.
""")

# --- Sidebar Filters ---
st.sidebar.header(" Filter Options")
selected_regions = st.sidebar.multiselect("Select Region(s):", options=df['Region'].unique(), default=df['Region'].unique())
selected_products = st.sidebar.multiselect("Select Product Category:", options=df['Product_Category'].unique(), default=df['Product_Category'].unique())
selected_months = st.sidebar.multiselect("Select Month(s):", options=df['Month'].unique(), default=df['Month'].unique())

# --- Filtered Data ---
filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Product_Category'].isin(selected_products)) &
    (df['Month'].isin(selected_months))
]

# --- KPI Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered_df['Monthly_Revenue'].sum():,.0f}")
col2.metric("Total Transactions", f"{filtered_df['Transactions'].sum():,}")
col3.metric("Avg Loyalty Users", f"{filtered_df['Loyalty_Users (%)'].mean():.1f}%")

st.markdown("---")

# --- Chart 1: Monthly Revenue Trends ---
st.subheader("Monthly Revenue Trends by Region")
rev_trend = filtered_df.groupby(['Month', 'Region'])['Monthly_Revenue'].sum().reset_index()
chart1 = alt.Chart(rev_trend).mark_line(point=True).encode(
    x='Month:N',
    y='Monthly_Revenue:Q',
    color='Region:N',
    tooltip=['Month', 'Region', 'Monthly_Revenue']
).properties(width=800)
st.altair_chart(chart1)

# --- Chart 2: Avg Daily Customers by Region ---
st.subheader("Total Monthly Customers by Region")
total_customers = filtered_df.groupby('Region')['Transactions'].sum().reset_index()
chart2 = alt.Chart(total_customers).mark_bar().encode(
    x='Transactions:Q',
    y=alt.Y('Region:N', sort='-x'),
    color='Region:N',
    tooltip=['Region', 'Transactions']
).properties(width=700, height=300)
st.altair_chart(chart2)


# --- Chart 3: Loyalty Program Usage (Pie Chart) ---
st.subheader("Revenue vs. Ad Spend by Region")

# Group and prepare data
rev_vs_ad = filtered_df.groupby('Region')[['Monthly_Revenue', 'Ad_Spend']].sum().reset_index()

# Plot with Streamlit’s built-in chart (simple and intuitive)
st.bar_chart(rev_vs_ad.set_index('Region'))



# --- Enhancement 1: Download Filtered Data ---
st.download_button("Download Filtered Data as CSV",
                   data=filtered_df.to_csv(index=False),
                   file_name="filtered_starbucks_data.csv",
                   mime="text/csv")

# --- Enhancement 2: Business Insight Summary ---
st.markdown("### 💡 Executive Insights")
st.markdown("""
- **Revenue Trends:** The **West region** shows consistently strong monthly revenue, indicating effective operations or market dominance. **North and South** show more volatility, which may warrant further investigation or localized marketing efforts.

- **Customer Engagement:** The **South region** has the highest number of total monthly customers, suggesting strong store traffic. This presents an opportunity for upselling or loyalty program expansion in that area.

- **Revenue vs. Ad Spend:** While the **East region** spends heavily on ads, its revenue return is relatively modest. In contrast, the **West region** demonstrates high revenue with comparatively efficient ad spending, highlighting a better marketing ROI.
""")

