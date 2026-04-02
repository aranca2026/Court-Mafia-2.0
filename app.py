import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data
import os

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

# ---------- UI ----------
st.markdown("""
<style>
.main { background-color: #f7f7f2; }

.card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    margin-bottom: 12px;
}

.highlight {
    border-left: 6px solid #1f7a6b;
    background-color: #eefaf6;
}

.score {
    font-size: 22px;
    font-weight: 700;
    margin-top: 6px;
}

.title { font-size: 18px; font-weight: 600; }
.subtitle { font-size: 13px; color: #555; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([1,5])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
with col2:
    st.title("Court Mafia 2.0")
    st.caption("Thane’s Defining Pickleball Tournament")

# ---------- LOAD ----------
df = load_data()
df.columns = df.columns.str.strip()

# Ensure score columns exist
for col in ['Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col] = ""

df['Start_DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + " " + df['Start Time'].astype(str),
    errors='coerce'
)

df = df.sort_values(by="Start_DateTime")

# ---------- UPCOMING ----------
st.subheader("🔥 Top 5 Upcoming Matches")

now = datetime.now()
upcoming = df[df['Start_DateTime'] >= now].head(5)

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

for _, row in df.iterrows():
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
