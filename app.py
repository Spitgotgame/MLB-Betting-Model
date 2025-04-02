def fetch_odds():
    games = fetch_live_games()
    num_games = len(games)
    
    if num_games == 0:
        empty_df = pd.DataFrame({
            "Game": ["No games available"], 
            "Moneyline Odds": ["-"], 
            "Run Line": ["-"], 
            "Total (O/U)": ["-"], 
            "Win Probability": ["-"], 
            "Expected Value": ["-"]
        })
        st.write("Generated Empty DataFrame:", empty_df)
        return empty_df

    odds_data = {
        "Game": games,
        "Moneyline Odds": ["+120" if i % 2 == 0 else "-150" for i in range(num_games)],
        "Run Line": ["-1.5 (+180)" if i % 2 == 0 else "+1.5 (-140)" for i in range(num_games)],
        "Total (O/U)": ["Over 8.5 (-110)" if i % 2 == 0 else "Under 9.5 (-105)" for i in range(num_games)],
        "Win Probability": [round(0.5 + (i % 2) * 0.1, 2) for i in range(num_games)],
        "Expected Value": ["+5.2%" if i % 2 == 0 else "-2.3%" for i in range(num_games)]
    }

    df = pd.DataFrame(odds_data)
    
    # Debugging: Print the DataFrame before returning
    st.write("Generated Odds DataFrame:", df)
    
    return df

