import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- SETTINGS ---
PREDICTIONS_DIR = r"C:\\MLB_Betting_AI\\daily_predictions"

# --- FUNCTIONS ---
def load_predictions(file_pattern):
    today = datetime.now().strftime('%Y%m%d')
    file_path = os.path.join(PREDICTIONS_DIR, f"{file_pattern}_{today}.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

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
        if selected_confidence != "All":
            df = df[(df['home_confidence'] == selected_confidence) | (df['away_confidence'] == selected_confidence)]
    else:
        df['confidence'] = df[edge_col_home].apply(classify_confidence)
        if selected_confidence != "All":
            df = df[df['confidence'] == selected_confidence]
    return df

# --- APP CONFIG ---
st.set_page_config(page_title="TheLastOdds - AI Sports Betting Dashboard", page_icon="⚡", layout="wide")

# --- SIDEBAR ---
st.sidebar.title("TheLastOdds Navigation")
page = st.sidebar.radio("Go to", ["Home", "AI Picks Dashboard", "Top 5 Picks", "Player Research Lab", "News & Injuries", "AI Betting Assistant"])

# --- LOAD DATA ---
moneyline_df = load_predictions("moneyline_predictions")
spread_df = load_predictions("spread_predictions")
totals_df = load_predictions("totals_predictions")

# --- LANDING PAGE ---
if page == "Home":
    st.markdown("""
    <h1 style='text-align: center; color: gold;'>TheLastOdds ⚡</h1>
    <h3 style='text-align: center; color: white;'>AI-Driven Winning Picks. Trusted by Sharps.</h3>
    """, unsafe_allow_html=True)
    st.markdown("""<div style='text-align: center;'><br>
    <a href='?page=AI Picks Dashboard' style='font-size:24px; padding:10px 20px; background-color:gold; color:black; text-decoration:none; border-radius:10px;'>Enter Dashboard</a>
    </div>""", unsafe_allow_html=True)

# --- PICKS DASHBOARD ---
elif page == "AI Picks Dashboard":
    st.header("📈 AI Sports Betting Picks")
    selected_bet_type = st.selectbox("Select Bet Type", ["Moneyline", "Spread", "Totals"])
    selected_confidence = st.selectbox("Select Confidence Tier", ["All", "Most Confident", "Very Confident", "Confident"])

    if selected_bet_type == "Moneyline":
        if not moneyline_df.empty:
            moneyline_df = apply_confidence_filter(moneyline_df, "home_edge", "away_edge")
            st.dataframe(moneyline_df, use_container_width=True)
        else:
            st.info("No Moneyline predictions available yet.")

    elif selected_bet_type == "Spread":
        if not spread_df.empty:
            spread_df = apply_confidence_filter(spread_df, "home_edge", "away_edge")
            st.dataframe(spread_df, use_container_width=True)
        else:
            st.info("No Spread predictions available yet.")

    elif selected_bet_type == "Totals":
        if not totals_df.empty:
            totals_df = apply_confidence_filter(totals_df, "over_edge", "under_edge")
            st.dataframe(totals_df, use_container_width=True)
        else:
            st.info("No Totals predictions available yet.")

# --- TOP 5 PICKS PAGE ---
elif page == "Top 5 Picks":
    st.header("🔥 Top 5 Picks of the Day")
    st.info("(Coming Soon) - Will auto-highlight the strongest edges daily!")

# --- PLAYER RESEARCH LAB ---
elif page == "Player Research Lab":
    st.header("📊 Player Research Lab")
    st.info("(Coming Soon) - Lookup rolling averages for any player over 5/10/20 games!")

# --- NEWS & INJURIES PAGE ---
elif page == "News & Injuries":
    st.header("📰 MLB News and Injury Updates")
    st.info("(Coming Soon) - Breaking injuries, trades, and rumor reports updated live!")

# --- AI BETTING ASSISTANT ---
elif page == "AI Betting Assistant":
    st.header("🤖 AI Betting Assistant")
    st.info("(Coming Soon) - Chat with TheLastOdds AI to get picks advice, explanations, and more!")

# --- FOOTER ---
st.markdown("""<hr><div style='text-align: center; color: gray;'>
Powered by TheLastOdds ⚡ | Built with AI 🚀
</div>""", unsafe_allow_html=True)
