import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import show_code


def mixed_strategy_calculator():
    st.subheader("Mixed Strategy Calculator")
    
    st.write("""
    Calculate optimal mixed strategies for 2x2 games. A mixed strategy involves 
    randomizing over pure strategies with specific probabilities.
    """)
    
    # Game setup
    st.write("### Game Setup")
    
    # Quick game templates
    game_template = st.selectbox(
        "Choose a template or customize:",
        ["Custom", "Matching Pennies", "Battle of the Sexes", "Chicken Game", "Rock Paper Scissors (2x2)"]
    )
    
    if game_template == "Matching Pennies":
        p1_matrix = np.array([[1, -1], [-1, 1]])
        p2_matrix = np.array([[-1, 1], [1, -1]])
    elif game_template == "Battle of the Sexes":
        p1_matrix = np.array([[2, 0], [0, 1]])
        p2_matrix = np.array([[1, 0], [0, 2]])
    elif game_template == "Chicken Game":
        p1_matrix = np.array([[0, -1], [1, -10]])
        p2_matrix = np.array([[0, 1], [-1, -10]])
    elif game_template == "Rock Paper Scissors (2x2)":
        p1_matrix = np.array([[0, -1], [1, 0]])
        p2_matrix = np.array([[0, 1], [-1, 0]])
    else:  # Custom
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Player 1 Payoffs**")
            p1_11 = st.number_input("(Strategy A, Strategy A)", value=1.0, key="p1_11")
            p1_12 = st.number_input("(Strategy A, Strategy B)", value=-1.0, key="p1_12")
            p1_21 = st.number_input("(Strategy B, Strategy A)", value=-1.0, key="p1_21")
            p1_22 = st.number_input("(Strategy B, Strategy B)", value=1.0, key="p1_22")
            p1_matrix = np.array([[p1_11, p1_12], [p1_21, p1_22]])
        
        with col2:
            st.write("**Player 2 Payoffs**")
            p2_11 = st.number_input("(Strategy A, Strategy A)", value=-1.0, key="p2_11")
            p2_12 = st.number_input("(Strategy A, Strategy B)", value=1.0, key="p2_12")
            p2_21 = st.number_input("(Strategy B, Strategy A)", value=1.0, key="p2_21")
            p2_22 = st.number_input("(Strategy B, Strategy B)", value=-1.0, key="p2_22")
            p2_matrix = np.array([[p2_11, p2_12], [p2_21, p2_22]])
    
    # Display current game
    st.write("### Current Game Matrix")
    game_display = pd.DataFrame(
        [
            [f"({p1_matrix[0,0]:.1f}, {p2_matrix[0,0]:.1f})", f"({p1_matrix[0,1]:.1f}, {p2_matrix[0,1]:.1f})"],
            [f"({p1_matrix[1,0]:.1f}, {p2_matrix[1,0]:.1f})", f"({p1_matrix[1,1]:.1f}, {p2_matrix[1,1]:.1f})"]
        ],
        columns=["Player 2: Strategy A", "Player 2: Strategy B"],
        index=["Player 1: Strategy A", "Player 1: Strategy B"]
    )
    st.dataframe(game_display)
    
    # Calculate mixed strategy equilibrium
    st.write("### Mixed Strategy Equilibrium")
    
    try:
        # For Player 1 to mix, Player 2 must be indifferent between their strategies
        # Expected payoff from Strategy A = Expected payoff from Strategy B
        # p2_11 * p + p2_21 * (1-p) = p2_12 * p + p2_22 * (1-p)
        
        denominator_p1 = (p2_matrix[0,0] - p2_matrix[1,0]) - (p2_matrix[0,1] - p2_matrix[1,1])
        if abs(denominator_p1) > 1e-10:
            p1_prob_a = (p2_matrix[1,1] - p2_matrix[1,0]) / denominator_p1
        else:
            p1_prob_a = None
        
        # For Player 2 to mix, Player 1 must be indifferent between their strategies
        denominator_p2 = (p1_matrix[0,0] - p1_matrix[0,1]) - (p1_matrix[1,0] - p1_matrix[1,1])
        if abs(denominator_p2) > 1e-10:
            p2_prob_a = (p1_matrix[1,1] - p1_matrix[0,1]) / denominator_p2
        else:
            p2_prob_a = None
        
        # Check if we have a valid mixed strategy equilibrium
        if (p1_prob_a is not None and p2_prob_a is not None and 
            0 <= p1_prob_a <= 1 and 0 <= p2_prob_a <= 1):
            
            st.success("Mixed Strategy Nash Equilibrium found!")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Player 1's Optimal Strategy:**")
                st.write(f"Play Strategy A with probability: {p1_prob_a:.3f}")
                st.write(f"Play Strategy B with probability: {1-p1_prob_a:.3f}")
            
            with col2:
                st.write("**Player 2's Optimal Strategy:**")
                st.write(f"Play Strategy A with probability: {p2_prob_a:.3f}")
                st.write(f"Play Strategy B with probability: {1-p2_prob_a:.3f}")
            
            # Calculate expected payoffs
            expected_p1 = (p1_prob_a * p2_prob_a * p1_matrix[0,0] + 
                          p1_prob_a * (1-p2_prob_a) * p1_matrix[0,1] + 
                          (1-p1_prob_a) * p2_prob_a * p1_matrix[1,0] + 
                          (1-p1_prob_a) * (1-p2_prob_a) * p1_matrix[1,1])
            
            expected_p2 = (p1_prob_a * p2_prob_a * p2_matrix[0,0] + 
                          p1_prob_a * (1-p2_prob_a) * p2_matrix[0,1] + 
                          (1-p1_prob_a) * p2_prob_a * p2_matrix[1,0] + 
                          (1-p1_prob_a) * (1-p2_prob_a) * p2_matrix[1,1])
            
            st.write("### Expected Payoffs")
            st.write(f"Player 1 expected payoff: {expected_p1:.3f}")
            st.write(f"Player 2 expected payoff: {expected_p2:.3f}")
            
            # Visualization
            st.write("### Strategy Visualization")
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Player 1 strategy
            strategies = ['Strategy A', 'Strategy B']
            probabilities_p1 = [p1_prob_a, 1-p1_prob_a]
            ax1.pie(probabilities_p1, labels=strategies, autopct='%.2f%%', startangle=90)
            ax1.set_title("Player 1's Mixed Strategy")
            
            # Player 2 strategy
            probabilities_p2 = [p2_prob_a, 1-p2_prob_a]
            ax2.pie(probabilities_p2, labels=strategies, autopct='%.2f%%', startangle=90)
            ax2.set_title("Player 2's Mixed Strategy")
            
            st.pyplot(fig)
            
        else:
            st.warning("No valid mixed strategy equilibrium found in the interior.")
            st.write("This game likely has pure strategy Nash equilibria or the equilibrium involves corner solutions.")
            
    except Exception as e:
        st.error(f"Error calculating mixed strategy equilibrium: {str(e)}")
    
    # Interactive strategy analyzer
    st.write("### Interactive Strategy Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        p1_strategy_prob = st.slider("Player 1: Probability of Strategy A", 0.0, 1.0, 0.5, 0.01)
    
    with col2:
        p2_strategy_prob = st.slider("Player 2: Probability of Strategy A", 0.0, 1.0, 0.5, 0.01)
    
    # Calculate expected payoffs for these probabilities
    expected_p1_interactive = (p1_strategy_prob * p2_strategy_prob * p1_matrix[0,0] + 
                              p1_strategy_prob * (1-p2_strategy_prob) * p1_matrix[0,1] + 
                              (1-p1_strategy_prob) * p2_strategy_prob * p1_matrix[1,0] + 
                              (1-p1_strategy_prob) * (1-p2_strategy_prob) * p1_matrix[1,1])
    
    expected_p2_interactive = (p1_strategy_prob * p2_strategy_prob * p2_matrix[0,0] + 
                              p1_strategy_prob * (1-p2_strategy_prob) * p2_matrix[0,1] + 
                              (1-p1_strategy_prob) * p2_strategy_prob * p2_matrix[1,0] + 
                              (1-p1_strategy_prob) * (1-p2_strategy_prob) * p2_matrix[1,1])
    
    st.write("**Expected Payoffs with Current Probabilities:**")
    st.write(f"Player 1: {expected_p1_interactive:.3f}")
    st.write(f"Player 2: {expected_p2_interactive:.3f}")
    
    # Best response given opponent's strategy
    st.write("### Best Response Analysis")
    
    # Player 1's best response to Player 2's mixed strategy
    p1_payoff_a = p2_strategy_prob * p1_matrix[0,0] + (1-p2_strategy_prob) * p1_matrix[0,1]
    p1_payoff_b = p2_strategy_prob * p1_matrix[1,0] + (1-p2_strategy_prob) * p1_matrix[1,1]
    
    # Player 2's best response to Player 1's mixed strategy
    p2_payoff_a = p1_strategy_prob * p2_matrix[0,0] + (1-p1_strategy_prob) * p2_matrix[1,0]
    p2_payoff_b = p1_strategy_prob * p2_matrix[0,1] + (1-p1_strategy_prob) * p2_matrix[1,1]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1's Best Response:**")
        if p1_payoff_a > p1_payoff_b:
            st.write("Strategy A is better")
            st.write(f"Expected payoff: {p1_payoff_a:.3f}")
        elif p1_payoff_b > p1_payoff_a:
            st.write("Strategy B is better")
            st.write(f"Expected payoff: {p1_payoff_b:.3f}")
        else:
            st.write("Indifferent between strategies")
            st.write(f"Expected payoff: {p1_payoff_a:.3f}")
    
    with col2:
        st.write("**Player 2's Best Response:**")
        if p2_payoff_a > p2_payoff_b:
            st.write("Strategy A is better")
            st.write(f"Expected payoff: {p2_payoff_a:.3f}")
        elif p2_payoff_b > p2_payoff_a:
            st.write("Strategy B is better")
            st.write(f"Expected payoff: {p2_payoff_b:.3f}")
        else:
            st.write("Indifferent between strategies")
            st.write(f"Expected payoff: {p2_payoff_a:.3f}")


st.set_page_config(page_title="Mixed Strategy", page_icon="🎲")
st.markdown("# Mixed Strategy Calculator 🎲")
st.sidebar.header("Mixed Strategy")
st.write("""
Calculate optimal mixed strategies for 2x2 games. Mixed strategies involve 
randomizing over pure strategies with specific probabilities.
""")

mixed_strategy_calculator()

show_code(mixed_strategy_calculator)