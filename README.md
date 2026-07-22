# ForecastPH — Streamlit rebuild

This is your original `index.html` dashboard (Tailwind + ApexCharts + Phosphor
Icons, unmodified visual design) wired to **real data and real trained models**
instead of the original's `Math.random()` mock generators. No database — CSV
in, forecast out, per session.

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Torch is the only heavy dependency (used for the LSTM). If it's not
installed, `services/forecasting.py` falls back to a naive baseline for the
LSTM model so the app still runs — just without a real LSTM.

## How the pieces fit together

```
app.py                          Orchestrates everything; renders the dashboard
├── services/data_validator.py  Validates any OHLCV CSV (bundled or uploaded)
├── services/data_loader.py     Loads data/raw/<SYMBOL>.csv → company + price data
├── services/feature_engineering.py   Lag/moving-average features
├── services/forecasting.py     Trains Lag-Informed Regression, ARIMA, LSTM
│                                + naive baseline; computes RMSE/MAE/MAPE/R²
└── assets/dashboard_template.html    Your original HTML/CSS/JS, patched to
                                       read window.APP_DATA instead of
                                       generating mock values
```

`app.py` builds a Python dict (`APP_DATA`), serializes it to JSON, and
substitutes it into the `__APP_DATA_JSON__` placeholder in
`dashboard_template.html` before handing the whole HTML string to
`st.iframe()`. The dashboard's own JS (routing, ApexCharts rendering) is
otherwise untouched.

## Replace the sample data with your real data

`data/raw/BDO.csv`, `JFC.csv`, and `ALI.csv` are **synthetic placeholders**
(clearly labeled, randomly generated) so the app runs end-to-end out of the
box. Replace them — and add the other 12 tickers — with your real PSE EDGE
CSVs (2020–2026, columns: `Date, Open, High, Low, Close, Volume`), named
`data/raw/<SYMBOL>.csv` to match the symbols in
`services/data_loader.py::COMPANY_META`.

## Plug in your actual trained models

Right now, `services/forecasting.py` trains all three models **on the fly**
from each CSV (fast for Lag Regression/ARIMA; the LSTM does ~60 quick epochs).
If you already have `.pkl` / `.pth` files from your capstone's actual
training run, load those in `forecasting.py` instead — the app only cares
that `run_all_models(df)` returns:

```python
{
  "metrics": {"lag_reg": {...}, "arima": {...}, "lstm": {...}, "naive": {...}},
  "next_close": {"lag": float, "arima": float, "lstm": float},
  "backtest30": [float, ...],  # last 30 predicted closes, for the details chart
}
```
where each metrics entry is `{"rmse": str, "mae": str, "mape": str, "r2": str}`.

## Live Prediction page — why the upload control is in the sidebar

`st.iframe()` sandboxes the embedded HTML — its JS can't call back into
Python directly. So the CSV uploader for the Live Prediction feature is a
native `st.file_uploader()` in the sidebar (not inside the embedded HTML).
Uploading a file there triggers Streamlit to validate it, run the real
models, and store the result in `st.session_state["live_prediction"]`; the
next rerun re-renders the embedded dashboard with that real result already
filled in. The Live Prediction page's own upload box just tells the user to
use the sidebar control.

If you outgrow this later and want the upload interaction to live fully
inside the styled dashboard itself, that requires Streamlit's Components V2
(bidirectional JS↔Python), which is a bigger lift than this hybrid approach.

## No database

Every run is stateless: CSV → validate → engineer features → train/predict →
render → discard. This matches the "no database" decision already reasoned
through for this project.
