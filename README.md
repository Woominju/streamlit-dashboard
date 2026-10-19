# Streamlit Dashboards

Interactive data dashboards built with Streamlit, pandas and Plotly (January 2026).

## Apps
| File | What it shows |
|---|---|
| `app.py` | Streamlit basics: widgets, sidebar filters, metric cards, column layouts |
| `minjudashboard/app.py` | Hands-on dashboards: the Plotly *tips* dataset (scatter and box plots with filters) and a stock-index dashboard with sidebar filters, charts and a table |
| `minjudashboard/app1.py` | All practice examples combined into one wide-layout app |

## Data
| File | Description |
|---|---|
| `indexData.csv` | Daily OHLCV data for world stock indices (Kaggle) |
| `melon_top100.csv` | Melon Top 100 chart: rank, title, artist, album |

## Run locally
```bash
pip install -r requirements.txt
streamlit run minjudashboard/app.py
```
The stock-index tab reads `indexData.csv` from a fixed local path set in `DATA_PATH`; change it to your copy of the file.
