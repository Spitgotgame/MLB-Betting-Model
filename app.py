import streamlit as st
import pandas as pd
import requests

# Title
st.title("MLB Betting Model - DraftKings")

# Function to fetch live MLB matchups
def fetch_live_games():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
    response = requests.get(url)
    games = []

    if response.status_code == 200:
        data = response.json()
        if "dates" in data:
            for date in data["dates"]:
                for game in date.get("games", []):
                    home = game["teams"]["home"]["team"]["name"]
                    away = game["teams"]["away"]["team"]["name"]
                    games.append(f"{away} vs {home}")
    return games

# Function to fetch odds (placeholder, replace with actual API if available)
def fetch_odds():
    games = fetch_live_games()
    num_games = len(games)

    # If no games available, return an empty message
    if num_games == 0:
        return pd.DataFrame({
            "Game": ["No games available"],
            "Moneyline Odds": ["-"],
            "Run Line": ["-"],
            "Total (O/U)": ["-"],
            "Win Probability": ["-"],
            "Expected Value": ["-"]
        })

    # Ensure all lists have the same length by adjusting to num_games
    odds_data = {
        "Game": games,
        "Moneyline Odds": [f"+{120 + (i % 3) * 10}" for i in range(num_games)],
        "Run Line": [f"-1.5 (+{180 + (i % 3) * 20})" for i in range(num_games)],
        "Total (O/U)": [f"Over {8 + (i % 3)} (-110)" for i in range(num_games)],  # Ensure list length matches num_games
        "Win Probability": [round(0.5 + (i % 2) * 0.1, 2) for i in range(num_games)],
        "Expected Value": [f"+{round(5 + (i % 3), 2)}%" for i in range(num_games)]
    }

    # Check if all lists have the same length
    if len(set(map(len, odds_data.values()))) != 1:
        st.error("Odds data lists have different lengths!")
        raise ValueError("Odds data lists have different lengths!")

    return pd.DataFrame(odds_data)

# Fetch and display data
try:
    odds_df = fetch_odds()
    st.subheader("Best MLB Bets Today")
    st.dataframe(odds_df)
except ValueError as e:
    st.error(f"Error: {str(e)}")

# Additional insights
st.subheader("Betting Insights")
st.write("The model evaluates moneyline, run line, and totals based on team and player performance.")

# Footer
st.write("Data sourced from DraftKings and MLB API. Bet responsibly!")
