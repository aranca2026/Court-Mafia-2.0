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
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
col1, col2 = st.columns([1,5])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=90)
with col2:
    st.markdown("<div class='header-title'>🏆 Court Mafia 2.0 🏆</div>", unsafe_allow_html=True)
    st.caption("Thane’s Defining Pickleball Tournament")

# ---------- LOAD ----------
df = load_data()

# Clean text safely
df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

# Ensure required columns exist safely
for col in ['Player 1','Player 2','Player 3','Player 4','Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col] = None

df['Start_DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + " " + df['Start Time'].astype(str),
    errors='coerce'
)

df = df.sort_values(by="Start_DateTime")

# ---------- FIXED TEAM LOGIC ----------
def create_team(col1, col2):
    if pd.isna(col1) or pd.isna(col2):
        return None
    return " & ".join(sorted([str(col1), str(col2)]))

team1 = df.apply(lambda row: create_team(row['Player 1'], row['Player 2']), axis=1)
team2 = df.apply(lambda row: create_team(row['Player 3'], row['Player 4']), axis=1)

all_teams = pd.concat([team1, team2]).dropna().unique()
total_teams = len(all_teams)

# ---------- STATS ----------
st.subheader("📊 Tournament Stats")
c1, c2 = st.columns(2)
c1.metric("Matches", len(df))
c2.metric("Teams", total_teams)

# ---------- UPCOMING ----------
st.subheader("🔥 Top 5 Upcoming Matches")

now = datetime.now()
upcoming = df[df['Start_DateTime'] >= now].head(5)

for _, row in upcoming.iterrows():
    score_display = ""
    if pd.notna(row['Team 1 Score']) or pd.notna(row['Team 2 Score']):
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
