import pandas as pd
import streamlit as st

@st.cache_data(ttl=20)
def load_data():
    sheet_id = "130OAkdOXSpFTk3vnvdww0of5hM8ABd4XdGfWT0F9PmA"

    schedule_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Schedule"
    scorecard_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Scorecard"

    try:
        schedule_df = pd.read_csv(schedule_url)
    except:
        schedule_df = pd.DataFrame()

    try:
        score_df = pd.read_csv(scorecard_url)
    except:
        score_df = pd.DataFrame()

    return schedule_df, score_df
