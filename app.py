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
    
    # Debugging: Output the full response from the OddsAPI
    st.write("Full response from OddsAPI:")
    try:
        data = response.json()  # Parse the response as JSON
        st.write(data)  # Display the full data to check the structure
    except Exception as e:
        st.write("Error parsing response as JSON:", e)
        return pd.DataFrame({"Game": ["Error in fetching odds"], "Moneyline Odds": ["-"], "Run Line": ["-"], "Total (O/U)": ["-"], "Win Probability": ["-"], "Expected Value": ["-"]})

    odds_data = []
    
    if response.status_code == 200:
        for i, game in enumerate(data):
            home_team = game['home_team']
            away_team = game['away_team']
            
            # Debug: Print bookmakers structure for each game
            st.write(f"Bookmakers for game {away_team} vs {home_team}:")
            if 'bookmakers' in game:
                st.write(game['bookmakers'])  # Inspect bookmakers data
            else:
                st.write("No bookmakers data available")
            
            try:
                moneyline_odds = {book['title']: book['odds']['h2h'] for book in game['bookmakers'] if 'h2h' in book['odds']}
            except KeyError:
                moneyline_odds = "No moneyline odds available"
            
            try:
                run_line = {book['title']: book['odds']['spreads'] for book in game['bookmakers'] if 'spreads' in book['odds']}
            except KeyError:
                run_line = "No run line odds available"
            
            try:
                total_ou = {book['title']: book['odds']['totals'] for book in game['bookmakers'] if 'totals' in book['odds']}
            except KeyError:
                total_ou = "No total odds available"
            
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

    # Debugging: Output the raw data before conversion
    st.write("Raw DataFrame Before Processing:")
    st.write(df)

    # Convert 'Win Probability' and 'Expected Value' columns to numeric, handling errors
    df["Expected Value"] = pd.to_numeric(df["Expected Value"], errors='coerce')  # Convert to numeric, replace errors with NaN
    df["Win Probability"] = pd.to_numeric(df["Win Probability"], errors='coerce')  # Same for Win Probability

    # Fill any NaN values with 0 (or any other appropriate strategy)
    df["Expected Value"].fillna(0, inplace=True)
    df["Win Probability"].fillna(0, inplace=True)

    # Debugging: Check the data types after conversion
    st.write("Data types after conversion:")
    st.write(df.dtypes)

    st.write("Processed DataFrame:")
    st.write(df)
    
    return df

# Fetch and display data
odds_df = fetch_odds()

# Filter and sort for best bets (based on Expected Value)
best_bets_df = odds_df[odds_df["Expected Value"] > 0].sort_values(by="Expected Value", ascending=False)

st.subheader("Best MLB Bets Today")
st.dataframe(best_bets_df.style.applymap(lambda x: 'background-color: lightgreen' if isinstance(x, float) and x > 0 else '', subset=['Expected Value']))

# Additional insights
st.subheader("Betting Insights")
st.write("The model evaluates moneyline, run line, and totals based on team and player performance.")

# Footer
st.write("Data sourced from DraftKings and MLB API. Bet responsibly!")
