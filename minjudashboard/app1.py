import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# must be at the very top
st.set_page_config(layout="wide", page_title="Streamlit Dashboards")

# ================================
# 0) Intro / Playground
# ================================
st.title("🧪 Streamlit Practice App")
st.write("This Streamlit app collects several practice examples in one file.")

st.divider()
st.header("1) Basic Widgets")

age_slider = st.slider("How old are you?", 0, 100, 25)
st.write(f"You are {age_slider} years old")

if st.button("Click me"):
    st.write("Button clicked!")

name = st.text_input("What is your name?")
st.write(f"Hello, {name}!")

age_input = st.number_input("Age", min_value=0, max_value=120, value=25)
st.write(f"You are {age_input} years old")

budget = st.slider("Budget ($)", 0, 10000, 5000)
st.write(f"Budget: ${budget}")

country = st.selectbox("Country", ["USA", "Korea", "UK", "Japan"])
st.write(f"Country: {country}")

interests = st.multiselect("Interests", ["Finance", "Data Science", "Web Dev", "AI"])
st.write(f"Interests: {interests}")

# ================================
# 2) Tips Dashboard (Plotly built-in dataset)
# ================================
st.divider()
st.header("2) 💰 Tips Dashboard (Plotly built-in dataset)")

tips = px.data.tips()

# Sidebar filters for tips dashboard
st.sidebar.header("Tips Dashboard Filters")
selected_days = st.sidebar.multiselect(
    "Day",
    tips["day"].unique(),
    default=list(tips["day"].unique())
)
selected_time = st.sidebar.selectbox("Time", ["All", "Lunch", "Dinner"])
bill_max = st.sidebar.slider(
    "Max Total Bill ($)",
    float(tips["total_bill"].min()),
    float(tips["total_bill"].max()),
    float(tips["total_bill"].max())
)

# Apply filters
filtered_tips = tips[tips["day"].isin(selected_days)]
if selected_time != "All":
    filtered_tips = filtered_tips[filtered_tips["time"] == selected_time]
filtered_tips = filtered_tips[filtered_tips["total_bill"] <= bill_max]

# Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Bill", f'${filtered_tips["total_bill"].sum():.0f}')
m2.metric("Avg Tip", f'${filtered_tips["tip"].mean():.2f}')
m3.metric("Records", len(filtered_tips))

# Charts
c1, c2 = st.columns(2)
with c1:
    fig = px.scatter(filtered_tips, x="total_bill", y="tip", color="time",
                     title="Tip vs Total Bill")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.box(filtered_tips, x="day", y="total_bill", color="time",
                 title="Total Bill Distribution by Day")
    st.plotly_chart(fig, use_container_width=True)

# ================================
# 3) Cryptocurrency Excel Dashboard (your file)
# ================================
st.divider()
st.header("3) 📈 Cryptocurrency Dashboard (Excel)")

crypto_path = Path(r"C:\kdt\visualization\minjudashboard\Cryptocurrency dataset.xlsx")

@st.cache_data
def load_crypto_data(path: Path) -> pd.DataFrame:
    return pd.read_excel(path)

if crypto_path.exists():
    crypto_df = load_crypto_data(crypto_path)

    st.subheader("Raw Data Preview")
    st.write(f"File: {crypto_path}")
    st.write(f"Shape: {crypto_df.shape}")
    st.dataframe(crypto_df.head())

    # Try to detect a date column
    date_cols = [c for c in crypto_df.columns if "date" in str(c).lower()]
    if date_cols:
        date_col = date_cols[0]
        crypto_df[date_col] = pd.to_datetime(crypto_df[date_col], errors="coerce")

    # Try to detect a coin/symbol column
    symbol_cols = [c for c in crypto_df.columns if str(c).lower() in ["symbol", "coin", "ticker", "name"]]
    symbol_col = symbol_cols[0] if symbol_cols else None

    # Sidebar filters for crypto
    st.sidebar.header("Crypto Filters")
    filtered_crypto = crypto_df.copy()

    if symbol_col is not None:
        symbols = sorted([s for s in filtered_crypto[symbol_col].dropna().unique()])
        selected_symbols = st.sidebar.multiselect(
            "Coin/Symbol",
            symbols,
            default=symbols[: min(5, len(symbols))] if len(symbols) > 0 else []
        )
        if selected_symbols:
            filtered_crypto = filtered_crypto[filtered_crypto[symbol_col].isin(selected_symbols)]

    if date_cols:
        dc = date_cols[0]
        valid_dates = filtered_crypto[dc].dropna()
        if not valid_dates.empty:
            dmin, dmax = valid_dates.min(), valid_dates.max()
            date_range = st.sidebar.date_input("Date range", value=(dmin.date(), dmax.date()))
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                filtered_crypto = filtered_crypto[
                    (filtered_crypto[dc] >= pd.to_datetime(start_date)) &
                    (filtered_crypto[dc] <= pd.to_datetime(end_date))
                ]

    st.subheader("Filtered Data")
    st.write(f"Records: {len(filtered_crypto)}")
    st.dataframe(filtered_crypto.head(20))

    st.subheader("Summary Statistics")
    st.write(filtered_crypto.describe(include="all"))

    # Auto-plot with numeric columns
    numeric_cols = filtered_crypto.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) >= 2:
        left, right = st.columns(2)
        with left:
            st.write("Auto Line Chart (first numeric column)")
            st.line_chart(filtered_crypto[numeric_cols[0]])
        with right:
            st.write("Auto Bar Chart (second numeric column)")
            st.bar_chart(filtered_crypto[numeric_cols[1]])

        st.subheader("Interactive Scatter (Plotly)")
        fig = px.scatter(
            filtered_crypto,
            x=numeric_cols[0],
            y=numeric_cols[1],
            color=symbol_col if symbol_col is not None else None,
            title=f"{numeric_cols[1]} vs {numeric_cols[0]}"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Automatic charts need at least 2 numeric columns. (Check the column types in the Excel file.)")

else:
    st.error("Could not find the cryptocurrency Excel file.")
    st.write("Check the path below:")
    st.code(str(crypto_path))

# ================================
# 4) Optional: House Price Dashboard (if house_data.csv exists)
# ================================
st.divider()
st.header("4) 🏠 House Price Dashboard (optional)")

house_path = Path("house_data.csv")
if house_path.exists():
    house_df = pd.read_csv(house_path)

    st.subheader("Raw Data Preview")
    st.write(f"Shape: {house_df.shape}")
    st.dataframe(house_df.head())

    st.sidebar.header("House Filters")
    price_max = st.sidebar.slider(
        "Max Price ($)",
        int(house_df["price"].min()),
        int(house_df["price"].max()),
        int(house_df["price"].max())
    )
    bedrooms_min = st.sidebar.slider("Min Bedrooms", 1, 10, 3)

    filtered_house = house_df[(house_df["price"] <= price_max) & (house_df["bedrooms"] >= bedrooms_min)]

    # Metrics
    h1, h2, h3 = st.columns(3)
    h1.metric("Avg Price", f'${filtered_house["price"].mean():.0f}')
    h2.metric("Count", len(filtered_house))
    h3.metric("Avg Bedrooms", f'{filtered_house["bedrooms"].mean():.1f}')

    # Charts
    fig1 = px.scatter(filtered_house, x="sqft_living", y="price", color="bedrooms",
                      title="Price vs Sqft Living")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(filtered_house, x="price", nbins=30, title="Price Distribution")
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.info("house_data.csv is not in the current folder, so the House dashboard is skipped.")
    st.write("Put house_data.csv in the same folder to enable it automatically.")
