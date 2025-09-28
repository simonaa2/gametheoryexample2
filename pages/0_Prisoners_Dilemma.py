import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import show_code


def prisoners_dilemma():
    st.subheader("Interactive Prisoner's Dilemma")
    
    st.write("""
    The Prisoner's Dilemma is a classic game theory scenario where two prisoners 
    must decide whether to cooperate or defect without knowing the other's choice.
    """)
    
    # Allow users to customize payoffs
    st.write("### Customize Payoffs")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        cc_payoff = st.number_input("Both Cooperate", value=3, min_value=0, max_value=10)
    with col2:
        cd_payoff = st.number_input("Cooperate vs Defect", value=0, min_value=0, max_value=10)
    with col3:
        dc_payoff = st.number_input("Defect vs Cooperate", value=5, min_value=0, max_value=10)
    with col4:
        dd_payoff = st.number_input("Both Defect", value=1, min_value=0, max_value=10)
    
    # Create payoff matrices
    payoff_matrix_p1 = np.array([[cc_payoff, cd_payoff], [dc_payoff, dd_payoff]])
    payoff_matrix_p2 = np.array([[cc_payoff, dc_payoff], [cd_payoff, dd_payoff]])
    
    # Display payoff matrices
    st.write("### Payoff Matrices")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1 Payoffs**")
        df1 = pd.DataFrame(payoff_matrix_p1, 
                          columns=["Player 2: Cooperate", "Player 2: Defect"],
                          index=["Player 1: Cooperate", "Player 1: Defect"])
        st.dataframe(df1)
    
    with col2:
        st.write("**Player 2 Payoffs**")
        df2 = pd.DataFrame(payoff_matrix_p2, 
                          columns=["Player 2: Cooperate", "Player 2: Defect"],
                          index=["Player 1: Cooperate", "Player 1: Defect"])
        st.dataframe(df2)
    
    # Nash equilibrium analysis
    st.write("### Nash Equilibrium Analysis")
    
    # Check for Nash equilibria
    nash_equilibria = []
    strategies = [("Cooperate", "Cooperate"), ("Cooperate", "Defect"), 
                 ("Defect", "Cooperate"), ("Defect", "Defect")]
    
    for i, (s1, s2) in enumerate(strategies):
        row, col = i // 2, i % 2
        
        # Check if this is a Nash equilibrium
        is_nash = True
        
        # Check Player 1's best response
        current_payoff_p1 = payoff_matrix_p1[row, col]
        alternative_payoff_p1 = payoff_matrix_p1[1-row, col]
        if alternative_payoff_p1 > current_payoff_p1:
            is_nash = False
        
        # Check Player 2's best response
        current_payoff_p2 = payoff_matrix_p2[row, col]
        alternative_payoff_p2 = payoff_matrix_p2[row, 1-col]
        if alternative_payoff_p2 > current_payoff_p2:
            is_nash = False
        
        if is_nash:
            nash_equilibria.append((s1, s2))
    
    if nash_equilibria:
        st.write("**Nash Equilibria found:**")
        for eq in nash_equilibria:
            st.write(f"- {eq[0]} vs {eq[1]}")
    else:
        st.write("No pure strategy Nash equilibria found.")
    
    # Interactive game simulation
    st.write("### Play the Game")
    
    if st.button("Play Round"):
        player1_choice = st.radio("Player 1 Choice:", ["Cooperate", "Defect"], key="p1")
        player2_choice = st.radio("Player 2 Choice:", ["Cooperate", "Defect"], key="p2")
        
        # Calculate outcomes
        p1_idx = 0 if player1_choice == "Cooperate" else 1
        p2_idx = 0 if player2_choice == "Cooperate" else 1
        
        p1_payoff = payoff_matrix_p1[p1_idx, p2_idx]
        p2_payoff = payoff_matrix_p2[p1_idx, p2_idx]
        
        st.write(f"**Result:**")
        st.write(f"Player 1 ({player1_choice}): {p1_payoff} points")
        st.write(f"Player 2 ({player2_choice}): {p2_payoff} points")
        
        # Analyze the outcome
        if player1_choice == "Cooperate" and player2_choice == "Cooperate":
            st.success("Both players cooperated! Mutual benefit achieved.")
        elif player1_choice == "Defect" and player2_choice == "Defect":
            st.warning("Both players defected. This is often the Nash equilibrium.")
        else:
            st.info("One player cooperated, one defected. Asymmetric outcome.")


st.set_page_config(page_title="Prisoner's Dilemma", page_icon="⚖️")
st.markdown("# Prisoner's Dilemma ⚖️")
st.sidebar.header("Prisoner's Dilemma")
st.write("""
The Prisoner's Dilemma demonstrates how rational individuals might not cooperate, 
even when it would be in their mutual interest to do so.
""")

prisoners_dilemma()

show_code(prisoners_dilemma)