import pandas as pd
import streamlit as st

@st.cache_data(ttl=20)
def load_data():
    sheet_id = "130OAkdOXSpFTk3vnvdww0of5hM8ABd4XdGfWT0F9PmA"

    schedule_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Schedule"
    scorecard_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Scorecard"

    schedule_df = pd.read_csv(schedule_url)
    score_df = pd.read_csv(scorecard_url)

    return schedule_df, score_df
