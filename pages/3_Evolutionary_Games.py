import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import show_code


def evolutionary_game_simulation():
    st.subheader("Evolutionary Game Theory Simulation")
    
    st.write("""
    Simulate population dynamics in evolutionary games. Watch how strategy frequencies 
    evolve over time based on relative fitness (payoffs).
    """)
    
    # Game selection
    st.write("### Select Game Type")
    
    game_type = st.selectbox(
        "Choose a game:",
        ["Hawk-Dove Game", "Prisoner's Dilemma", "Custom Game"]
    )
    
    if game_type == "Hawk-Dove Game":
        # Classic hawk-dove parameters
        V = st.slider("Value of resource (V)", 1, 20, 10)
        C = st.slider("Cost of fighting (C)", 1, 30, 15)
        
        # Payoff matrix: [Hawk vs Hawk, Hawk vs Dove, Dove vs Hawk, Dove vs Dove]
        hawk_vs_hawk = (V - C) / 2
        hawk_vs_dove = V
        dove_vs_hawk = 0
        dove_vs_dove = V / 2
        
        payoff_matrix = np.array([[hawk_vs_hawk, hawk_vs_dove], 
                                 [dove_vs_hawk, dove_vs_dove]])
        
        st.write(f"**Payoff Matrix (V={V}, C={C}):**")
        
    elif game_type == "Prisoner's Dilemma":
        T = st.slider("Temptation payoff", 1, 10, 5)  # Defect vs Cooperate
        R = st.slider("Reward payoff", 1, 10, 3)      # Cooperate vs Cooperate
        P = st.slider("Punishment payoff", 0, 5, 1)   # Defect vs Defect
        S = st.slider("Sucker payoff", 0, 5, 0)       # Cooperate vs Defect
        
        payoff_matrix = np.array([[R, S], [T, P]])
        
        st.write(f"**Payoff Matrix (T={T}, R={R}, P={P}, S={S}):**")
        
    else:  # Custom Game
        col1, col2 = st.columns(2)
        
        with col1:
            a11 = st.number_input("Strategy A vs A", value=1.0)
            a12 = st.number_input("Strategy A vs B", value=0.0)
        
        with col2:
            a21 = st.number_input("Strategy B vs A", value=2.0)
            a22 = st.number_input("Strategy B vs B", value=1.0)
        
        payoff_matrix = np.array([[a11, a12], [a21, a22]])
        
        st.write("**Custom Payoff Matrix:**")
    
    # Display payoff matrix
    payoff_df = pd.DataFrame(
        payoff_matrix,
        columns=["vs Strategy A", "vs Strategy B"],
        index=["Strategy A", "Strategy B"]
    )
    st.dataframe(payoff_df)
    
    # Simulation parameters
    st.write("### Simulation Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        initial_freq_a = st.slider("Initial frequency of Strategy A", 0.0, 1.0, 0.5, 0.01)
    
    with col2:
        num_generations = st.slider("Number of generations", 10, 500, 100)
    
    with col3:
        selection_strength = st.slider("Selection strength", 0.1, 2.0, 1.0, 0.1)
    
    # Run simulation
    if st.button("Run Simulation"):
        
        # Initialize
        freq_a = np.zeros(num_generations + 1)
        freq_a[0] = initial_freq_a
        
        avg_fitness_a = np.zeros(num_generations)
        avg_fitness_b = np.zeros(num_generations)
        avg_fitness_pop = np.zeros(num_generations)
        
        # Replicator dynamics simulation
        for t in range(num_generations):
            p = freq_a[t]  # Frequency of strategy A
            q = 1 - p      # Frequency of strategy B
            
            # Calculate fitness (expected payoffs)
            fitness_a = p * payoff_matrix[0, 0] + q * payoff_matrix[0, 1]
            fitness_b = p * payoff_matrix[1, 0] + q * payoff_matrix[1, 1]
            avg_fitness = p * fitness_a + q * fitness_b
            
            # Store fitness values
            avg_fitness_a[t] = fitness_a
            avg_fitness_b[t] = fitness_b
            avg_fitness_pop[t] = avg_fitness
            
            # Replicator equation: dp/dt = p * (fitness_a - avg_fitness) * selection_strength
            if avg_fitness != 0:
                delta_p = p * (fitness_a - avg_fitness) * selection_strength * 0.01
                freq_a[t + 1] = max(0, min(1, p + delta_p))
            else:
                freq_a[t + 1] = p
        
        # Results
        st.write("### Simulation Results")
        
        # Final frequencies
        final_freq_a = freq_a[-1]
        final_freq_b = 1 - final_freq_a
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Final frequency of Strategy A", f"{final_freq_a:.3f}")
        
        with col2:
            st.metric("Final frequency of Strategy B", f"{final_freq_b:.3f}")
        
        # Plot evolution
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Frequency evolution
        generations = np.arange(num_generations + 1)
        ax1.plot(generations, freq_a, 'b-', linewidth=2, label='Strategy A')
        ax1.plot(generations, 1 - freq_a, 'r-', linewidth=2, label='Strategy B')
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Evolution of Strategy Frequencies')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, 1)
        
        # Fitness evolution
        generations_fitness = np.arange(num_generations)
        ax2.plot(generations_fitness, avg_fitness_a, 'b--', label='Fitness A')
        ax2.plot(generations_fitness, avg_fitness_b, 'r--', label='Fitness B')
        ax2.plot(generations_fitness, avg_fitness_pop, 'g-', linewidth=2, label='Population Average')
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Fitness')
        ax2.set_title('Evolution of Fitness')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Equilibrium analysis
        st.write("### Equilibrium Analysis")
        
        # Calculate evolutionary stable strategy (ESS)
        try:
            # For a mixed ESS, we need: fitness_a = fitness_b when both are present
            # p * a11 + (1-p) * a12 = p * a21 + (1-p) * a22
            # Solving for p:
            denominator = (payoff_matrix[0,0] - payoff_matrix[0,1]) - (payoff_matrix[1,0] - payoff_matrix[1,1])
            
            if abs(denominator) > 1e-10:
                ess_freq = (payoff_matrix[1,1] - payoff_matrix[0,1]) / denominator
                
                if 0 < ess_freq < 1:
                    st.success(f"Mixed Evolutionary Stable Strategy found!")
                    st.write(f"ESS frequency of Strategy A: {ess_freq:.3f}")
                    st.write(f"ESS frequency of Strategy B: {1-ess_freq:.3f}")
                    
                    # Check if simulation converged to ESS
                    if abs(final_freq_a - ess_freq) < 0.05:
                        st.success("✅ Simulation converged to the ESS!")
                    else:
                        st.warning("⚠️ Simulation did not converge to the theoretical ESS.")
                
                elif ess_freq <= 0:
                    st.info("Strategy B is evolutionarily stable (dominates)")
                    if final_freq_a < 0.05:
                        st.success("✅ Simulation converged: Strategy A eliminated")
                
                elif ess_freq >= 1:
                    st.info("Strategy A is evolutionarily stable (dominates)")
                    if final_freq_a > 0.95:
                        st.success("✅ Simulation converged: Strategy B eliminated")
            
            else:
                st.info("Neutral evolution - fitness difference is constant")
        
        except:
            st.warning("Could not determine theoretical ESS")
        
        # Phase portrait (simplified)
        st.write("### Direction Field")
        
        p_values = np.linspace(0, 1, 21)
        dp_dt_values = []
        
        for p in p_values:
            q = 1 - p
            fitness_a = p * payoff_matrix[0, 0] + q * payoff_matrix[0, 1]
            fitness_b = p * payoff_matrix[1, 0] + q * payoff_matrix[1, 1]
            avg_fitness = p * fitness_a + q * fitness_b
            
            if p > 0 and p < 1:
                dp_dt = p * (fitness_a - avg_fitness) * selection_strength
            else:
                dp_dt = 0
            
            dp_dt_values.append(dp_dt)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(p_values, dp_dt_values, 'b-', linewidth=2)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax.set_xlabel('Frequency of Strategy A')
        ax.set_ylabel('Change in frequency (dp/dt)')
        ax.set_title('Evolutionary Dynamics - Direction Field')
        ax.grid(True, alpha=0.3)
        
        # Mark equilibria
        zero_crossings = []
        for i in range(len(dp_dt_values)-1):
            if dp_dt_values[i] * dp_dt_values[i+1] < 0:
                zero_crossings.append(p_values[i])
        
        for crossing in zero_crossings:
            ax.axvline(x=crossing, color='r', linestyle=':', alpha=0.7, label=f'Equilibrium at p={crossing:.2f}')
        
        if zero_crossings:
            ax.legend()
        
        st.pyplot(fig)


st.set_page_config(page_title="Evolutionary Games", page_icon="🧬")
st.markdown("# Evolutionary Game Theory 🧬")
st.sidebar.header("Evolutionary Games")
st.write("""
Simulate how strategies evolve in populations over time. In evolutionary game theory,
strategies that perform better (have higher fitness) become more common in the population.
""")

evolutionary_game_simulation()

show_code(evolutionary_game_simulation)