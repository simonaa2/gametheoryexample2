# Copyright (c) 2024 Game Theory Applications
# Prisoner's Dilemma Interactive Game

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def prisoners_dilemma_game():
    st.set_page_config(page_title="Prisoner's Dilemma", page_icon="⛓️")
    st.markdown("# Prisoner's Dilemma Game")
    st.sidebar.header("Prisoner's Dilemma")
    
    st.write("""
    The Prisoner's Dilemma is one of the most famous games in game theory. It demonstrates 
    why two rational individuals might not cooperate even when it would be in their best interest to do so.
    """)
    
    # Game explanation
    with st.expander("📚 About the Prisoner's Dilemma"):
        st.write("""
        **The Story:**
        Two prisoners are arrested and held in separate cells. They cannot communicate with each other. 
        Each prisoner has two options: Cooperate (remain silent) or Defect (betray the other).
        
        **The Dilemma:**
        - If both cooperate: Both get a light sentence
        - If both defect: Both get a heavy sentence  
        - If one defects and one cooperates: The defector goes free, the cooperator gets the worst sentence
        
        **Key Insight:**
        Even though mutual cooperation gives a better outcome than mutual defection, 
        the rational choice for each individual prisoner is to defect.
        """)
    
    # Payoff customization
    st.subheader("Customize Payoffs")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cc_payoff = st.number_input("Both Cooperate", value=3, min_value=0, max_value=10)
    with col2:
        cd_payoff = st.number_input("Cooperate vs Defect", value=0, min_value=0, max_value=10)
    with col3:
        dc_payoff = st.number_input("Defect vs Cooperate", value=5, min_value=0, max_value=10)
    with col4:
        dd_payoff = st.number_input("Both Defect", value=1, min_value=0, max_value=10)
    
    # Display payoff matrix
    st.subheader("Payoff Matrix")
    payoff_matrix = pd.DataFrame([
        [f"({cc_payoff}, {cc_payoff})", f"({cd_payoff}, {dc_payoff})"],
        [f"({dc_payoff}, {cd_payoff})", f"({dd_payoff}, {dd_payoff})"]
    ], 
    index=["Cooperate", "Defect"],
    columns=["Cooperate", "Defect"])
    payoff_matrix.index.name = "Player 1"
    payoff_matrix.columns.name = "Player 2"
    
    st.dataframe(payoff_matrix)
    
    # Interactive game
    st.subheader("Play the Game")
    
    # Initialize session state
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if 'total_score_p1' not in st.session_state:
        st.session_state.total_score_p1 = 0
    if 'total_score_p2' not in st.session_state:
        st.session_state.total_score_p2 = 0
    
    # Game mode selection
    game_mode = st.radio("Choose game mode:", 
                        ["Single Round", "Multiple Rounds", "Against Computer"])
    
    if game_mode == "Single Round":
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Player 1 Choice:**")
            p1_choice = st.radio("Player 1", ["Cooperate", "Defect"], key="p1_single")
        
        with col2:
            st.write("**Player 2 Choice:**")
            p2_choice = st.radio("Player 2", ["Cooperate", "Defect"], key="p2_single")
        
        if st.button("Play Round"):
            # Calculate payoffs
            if p1_choice == "Cooperate" and p2_choice == "Cooperate":
                p1_score, p2_score = cc_payoff, cc_payoff
            elif p1_choice == "Cooperate" and p2_choice == "Defect":
                p1_score, p2_score = cd_payoff, dc_payoff
            elif p1_choice == "Defect" and p2_choice == "Cooperate":
                p1_score, p2_score = dc_payoff, cd_payoff
            else:  # Both defect
                p1_score, p2_score = dd_payoff, dd_payoff
            
            st.success(f"**Result:** Player 1 gets {p1_score} points, Player 2 gets {p2_score} points")
            
            # Outcome analysis
            if p1_choice == "Cooperate" and p2_choice == "Cooperate":
                st.info("🤝 Both players cooperated! This is the socially optimal outcome.")
            elif p1_choice == "Defect" and p2_choice == "Defect":
                st.warning("💥 Both players defected! This is the Nash equilibrium but suboptimal.")
            else:
                st.error("😔 One player was betrayed! Trust was broken.")
    
    elif game_mode == "Multiple Rounds":
        rounds = st.slider("Number of rounds", 1, 20, 5)
        
        if st.button("Start Game"):
            st.session_state.game_history = []
            st.session_state.total_score_p1 = 0
            st.session_state.total_score_p2 = 0
        
        for round_num in range(1, rounds + 1):
            if len(st.session_state.game_history) < round_num:
                st.write(f"**Round {round_num}**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    p1_choice = st.selectbox(f"Player 1 Round {round_num}", 
                                           ["Cooperate", "Defect"], key=f"p1_r{round_num}")
                with col2:
                    p2_choice = st.selectbox(f"Player 2 Round {round_num}", 
                                           ["Cooperate", "Defect"], key=f"p2_r{round_num}")
                with col3:
                    if st.button(f"Play Round {round_num}", key=f"play_r{round_num}"):
                        # Calculate payoffs
                        if p1_choice == "Cooperate" and p2_choice == "Cooperate":
                            p1_score, p2_score = cc_payoff, cc_payoff
                        elif p1_choice == "Cooperate" and p2_choice == "Defect":
                            p1_score, p2_score = cd_payoff, dc_payoff
                        elif p1_choice == "Defect" and p2_choice == "Cooperate":
                            p1_score, p2_score = dc_payoff, cd_payoff
                        else:
                            p1_score, p2_score = dd_payoff, dd_payoff
                        
                        st.session_state.game_history.append({
                            'Round': round_num,
                            'Player 1': p1_choice,
                            'Player 2': p2_choice,
                            'P1 Score': p1_score,
                            'P2 Score': p2_score
                        })
                        
                        st.session_state.total_score_p1 += p1_score
                        st.session_state.total_score_p2 += p2_score
                        
                        st.rerun()
                break
        
        # Show results
        if st.session_state.game_history:
            st.subheader("Game Results")
            df = pd.DataFrame(st.session_state.game_history)
            st.dataframe(df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Player 1 Total Score", st.session_state.total_score_p1)
            with col2:
                st.metric("Player 2 Total Score", st.session_state.total_score_p2)
    
    elif game_mode == "Against Computer":
        st.write("Choose your strategy and play against different computer strategies:")
        
        computer_strategy = st.selectbox("Computer Strategy", [
            "Always Cooperate",
            "Always Defect", 
            "Tit-for-Tat",
            "Random"
        ])
        
        if 'computer_history' not in st.session_state:
            st.session_state.computer_history = []
            st.session_state.computer_last_choice = "Cooperate"
        
        your_choice = st.radio("Your choice:", ["Cooperate", "Defect"], key="human_choice")
        
        if st.button("Play Against Computer"):
            # Computer's choice based on strategy
            if computer_strategy == "Always Cooperate":
                computer_choice = "Cooperate"
            elif computer_strategy == "Always Defect":
                computer_choice = "Defect"
            elif computer_strategy == "Tit-for-Tat":
                if st.session_state.computer_history:
                    # Copy player's last move
                    computer_choice = st.session_state.computer_history[-1]['Your Choice']
                else:
                    computer_choice = "Cooperate"  # Start cooperating
            else:  # Random
                computer_choice = np.random.choice(["Cooperate", "Defect"])
            
            # Calculate scores
            if your_choice == "Cooperate" and computer_choice == "Cooperate":
                your_score, computer_score = cc_payoff, cc_payoff
            elif your_choice == "Cooperate" and computer_choice == "Defect":
                your_score, computer_score = cd_payoff, dc_payoff
            elif your_choice == "Defect" and computer_choice == "Cooperate":
                your_score, computer_score = dc_payoff, cd_payoff
            else:
                your_score, computer_score = dd_payoff, dd_payoff
            
            # Update history
            st.session_state.computer_history.append({
                'Round': len(st.session_state.computer_history) + 1,
                'Your Choice': your_choice,
                'Computer Choice': computer_choice,
                'Your Score': your_score,
                'Computer Score': computer_score
            })
            
            st.success(f"You: {your_choice}, Computer: {computer_choice}")
            st.info(f"Scores - You: {your_score}, Computer: {computer_score}")
            
            if st.session_state.computer_history:
                st.subheader("Game History")
                df = pd.DataFrame(st.session_state.computer_history)
                st.dataframe(df)
                
                total_your_score = df['Your Score'].sum()
                total_computer_score = df['Computer Score'].sum()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Your Total Score", total_your_score)
                with col2:
                    st.metric("Computer Total Score", total_computer_score)

if __name__ == "__main__":
    prisoners_dilemma_game()