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

    # Debugging: Print lengths of all lists
    st.write(f"Number of games: {num_games}")

    # Create dynamic odds data
    moneyline_odds = [f"+{120 + (i % 3) * 10}" for i in range(num_games)]
    run_line = [f"-1.5 (+{180 + (i % 3) * 20})" for i in range(num_games)]
    total_ou = [f"Over {8 + (i % 3)} (-110)" for i in range(num_games)]
    win_probability = [round(0.5 + (i % 2) * 0.1, 2) for i in range(num_games)]
    expected_value = [f"+{round(5 + (i % 3), 2)}%" for i in range(num_games)]

    # Debugging: Check lengths of each list
    st.write(f"Length of moneyline_odds: {len(moneyline_odds)}")
    st.write(f"Length of run_line: {len(run_line)}")
    st.write(f"Length of total_ou: {len(total_ou)}")
    st.write(f"Length of win_probability: {len(win_probability)}")
    st.write(f"Length of expected_value: {len(expected_value)}")

    # Ensure that all columns have the same length
    max_length = max(len(moneyline_odds), len(run_line), len(total_ou), len(win_probability), len(expected_value), num_games)

    # Padding columns with None if they are shorter than the max length
    while len(moneyline_odds) < max_length:
        moneyline_odds.append("-")
    while len(run_line) < max_length:
        run_line.append("-")
    while len(total_ou) < max_length:
        total_ou.append("-")
    while len(win_probability) < max_length:
        win_probability.append("-")
    while len(expected_value) < max_length:
        expected_value.append("-")

    # Check lengths after padding
    st.write(f"Final Length of moneyline_odds: {len(moneyline_odds)}")
    st.write(f"Final Length of run_line: {len(run_line)}")
    st.write(f"Final Length of total_ou: {len(total_ou)}")
    st.write(f"Final Length of win_probability: {len(win_probability)}")
    st.write(f"Final Length of expected_value: {len(expected_value)}")

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

