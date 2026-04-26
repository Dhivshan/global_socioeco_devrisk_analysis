import streamlit as st
import pandas as pd
import plotly.express as px
import sqlalchemy
import urllib.parse

# Connection string: MySQL credentials
user = "root"
password = urllib.parse.quote_plus("Root@123")
host = "localhost"
database = "global_socioeco_devrisk"


# Connect to SQL
engine = sqlalchemy.create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

page = st.sidebar.radio("Select Page", ["Global Overview", "Health & Economic Risk", "Segmentation Insights"])

# KPI Queries
avg_income = pd.read_sql("SELECT AVG(income) AS avg_income FROM country_stats", engine).iloc[0,0]
avg_life = pd.read_sql("SELECT AVG(life_expec) AS avg_life_expectancy FROM country_stats", engine).iloc[0,0]
avg_child = pd.read_sql("SELECT AVG(child_mort) AS avg_child_mortality FROM country_stats", engine).iloc[0,0]
high_risk = pd.read_sql("SELECT COUNT(DISTINCT country) AS high_risk_count FROM country_stats WHERE Segment ='High Risk Country' AND Risk_Flag=1 GROUP BY Segment;", engine).iloc[0,0]

# KPI Cards
st.metric("Avg Income", f"{avg_income:,.2f}")
st.metric("Avg Life Expectancy", f"{avg_life:.1f}")
st.metric("Avg Child Mortality", f"{avg_child:.2f}")
st.metric("High-Risk Countries", high_risk)

# World Map
map_data = pd.read_sql("SELECT country, Segment FROM country_stats", engine)
fig_map = px.scatter_geo(map_data, color="Segment", hover_name="country")
st.plotly_chart(fig_map)

# Scatter Plot
scatter_data = pd.read_sql("SELECT country, income, life_expec FROM country_stats", engine)
fig_scatter = px.scatter(scatter_data, x="income", y="life_expec", hover_name="country")
st.plotly_chart(fig_scatter)

# ---------------- PAGE 2: Health & Economic Risk ----------------
st.title("⚕️ Health & Economic Risk")

# 1. Child Mortality by Country
mortality_data = pd.read_sql("""
    SELECT country, child_mort, Segment
    FROM country_stats
    ORDER BY child_mort DESC
    LIMIT 20;
""", engine)

fig_mort = px.bar(mortality_data, x="country", y="child_mort", color="Segment",
                  title="Child Mortality by Country")
st.plotly_chart(fig_mort, use_container_width=True)


# 2. Health vs Mortality Scatter Plot
health_mort_data = pd.read_sql("""
    SELECT country, health, child_mort, Segment
    FROM country_stats;
""", engine)

fig_health = px.scatter(health_mort_data, x="health", y="child_mort", color="Segment",
                        hover_name="country", title="Health Expenditure vs Child Mortality")
st.plotly_chart(fig_health, use_container_width=True)

# 3. Inflation Risk Chart
inflation_data = pd.read_sql("""
    SELECT country, inflation, Segment
    FROM country_stats
    ORDER BY inflation DESC
    LIMIT 20;
""", engine)

fig_inflation = px.bar(inflation_data, x="country", y="inflation", color="Segment",
                       title="Top Inflation Risk Countries")
st.plotly_chart(fig_inflation, use_container_width=True)

# 4. Fertility vs GDP Visualization
fertility_gdp_data = pd.read_sql("""
    SELECT country, gdpp, total_fer, Segment
    FROM country_stats;
""", engine)

fig_fertility = px.scatter(fertility_gdp_data, x="gdpp", y="total_fer", color="Segment",
                           hover_name="country", trendline="ols",
                           title="Fertility Rate vs GDP per Capita")
st.plotly_chart(fig_fertility, use_container_width=True)



st.title("Segmentation Insights")
# Segment Distribution
seg_dist = pd.read_sql("""
        SELECT Segment, COUNT(DISTINCT country) AS country_count
        FROM country_stats
        GROUP BY Segment
    """, engine)
fig_seg_dist = px.bar(seg_dist, x="Segment", y="country_count", title="Segment Distribution")
st.plotly_chart(fig_seg_dist)

# Income by Segment
income_seg = pd.read_sql("""
        SELECT Segment, AVG(income) AS avg_income
        FROM country_stats
        GROUP BY Segment
    """, engine)
fig_income_seg = px.bar(income_seg, x="Segment", y="avg_income", title="Income by Segment")
st.plotly_chart(fig_income_seg)

# GDP by Segment
gdp_seg = pd.read_sql("""
        SELECT Segment, AVG(gdpp) AS avg_gdp
        FROM country_stats
        GROUP BY Segment
    """, engine)
fig_gdp_seg = px.bar(gdp_seg, x="Segment", y="avg_gdp", title="GDP by Segment")
st.plotly_chart(fig_gdp_seg)


