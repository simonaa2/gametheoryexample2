# Copyright (c) 2024 Game Theory Applications
# Nash Equilibrium Calculator

import numpy as np
import pandas as pd
import streamlit as st
from itertools import product

def find_nash_equilibria(payoff_matrix_1, payoff_matrix_2):
    """Find pure strategy Nash equilibria for a 2-player game."""
    rows, cols = payoff_matrix_1.shape
    nash_equilibria = []
    
    for i in range(rows):
        for j in range(cols):
            # Check if (i,j) is a Nash equilibrium
            is_nash = True
            
            # Player 1's best response check
            player1_payoffs = payoff_matrix_1[:, j]
            if payoff_matrix_1[i, j] < np.max(player1_payoffs):
                is_nash = False
            
            # Player 2's best response check
            player2_payoffs = payoff_matrix_2[i, :]
            if payoff_matrix_2[i, j] < np.max(player2_payoffs):
                is_nash = False
            
            if is_nash:
                nash_equilibria.append((i, j))
    
    return nash_equilibria

def nash_equilibrium_calculator():
    st.set_page_config(page_title="Nash Equilibrium Calculator", page_icon="⚖️")
    st.markdown("# Nash Equilibrium Calculator")
    st.sidebar.header("Nash Equilibrium Calculator")
    
    st.write("""
    This tool helps you find Nash equilibria in 2-player strategic form games.
    Enter the payoff matrices for both players and we'll find all pure strategy Nash equilibria.
    """)
    
    # Game size selection
    st.subheader("Game Setup")
    col1, col2 = st.columns(2)
    
    with col1:
        rows = st.selectbox("Player 1 strategies (rows)", [2, 3, 4], index=0)
    with col2:
        cols = st.selectbox("Player 2 strategies (columns)", [2, 3, 4], index=0)
    
    # Payoff matrix input
    st.subheader("Payoff Matrices")
    
    # Initialize matrices
    if 'payoff_1' not in st.session_state:
        st.session_state.payoff_1 = np.array([[3, 0], [0, 3]])
        st.session_state.payoff_2 = np.array([[3, 0], [0, 3]])
    
    # Resize matrices if needed
    if st.session_state.payoff_1.shape != (rows, cols):
        st.session_state.payoff_1 = np.zeros((rows, cols))
        st.session_state.payoff_2 = np.zeros((rows, cols))
    
    # Input matrices
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1 Payoffs**")
        payoff_1 = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                payoff_1[i, j] = st.number_input(
                    f"P1({i+1},{j+1})", 
                    value=float(st.session_state.payoff_1[i, j]),
                    key=f"p1_{i}_{j}"
                )
    
    with col2:
        st.write("**Player 2 Payoffs**")
        payoff_2 = np.zeros((rows, cols))
        for i in range(rows):
            for j in range(cols):
                payoff_2[i, j] = st.number_input(
                    f"P2({i+1},{j+1})", 
                    value=float(st.session_state.payoff_2[i, j]),
                    key=f"p2_{i}_{j}"
                )
    
    # Update session state
    st.session_state.payoff_1 = payoff_1
    st.session_state.payoff_2 = payoff_2
    
    # Preset games
    st.subheader("Preset Games")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Prisoner's Dilemma"):
            st.session_state.payoff_1 = np.array([[3, 0], [5, 1]])
            st.session_state.payoff_2 = np.array([[3, 5], [0, 1]])
            st.rerun()
    
    with col2:
        if st.button("Coordination Game"):
            st.session_state.payoff_1 = np.array([[2, 0], [0, 1]])
            st.session_state.payoff_2 = np.array([[2, 0], [0, 1]])
            st.rerun()
    
    with col3:
        if st.button("Battle of Sexes"):
            st.session_state.payoff_1 = np.array([[2, 0], [0, 1]])
            st.session_state.payoff_2 = np.array([[1, 0], [0, 2]])
            st.rerun()
    
    # Display game matrix
    st.subheader("Game Matrix")
    game_display = []
    strategy_labels_1 = [f"S{i+1}" for i in range(rows)]
    strategy_labels_2 = [f"S{j+1}" for j in range(cols)]
    
    for i in range(rows):
        row = []
        for j in range(cols):
            cell = f"({payoff_1[i,j]:.1f}, {payoff_2[i,j]:.1f})"
            row.append(cell)
        game_display.append(row)
    
    df = pd.DataFrame(game_display, 
                     index=[f"Player 1: {s}" for s in strategy_labels_1],
                     columns=[f"Player 2: {s}" for s in strategy_labels_2])
    st.dataframe(df)
    
    # Find Nash equilibria
    if st.button("Find Nash Equilibria"):
        nash_eq = find_nash_equilibria(payoff_1, payoff_2)
        
        st.subheader("Results")
        if nash_eq:
            st.success(f"Found {len(nash_eq)} pure strategy Nash equilibria:")
            for i, (row, col) in enumerate(nash_eq):
                st.write(f"**Equilibrium {i+1}:** Player 1 plays S{row+1}, Player 2 plays S{col+1}")
                st.write(f"Payoffs: Player 1 gets {payoff_1[row, col]}, Player 2 gets {payoff_2[row, col]}")
        else:
            st.warning("No pure strategy Nash equilibria found.")
            st.info("This game might have mixed strategy equilibria only.")
    
    # Show analysis
    st.subheader("Game Analysis")
    
    # Dominant strategies
    st.write("**Dominant Strategy Analysis:**")
    
    # Player 1 dominant strategies
    for i in range(rows):
        dominates = []
        for k in range(rows):
            if k != i and all(payoff_1[i, j] >= payoff_1[k, j] for j in range(cols)):
                if any(payoff_1[i, j] > payoff_1[k, j] for j in range(cols)):
                    dominates.append(k)
        if dominates:
            st.write(f"Player 1: Strategy S{i+1} dominates strategies {[f'S{k+1}' for k in dominates]}")
    
    # Player 2 dominant strategies  
    for j in range(cols):
        dominates = []
        for k in range(cols):
            if k != j and all(payoff_2[i, j] >= payoff_2[i, k] for i in range(rows)):
                if any(payoff_2[i, j] > payoff_2[i, k] for i in range(rows)):
                    dominates.append(k)
        if dominates:
            st.write(f"Player 2: Strategy S{j+1} dominates strategies {[f'S{k+1}' for k in dominates]}")

if __name__ == "__main__":
    nash_equilibrium_calculator()