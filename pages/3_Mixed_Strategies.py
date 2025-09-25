# Copyright (c) 2024 Game Theory Applications
# Mixed Strategy Calculator

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import sympy as sp

def calculate_mixed_strategy_2x2(payoff_1, payoff_2):
    """Calculate mixed strategy Nash equilibrium for 2x2 games."""
    # Player 1's mixed strategy: probability p of playing strategy 0
    # Player 2's mixed strategy: probability q of playing strategy 0
    
    # For Player 2 to be indifferent between strategies:
    # EU2(strategy 0) = EU2(strategy 1)
    # p * payoff_2[0,0] + (1-p) * payoff_2[1,0] = p * payoff_2[0,1] + (1-p) * payoff_2[1,1]
    
    # Solve for p
    numerator = payoff_2[1,1] - payoff_2[1,0]
    denominator = payoff_2[0,0] - payoff_2[0,1] - payoff_2[1,0] + payoff_2[1,1]
    
    if abs(denominator) < 1e-10:
        p_optimal = None  # Player 2 is not indifferent
    else:
        p_optimal = numerator / denominator
    
    # For Player 1 to be indifferent between strategies:
    # EU1(strategy 0) = EU1(strategy 1)
    # q * payoff_1[0,0] + (1-q) * payoff_1[0,1] = q * payoff_1[1,0] + (1-q) * payoff_1[1,1]
    
    # Solve for q
    numerator = payoff_1[1,1] - payoff_1[0,1]
    denominator = payoff_1[0,0] - payoff_1[1,0] - payoff_1[0,1] + payoff_1[1,1]
    
    if abs(denominator) < 1e-10:
        q_optimal = None  # Player 1 is not indifferent
    else:
        q_optimal = numerator / denominator
    
    return p_optimal, q_optimal

def mixed_strategy_calculator():
    st.set_page_config(page_title="Mixed Strategy Calculator", page_icon="🎲")
    st.markdown("# Mixed Strategy Calculator")
    st.sidebar.header("Mixed Strategies")
    
    st.write("""
    Calculate mixed strategy Nash equilibria for strategic form games. 
    A mixed strategy is a probability distribution over pure strategies.
    """)
    
    with st.expander("📚 About Mixed Strategies"):
        st.write("""
        **Mixed Strategy**: Instead of always playing the same pure strategy, a player randomizes 
        over their available strategies according to some probability distribution.
        
        **Mixed Strategy Nash Equilibrium**: A strategy profile where each player's mixed strategy 
        is a best response to the other players' mixed strategies.
        
        **Key Properties**:
        - Every finite game has at least one Nash equilibrium (pure or mixed)
        - In a mixed strategy equilibrium, players are indifferent between the strategies 
          they play with positive probability
        - Mixed strategies can be optimal even when pure strategy equilibria exist
        """)
    
    # Game setup
    st.subheader("Game Setup")
    
    # For now, focus on 2x2 games for mixed strategy calculation
    st.info("Currently supporting 2x2 games for mixed strategy Nash equilibrium calculation.")
    
    # Predefined games
    games = {
        "Custom": None,
        "Matching Pennies": {
            "p1": np.array([[1, -1], [-1, 1]]),
            "p2": np.array([[-1, 1], [1, -1]]),
            "strategies_p1": ["Heads", "Tails"],
            "strategies_p2": ["Heads", "Tails"]
        },
        "Battle of Sexes": {
            "p1": np.array([[2, 0], [0, 1]]),
            "p2": np.array([[1, 0], [0, 2]]),
            "strategies_p1": ["Opera", "Football"],
            "strategies_p2": ["Opera", "Football"]
        },
        "Chicken Game": {
            "p1": np.array([[0, -1], [1, -10]]),
            "p2": np.array([[0, 1], [-1, -10]]),
            "strategies_p1": ["Swerve", "Straight"],
            "strategies_p2": ["Swerve", "Straight"]
        }
    }
    
    selected_game = st.selectbox("Choose a game:", list(games.keys()))
    
    if selected_game != "Custom":
        game_data = games[selected_game]
        payoff_1 = game_data["p1"]
        payoff_2 = game_data["p2"]
        strategies_p1 = game_data["strategies_p1"]
        strategies_p2 = game_data["strategies_p2"]
    else:
        # Custom 2x2 game
        st.subheader("Custom 2x2 Game")
        
        # Strategy names
        col1, col2 = st.columns(2)
        with col1:
            s1_p1 = st.text_input("Player 1 Strategy 1", value="Strategy A")
            s2_p1 = st.text_input("Player 1 Strategy 2", value="Strategy B")
            strategies_p1 = [s1_p1, s2_p1]
        
        with col2:
            s1_p2 = st.text_input("Player 2 Strategy 1", value="Strategy A")
            s2_p2 = st.text_input("Player 2 Strategy 2", value="Strategy B")
            strategies_p2 = [s1_p2, s2_p2]
        
        # Payoff inputs
        st.write("**Payoff Matrix Input:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            p1_00 = st.number_input(f"P1: {s1_p1} vs {s1_p2}", value=0.0)
            p2_00 = st.number_input(f"P2: {s1_p1} vs {s1_p2}", value=0.0)
        
        with col2:
            p1_01 = st.number_input(f"P1: {s1_p1} vs {s2_p2}", value=0.0)
            p2_01 = st.number_input(f"P2: {s1_p1} vs {s2_p2}", value=0.0)
        
        with col3:
            p1_10 = st.number_input(f"P1: {s2_p1} vs {s1_p2}", value=0.0)
            p2_10 = st.number_input(f"P2: {s2_p1} vs {s1_p2}", value=0.0)
        
        with col4:
            p1_11 = st.number_input(f"P1: {s2_p1} vs {s2_p2}", value=0.0)
            p2_11 = st.number_input(f"P2: {s2_p1} vs {s2_p2}", value=0.0)
        
        payoff_1 = np.array([[p1_00, p1_01], [p1_10, p1_11]])
        payoff_2 = np.array([[p2_00, p2_01], [p2_10, p2_11]])
    
    # Display game matrix
    st.subheader("Game Matrix")
    game_display = [
        [f"({payoff_1[0,0]:.1f}, {payoff_2[0,0]:.1f})", f"({payoff_1[0,1]:.1f}, {payoff_2[0,1]:.1f})"],
        [f"({payoff_1[1,0]:.1f}, {payoff_2[1,0]:.1f})", f"({payoff_1[1,1]:.1f}, {payoff_2[1,1]:.1f})"]
    ]
    
    df_display = pd.DataFrame(game_display,
                             index=[f"P1: {strategies_p1[0]}", f"P1: {strategies_p1[1]}"],
                             columns=[f"P2: {strategies_p2[0]}", f"P2: {strategies_p2[1]}"])
    st.dataframe(df_display)
    
    # Calculate mixed strategy equilibrium
    if st.button("Calculate Mixed Strategy Nash Equilibrium"):
        st.subheader("Mixed Strategy Analysis")
        
        # First check for pure strategy Nash equilibria
        pure_nash = []
        for i in range(2):
            for j in range(2):
                is_nash = True
                # Check Player 1's best response
                if payoff_1[i, j] < np.max(payoff_1[:, j]):
                    is_nash = False
                # Check Player 2's best response
                if payoff_2[i, j] < np.max(payoff_2[i, :]):
                    is_nash = False
                if is_nash:
                    pure_nash.append((i, j))
        
        if pure_nash:
            st.write("**Pure Strategy Nash Equilibria:**")
            for i, (row, col) in enumerate(pure_nash):
                st.success(f"Equilibrium {i+1}: ({strategies_p1[row]}, {strategies_p2[col]}) "
                          f"with payoffs ({payoff_1[row, col]:.2f}, {payoff_2[row, col]:.2f})")
        
        # Calculate mixed strategy equilibrium
        p_optimal, q_optimal = calculate_mixed_strategy_2x2(payoff_1, payoff_2)
        
        st.write("**Mixed Strategy Nash Equilibrium:**")
        
        if p_optimal is not None and q_optimal is not None:
            if 0 <= p_optimal <= 1 and 0 <= q_optimal <= 1:
                st.success("Mixed strategy Nash equilibrium found!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Player 1's Mixed Strategy:**")
                    st.write(f"Play {strategies_p1[0]} with probability {p_optimal:.3f}")
                    st.write(f"Play {strategies_p1[1]} with probability {1-p_optimal:.3f}")
                    
                    # Expected payoffs
                    eu1_0 = q_optimal * payoff_1[0,0] + (1-q_optimal) * payoff_1[0,1]
                    eu1_1 = q_optimal * payoff_1[1,0] + (1-q_optimal) * payoff_1[1,1]
                    st.write(f"Expected payoff: {eu1_0:.3f}")
                
                with col2:
                    st.write("**Player 2's Mixed Strategy:**")
                    st.write(f"Play {strategies_p2[0]} with probability {q_optimal:.3f}")
                    st.write(f"Play {strategies_p2[1]} with probability {1-q_optimal:.3f}")
                    
                    # Expected payoffs
                    eu2_0 = p_optimal * payoff_2[0,0] + (1-p_optimal) * payoff_2[1,0]
                    eu2_1 = p_optimal * payoff_2[0,1] + (1-p_optimal) * payoff_2[1,1]
                    st.write(f"Expected payoff: {eu2_0:.3f}")
                
                # Visualization
                st.subheader("Strategy Visualization")
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
                
                # Player 1's mixed strategy
                labels1 = strategies_p1
                sizes1 = [p_optimal, 1-p_optimal]
                ax1.pie(sizes1, labels=labels1, autopct='%1.1f%%', startangle=90)
                ax1.set_title("Player 1's Mixed Strategy")
                
                # Player 2's mixed strategy
                labels2 = strategies_p2
                sizes2 = [q_optimal, 1-q_optimal]
                ax2.pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=90)
                ax2.set_title("Player 2's Mixed Strategy")
                
                st.pyplot(fig)
                
            else:
                st.warning("Mixed strategy probabilities are outside [0,1] range. "
                          "The game may only have pure strategy equilibria.")
                if p_optimal is not None:
                    st.write(f"Player 1's calculated probability: {p_optimal:.3f}")
                if q_optimal is not None:
                    st.write(f"Player 2's calculated probability: {q_optimal:.3f}")
        else:
            st.warning("Could not calculate mixed strategy equilibrium. "
                      "One or both players may have a dominant strategy.")
    
    # Expected payoff calculator
    st.subheader("Expected Payoff Calculator")
    st.write("Calculate expected payoffs for given mixed strategies:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1's Strategy:**")
        prob_p1_s1 = st.slider(f"Probability of {strategies_p1[0]}", 0.0, 1.0, 0.5, 0.01, key="p1_slider")
        prob_p1_s2 = 1 - prob_p1_s1
        st.write(f"Probability of {strategies_p1[1]}: {prob_p1_s2:.2f}")
    
    with col2:
        st.write("**Player 2's Strategy:**")
        prob_p2_s1 = st.slider(f"Probability of {strategies_p2[0]}", 0.0, 1.0, 0.5, 0.01, key="p2_slider")
        prob_p2_s2 = 1 - prob_p2_s1
        st.write(f"Probability of {strategies_p2[1]}: {prob_p2_s2:.2f}")
    
    # Calculate expected payoffs
    expected_payoff_1 = (prob_p1_s1 * prob_p2_s1 * payoff_1[0,0] +
                        prob_p1_s1 * prob_p2_s2 * payoff_1[0,1] +
                        prob_p1_s2 * prob_p2_s1 * payoff_1[1,0] +
                        prob_p1_s2 * prob_p2_s2 * payoff_1[1,1])
    
    expected_payoff_2 = (prob_p1_s1 * prob_p2_s1 * payoff_2[0,0] +
                        prob_p1_s1 * prob_p2_s2 * payoff_2[0,1] +
                        prob_p1_s2 * prob_p2_s1 * payoff_2[1,0] +
                        prob_p1_s2 * prob_p2_s2 * payoff_2[1,1])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Player 1 Expected Payoff", f"{expected_payoff_1:.3f}")
    with col2:
        st.metric("Player 2 Expected Payoff", f"{expected_payoff_2:.3f}")
    
    # Best response analysis
    st.subheader("Best Response Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1's Best Response to Player 2's Strategy:**")
        eu1_s1 = prob_p2_s1 * payoff_1[0,0] + prob_p2_s2 * payoff_1[0,1]
        eu1_s2 = prob_p2_s1 * payoff_1[1,0] + prob_p2_s2 * payoff_1[1,1]
        
        st.write(f"EU({strategies_p1[0]}) = {eu1_s1:.3f}")
        st.write(f"EU({strategies_p1[1]}) = {eu1_s2:.3f}")
        
        if eu1_s1 > eu1_s2:
            st.success(f"Best response: {strategies_p1[0]}")
        elif eu1_s2 > eu1_s1:
            st.success(f"Best response: {strategies_p1[1]}")
        else:
            st.info("Player 1 is indifferent between strategies")
    
    with col2:
        st.write("**Player 2's Best Response to Player 1's Strategy:**")
        eu2_s1 = prob_p1_s1 * payoff_2[0,0] + prob_p1_s2 * payoff_2[1,0]
        eu2_s2 = prob_p1_s1 * payoff_2[0,1] + prob_p1_s2 * payoff_2[1,1]
        
        st.write(f"EU({strategies_p2[0]}) = {eu2_s1:.3f}")
        st.write(f"EU({strategies_p2[1]}) = {eu2_s2:.3f}")
        
        if eu2_s1 > eu2_s2:
            st.success(f"Best response: {strategies_p2[0]}")
        elif eu2_s2 > eu2_s1:
            st.success(f"Best response: {strategies_p2[1]}")
        else:
            st.info("Player 2 is indifferent between strategies")

if __name__ == "__main__":
    mixed_strategy_calculator()