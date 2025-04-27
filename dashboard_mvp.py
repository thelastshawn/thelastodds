import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- SETTINGS ---
PREDICTIONS_DIR = r"C:\\MLB_Betting_AI\\daily_predictions"

def load_predictions(file_pattern):
    today = datetime.now().strftime('%Y%m%d')
    file_path = os.path.join(PREDICTIONS_DIR, f"{file_pattern}_{today}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

# --- MAIN ---
st.set_page_config(page_title="TheLastOdds - AI MLB Dashboard", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .css-18e3th9 {
        background-color: #0e1117;
    }
    .css-1d391kg {
        background-color: #0e1117;
    }
    .css-1v3fvcr {
        color: gold;
        font-size: 28px;
        font-weight: bold;
        text-align: center;
    }
    footer {
        visibility: hidden;
    }
    .footer {
        visibility: visible;
        text-align: center;
        color: gray;
        font-size: 12px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: gold;'>TheLastOdds ⚡</h1>", unsafe_allow_html=True)
st.caption("Model-Driven Confidence Picks 🔥 No Emotions, Just Data.")

# --- Load Data ---
moneyline_df = load_predictions("moneyline_predictions")
spread_df = load_predictions("spread_predictions")
totals_df = load_predictions("totals_predictions")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
bet_type = st.sidebar.selectbox("Select Bet Type", ["Moneyline", "Spread", "Totals"])
confidence_level = st.sidebar.selectbox("Select Confidence Tier", ["All", "Most Confident", "Very Confident", "Confident"])

# --- Functions for Confidence Filtering ---
def classify_confidence(edge):
    if edge >= 10:
        return "Most Confident"
    elif 5 <= edge < 10:
        return "Very Confident"
    elif 2 <= edge < 5:
        return "Confident"
    else:
        return "Low Confidence"

def apply_confidence_filter(df, edge_col_home, edge_col_away=None):
    if df.empty:
        return df
    if edge_col_away:
        df['home_confidence'] = df[edge_col_home].apply(classify_confidence)
        df['away_confidence'] = df[edge_col_away].apply(classify_confidence)
        if confidence_level != "All":
            df = df[(df['home_confidence'] == confidence_level) | (df['away_confidence'] == confidence_level)]
    else:
        df['confidence'] = df[edge_col_home].apply(classify_confidence)
        if confidence_level != "All":
            df = df[df['confidence'] == confidence_level]
    return df

# --- Display Data ---
if bet_type == "Moneyline":
    st.subheader("💰 Moneyline Picks")
    if not moneyline_df.empty:
        moneyline_df = apply_confidence_filter(moneyline_df, "home_edge", "away_edge")
        st.dataframe(moneyline_df, use_container_width=True)
    else:
        st.info("No Moneyline predictions available yet.")

elif bet_type == "Spread":
    st.subheader("📏 Spread Picks")
    if not spread_df.empty:
        spread_df = apply_confidence_filter(spread_df, "home_edge", "away_edge")
        st.dataframe(spread_df, use_container_width=True)
    else:
        st.info("No Spread predictions available yet.")

elif bet_type == "Totals":
    st.subheader("📊 Totals (Over/Under) Picks")
    if not totals_df.empty:
        totals_df = apply_confidence_filter(totals_df, "over_edge", "under_edge")
        st.dataframe(totals_df, use_container_width=True)
    else:
        st.info("No Totals predictions available yet.")

st.markdown("""<div class='footer'>
Powered by TheLastOdds ⚡ | Built with AI 🚀
</div>""", unsafe_allow_html=True)
