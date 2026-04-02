import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data
import os

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

st.markdown("""
<style>
.main { background-color: #f7f7f2; }
.card {
    background: white;
    padding: 14px;
    border-radius: 14px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 10px;
}
.highlight { border-left: 6px solid #1f7a6b; background-color: #eefaf6; }
.completed { opacity: 0.6; }
.title { font-size: 18px; font-weight: 600; }
.subtitle { font-size: 13px; color: #555; }
.score { font-size: 20px; font-weight: bold; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1,5])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)

with col2:
    st.title("Court Mafia 2.0")
    st.caption("Thane’s Defining Pickleball Tournament")

df = load_data()
df['Start_DateTime'] = pd.to_datetime(df['Date'].astype(str) + " " + df['Start Time'].astype(str))
df = df.sort_values(by="Start_DateTime")

st.sidebar.header("Filters")
player = st.sidebar.text_input("Search Player")
category = st.sidebar.multiselect("Category", df['Category'].dropna().unique())
court = st.sidebar.multiselect("Court", df['Court No'].dropna().unique())
venue = st.sidebar.multiselect("Venue", df['Venue'].dropna().unique())

filtered = df.copy()

if player:
    filtered = filtered[filtered['Match Details'].astype(str).str.contains(player, case=False, na=False)]

if category:
    filtered = filtered[filtered['Category'].isin(category)]

if court:
    filtered = filtered[filtered['Court No'].isin(court)]

if venue:
    filtered = filtered[filtered['Venue'].isin(venue)]

st.subheader("🔥 Top 5 Upcoming Matches")

now = datetime.now()
upcoming = filtered[filtered['Start_DateTime'] >= now].head(5)

for _, row in upcoming.iterrows():
    status = str(row.get("Status", "Upcoming"))
    score_a = row.get("Score A", "")
    score_b = row.get("Score B", "")

    highlight_class = "highlight" if status.lower() == "live" else ""

    st.markdown(f"""
    <div class="card {highlight_class}">
        <div class="title">{row['Match Details']}</div>
        <div class="subtitle">
            {row['Date']} | {row['Start Time']} - {row['End Time']} <br>
            Court {row['Court No']} | {row['Category']} | {row['Venue']}
        </div>
        <div class="score">{score_a} - {score_b}</div>
        <div class="subtitle">Status: {status}</div>
    </div>
    """, unsafe_allow_html=True)

st.subheader("📅 Full Schedule")

for _, row in filtered.iterrows():
    status = str(row.get("Status", "Upcoming"))
    score_a = row.get("Score A", "")
    score_b = row.get("Score B", "")

    completed_class = "completed" if status.lower() == "completed" else ""

    st.markdown(f"""
    <div class="card {completed_class}">
        <div class="title">{row['Match Details']}</div>
        <div class="subtitle">
            {row['Date']} | {row['Start Time']} - {row['End Time']} <br>
            Court {row['Court No']} | {row['Category']} | {row['Venue']}
        </div>
        <div class="score">{score_a} - {score_b}</div>
        <div class="subtitle">Status: {status}</div>
    </div>
    """, unsafe_allow_html=True)
