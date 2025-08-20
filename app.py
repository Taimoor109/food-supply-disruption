import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="SG-MY Vegetable Disruption Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("sg_mys_vegetable_disruptions_risk_matrix.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Disruptions")
veggie = st.sidebar.multiselect("Select Vegetable", options=df['vegetable'].unique(), default=df['vegetable'].unique())
risk_level = st.sidebar.multiselect("Select Risk Level", options=df['risk_level'].unique(), default=df['risk_level'].unique())

# Apply filters
filtered_df = df[(df['vegetable'].isin(veggie)) & (df['risk_level'].isin(risk_level))]

# Dashboard layout
st.title("🇸🇬 Singapore - 🇲🇾 Malaysia Vegetable Disruption Risk Dashboard")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Price Increase by Vegetable")
    fig1 = px.bar(filtered_df, x="vegetable", y="price_increase_pct", color="risk_level", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("📉 Supply Reduction by Vegetable")
    fig2 = px.bar(filtered_df, x="vegetable", y="supply_reduction_pct", color="risk_level", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("🧠 3D Risk Scoring Cube")
fig3 = px.scatter_3d(
    filtered_df,
    x='likelihood_score',
    y='severity_score',
    z='human_control_score',
    color='risk_level',
    hover_data=['vegetable', 'cause']
)
fig3.update_traces(marker=dict(size=5))
st.plotly_chart(fig3, use_container_width=True)

st.subheader("📊 Risk Level Distribution")
fig4 = px.histogram(filtered_df, x='risk_level', color='risk_level')
st.plotly_chart(fig4, use_container_width=True)

st.subheader("🗃️ Disruption Dataset Preview")
st.dataframe(filtered_df)
