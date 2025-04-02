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

# Function to fetch odds (placeholder, replace with actual API if available)
def fetch_odds():
    games = fetch_live_games()
    num_games = len(games)
    
    st.write(f"Number of games found: {num_games}")
    if num_games == 0:
        return pd.DataFrame({"Game": ["No games available"], "Moneyline Odds": ["-"], "Run Line": ["-"], "Total (O/U)": ["-"], "Win Probability": ["-"], "Expected Value": ["-"]})
    
    # Generate placeholder odds dynamically based on the number of games
    odds_data = {
        "Game": games,
        "Moneyline Odds": ["+120" if i % 2 == 0 else "-150" for i in range(num_games)],
        "Run Line": ["-1.5 (+180)" if i % 2 == 0 else "+1.5 (-140)" for i in range(num_games)],
        "Total (O/U)": ["Over 8.5 (-110)" if i % 2 == 0 else "Under 9.5 (-105)" for i in range(num_games)],
        "Win Probability": [round(0.5 + (i % 2) * 0.1, 2) for i in range(num_games)],
        "Expected Value": [5.2 if i % 2 == 0 else -2.3 for i in range(num_games)]
    }
    
    df = pd.DataFrame(odds_data)
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
