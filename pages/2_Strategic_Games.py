# Copyright (c) 2024 Game Theory Applications
# Strategic Form Games Analyzer

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def strategic_games_analyzer():
    st.set_page_config(page_title="Strategic Games Analyzer", page_icon="🎯")
    st.markdown("# Strategic Form Games Analyzer")
    st.sidebar.header("Strategic Games")
    
    st.write("""
    Analyze strategic form games, find dominant strategies, and explore various game theory concepts.
    This tool helps you understand payoff matrices and strategic interactions.
    """)
    
    # Game examples
    st.subheader("Game Examples")
    
    game_examples = {
        "Custom Game": None,
        "Prisoner's Dilemma": {
            "p1": np.array([[3, 0], [5, 1]]),
            "p2": np.array([[3, 5], [0, 1]]),
            "strategies_p1": ["Cooperate", "Defect"],
            "strategies_p2": ["Cooperate", "Defect"]
        },
        "Battle of the Sexes": {
            "p1": np.array([[2, 0], [0, 1]]),
            "p2": np.array([[1, 0], [0, 2]]),
            "strategies_p1": ["Opera", "Football"],
            "strategies_p2": ["Opera", "Football"]
        },
        "Matching Pennies": {
            "p1": np.array([[1, -1], [-1, 1]]),
            "p2": np.array([[-1, 1], [1, -1]]),
            "strategies_p1": ["Heads", "Tails"],
            "strategies_p2": ["Heads", "Tails"]
        },
        "Coordination Game": {
            "p1": np.array([[2, 0], [0, 1]]),
            "p2": np.array([[2, 0], [0, 1]]),
            "strategies_p1": ["Action A", "Action B"],
            "strategies_p2": ["Action A", "Action B"]
        },
        "Chicken Game": {
            "p1": np.array([[0, -1], [1, -10]]),
            "p2": np.array([[0, 1], [-1, -10]]),
            "strategies_p1": ["Swerve", "Straight"],
            "strategies_p2": ["Swerve", "Straight"]
        }
    }
    
    selected_game = st.selectbox("Choose a game:", list(game_examples.keys()))
    
    if selected_game != "Custom Game":
        game_data = game_examples[selected_game]
        payoff_1 = game_data["p1"]
        payoff_2 = game_data["p2"]
        strategies_p1 = game_data["strategies_p1"]
        strategies_p2 = game_data["strategies_p2"]
        rows, cols = payoff_1.shape
    else:
        # Custom game setup
        st.subheader("Custom Game Setup")
        col1, col2 = st.columns(2)
        
        with col1:
            rows = st.selectbox("Player 1 strategies", [2, 3, 4], index=0)
        with col2:
            cols = st.selectbox("Player 2 strategies", [2, 3, 4], index=0)
        
        # Strategy names
        strategies_p1 = []
        strategies_p2 = []
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Player 1 Strategy Names:**")
            for i in range(rows):
                name = st.text_input(f"Strategy {i+1}", value=f"S{i+1}", key=f"p1_name_{i}")
                strategies_p1.append(name)
        
        with col2:
            st.write("**Player 2 Strategy Names:**")
            for j in range(cols):
                name = st.text_input(f"Strategy {j+1}", value=f"S{j+1}", key=f"p2_name_{j}")
                strategies_p2.append(name)
        
        # Payoff matrices
        st.subheader("Payoff Matrices")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Player 1 Payoffs**")
            payoff_1 = np.zeros((rows, cols))
            for i in range(rows):
                for j in range(cols):
                    payoff_1[i, j] = st.number_input(
                        f"{strategies_p1[i]} vs {strategies_p2[j]}", 
                        value=0.0,
                        key=f"custom_p1_{i}_{j}"
                    )
        
        with col2:
            st.write("**Player 2 Payoffs**")
            payoff_2 = np.zeros((rows, cols))
            for i in range(rows):
                for j in range(cols):
                    payoff_2[i, j] = st.number_input(
                        f"{strategies_p1[i]} vs {strategies_p2[j]}", 
                        value=0.0,
                        key=f"custom_p2_{i}_{j}"
                    )
    
    # Display game matrix
    st.subheader("Game Matrix")
    game_display = []
    for i in range(rows):
        row = []
        for j in range(cols):
            cell = f"({payoff_1[i,j]:.1f}, {payoff_2[i,j]:.1f})"
            row.append(cell)
        game_display.append(row)
    
    df_display = pd.DataFrame(game_display, 
                             index=[f"P1: {s}" for s in strategies_p1],
                             columns=[f"P2: {s}" for s in strategies_p2])
    st.dataframe(df_display)
    
    # Analysis
    st.subheader("Game Analysis")
    
    # Best response analysis
    st.write("**Best Response Analysis:**")
    
    # Player 1 best responses
    st.write("*Player 1 Best Responses:*")
    for j in range(cols):
        best_responses = []
        max_payoff = np.max(payoff_1[:, j])
        for i in range(rows):
            if payoff_1[i, j] == max_payoff:
                best_responses.append(strategies_p1[i])
        st.write(f"Against P2's {strategies_p2[j]}: {', '.join(best_responses)} (payoff: {max_payoff})")
    
    # Player 2 best responses
    st.write("*Player 2 Best Responses:*")
    for i in range(rows):
        best_responses = []
        max_payoff = np.max(payoff_2[i, :])
        for j in range(cols):
            if payoff_2[i, j] == max_payoff:
                best_responses.append(strategies_p2[j])
        st.write(f"Against P1's {strategies_p1[i]}: {', '.join(best_responses)} (payoff: {max_payoff})")
    
    # Dominant strategy analysis
    st.write("**Dominant Strategy Analysis:**")
    
    # Player 1 dominance
    dominant_strategies_p1 = []
    dominated_strategies_p1 = []
    
    for i in range(rows):
        dominates = []
        dominated_by = []
        
        for k in range(rows):
            if k != i:
                # Check if strategy i dominates strategy k
                if all(payoff_1[i, j] >= payoff_1[k, j] for j in range(cols)):
                    if any(payoff_1[i, j] > payoff_1[k, j] for j in range(cols)):
                        dominates.append(strategies_p1[k])
                
                # Check if strategy i is dominated by strategy k
                if all(payoff_1[k, j] >= payoff_1[i, j] for j in range(cols)):
                    if any(payoff_1[k, j] > payoff_1[i, j] for j in range(cols)):
                        dominated_by.append(strategies_p1[k])
        
        if dominates:
            st.write(f"P1's {strategies_p1[i]} dominates: {', '.join(dominates)}")
            dominant_strategies_p1.append(strategies_p1[i])
        
        if dominated_by:
            st.write(f"P1's {strategies_p1[i]} is dominated by: {', '.join(dominated_by)}")
            dominated_strategies_p1.append(strategies_p1[i])
    
    # Player 2 dominance
    dominant_strategies_p2 = []
    dominated_strategies_p2 = []
    
    for j in range(cols):
        dominates = []
        dominated_by = []
        
        for k in range(cols):
            if k != j:
                # Check if strategy j dominates strategy k
                if all(payoff_2[i, j] >= payoff_2[i, k] for i in range(rows)):
                    if any(payoff_2[i, j] > payoff_2[i, k] for i in range(rows)):
                        dominates.append(strategies_p2[k])
                
                # Check if strategy j is dominated by strategy k
                if all(payoff_2[i, k] >= payoff_2[i, j] for i in range(rows)):
                    if any(payoff_2[i, k] > payoff_2[i, j] for i in range(rows)):
                        dominated_by.append(strategies_p2[k])
        
        if dominates:
            st.write(f"P2's {strategies_p2[j]} dominates: {', '.join(dominates)}")
            dominant_strategies_p2.append(strategies_p2[j])
        
        if dominated_by:
            st.write(f"P2's {strategies_p2[j]} is dominated by: {', '.join(dominated_by)}")
            dominated_strategies_p2.append(strategies_p2[j])
    
    if not dominant_strategies_p1 and not dominated_strategies_p1:
        st.write("Player 1 has no dominant or dominated strategies.")
    if not dominant_strategies_p2 and not dominated_strategies_p2:
        st.write("Player 2 has no dominant or dominated strategies.")
    
    # Nash equilibria
    st.write("**Pure Strategy Nash Equilibria:**")
    nash_equilibria = []
    
    for i in range(rows):
        for j in range(cols):
            # Check if (i,j) is a Nash equilibrium
            is_nash = True
            
            # Player 1's best response check
            p1_payoffs = payoff_1[:, j]
            if payoff_1[i, j] < np.max(p1_payoffs):
                is_nash = False
            
            # Player 2's best response check
            p2_payoffs = payoff_2[i, :]
            if payoff_2[i, j] < np.max(p2_payoffs):
                is_nash = False
            
            if is_nash:
                nash_equilibria.append((i, j))
    
    if nash_equilibria:
        for i, (row, col) in enumerate(nash_equilibria):
            st.success(f"Nash Equilibrium {i+1}: ({strategies_p1[row]}, {strategies_p2[col]}) with payoffs ({payoff_1[row, col]}, {payoff_2[row, col]})")
    else:
        st.warning("No pure strategy Nash equilibria found.")
    
    # Game classification
    st.write("**Game Classification:**")
    
    # Zero-sum check
    is_zero_sum = np.allclose(payoff_1 + payoff_2, 0)
    if is_zero_sum:
        st.info("This is a **zero-sum game** - one player's gain equals the other's loss.")
    else:
        st.info("This is a **non-zero-sum game** - players' interests are not completely opposed.")
    
    # Coordination check
    coordination_cells = 0
    total_cells = rows * cols
    for i in range(rows):
        for j in range(cols):
            if (payoff_1[i, j] > 0 and payoff_2[i, j] > 0) or (payoff_1[i, j] < 0 and payoff_2[i, j] < 0):
                coordination_cells += 1
    
    if coordination_cells > total_cells / 2:
        st.info("This appears to be a **coordination game** - players benefit from coordinating their actions.")
    
    # Visualizations
    st.subheader("Payoff Visualizations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(payoff_1, annot=True, fmt='.1f', 
                   xticklabels=strategies_p2, yticklabels=strategies_p1,
                   cmap='RdYlBu_r', ax=ax)
        ax.set_title('Player 1 Payoffs')
        st.pyplot(fig)
    
    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(payoff_2, annot=True, fmt='.1f',
                   xticklabels=strategies_p2, yticklabels=strategies_p1,
                   cmap='RdYlBu_r', ax=ax)
        ax.set_title('Player 2 Payoffs')
        st.pyplot(fig)

if __name__ == "__main__":
    strategic_games_analyzer()