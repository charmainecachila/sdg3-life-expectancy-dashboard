import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="SDG 3 Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ------------------------
# LOAD DATA
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Life Expectancy Data.csv")

    df.columns = df.columns.str.strip()

    df = df.dropna()

    return df

df = load_data()

# ------------------------
# TITLE
# ------------------------
st.title("🌍 SDG 3: Good Health and Well-Being")
st.markdown(
"""
### Factors Influencing Life Expectancy Across Countries

This dashboard explores the drivers of life expectancy using
health, economic, and educational indicators.
"""
)

# ------------------------
# SIDEBAR
# ------------------------
st.sidebar.header("Filters")

selected_year = st.sidebar.slider(
    "Select Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    int(df["Year"].max())
)

countries = sorted(df["Country"].unique())

selected_country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=countries[:10]
)

filtered_df = df[
    (df["Year"] == selected_year)
]

# ------------------------
# KPI SECTION
# ------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Life Expectancy",
    f"{filtered_df['Life expectancy'].mean():.2f}"
)

col2.metric(
    "Average GDP",
    f"{filtered_df['GDP'].mean():,.0f}"
)

col3.metric(
    "Average Schooling",
    f"{filtered_df['Schooling'].mean():.2f}"
)

col4.metric(
    "Countries",
    filtered_df["Country"].nunique()
)

# ------------------------
# TOP COUNTRIES
# ------------------------
st.subheader("Top 15 Countries by Life Expectancy")

top15 = (
    filtered_df
    .sort_values("Life expectancy", ascending=False)
    .head(15)
)

fig1 = px.bar(
    top15,
    x="Country",
    y="Life expectancy",
    title=f"Top Countries ({selected_year})"
)

st.plotly_chart(fig1, use_container_width=True)

# ------------------------
# GDP VS LIFE EXPECTANCY
# ------------------------
st.subheader("GDP vs Life Expectancy")

fig2 = px.scatter(
    filtered_df,
    x="GDP",
    y="Life expectancy",
    hover_name="Country",
    color="Status",
    size="Population",
    title="Relationship Between GDP and Life Expectancy"
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------
# SCHOOLING VS LIFE EXPECTANCY
# ------------------------
st.subheader("Schooling vs Life Expectancy")

fig3 = px.scatter(
    filtered_df,
    x="Schooling",
    y="Life expectancy",
    hover_name="Country",
    color="Status",
    title="Relationship Between Education and Life Expectancy"
)

st.plotly_chart(fig3, use_container_width=True)

# ------------------------
# TREND OVER TIME
# ------------------------
st.subheader("Global Life Expectancy Trend")

trend = (
    df.groupby("Year")["Life expectancy"]
    .mean()
    .reset_index()
)

fig4 = px.line(
    trend,
    x="Year",
    y="Life expectancy",
    markers=True,
    title="Average Global Life Expectancy"
)

st.plotly_chart(fig4, use_container_width=True)

# ------------------------
# COUNTRY COMPARISON
# ------------------------
st.subheader("Country Comparison")

comparison = df[
    df["Country"].isin(selected_country)
]

fig5 = px.line(
    comparison,
    x="Year",
    y="Life expectancy",
    color="Country",
    title="Life Expectancy by Country"
)

st.plotly_chart(fig5, use_container_width=True)

# ------------------------
# REGRESSION INSIGHTS
# ------------------------
st.subheader("Regression Analysis Findings")

st.success(
"""
Key drivers identified from the regression analysis:

• GDP positively influences Life Expectancy

• Schooling positively influences Life Expectancy

• Adult Mortality negatively influences Life Expectancy

• HIV/AIDS prevalence negatively influences Life Expectancy

These variables were statistically significant predictors
of SDG 3 outcomes.
"""
)

# ------------------------
# FOOTER
# ------------------------
st.markdown("---")

st.caption(
"Dataset: WHO Life Expectancy Dataset | SDG 3 Project"
)