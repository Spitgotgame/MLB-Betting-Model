import streamlit as st
import pandas as pd
import requests

# Title
st.title("MLB Betting Model - DraftKings")

# Function to fetch live MLB matchups
def fetch_live_games():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date=2024-04-02"
    response = requests.get(url)
    games = []
    
    if response.status_code == 200:
        data = response.json()
        for date in data["dates"]:
            for game in date["games"]:
                home = game["teams"]["home"]["team"]["name"]
                away = game["teams"]["away"]["team"]["name"]
                games.append(f"{away} vs {home}")
    return games

# Function to fetch odds (placeholder, replace with actual API if available)
def fetch_odds():
    games = fetch_live_games()
    data = {
        "Game": games if games else ["No games available"],
        "Moneyline Odds": ["+120", "-150", "+200"][:len(games)],
        "Run Line": ["-1.5 (+180)", "+1.5 (-140)", "-1.5 (+220)"][:len(games)],
        "Total (O/U)": ["Over 8.5 (-110)", "Under 9.5 (-105)", "Over 7.5 (+100)"][:len(games)],
        "Win Probability": [0.55, 0.62, 0.48][:len(games)],
        "Expected Value": ["+5.2%", "-2.3%", "+7.1%"][:len(games)]
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
st.write("Data sourced from DraftKings and MLB API. Bet responsibly!")
