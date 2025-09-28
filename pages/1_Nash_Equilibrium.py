import streamlit as st
import numpy as np
import pandas as pd
from utils import show_code


def nash_equilibrium_finder():
    st.subheader("2x2 Game Nash Equilibrium Finder")
    
    st.write("""
    Enter payoffs for a 2x2 game and find all pure strategy Nash equilibria.
    A Nash equilibrium is a strategy profile where no player can improve their payoff by unilaterally changing their strategy.
    """)
    
    # Input section for payoff matrices
    st.write("### Enter Payoff Matrices")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1 Payoffs**")
        p1_tl = st.number_input("Top-Left", value=3, key="p1_tl")
        p1_tr = st.number_input("Top-Right", value=0, key="p1_tr")
        p1_bl = st.number_input("Bottom-Left", value=5, key="p1_bl")
        p1_br = st.number_input("Bottom-Right", value=1, key="p1_br")
    
    with col2:
        st.write("**Player 2 Payoffs**")
        p2_tl = st.number_input("Top-Left", value=3, key="p2_tl")
        p2_tr = st.number_input("Top-Right", value=5, key="p2_tr")
        p2_bl = st.number_input("Bottom-Left", value=0, key="p2_bl")
        p2_br = st.number_input("Bottom-Right", value=1, key="p2_br")
    
    # Create matrices
    payoff_p1 = np.array([[p1_tl, p1_tr], [p1_bl, p1_br]])
    payoff_p2 = np.array([[p2_tl, p2_tr], [p2_bl, p2_br]])
    
    # Display matrices nicely
    st.write("### Game Matrix")
    
    # Create a combined display
    game_display = pd.DataFrame(
        [
            [f"({p1_tl}, {p2_tl})", f"({p1_tr}, {p2_tr})"],
            [f"({p1_bl}, {p2_bl})", f"({p1_br}, {p2_br})"]
        ],
        columns=["Player 2: Strategy A", "Player 2: Strategy B"],
        index=["Player 1: Strategy A", "Player 1: Strategy B"]
    )
    st.dataframe(game_display)
    
    # Find Nash equilibria
    st.write("### Nash Equilibrium Analysis")
    
    nash_equilibria = []
    strategy_names = [("Strategy A", "Strategy A"), ("Strategy A", "Strategy B"), 
                      ("Strategy B", "Strategy A"), ("Strategy B", "Strategy B")]
    
    # Check each strategy combination
    for i in range(2):
        for j in range(2):
            is_nash = True
            
            # Check Player 1's best response
            current_p1 = payoff_p1[i, j]
            alternative_p1 = payoff_p1[1-i, j]
            
            # Check Player 2's best response
            current_p2 = payoff_p2[i, j]
            alternative_p2 = payoff_p2[i, 1-j]
            
            # Is this a Nash equilibrium?
            p1_satisfied = current_p1 >= alternative_p1
            p2_satisfied = current_p2 >= alternative_p2
            
            if p1_satisfied and p2_satisfied:
                nash_equilibria.append((strategy_names[i*2 + j], current_p1, current_p2))
    
    if nash_equilibria:
        st.success(f"Found {len(nash_equilibria)} pure strategy Nash equilibrium/equilibria:")
        for i, (strategies, p1_payoff, p2_payoff) in enumerate(nash_equilibria):
            st.write(f"**Equilibrium {i+1}:** {strategies[0]} vs {strategies[1]}")
            st.write(f"  - Player 1 payoff: {p1_payoff}")
            st.write(f"  - Player 2 payoff: {p2_payoff}")
    else:
        st.warning("No pure strategy Nash equilibria found.")
        
        # Check for mixed strategy equilibrium
        st.write("### Mixed Strategy Analysis")
        st.write("When no pure strategy Nash equilibrium exists, there might be a mixed strategy equilibrium.")
        
        # Calculate mixed strategy equilibrium
        try:
            # For Player 1 to mix, Player 2 must be indifferent
            # p2_tl * p + p2_bl * (1-p) = p2_tr * p + p2_br * (1-p)
            # Solving for p (probability Player 1 plays Strategy A)
            if (p2_tl - p2_bl) != (p2_tr - p2_br):
                p1_prob_a = (p2_br - p2_bl) / ((p2_tl - p2_bl) - (p2_tr - p2_br))
                
                # For Player 2 to mix, Player 1 must be indifferent
                # p1_tl * q + p1_tr * (1-q) = p1_bl * q + p1_br * (1-q)
                if (p1_tl - p1_tr) != (p1_bl - p1_br):
                    p2_prob_a = (p1_br - p1_tr) / ((p1_tl - p1_tr) - (p1_bl - p1_br))
                    
                    # Check if probabilities are valid (between 0 and 1)
                    if 0 <= p1_prob_a <= 1 and 0 <= p2_prob_a <= 1:
                        st.success("Mixed Strategy Nash Equilibrium found:")
                        st.write(f"Player 1 plays Strategy A with probability: {p1_prob_a:.3f}")
                        st.write(f"Player 2 plays Strategy A with probability: {p2_prob_a:.3f}")
                        
                        # Calculate expected payoffs
                        expected_p1 = (p1_prob_a * p2_prob_a * p1_tl + 
                                     p1_prob_a * (1-p2_prob_a) * p1_tr + 
                                     (1-p1_prob_a) * p2_prob_a * p1_bl + 
                                     (1-p1_prob_a) * (1-p2_prob_a) * p1_br)
                        
                        expected_p2 = (p1_prob_a * p2_prob_a * p2_tl + 
                                     p1_prob_a * (1-p2_prob_a) * p2_tr + 
                                     (1-p1_prob_a) * p2_prob_a * p2_bl + 
                                     (1-p1_prob_a) * (1-p2_prob_a) * p2_br)
                        
                        st.write(f"Expected payoff for Player 1: {expected_p1:.3f}")
                        st.write(f"Expected payoff for Player 2: {expected_p2:.3f}")
                    else:
                        st.info("Mixed strategy equilibrium exists but involves probabilities outside [0,1].")
        except:
            st.info("Unable to calculate mixed strategy equilibrium for this game.")
    
    # Best response analysis
    st.write("### Best Response Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1's Best Responses:**")
        if payoff_p1[0, 0] > payoff_p1[1, 0]:
            st.write("vs Player 2's Strategy A: Strategy A")
        elif payoff_p1[0, 0] < payoff_p1[1, 0]:
            st.write("vs Player 2's Strategy A: Strategy B")
        else:
            st.write("vs Player 2's Strategy A: Indifferent")
            
        if payoff_p1[0, 1] > payoff_p1[1, 1]:
            st.write("vs Player 2's Strategy B: Strategy A")
        elif payoff_p1[0, 1] < payoff_p1[1, 1]:
            st.write("vs Player 2's Strategy B: Strategy B")
        else:
            st.write("vs Player 2's Strategy B: Indifferent")
    
    with col2:
        st.write("**Player 2's Best Responses:**")
        if payoff_p2[0, 0] > payoff_p2[0, 1]:
            st.write("vs Player 1's Strategy A: Strategy A")
        elif payoff_p2[0, 0] < payoff_p2[0, 1]:
            st.write("vs Player 1's Strategy A: Strategy B")
        else:
            st.write("vs Player 1's Strategy A: Indifferent")
            
        if payoff_p2[1, 0] > payoff_p2[1, 1]:
            st.write("vs Player 1's Strategy B: Strategy A")
        elif payoff_p2[1, 0] < payoff_p2[1, 1]:
            st.write("vs Player 1's Strategy B: Strategy B")
        else:
            st.write("vs Player 1's Strategy B: Indifferent")


st.set_page_config(page_title="Nash Equilibrium", page_icon="🎯")
st.markdown("# Nash Equilibrium Calculator 🎯")
st.sidebar.header("Nash Equilibrium")
st.write("""
Find Nash equilibria in 2x2 games. A Nash equilibrium occurs when each player's 
strategy is a best response to the other player's strategy.
""")

nash_equilibrium_finder()

show_code(nash_equilibrium_finder)