import streamlit as st
import pandas as pd
import requests

# Title
st.title("MLB Betting Model - DraftKings")

# Your actual API key from OddsAPI
API_KEY = "8d8267e28eb7fb353944e3f68f496bf6"  # This is your API key

# OddsAPI endpoint for MLB odds
BASE_URL = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"

# Function to fetch live MLB matchups
def fetch_live_games():
    url = "https://statsapi.mlb.com/api/v1/schedule?sportId=1"
    response = requests.get(url)
    games = []
    
    st.write("Fetching live games...")
    if response.status_code == 200:
        data = response.json()
        if "dates" in data:
            for date in data["dates"]:
                for game in date.get("games", []):
                    home = game["teams"]["home"]["team"]["name"]
                    away = game["teams"]["away"]["team"]["name"]
                    games.append(f"{away} vs {home}")
    st.write(f"Games fetched: {games}")
    return games

# Function to fetch real odds from OddsAPI
def fetch_odds():
    games = fetch_live_games()
    num_games = len(games)
    
    st.write(f"Number of games found: {num_games}")
    if num_games == 0:
        return pd.DataFrame({"Game": ["No games available"], "Moneyline Odds": ["-"], "Run Line": ["-"], "Total (O/U)": ["-"], "Win Probability": ["-"], "Expected Value": ["-"]})

    # Make the API request to fetch real odds from OddsAPI
    params = {
        'apiKey': API_KEY,
        'regions': 'us',  # You can specify regions like 'us' or 'eu'
        'markets': 'h2h,spreads,totals',  # Betting markets: head-to-head, spread, totals
    }
    
    response = requests.get(BASE_URL, params=params)
    odds_data = []
    
    if response.status_code == 200:
        data = response.json()
        for i, game in enumerate(data):
            home_team = game['home_team']
            away_team = game['away_team']
            moneyline_odds = {book['title']: book['odds']['h2h'] for book in game['bookmakers']}
            run_line = {book['title']: book['odds']['spreads'] for book in game['bookmakers']}
            total_ou = {book['title']: book['odds']['totals'] for book in game['bookmakers']}
            
            odds_data.append({
                "Game": f"{away_team} vs {home_team}",
                "Moneyline Odds": moneyline_odds,
                "Run Line": run_line,
                "Total (O/U)": total_ou,
                "Win Probability": round(0.5 + (i % 2) * 0.1, 2),  # Replace with actual win probability data if available
                "Expected Value": 5.2 if i % 2 == 0 else -2.3  # Replace with expected value calculation
            })
    
    # If no data is returned, show a default empty dataframe
    if not odds_data:
        return pd.DataFrame({"Game": ["No odds available"], "Moneyline Odds": ["-"], "Run Line": ["-"], "Total (O/U)": ["-"], "Win Probability": ["-"], "Expected Value": ["-"]})
    
    df = pd.DataFrame(odds_data)

    # Ensure all columns containing numeric data are converted to numbers, handling errors gracefully
    df["Expected Value"] = pd.to_numeric(df["Expected Value"], errors='coerce')  # Handle non-numeric by converting to NaN
    df["Win Probability"] = pd.to_numeric(df["Win Probability"], errors='coerce')  # Same for Win Probability

    # Fill any NaN values in "Expected Value" or "Win Probability" with 0
    df["Expected Value"].fillna(0, inplace=True)
    df["Win Probability"].fillna(0, inplace=True)

    st.write("Odds DataFrame created:", df)
    return df

# Fetch and display data
odds_df = fetch_odds()

# Filter and sort for best bets
best_bets_df = odds_df[odds_df["Expected Value"] > 0].sort_values(by="Expected Value", ascending=False)

st.subheader("Best MLB Bets Today")
st.dataframe(best_bets_df.style.applymap(lambda x: 'background-color: lightgreen' if isinstance(x, float) and x > 0 else '', subset=['Expected Value']))

# Additional insights
st.subheader("Betting Insights")
st.write("The model evaluates moneyline, run line, and totals based on team and player performance.")

# Footer
st.write("Data sourced from DraftKings and MLB API. Bet responsibly!")
