import requests
import pandas as pd
import streamlit as st

# Your API key for fetching odds
API_KEY = 'fa612feb0c3313f6b04958c46016f9fa'  # Replace with your actual API key
SPORT = 'baseball_mlb'
BASE_URL = f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds'

def fetch_odds():
    """Fetch real-time odds for MLB games."""
    try:
        # Request the odds data from the API
        params = {
            'apiKey': API_KEY,
            'regions': 'us',  # US odds
            'markets': 'h2h,totals',  # Moneyline (h2h) and totals (over/under)
        }
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Parse the odds data
        games = []
        for game in data:
            game_info = {
                'home_team': game['home_team'],
                'away_team': game['away_team'],
                'moneyline': {book['title']: book['odds']['h2h'] for book in game['bookmakers']},
                'totals': {book['title']: book['odds']['totals'] for book in game['bookmakers']},
            }
            games.append(game_info)

        # Convert the odds data into a DataFrame
        odds_df = pd.DataFrame(games)
        return odds_df

    except Exception as e:
        print("Error fetching odds:", e)
        return pd.DataFrame()  # Return empty DataFrame on error

def calculate_expected_value(odds, probability):
    """Calculate the expected value of a bet given the odds and probability."""
    decimal_odds = odds + 100 if odds > 0 else 100 / abs(odds) + 1
    expected_value = (probability * decimal_odds) - (1 - probability)
    return expected_value

def evaluate_bets(odds_df, model_predictions):
    """Evaluate which bets to place based on expected value."""
    bets = []
    for index, row in odds_df.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']

        # Get model's predicted probabilities for each team
        home_prob = model_predictions.get(home_team, 0.50)  # Default to 50% if model doesn't have a prediction
        away_prob = model_predictions.get(away_team, 0.50)  # Default to 50% if model doesn't have a prediction

        # Compare model's probabilities with the current odds to calculate expected value
        home_odds = row['moneyline'].get('DraftKings', None)  # Example using DraftKings
        away_odds = row['moneyline'].get('DraftKings', None)

        # Calculate expected value for home and away team
        if home_odds and away_odds:
            home_ev = calculate_expected_value(home_odds[0], home_prob)
            away_ev = calculate_expected_value(away_odds[0], away_prob)

            # If the expected value is positive, it's a good bet
            if home_ev > 0:
                bets.append({'team': home_team, 'bet': 'moneyline', 'ev': home_ev, 'odds': home_odds[0]})
            if away_ev > 0:
                bets.append({'team': away_team, 'bet': 'moneyline', 'ev': away_ev, 'odds': away_odds[0]})

    return pd.DataFrame(bets)

# Streamlit input for model predictions
st.title("MLB Betting Model")

model_predictions_input = st.text_area(
    "Enter model predictions as a dictionary (e.g., {'Team A': 0.55, 'Team B': 0.45})",
    '{"Team A": 0.55, "Team B": 0.45, "Team C": 0.60, "Team D": 0.40}'
)

# Convert input to a dictionary
try:
    model_predictions = eval(model_predictions_input)
except:
    st.error("Invalid format. Ensure your predictions are in the correct dictionary format.")

# Fetch odds and evaluate bets
if model_predictions:
    odds_df = fetch_odds()  # Get the latest odds
    if not odds_df.empty:
        bets_df = evaluate_bets(odds_df, model_predictions)
        bets_df = bets_df.sort_values(by='ev', ascending=False)  # Sort by expected value

        # Display the recommended bets
        if not bets_df.empty:
            st.write("Recommended Bets with Positive EV:")
            st.dataframe(bets_df)
        else:
            st.write("No recommended bets at the moment.")
    else:
        st.write("Unable to fetch the odds. Please try again later.")
