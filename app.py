# Function to fetch odds (placeholder, replace with actual API if available)
def fetch_odds():
    games = fetch_live_games()
    num_games = len(games)

    if num_games == 0:
        return pd.DataFrame({
            "Game": ["No games available"], 
            "Moneyline Odds": ["-"], 
            "Run Line": ["-"], 
            "Total (O/U)": ["-"], 
            "Win Probability": ["-"], 
            "Expected Value": ["-"]
        })

    # Generate placeholder odds dynamically based on the number of games
    moneyline_odds = ["+120" if i % 2 == 0 else "-150" for i in range(num_games)]
    run_line = ["-1.5 (+180)" if i % 2 == 0 else "+1.5 (-140)" for i in range(num_games)]
    total_ou = ["Over 8.5 (-110)" if i % 2 == 0 else "Under 9.5 (-105)" for i in range(num_games)]
    win_probability = [round(0.5 + (i % 2) * 0.1, 2) for i in range(num_games)]
    expected_value = ["+5.2%" if i % 2 == 0 else "-2.3%" for i in range(num_games)]

    # Debugging: Log list lengths before creating DataFrame
    list_lengths = {
        "games": len(games),
        "moneyline_odds": len(moneyline_odds),
        "run_line": len(run_line),
        "total_ou": len(total_ou),
        "win_probability": len(win_probability),
        "expected_value": len(expected_value),
    }
    
    st.write("List lengths:", list_lengths)  # Debugging output in Streamlit

    # Ensure all lists are the same length before creating DataFrame
    assert all(len(lst) == num_games for lst in [moneyline_odds, run_line, total_ou, win_probability, expected_value]), "List lengths do not match!"

    # Create DataFrame
    odds_data = {
        "Game": games,
        "Moneyline Odds": moneyline_odds,
        "Run Line": run_line,
        "Total (O/U)": total_ou,
        "Win Probability": win_probability,
        "Expected Value": expected_value
    }

    return pd.DataFrame(odds_data)
