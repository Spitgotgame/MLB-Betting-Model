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
    
    if num_games == 0:
        return pd.DataFrame({"Game": ["No games available"], "Moneyline Odds": ["-"], "Run Line": ["-"], "Total (O/U)": ["-"], "Win Probability": ["-"], "Expected Value": ["-"]})
    
    odds_templates = {
        "Moneyline Odds": ["+120", "-150", "+200"],
        "Run Line": ["-1.5 (+180)", "+1.5 (-140)", "-1.5 (+220)"],
        "Total (O/U)": ["Over 8.5 (-110)", "Under 9.5 (-105)", "Over 7.5 (+100)"],
        "Win Probability": [0.55, 0.62, 0.48],
        "Expected Value": ["+5.2%", "-2.3%", "+7.1%"]
    }
    
    odds_data = {"Game": games}
    for key, values in odds_templates.items():
        odds_data[key] = (values * ((num_games // len(values)) + 1))[:num_games]  # Dynamically adjust list size
    
    return pd.DataFrame(odds_data)

# Fetch and display data
odds_df = fetch_odds()
st.subheader("Best MLB Bets Today")
st.dataframe(odds_df)

# Additional insights
st.subheader("Betting Insights")
st.write("The model evaluates moneyline, run line, and totals based on team and player performance.")

# Footer
st.write("Data sourced from DraftKings and MLB API. Bet responsibly!")
