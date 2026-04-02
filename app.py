import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data
import os

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

# ---------- UI ----------
st.markdown("""
<style>
.card {
    background-color: var(--secondary-background-color);
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.10);
    margin-bottom: 12px;
}

.highlight { border-left: 6px solid #1f7a6b; }

.title { font-size: 18px; font-weight: 600; color: var(--text-color); }

.subtitle { font-size: 13px; color: var(--text-color); opacity: 0.7; }

.score { font-size: 24px; font-weight: 800; margin-top: 6px; color: var(--text-color); }

.header-title {
    font-size: 36px;
    font-weight: 800;
    color: var(--text-color);
}

.tagline {
    font-size: 14px;
    color: var(--text-color);
    opacity: 0.6;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([1,5])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=90)

with col2:
    st.markdown("<div class='header-title'>🏆 Court Mafia 2.0 🏆</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>Thane’s Defining Pickleball Tournament</div>", unsafe_allow_html=True)

# ---------- LOAD ----------
df = load_data()

df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

for col in ['Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col] = ""

df['Start_DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + " " + df['Start Time'].astype(str),
    errors='coerce'
)

df = df.sort_values(by="Start_DateTime")

# ---------- FILTERS ----------
st.sidebar.header("Filters")

player = st.sidebar.text_input("Search Player")
category = st.sidebar.multiselect("Category", df['Category'].dropna().unique())
venue = st.sidebar.multiselect("Venue", df['Venue'].dropna().unique())

filtered = df.copy()

if player:
    player = player.strip().lower()

    filtered = filtered[
        filtered['Match Details'].astype(str).str.lower().str.contains(player, na=False) |
        filtered.get('Player 1', '').astype(str).str.lower().str.contains(player, na=False) |
        filtered.get('Player 2', '').astype(str).str.lower().str.contains(player, na=False) |
        filtered.get('Player 3', '').astype(str).str.lower().str.contains(player, na=False) |
        filtered.get('Player 4', '').astype(str).str.lower().str.contains(player, na=False)
    ]

if category:
    filtered = filtered[filtered['Category'].isin(category)]

if venue:
    filtered = filtered[filtered['Venue'].isin(venue)]

# ---------- UPCOMING ----------
st.subheader("🔥 Top 5 Upcoming Matches")

now = datetime.now()
upcoming = filtered[filtered['Start_DateTime'] >= now].head(5)

for _, row in upcoming.iterrows():
    score_display = ""
    if str(row['Team 1 Score']) != "" or str(row['Team 2 Score']) != "":
        score_display = f"<div class='score'>{row['Team 1 Score']} - {row['Team 2 Score']}</div>"

    st.markdown(f"""
    <div class="card highlight">
        <div class="title">{row.get('Match Details','')}</div>
        {score_display}
        <div class="subtitle">
            {row.get('Date','')} | {row.get('Start Time','')} <br>
            Court {row.get('Court No','')} | {row.get('Category','')} | {row.get('Venue','')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- FULL ----------
st.subheader("📅 Full Schedule")

for _, row in filtered.iterrows():
    score_display = ""
    if str(row['Team 1 Score']) != "" or str(row['Team 2 Score']) != "":
        score_display = f"<div class='score'>{row['Team 1 Score']} - {row['Team 2 Score']}</div>"

    st.markdown(f"""
    <div class="card">
        <div class="title">{row.get('Match Details','')}</div>
        {score_display}
        <div class="subtitle">
            {row.get('Date','')} | {row.get('Start Time','')} <br>
            Court {row.get('Court No','')} | {row.get('Category','')} | {row.get('Venue','')}
        </div>
    </div>
    """, unsafe_allow_html=True)
