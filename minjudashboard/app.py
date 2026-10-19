"""
Streamlit Dashboard Homework
- Challenge 1: Tips dataset dashboard (filters, metrics, 2 charts)
- Challenge 2: Kaggle dataset dashboard (2+ filters, 3+ chart types, data table)
- Challenge 3: Polish (wide layout, dividers, tabs, docstrings)
"""

from __future__ import annotations

import pandas as pd
import streamlit as st
import plotly.express as px


# -----------------------------
# Page Config (Challenge 3)
# -----------------------------
st.set_page_config(layout="wide", page_title="Homework Dashboards")


# -----------------------------
# Utilities (with docstrings)
# -----------------------------
@st.cache_data
def load_tips_data() -> pd.DataFrame:
    """Load Plotly's built-in Tips dataset."""
    return px.data.tips()


@st.cache_data
def load_csv(uploaded_file) -> pd.DataFrame:
    """
    Load a CSV file from Streamlit uploader.

    Parameters
    ----------
    uploaded_file : UploadedFile
        A file object returned by st.file_uploader.

    Returns
    -------
    pd.DataFrame
        Loaded dataframe.
    """
    return pd.read_csv(uploaded_file)


def safe_numeric(series: pd.Series) -> pd.Series:
    """Convert a Series to numeric if possible; non-convertible values become NaN."""
    return pd.to_numeric(series, errors="coerce")


def pick_first_existing_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Return the first column name that exists in df from a list of candidates."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


# -----------------------------
# App Title + Tabs (Challenge 3)
# -----------------------------
st.title("📊 Hands-On: Build Your Dashboard")
st.divider()

tab1, tab2, tab3 = st.tabs(["Challenge 1: Tips", "Challenge 2: Kaggle Dataset", "Challenge 3: Polish Notes"])


# =========================================================
# Challenge 1 (20 min): Tips dataset dashboard
# =========================================================
with tab1:
    st.header("💰 Tips Dashboard (Challenge 1)")
    st.write("Requirements: Day filter (sidebar), metrics (total/mean tip), scatter plot colored by time, one extra chart")

    tips = load_tips_data()

    # Sidebar filter: day (required)
    st.sidebar.header("Challenge 1 Filters (Tips)")
    day_options = list(tips["day"].unique())
    selected_days = st.sidebar.multiselect(
        "Day",
        options=day_options,
        default=day_options,
    )

    filtered = tips[tips["day"].isin(selected_days)].copy()

    st.divider()

    # Metrics: total + avg tip (required)
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Bill (sum)", f'${filtered["total_bill"].sum():.0f}')
    m2.metric("Tip (avg)", f'${filtered["tip"].mean():.2f}')
    m3.metric("Records", f"{len(filtered)}")

    st.divider()

    # Scatter plot (required): color by time
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Scatter: total_bill vs tip (color=time)")
        fig = px.scatter(
            filtered,
            x="total_bill",
            y="tip",
            color="time",
            hover_data=["day", "sex", "smoker", "size"],
        )
        st.plotly_chart(fig, use_container_width=True)

    # Second chart (your choice) (required) -> Box plot by day
    with c2:
        st.subheader("Second Chart: Box (total_bill by day, color=time)")
        fig2 = px.box(
            filtered,
            x="day",
            y="total_bill",
            color="time",
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("Data Table")
    st.dataframe(filtered, use_container_width=True)


# =========================
# Challenge 2: More Filters
# (Place this right after: filtered2 = df.copy())
# =========================
with tab2:
    st.header("📁 Challenge 2: Kaggle Dataset Dashboard")
    st.write("Loads the CSV (indexData.csv) from a fixed path and builds 2+ filters, 3+ charts and a table.")
    st.divider()

    # 1) Load data (fixed path)
    DATA_PATH = r"C:\kdt\visualization\minjudashboard\indexData.csv"

    @st.cache_data
    def load_index_data(path: str):
        """Load Kaggle CSV from a fixed local path."""
        return pd.read_csv(path)

    try:
        df = load_index_data(DATA_PATH)
    except Exception as e:
        st.error("Could not load the data. Check the path and file name.")
        st.code(DATA_PATH)
        st.exception(e)
        st.stop()

    st.subheader("Raw Data Preview")
    st.write(f"Shape: {df.shape}")
    st.dataframe(df.head(20), use_container_width=True)

    # 2) Sidebar filters (always visible)
    st.sidebar.header("Filters (Challenge 2)")

    # (A) View options
    show_table = st.sidebar.checkbox("Show data table", value=True)
    top_n = st.sidebar.slider("Rows to show", 10, 500, 100, step=10)

    # (B) Detect date column for Year filter
    date_col = None
    for c in df.columns:
        if "date" in str(c).lower() or "time" in str(c).lower():
            date_col = c
            break

    filtered2 = df.copy()

    # Year filter
    if date_col is not None:
        filtered2[date_col] = pd.to_datetime(filtered2[date_col], errors="coerce")
        years = sorted(filtered2[date_col].dropna().dt.year.unique().tolist())
        if years:
            selected_year = st.sidebar.slider("Select Year", int(min(years)), int(max(years)), int(max(years)))
            filtered2 = filtered2[filtered2[date_col].dt.year == selected_year]
        else:
            st.sidebar.caption("ℹ️ Found a date column but could not parse the year.")
    else:
        st.sidebar.caption("ℹ️ No date/time column found, so the Year filter is disabled.")

    # (C) Category filter (object columns)
    cat_cols = [c for c in df.columns if df[c].dtype == "object"]
    category_col = st.sidebar.selectbox("Category column", ["(none)"] + cat_cols, index=0)

    if category_col != "(none)":
        cats = sorted([x for x in filtered2[category_col].dropna().unique().tolist()])
        # includes the All option
        cats_with_all = ["All"] + cats
        selected_cat = st.sidebar.selectbox("Category", cats_with_all, index=0)

        if selected_cat != "All":
            filtered2 = filtered2[filtered2[category_col] == selected_cat]

        # multiselect (optional)
        enable_multi = st.sidebar.checkbox("Enable multi-select values", value=False)
        if enable_multi:
            selected_vals = st.sidebar.multiselect(
                "Pick multiple",
                options=cats,
                default=cats[: min(5, len(cats))]
            )
            if selected_vals:
                filtered2 = filtered2[filtered2[category_col].isin(selected_vals)]

    # (D) Numeric range filter (strengthens the 2+ filters requirement)
    num_cols = filtered2.select_dtypes(include="number").columns.tolist()
    num_col = st.sidebar.selectbox("Numeric column (range)", ["(none)"] + num_cols, index=0)

    if num_col != "(none)":
        s = pd.to_numeric(filtered2[num_col], errors="coerce").dropna()
        if not s.empty:
            lo, hi = float(s.min()), float(s.max())
            r = st.sidebar.slider(f"{num_col} range", lo, hi, (lo, hi))
            filtered2 = filtered2[pd.to_numeric(filtered2[num_col], errors="coerce").between(r[0], r[1])]
        else:
            st.sidebar.caption("ℹ️ The selected numeric column has no valid values.")

    # (E) Outlier removal (optional polish)
    remove_outliers = st.sidebar.checkbox("Remove outliers (IQR)", value=False)
    if remove_outliers and num_col != "(none)":
        s = pd.to_numeric(filtered2[num_col], errors="coerce").dropna()
        if not s.empty:
            q1, q3 = s.quantile(0.25), s.quantile(0.75)
            iqr = q3 - q1
            low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            filtered2 = filtered2[pd.to_numeric(filtered2[num_col], errors="coerce").between(low, high)]

    # (F) Sort
    sort_col = st.sidebar.selectbox("Sort by", options=filtered2.columns.tolist())
    ascending = st.sidebar.checkbox("Ascending", value=False)
    filtered2 = filtered2.sort_values(sort_col, ascending=ascending)

    st.sidebar.divider()
    st.sidebar.metric("Records", len(filtered2))

    # 3) Metrics (nice to have)
    st.divider()
    st.subheader("Quick Metrics")
    m1, m2, m3 = st.columns(3)
    m1.metric("Rows", len(filtered2))
    m2.metric("Columns", filtered2.shape[1])
    m3.metric("Missing cells", int(filtered2.isna().sum().sum()))

    # 4) Charts (3+ different chart types)
    st.divider()
    st.subheader("Charts (3+ types)")

    numeric_cols2 = filtered2.select_dtypes(include="number").columns.tolist()

    # Chart 1: Scatter (needs 2 numeric columns)
    c1, c2 = st.columns(2)

    with c1:
        st.write("1) Scatter")
        if len(numeric_cols2) >= 2:
            xcol = st.selectbox("Scatter X", numeric_cols2, index=0, key="sc_x")
            ycol = st.selectbox("Scatter Y", numeric_cols2, index=1, key="sc_y")
            fig = px.scatter(
                filtered2,
                x=xcol,
                y=ycol,
                color=category_col if category_col != "(none)" else None,
                title=f"{ycol} vs {xcol}"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("A scatter plot needs at least 2 numeric columns.")

    # Chart 2: Histogram (needs 1 numeric column)
    with c2:
        st.write("2) Histogram")
        if len(numeric_cols2) >= 1:
            hcol = st.selectbox("Histogram column", numeric_cols2, index=0, key="hist")
            fig = px.histogram(filtered2, x=hcol, nbins=30, title=f"Distribution of {hcol}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("A histogram needs at least 1 numeric column.")

    # Chart 3: Line (if date exists) else Box/Bar fallback
    st.write("3) Line / Box / Bar (auto)")

    if date_col is not None and len(numeric_cols2) >= 1:
        temp = filtered2.dropna(subset=[date_col]).copy()
        temp = temp.sort_values(date_col)
        ycol = st.selectbox("Line Y", numeric_cols2, index=0, key="line_y")
        fig = px.line(temp, x=date_col, y=ycol, title=f"{ycol} over time")
        st.plotly_chart(fig, use_container_width=True)
    elif category_col != "(none)" and len(numeric_cols2) >= 1:
        ycol = st.selectbox("Box Y", numeric_cols2, index=0, key="box_y")
        fig = px.box(filtered2, x=category_col, y=ycol, title=f"{ycol} by {category_col}")
        st.plotly_chart(fig, use_container_width=True)
    elif category_col != "(none)":
        vc = filtered2[category_col].value_counts().reset_index()
        vc.columns = [category_col, "count"]
        fig = px.bar(vc, x=category_col, y="count", title=f"Count by {category_col}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No date or category column, so the third chart cannot be built automatically.")

    # 5) Data table + download
    st.divider()
    st.subheader("Data Table")
    if show_table:
        st.dataframe(filtered2.head(top_n), use_container_width=True)

    st.subheader("Download")
    csv_bytes = filtered2.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download filtered CSV", data=csv_bytes, file_name="filtered_indexData.csv", mime="text/csv")



# =========================================================
# Challenge 3 (10 min): Polish & style notes
# =========================================================
with tab3:
    st.header("✨ Polish & Style (Challenge 3 checklist)")
    st.write(
        "- ✅ `st.set_page_config(layout='wide')` : applied at the top\n"
        "- ✅ `st.divider()` : used to separate sections\n"
        "- ✅ Tabs: `st.tabs()` used for each challenge\n"
        "- ✅ Docstrings: included in `load_tips_data`, `load_csv`, `safe_numeric`, `pick_first_existing_column`\n\n"
        "To make it feel more like a dashboard:\n"
        "1) Separate the sidebar by challenge (Tips and Kaggle currently share it)\n"
        "2) Make titles and descriptions consistent in tone\n"
        "3) Specify the Kaggle columns explicitly instead of auto-detecting them, for better UX\n"
    )
