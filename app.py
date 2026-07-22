import streamlit as st

st.set_page_config(
    page_title="ForecastPH",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 ForecastPH")

st.markdown(
    """
Welcome to **ForecastPH**.

This dashboard provides:

- 📈 Live Prediction
- 🏢 Company List
- 📊 Model Performance
- 📚 Learn
- ℹ️ About

Select a page from the navigation menu.
"""
)