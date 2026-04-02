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

.stat-card {
    background: linear-gradient(135deg, #1f7a6b, #145c52);
    color: white;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
}

.stat-value { font-size: 26px; font-weight: 800; }
.stat-label { font-size: 12px; opacity: 0.8; }

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

for col in ['Player 1','Player 2','Player 3','Player 4','Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col] = None

df['Start_DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + " " + df['Start Time'].astype(str),
    errors='coerce'
)

df = df.sort_values(by="Start_DateTime")

# ---------- STATS ----------
def create_team(a,b):
    if pd.isna(a) or pd.isna(b):
        return None
    return " & ".join(sorted([str(a), str(b)]))

team1 = df.apply(lambda r: create_team(r['Player 1'], r['Player 2']), axis=1)
team2 = df.apply(lambda r: create_team(r['Player 3'], r['Player 4']), axis=1)

total_teams = len(pd.concat([team1, team2]).dropna().unique())
total_matches = len(df)

# duration
df['duration'] = pd.to_datetime(df['End Time'], errors='coerce') - pd.to_datetime(df['Start Time'], errors='coerce')
total_minutes = int(df['duration'].dt.total_seconds().sum()/60) if 'duration' in df else 0

st.subheader("📊 Tournament Stats")
c1,c2,c3 = st.columns(3)

stats = [("Matches", total_matches), ("Teams", total_teams), ("Minutes", total_minutes)]

for col,(label,val) in zip([c1,c2,c3], stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- FILTERS ----------
st.sidebar.header("Filters")

player = st.sidebar.text_input("Search Player")
category = st.sidebar.multiselect("Category", df['Category'].dropna().unique())
venue = st.sidebar.multiselect("Venue", df['Venue'].dropna().unique())

filtered = df.copy()

if player:
    player = player.lower()
    filtered = filtered[
        filtered['Match Details'].astype(str).str.lower().str.contains(player, na=False) |
        filtered['Player 1'].astype(str).str.lower().str.contains(player, na=False) |
        filtered['Player 2'].astype(str).str.lower().str.contains(player, na=False) |
        filtered['Player 3'].astype(str).str.lower().str.contains(player, na=False) |
        filtered['Player 4'].astype(str).str.lower().str.contains(player, na=False)
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
    score = ""
    if pd.notna(row['Team 1 Score']) or pd.notna(row['Team 2 Score']):
        score = f"<div class='score'>{row['Team 1 Score']} - {row['Team 2 Score']}</div>"

    st.markdown(f"""
    <div class="card highlight">
        <div class="title">{row.get('Match Details','')}</div>
        {score}
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
    st.info("Upload partners.png in repo")
