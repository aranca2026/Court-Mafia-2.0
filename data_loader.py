import pandas as pd
import streamlit as st

@st.cache_data(ttl=10)
def load_data():
    sheet_id="130OAkdOXSpFTk3vnvdww0of5hM8ABd4XdGfWT0F9PmA"
    url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Schedule"
    return pd.read_csv(url)
