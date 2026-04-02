import streamlit as st
import pandas as pd
from data_loader import load_data

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

st.title("Court Mafia 2.0")
st.caption("Leaderboard + Fixtures")

schedule_df, score_df = load_data()

schedule_df.columns = schedule_df.columns.str.strip()
score_df.columns = score_df.columns.str.strip()

# -------- CLEAN SCORECARD --------
score_df = score_df.dropna(how='all')

# try to find header row
header_idx = None
for i, row in score_df.iterrows():
    if 'Category' in str(row.values):
        header_idx = i
        break

if header_idx is not None:
    score_df.columns = score_df.iloc[header_idx]
    score_df = score_df.iloc[header_idx+1:]
    score_df = score_df.dropna(how='all')

# -------- LEADERBOARD --------
st.subheader("🏆 Leaderboard")

if 'Points' in score_df.columns:
    score_df = score_df.sort_values(by='Points', ascending=False)

    for i, row in score_df.head(10).iterrows():
        st.markdown(f"**#{i+1} {row.get('Teams','')}** — {row.get('Points','')}")
else:
    st.info("Scorecard format not detected")

# -------- MY MATCHES --------
player = st.text_input("🔍 Search Your Name")

if player:
    st.subheader("🎯 My Matches")
    my_df = schedule_df[
        schedule_df[['Player 1','Player 2','Player 3','Player 4']].astype(str)
        .apply(lambda x: x.str.contains(player, case=False, na=False))
        .any(axis=1)
    ]

    for _, row in my_df.iterrows():
        st.write(f"{row['Match Details']} | {row['Start Time']}")

# -------- SCHEDULE --------
st.subheader("📅 Schedule")

for _, row in schedule_df.iterrows():
    scoreA = row.get('Team 1 Score', "")
    scoreB = row.get('Team 2 Score', "")

    st.write(
        row['Match Details'],
        "|", row['Start Time'],
        "| Score:", scoreA, "-", scoreB
    )
