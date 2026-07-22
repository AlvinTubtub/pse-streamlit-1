import streamlit as st

from services.data_loader import load_companies

st.title("📈 ForecastPH Dashboard")

companies, dataframes, missing = load_companies()

st.write(type(companies))
st.write(type(dataframes))
st.write(companies)
st.write(dataframes.keys())

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Companies",
        len(companies),
    )

with col2:
    st.metric(
        "Forecast Models",
        3,
    )

with col3:
    st.metric(
        "Datasets",
        len(dataframes),
    )

with col4:
    st.metric(
        "Missing",
        len(missing),
    )

selected = st.selectbox(
    "Select Company",
    companies,
)

if selected not in dataframes:
    st.error(f"No dataset available for {selected}.")
    st.stop()

df = dataframes[selected]

chart = (
    df[["Date", "Close"]]
    .copy()
    .set_index("Date")
)

st.subheader("Historical Closing Prices")

st.line_chart(
    chart,
    use_container_width=True,
)

st.subheader("Company Information")

col1, col2 = st.columns(2)

with col1:
    st.write("**Ticker**")
    st.success(selected)

with col2:
    st.write("**Rows**")
    st.success(len(df))

if df.empty:
    st.warning("The selected dataset is empty.")
    st.stop()
latest = df.iloc[-1]

st.subheader("Latest Trading Day")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Open", f"{latest.Open:,.2f}")
c2.metric("High", f"{latest.High:,.2f}")
c3.metric("Low", f"{latest.Low:,.2f}")
c4.metric("Close", f"{latest.Close:,.2f}")
c5.metric("Volume", f"{latest.Volume:,.0f}")

st.subheader("Dataset Preview")

st.dataframe(
    df.tail(10),
    use_container_width=True,
)