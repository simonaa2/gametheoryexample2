#!/usr/bin/env Rscript

# Game Theory Demo Script
# Demonstrates the capabilities of the R Game Theory Analyzer

cat("==========================================\n")
cat("     GAME THEORY ANALYZER DEMO\n")
cat("     Built with R for Educational Use\n")
cat("==========================================\n\n")

# Source the main game theory functions
source("game_theory.R")

cat("This demo showcases the Game Theory Analyzer's capabilities:\n\n")

# Demo 1: Prisoner's Dilemma
cat("DEMO 1: Analyzing the classic Prisoner's Dilemma\n")
cat("=" , rep("=", 50), "\n")
prisoners_dilemma()

cat("\nPress Enter to continue to the next demo...")
if (interactive()) readline()

# Demo 2: Battle of the Sexes
cat("\n\nDEMO 2: Battle of the Sexes - Coordination Game\n")
cat("=" , rep("=", 50), "\n")
battle_of_sexes()

cat("\nPress Enter to continue to the next demo...")
if (interactive()) readline()

# Demo 3: Rock Paper Scissors
cat("\n\nDEMO 3: Rock-Paper-Scissors - Zero Sum Game\n")
cat("=" , rep("=", 50), "\n")
rock_paper_scissors()

cat("\nPress Enter to continue to the custom game demo...")
if (interactive()) readline()

# Demo 4: Custom Game Example - Matching Pennies
cat("\n\nDEMO 4: Custom Game - Matching Pennies\n")
cat("=" , rep("=", 50), "\n")
cat("Creating a Matching Pennies game where:\n")
cat("- Player 1 wins when both players match (both Heads or both Tails)\n")
cat("- Player 2 wins when players don't match\n")
cat("- This is a zero-sum game\n\n")

# Matching Pennies: P1 wins on match, P2 wins on mismatch
analyze_custom_game(1, -1, -1, 1, -1, 1, 1, -1)

cat("\nPress Enter to continue...")
if (interactive()) readline()

# Demo 5: Chicken Game
cat("\n\nDEMO 5: Custom Game - Chicken Game\n")
cat("=" , rep("=", 50), "\n")
cat("The Chicken Game models conflict situations:\n")
cat("- Both cooperate: (3,3) - mutual benefit\n")
cat("- One defects, one cooperates: (5,1) - winner takes all\n")
cat("- Both defect: (0,0) - mutual destruction\n\n")

analyze_custom_game(3, 1, 5, 0, 3, 5, 1, 0)

cat("\n\nDEMO COMPLETE!\n")
cat("=" , rep("=", 50), "\n")
cat("Key insights from these demonstrations:\n")
cat("1. Different games have different equilibrium structures\n")
cat("2. Some games have multiple equilibria (Battle of Sexes)\n")
cat("3. Mixed strategies emerge when no pure equilibrium exists\n")
cat("4. Dominant strategies lead to predictable outcomes (Prisoner's Dilemma)\n")
cat("5. Zero-sum games often require randomization (Rock-Paper-Scissors)\n\n")

cat("To explore further:\n")
cat("- Run 'Rscript game_theory.R' for interactive mode\n")
cat("- Open 'index.html' in your browser for the web interface\n")
cat("- Modify payoff matrices to create your own games\n\n")

cat("Thank you for exploring Game Theory with R! 🎯\n")