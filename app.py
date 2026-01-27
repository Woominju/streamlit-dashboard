import streamlit as st

st.title("🎯 My First Streamlit App")
st.write("Welcome to Streamlit!")

st.divider()

# Simple slider + button
age_slider = st.slider("How old are you?", 0, 100, 25)
st.write(f"You are {age_slider} years old")

if st.button("Click me"):
    st.write("Button clicked!")

st.divider()

# Text input + number input + budget slider
name = st.text_input("What is your name?")
st.write(f"Hello, {name}!")

age_input = st.number_input("Age", min_value=0, max_value=120, value=25)
st.write(f"You are {age_input} years old")

budget = st.slider("Budget ($)", 0, 10000, 5000)
st.write(f"Budget: ${budget}")

st.divider()

# Selectbox + multiselect
country = st.selectbox("Country", ["USA", "Korea", "UK", "Japan"])
st.write(f"Country: {country}")

interests = st.multiselect("Interests", ["Finance", "Data Science", "Web Dev", "AI"])
st.write(f"Interests: {interests}")

st.divider()

st.header("Dashboard Layout")

# Sidebar filters (리스트를 제대로 닫아줌)
st.sidebar.header("Filters")
year_filter = st.sidebar.slider("Select Year", 2020, 2025, 2023)
category_filter = st.sidebar.selectbox("Category", ["All", "A", "B", "C"])

st.write(f"Selected year: {year_filter}")
st.write(f"Selected category: {category_filter}")

# Main content with columns
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales", "$125K", "+12%")
with col2:
    st.metric("Orders", "1,234", "+5%")
with col3:
    st.metric("Customers", "567", "+8%")

st.divider()

# Two-column layout for charts
chart_col1, chart_col2 = st.columns(2)
with chart_col1:
    st.subheader("Chart 1")
    st.write("Chart will go here")
with chart_col2:
    st.subheader("Chart 2")
    st.write("Another chart here")

    
