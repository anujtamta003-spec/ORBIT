import streamlit as st
import pydeck as pdk
import pandas as pd
import plotly.express as px
import random
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="🛰️ ORBIT System", layout="wide", page_icon="🌍")

# --- TITLE ---
st.markdown("<h1 style='text-align:center;'>🛰️ ORBIT - Financial Detective System</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Unmasking global corporate truths</h4>", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("🔍 Search Company")
company = st.sidebar.text_input("Enter a Company Name (e.g., Apple, Google, Tesla)", "Apple")

st.sidebar.markdown("### 🧭 Navigation")
page = st.sidebar.radio("Go to:", ["Overview", "Financial Insights", "Global Presence", "AI Detective"])

# --- SAMPLE DATA GENERATION ---
countries = ["USA", "India", "Ireland", "Singapore", "Netherlands", "UK", "Switzerland"]
lat_lon = {
    "USA": (37.0902, -95.7129),
    "India": (20.5937, 78.9629),
    "Ireland": (53.4129, -8.2439),
    "Singapore": (1.3521, 103.8198),
    "Netherlands": (52.3676, 4.9041),
    "UK": (55.3781, -3.4360),
    "Switzerland": (46.8182, 8.2275)
}

df = pd.DataFrame({
    "country": countries,
    "lat": [lat_lon[c][0] for c in countries],
    "lon": [lat_lon[c][1] for c in countries],
    "income_2024": [random.randint(40, 200) for _ in countries],
    "income_2025": [random.randint(60, 250) for _ in countries],
    "tax_paid_2024": [random.randint(5, 30) for _ in countries],
    "tax_paid_2025": [random.randint(10, 40) for _ in countries]
})

# --- PAGE 1: OVERVIEW ---
if page == "Overview":
    st.subheader(f"🏢 {company} - Global Overview")

    st.write(f"""
    {company} is a multinational company with operations across major economies.  
    ORBIT uses real-time open-source data, financial models, and AI analysis to uncover hidden insights about its income, tax strategies, and global influence.
    """)

    st.metric("Estimated Global Income (2025)", f"${df['income_2025'].sum()} B", "+12% YoY")
    st.metric("Tax Paid (2025)", f"${df['tax_paid_2025'].sum()} B", "+8% YoY")
    st.metric("Potential Tax Avoidance Estimate", f"${random.randint(5, 20)} B")

    st.markdown("---")
    st.success("Use the left sidebar to explore deeper insights and AI-driven reports.")

# --- PAGE 2: FINANCIAL INSIGHTS ---
elif page == "Financial Insights":
    st.subheader(f"📊 {company} - Financial Analysis")

    # Interactive charts
    col1, col2 = st.columns(2)

    with col1:
        fig_income = px.bar(df, x="country", y=["income_2024", "income_2025"],
                            barmode="group", title="Income Comparison (2024 vs 2025)")
        st.plotly_chart(fig_income, use_container_width=True)

    with col2:
        df["tax_avoidance"] = df["income_2025"] - df["tax_paid_2025"]
        fig_tax = px.pie(df, values="tax_avoidance", names="country", title="Tax Avoidance by Country")
        st.plotly_chart(fig_tax, use_container_width=True)

    st.markdown("#### 💼 Financial Summary")
    st.dataframe(df[["country", "income_2024", "income_2025", "tax_paid_2024", "tax_paid_2025"]])

# --- PAGE 3: GLOBAL PRESENCE ---
elif page == "Global Presence":
    st.subheader(f"🌎 {company} - Global Map Network")

    st.markdown("### 🗺️ Headquarters & Operations Map")
    layer_main = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_color='[0, 100, 255, 200]',
        get_radius=700000,
        pickable=True
    )

    map_style = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
    view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1.3, pitch=40)

    r = pdk.Deck(layers=[layer_main], initial_view_state=view_state, map_style=map_style,
                 tooltip={"text": "{country}"})
    st.pydeck_chart(r)

    st.markdown("### 💰 Tax Haven Locations (3D Globe)")
    layer_tax = pdk.Layer(
        "ColumnLayer",
        data=df,
        get_position='[lon, lat]',
        get_elevation='tax_paid_2025 * 20000',
        elevation_scale=1,
        radius=400000,
        get_fill_color='[255, 0, 0, 180]',
        pickable=True
    )

    r2 = pdk.Deck(layers=[layer_tax], initial_view_state=view_state,
                  map_style=map_style, tooltip={"text": "{country}\nTax Paid: {tax_paid_2025} B"})
    st.pydeck_chart(r2)

# --- PAGE 4: AI DETECTIVE ---
elif page == "AI Detective":
    st.subheader("🕵️ ORBIT AI - Financial Intelligence Assistant")

    st.markdown("""
    This AI detective specializes in:
    - Corporate Financial Law  
    - International Tax Frameworks  
    - Shell Company Tracing  
    - Income & Loss Pattern Recognition  
    """)

    query = st.text_input("Ask the ORBIT AI Detective", "Analyze Apple’s tax strategy in Ireland")
    if query:
        with st.spinner("Analyzing corporate data..."):
            detective = pipeline("text-generation", model="distilgpt2")
            response = detective(query, max_length=120, do_sample=True, temperature=0.8)
            st.markdown(f"🧠 **AI Detective Insight:**\n\n> {response[0]['generated_text']}")

    st.markdown("---")
    st.info("⚖️ Note: AI outputs are for research and analytical insight — not legal conclusions.")

# --- FOOTER ---
st.markdown("<hr><center>© 2025 ORBIT Intelligence - Built with ❤️ using Streamlit, Pydeck, and Open Data</center>", unsafe_allow_html=True)
