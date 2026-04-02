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
.header-title { font-size: 34px; font-weight: 800; color: var(--text-color); text-align:center; }
.stat-card {
    background: linear-gradient(135deg, #1f7a6b, #145c52);
    color: white;
    padding: 14px;
    border-radius: 12px;
    text-align: center;
    min-width: 120px;
}
.stat-value { font-size: 22px; font-weight: 800; }
.stat-label { font-size: 12px; opacity: 0.85; }
</style>
""", unsafe_allow_html=True)

# ---------- PARTNERS (TOP) ----------
st.markdown("<h2 style='text-align:center;'>🤝 Our Esteemed Partners</h2>", unsafe_allow_html=True)
st.image("partners.png", use_container_width=True)

# ---------- HEADER ----------
st.markdown("<div class='header-title'>🏆 Court Mafia 2.0 🏆</div>", unsafe_allow_html=True)
st.caption("Thane’s Defining Pickleball Tournament")

# ---------- LOAD ----------
df = load_data()
# clean strings safely
df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

# ensure columns
for col in ['Player 1','Player 2','Player 3','Player 4','Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col] = None

# datetime
df['Start_DateTime'] = pd.to_datetime(df['Date'].astype(str) + " " + df['Start Time'].astype(str), errors='coerce')
df = df.sort_values(by="Start_DateTime")

# ---------- STATS ----------
def team(a,b):
    if pd.isna(a) or pd.isna(b): return None
    return " & ".join(sorted([str(a),str(b)]))

t1 = df.apply(lambda r: team(r['Player 1'], r['Player 2']), axis=1)
t2 = df.apply(lambda r: team(r['Player 3'], r['Player 4']), axis=1)

total_teams = len(pd.concat([t1, t2]).dropna().unique())
total_matches = len(df)

# duration in minutes
try:
    duration = pd.to_datetime(df['End Time'], errors='coerce') - pd.to_datetime(df['Start Time'], errors='coerce')
    total_minutes = int(duration.dt.total_seconds().sum() / 60)
except Exception:
    total_minutes = 0

st.subheader("📊 Tournament Stats")
stats = [("Matches", total_matches), ("Teams", total_teams), ("Minutes", total_minutes)]
cols = st.columns(len(stats))
for col, (label, val) in zip(cols, stats):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------- FILTERS (TOP, NOT SIDEBAR) ----------
st.subheader("🔍 Filters")
f1, f2, f3 = st.columns(3)
with f1:
    player = st.text_input("Search Player")
with f2:
    category = st.multiselect("Category", df['Category'].dropna().unique() if 'Category' in df.columns else [])
with f3:
    venue = st.multiselect("Venue", df['Venue'].dropna().unique() if 'Venue' in df.columns else [])

filtered = df.copy()

if player:
    p = player.lower()
    filtered = filtered[
        filtered['Match Details'].astype(str).str.lower().str.contains(p, na=False) |
        filtered['Player 1'].astype(str).str.lower().str.contains(p, na=False) |
        filtered['Player 2'].astype(str).str.lower().str.contains(p, na=False) |
        filtered['Player 3'].astype(str).str.lower().str.contains(p, na=False) |
        filtered['Player 4'].astype(str).str.lower().str.contains(p, na=False)
    ]

if category and 'Category' in filtered.columns:
    filtered = filtered[filtered['Category'].isin(category)]
if venue and 'Venue' in filtered.columns:
    filtered = filtered[filtered['Venue'].isin(venue)]

# ---------- UPCOMING ----------
st.subheader("🔥 Top 5 Upcoming Matches")
now = datetime.now()
upcoming = filtered[filtered['Start_DateTime'] >= now].head(5)

for _, r in upcoming.iterrows():
    score = ""
    if pd.notna(r.get('Team 1 Score')) or pd.notna(r.get('Team 2 Score')):
        score = f"<div class='score'>{r.get('Team 1 Score','')} - {r.get('Team 2 Score','')}</div>"
    st.markdown(f"""
    <div class="card highlight">
        <div class="title">{r.get('Match Details','')}</div>
        {score}
        <div class="subtitle">
            {r.get('Date','')} | {r.get('Start Time','')} <br>
            Court {r.get('Court No','')} | {r.get('Category','')} | {r.get('Venue','')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- FULL SCHEDULE ----------
st.subheader("📅 Full Schedule")
for _, r in filtered.iterrows():
    score = ""
    if pd.notna(r.get('Team 1 Score')) or pd.notna(r.get('Team 2 Score')):
        score = f"<div class='score'>{r.get('Team 1 Score','')} - {r.get('Team 2 Score','')}</div>"
    st.markdown(f"""
    <div class="card">
        <div class="title">{r.get('Match Details','')}</div>
        {score}
        <div class="subtitle">
            {r.get('Date','')} | {r.get('Start Time','')} <br>
            Court {r.get('Court No','')} | {r.get('Category','')} | {r.get('Venue','')}
        </div>
    </div>
    """, unsafe_allow_html=True)
