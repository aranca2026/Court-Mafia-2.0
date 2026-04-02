import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data
import os

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

st.title("Court Mafia 2.0")
st.caption("Thane’s Defining Pickleball Tournament")

df = load_data()
df.columns = df.columns.str.strip()

df['Start_DateTime'] = pd.to_datetime(df['Date'].astype(str) + " " + df['Start Time'].astype(str), errors='coerce')
df = df.sort_values(by="Start_DateTime")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

player_search = st.sidebar.text_input("Search Player (My Matches)")

# ---------------- MY MATCHES ----------------
if player_search:
    st.subheader("🎯 My Matches")
    my_df = df[
        df[['Player 1','Player 2','Player 3','Player 4']].astype(str)
        .apply(lambda x: x.str.contains(player_search, case=False, na=False))
        .any(axis=1)
    ]

    for _, row in my_df.iterrows():
        scoreA = row.get('Team 1 Score', "")
        scoreB = row.get('Team 2 Score', "")

        st.markdown(f"""
        **{row['Match Details']}**

        {row['Date']} | {row['Start Time']}  
        Court {row['Court No']} | {row['Category']}

        **Score:** {scoreA} - {scoreB}
        ---
        """)

# ---------------- PLAYER STATS ----------------
st.subheader("📊 Player Stats Dashboard")

players = []

for _, row in df.iterrows():
    for p in ['Player 1','Player 2','Player 3','Player 4']:
        if pd.notna(row.get(p)):
            players.append(row[p])

players_df = pd.DataFrame(players, columns=["Player"])

stats = players_df.value_counts().reset_index()
stats.columns = ["Player", "Matches Played"]

st.dataframe(stats)

# ---------------- UPCOMING ----------------
st.subheader("🔥 Top 5 Upcoming Matches")

now = datetime.now()
upcoming = df[df['Start_DateTime'] >= now].head(5)

for _, row in upcoming.iterrows():
    st.write(row['Match Details'], "|", row['Start Time'])

# ---------------- FULL SCHEDULE ----------------
st.subheader("📅 Full Schedule")

for _, row in df.iterrows():
    scoreA = row.get('Team 1 Score', "")
    scoreB = row.get('Team 2 Score', "")

    st.write(
        row['Match Details'],
        "|", row['Date'],
        "|", row['Start Time'],
        "| Score:", scoreA, "-", scoreB
    )
