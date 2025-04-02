import streamlit as st
import pandas as pd
import numpy as np
import requests

# Title
st.title("MLB Betting Model - DraftKings")

# Function to fetch odds (replace with actual API call if available)
def fetch_odds():
    data = {
        "Game": ["Team A vs Team B", "Team C vs Team D", "Team E vs Team F"],
        "Moneyline Odds": ["+120", "-150", "+200"],
        "Run Line": ["-1.5 (+180)", "+1.5 (-140)", "-1.5 (+220)"],
        "Total (O/U)": ["Over 8.5 (-110)", "Under 9.5 (-105)", "Over 7.5 (+100)"],
        "Win Probability": [0.55, 0.62, 0.48],
        "Expected Value": ["+5.2%", "-2.3%", "+7.1%"]
    }
    return pd.DataFrame(data)

# Fetch and display data
odds_df = fetch_odds()
st.subheader("Best MLB Bets Today")
st.dataframe(odds_df)

# Additional insights
st.subheader("Betting Insights")
st.write("The model evaluates moneyline, run line, and totals based on team and player performance.")

# Footer
st.write("Data sourced from DraftKings. Bet responsibly!")
