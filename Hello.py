import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import show_code


def run():
    st.set_page_config(
        page_title="Game Theory Examples",
        page_icon="🎯",
    )

    st.write("# Game Theory Examples 🎯")

    st.sidebar.success("Select a game theory demo above.")

    st.markdown(
        """
        This application demonstrates fundamental concepts in **Game Theory** through interactive examples.
        **👈 Select a demo from the sidebar** to explore different game theory concepts!
        
        ### Available Demos:
        - **Prisoner's Dilemma** - Classic two-player game demonstrating strategic interaction
        - **Nash Equilibrium** - Find equilibrium points in 2x2 games
        - **Mixed Strategy** - Calculate optimal mixed strategies
        - **Evolutionary Games** - Simulate population dynamics
        
        ### What is Game Theory?
        Game theory is the mathematical study of strategic decision making among rational agents. 
        It has applications in economics, political science, biology, and computer science.
        
        ### Key Concepts:
        - **Nash Equilibrium**: A solution concept where no player can benefit by unilaterally changing their strategy
        - **Dominant Strategy**: A strategy that yields the best outcome regardless of what opponents do
        - **Zero-Sum Games**: Games where one player's gain equals another's loss
        - **Mixed Strategies**: Randomizing over pure strategies with certain probabilities
    """
    )
    
    # Simple payoff matrix visualization as a teaser
    st.subheader("Example: Simple 2x2 Game Payoff Matrix")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Player 1 Payoffs**")
        payoff_p1 = pd.DataFrame(
            [[3, 0], [5, 1]], 
            columns=["Cooperate", "Defect"], 
            index=["Cooperate", "Defect"]
        )
        st.dataframe(payoff_p1)
    
    with col2:
        st.write("**Player 2 Payoffs**")
        payoff_p2 = pd.DataFrame(
            [[3, 5], [0, 1]], 
            columns=["Cooperate", "Defect"], 
            index=["Cooperate", "Defect"]
        )
        st.dataframe(payoff_p2)
    
    st.write("In this example, (Defect, Defect) is the Nash equilibrium, even though (Cooperate, Cooperate) gives higher payoffs for both players!")
    
    st.markdown("---")
    st.write("Use the sidebar to explore interactive game theory demos and learn more about strategic decision making.")


if __name__ == "__main__":
    run()
