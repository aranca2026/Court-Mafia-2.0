import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data
import os

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

# -------- UI --------
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
.live {
    border-left: 6px solid #00c853;
    background-color: #e8f5e9;
}
.highlight {
    border-left: 6px solid #1f7a6b;
    background-color: #eefaf6;
}
.title { font-size: 18px; font-weight: 600; }
.subtitle { font-size: 13px; color: #555; }
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
col1, col2 = st.columns([1,5])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
with col2:
    st.title("Court Mafia 2.0")
    st.caption("Thane’s Defining Pickleball Tournament")

# -------- LOAD DATA --------
df = load_data()

# Clean columns
df.columns = df.columns.str.strip()

# Ensure score + status columns exist
for col in ['Team 1 Score','Team 2 Score','Status']:
    if col not in df.columns:
        df[col] = ""

# Create datetime
df['Start_DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + " " + df['Start Time'].astype(str),
    errors='coerce'
)

df = df.sort_values(by="Start_DateTime")

# -------- LIVE MATCHES --------
st.subheader("🔴 Live Matches")

live_df = df[df['Status'].astype(str).str.strip() == 'Live']

if live_df.empty:
    st.info("No live matches")
else:
    for _, row in live_df.iterrows():
        st.markdown(f"""
        <div class="card live">
            <div class="title">{row.get('Match Details','')}</div>
            <div class="subtitle">
                Score: {row.get('Team 1 Score','')} - {row.get('Team 2 Score','')} <br>
                Court {row.get('Court No','')} | {row.get('Category','')}
            </div>
        </div>
        """, unsafe_allow_html=True)

# -------- UPCOMING --------
st.subheader("🔥 Top 5 Upcoming Matches")

now = datetime.now()
upcoming = df[df['Start_DateTime'] >= now].head(5)

for _, row in upcoming.iterrows():
    st.markdown(f"""
    <div class="card highlight">
        <div class="title">{row.get('Match Details','')}</div>
        <div class="subtitle">
            {row.get('Date','')} | {row.get('Start Time','')} <br>
            Court {row.get('Court No','')} | {row.get('Category','')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------- FULL SCHEDULE --------
st.subheader("📅 Full Schedule")

for _, row in df.iterrows():
    st.markdown(f"""
    <div class="card">
        <div class="title">{row.get('Match Details','')}</div>
        <div class="subtitle">
            {row.get('Date','')} | {row.get('Start Time','')} <br>
            Court {row.get('Court No','')} | {row.get('Category','')}
        </div>
    </div>
    """, unsafe_allow_html=True)
