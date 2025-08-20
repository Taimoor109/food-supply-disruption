# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load data
df = pd.read_csv("sg_mys_vegetable_disruptions_risk_matrix.csv")

# Page setup
st.set_page_config(page_title="SG-MY Vegetable Disruption Dashboard", layout="wide")
st.title("🇸🇬 SG Vegetable Supply Disruptions – Malaysia Imports")
st.markdown("""
This dashboard visualizes flood-related disruption events for vegetables imported from Malaysia to Singapore (2019–2024). It includes price, supply, and risk scoring analytics.
""")

# Sidebar Filters
st.sidebar.header("🔎 Filter Options")
veg_filter = st.sidebar.multiselect("🥬 Select Vegetables", df["vegetable"].unique(), default=df["vegetable"].unique())
cause_filter = st.sidebar.multiselect("🌧️ Disruption Causes", df["cause"].unique(), default=df["cause"].unique())
region_filter = st.sidebar.multiselect("🌍 Malaysian Region", df["affected_region_malaysia"].unique(), default=df["affected_region_malaysia"].unique())
risk_filter = st.sidebar.multiselect("📊 Risk Level", df["risk_level"].unique(), default=df["risk_level"].unique())

# Filter Data
filtered_df = df[
    (df["vegetable"].isin(veg_filter)) &
    (df["cause"].isin(cause_filter)) &
    (df["affected_region_malaysia"].isin(region_filter)) &
    (df["risk_level"].isin(risk_filter))
]

# KPIs
st.markdown(f"### 📊 {len(filtered_df)} Events Matched")
k1, k2, k3 = st.columns(3)
k1.metric("💹 Avg. Price Increase (%)", f"{filtered_df['price_increase_pct'].mean():.2f}")
k2.metric("📉 Avg. Supply Reduction (%)", f"{filtered_df['supply_reduction_pct'].mean():.2f}")
k3.metric("⚠️ Avg. Risk Score", f"{filtered_df['risk_score'].mean():.2f}")

# Charts Layout
col1, col2 = st.columns(2)

# Chart 1 - Price Increase by Vegetable
with col1:
    st.markdown("#### 💰 Price Impact by Vegetable")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=filtered_df, x="vegetable", y="price_increase_pct", palette="coolwarm", ax=ax1)
    ax1.set_xlabel("Vegetable")
    ax1.set_ylabel("Price Increase (%)")
    ax1.tick_params(axis='x', rotation=45)
    st.pyplot(fig1)

# Chart 2 - Supply Reduction by Cause
with col2:
    st.markdown("#### 🚛 Supply Reduction by Cause")
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(data=filtered_df, x="cause", y="supply_reduction_pct", estimator="mean", palette="YlOrBr", ax=ax2)
    ax2.set_xlabel("Cause")
    ax2.set_ylabel("Avg. Supply Reduction (%)")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

# Chart 3 - Logistics Impact
st.markdown("#### 🔗 Logistics Impact Distribution")
fig3, ax3 = plt.subplots(figsize=(10, 3))
sns.countplot(data=filtered_df, x="logistics_impact", palette="Set2", ax=ax3)
ax3.set_xlabel("Logistics Issue Type")
ax3.set_ylabel("Event Count")
ax3.tick_params(axis='x', rotation=45)
st.pyplot(fig3)

# RISK MATRIX TAB
st.markdown("### 🧠 Risk Scoring Cube (3D)")
fig4 = px.scatter_3d(
    filtered_df,
    x="likelihood_score",
    y="severity_score",
    z="human_control_score",
    color="risk_level",
    hover_data=["vegetable", "cause", "event_start_date"],
    color_discrete_map={"Low Risk": "green", "Moderate Risk": "orange", "High Risk": "red"},
    title="3D Risk Cube - Likelihood vs Severity vs Human Control"
)
fig4.update_layout(margin=dict(l=0, r=0, b=0, t=30))
st.plotly_chart(fig4, use_container_width=True)

# Risk Distribution
st.markdown("#### 🧮 Risk Level Frequency")
fig5 = px.histogram(
    filtered_df,
    x="risk_level",
    color="risk_level",
    color_discrete_map={"Low Risk": "green", "Moderate Risk": "orange", "High Risk": "red"},
    title="Distribution of Risk Levels"
)
st.plotly_chart(fig5, use_container_width=True)

# Data Table
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df.reset_index(drop=True))
