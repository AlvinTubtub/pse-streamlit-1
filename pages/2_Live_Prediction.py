import io

import streamlit as st

from services.data_validator import (
    CSVValidationError,
    validate_ohlcv_csv,
)
from services.forecasting import run_all_models


st.set_page_config(layout="wide")

st.title("📈 Live Prediction")

st.caption(
    "Upload an OHLCV CSV file to generate a next-day stock price forecast."
)

uploaded_file = st.file_uploader(
    "Drag & drop your OHLCV CSV here or click to browse from your computer",
    type=["csv"],
    help="Required columns: `Date, Open, High, Low, Close, Volume`",
)

st.caption("Required columns: `Date, Open, High, Low, Close, Volume`")

if uploaded_file is None:
    st.info("Please upload a CSV file.")
    st.stop()

try:
    df = validate_ohlcv_csv(io.BytesIO(uploaded_file.getvalue()))

except CSVValidationError as e:
    st.error(str(e))
    st.stop()

st.subheader("Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True,
)

st.subheader("Forecast Model")

model = st.radio(
    "Choose a forecasting model",
    [
        "Lag Regression",
        "ARIMA",
        "LSTM",
        "Compare All",
    ],
    horizontal=True,
)

predict = st.button(
    "Predict Next-Day Forecast",
    type="primary",
    use_container_width=True,
)

if predict:

    with st.spinner("Running forecasting models..."):

        result = run_all_models(df)

    pred = result["next_close"]

    st.subheader("Prediction Results")

    col1, col2, col3 = st.columns(3)

    latest_close = df.iloc[-1]["Close"]

    with col1:
        st.metric(
            "Latest Close",
            f"{latest_close:,.2f}",
        )

    with col2:

        if model == "Lag Regression":
            value = pred["lag"]

        elif model == "ARIMA":
            value = pred["arima"]

        elif model == "LSTM":
            value = pred["lstm"]

        else:
            value = sum(pred.values()) / len(pred)

        st.metric(
            "Predicted Close",
            f"{value:,.2f}",
            f"{value-latest_close:,.2f}",
        )

    with col3:
        direction = "▲ Bullish" if value < latest_close else "▼ Bearish"
        st.metric("Direction", direction)

    chart = (
        df[["Date", "Close"]]
        .copy()
        .set_index("Date")    
    )

    st.subheader("Historical Prices")
    st.line_chart(chart)