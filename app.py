import streamlit as st
import pandas as pd
from datetime import datetime
from data_loader import load_data
import os

st.set_page_config(page_title="Court Mafia 2.0", layout="wide")

st.markdown("<h2 style='text-align:center;'>🤝 Our Esteemed Partners</h2>", unsafe_allow_html=True)

if os.path.exists("partners.png"):
    st.image("partners.png", use_container_width=True)

st.markdown("<h1 style='text-align:center;'>🏆 Court Mafia 2.0 🏆</h1>", unsafe_allow_html=True)
st.caption("Thane’s Defining Pickleball Tournament")

df = load_data()
df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x,str) else x))

for col in ['Player 1','Player 2','Player 3','Player 4','Team 1 Score','Team 2 Score']:
    if col not in df.columns:
        df[col]=None

df['Start_DateTime']=pd.to_datetime(df['Date'].astype(str)+" "+df['Start Time'].astype(str), errors='coerce')
df=df.sort_values(by="Start_DateTime")

def team(a,b):
    if pd.isna(a) or pd.isna(b): return None
    return " & ".join(sorted([str(a),str(b)]))

t1=df.apply(lambda r: team(r['Player 1'],r['Player 2']),axis=1)
t2=df.apply(lambda r: team(r['Player 3'],r['Player 4']),axis=1)

total_teams=len(pd.concat([t1,t2]).dropna().unique())

st.write("Matches:",len(df)," | Teams:",total_teams)

st.sidebar.header("Filters")
player=st.sidebar.text_input("Search Player")
category=st.sidebar.multiselect("Category",df['Category'].dropna().unique())
venue=st.sidebar.multiselect("Venue",df['Venue'].dropna().unique())

filtered=df.copy()

if player:
    player=player.lower()
    filtered=filtered[
        filtered['Match Details'].astype(str).str.lower().str.contains(player,na=False)|
        filtered['Player 1'].astype(str).str.lower().str.contains(player,na=False)|
        filtered['Player 2'].astype(str).str.lower().str.contains(player,na=False)|
        filtered['Player 3'].astype(str).str.lower().str.contains(player,na=False)|
        filtered['Player 4'].astype(str).str.lower().str.contains(player,na=False)
    ]

if category:
    filtered=filtered[filtered['Category'].isin(category)]
if venue:
    filtered=filtered[filtered['Venue'].isin(venue)]

st.subheader("Top 5 Upcoming Matches")
now=datetime.now()
upcoming=filtered[filtered['Start_DateTime']>=now].head(5)

for _,r in upcoming.iterrows():
    score=""
    if pd.notna(r['Team 1 Score']) or pd.notna(r['Team 2 Score']):
        score=f"{r['Team 1 Score']} - {r['Team 2 Score']}"
    st.write(r.get('Match Details',''),"|",score)

st.subheader("Full Schedule")
for _,r in filtered.iterrows():
    score=""
    if pd.notna(r['Team 1 Score']) or pd.notna(r['Team 2 Score']):
        score=f"{r['Team 1 Score']} - {r['Team 2 Score']}"
    st.write(r.get('Match Details',''),"|",score)
