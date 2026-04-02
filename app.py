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

.partner-title {
    font-size: 24px;
    font-weight: 700;
    text-align: center;
    margin-top: 30px;
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
df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

for col in ['Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col] = ""

df['Start_DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + " " + df['Start Time'].astype(str),
    errors='coerce'
)

df = df.sort_values(by="Start_DateTime")

# ---------- STATS ----------
total_matches = len(df)

team1 = df[['Player 1', 'Player 2']].astype(str).apply(lambda x: " & ".join(sorted(x)), axis=1)
team2 = df[['Player 3', 'Player 4']].astype(str).apply(lambda x: " & ".join(sorted(x)), axis=1)

total_teams = len(pd.concat([team1, team2]).dropna().unique())

st.subheader("📊 Tournament Stats")
c1, c2 = st.columns(2)
c1.metric("Matches", total_matches)
c2.metric("Teams", total_teams)

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

# ---------- PARTNERS ----------
st.markdown("<div class='partner-title'>🤝 Our Esteemed Partners</div>", unsafe_allow_html=True)

if os.path.exists("partners.png"):
    st.image("partners.png", use_container_width=True)
else:
    st.info("Upload partners.png in repo to display partner logos")
