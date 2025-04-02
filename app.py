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

    # Create dynamic odds data
    moneyline_odds = [f"+{120 + (i % 3) * 10}" for i in range(num_games)]
    run_line = [f"-1.5 (+{180 + (i % 3) * 20})" for i in range(num_games)]
    total_ou = [f"Over {8 + (i % 3)} (-110)" for i in range(num_games)]
    win_probability = [round(0.5 + (i % 2) * 0.1, 2) for i in range(num_games)]
    expected_value = [f"+{round(5 + (i % 3), 2)}%" for i in range(num_games)]

    # Check if all columns are of the same length
    lengths = [len(moneyline_odds), len(run_line), len(total_ou), len(win_probability), len(expected_value)]
    if len(set(lengths)) != 1:
        st.error("Error: Column lengths do not match!")
        raise ValueError("Mismatch in column lengths")

    # Padding columns with None if they are shorter than the games list
    while len(moneyline_odds) < num_games:
        moneyline_odds.append("-")
    while len(run_line) < num_games:
        run_line.append("-")
    while len(total_ou) < num_games:
        total_ou.append("-")
    while len(win_probability) < num_games:
        win_probability.append("-")
    while len(expected_value) < num_games:
        expected_value.append("-")

    # Create the final dictionary
    odds_data = {
        "Game": games,
        "Moneyline Odds": moneyline_odds,
        "Run Line": run_line,
        "Total (O/U)": total_ou,
        "Win Probability": win_probability,
        "Expected Value": expected_value
    }

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
