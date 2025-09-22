# Game Theory Application in R
# Author: AI Assistant
# Description: Interactive game theory application with multiple game types

# Load required libraries (fall back to base R if packages not available)
tryCatch({
  library(shiny)
  SHINY_AVAILABLE <- TRUE
}, error = function(e) {
  SHINY_AVAILABLE <- FALSE
  cat("Shiny package not available. Using base R interface.\n")
})

# =============================================================================
# CORE GAME THEORY FUNCTIONS
# =============================================================================

# Function to create a payoff matrix for 2x2 games
create_payoff_matrix <- function(a11, a12, a21, a22, b11, b12, b21, b22) {
  # Create payoff matrix for a 2x2 game
  # a_ij represents Player 1's payoff when Player 1 plays strategy i and Player 2 plays strategy j
  # b_ij represents Player 2's payoff when Player 1 plays strategy i and Player 2 plays strategy j
  
  payoff_matrix <- list(
    player1 = matrix(c(a11, a12, a21, a22), nrow = 2, ncol = 2, byrow = TRUE,
                     dimnames = list(c("Strategy 1", "Strategy 2"), 
                                   c("Strategy 1", "Strategy 2"))),
    player2 = matrix(c(b11, b12, b21, b22), nrow = 2, ncol = 2, byrow = TRUE,
                     dimnames = list(c("Strategy 1", "Strategy 2"), 
                                   c("Strategy 1", "Strategy 2")))
  )
  return(payoff_matrix)
}

# Function to find Nash Equilibria in pure strategies
find_nash_equilibria <- function(payoff_matrix) {
  p1_matrix <- payoff_matrix$player1
  p2_matrix <- payoff_matrix$player2
  
  equilibria <- list()
  
  # Check each cell for Nash equilibrium
  for (i in 1:2) {
    for (j in 1:2) {
      # Check if this is a Nash equilibrium
      # Player 1 should not want to deviate given Player 2's strategy
      player1_best <- which.max(p1_matrix[, j])
      # Player 2 should not want to deviate given Player 1's strategy  
      player2_best <- which.max(p2_matrix[i, ])
      
      if (i == player1_best && j == player2_best) {
        equilibria[[length(equilibria) + 1]] <- list(
          player1_strategy = i,
          player2_strategy = j,
          player1_payoff = p1_matrix[i, j],
          player2_payoff = p2_matrix[i, j]
        )
      }
    }
  }
  
  return(equilibria)
}

# Function to calculate mixed strategy Nash equilibrium for 2x2 games
find_mixed_nash <- function(payoff_matrix) {
  p1_matrix <- payoff_matrix$player1
  p2_matrix <- payoff_matrix$player2
  
  # For mixed strategy equilibrium, each player must be indifferent between strategies
  # Player 1's indifference condition: p * p1_matrix[1,1] + (1-p) * p1_matrix[1,2] = p * p1_matrix[2,1] + (1-p) * p1_matrix[2,2]
  # Solving for p (Player 2's probability of playing strategy 1)
  
  denom_p2 <- (p1_matrix[1,1] - p1_matrix[1,2] - p1_matrix[2,1] + p1_matrix[2,2])
  if (abs(denom_p2) < 1e-10) {
    p2_prob1 <- NA  # No mixed strategy equilibrium
  } else {
    p2_prob1 <- (p1_matrix[2,2] - p1_matrix[1,2]) / denom_p2
  }
  
  # Player 2's indifference condition
  denom_p1 <- (p2_matrix[1,1] - p2_matrix[2,1] - p2_matrix[1,2] + p2_matrix[2,2])
  if (abs(denom_p1) < 1e-10) {
    p1_prob1 <- NA  # No mixed strategy equilibrium
  } else {
    p1_prob1 <- (p2_matrix[2,2] - p2_matrix[2,1]) / denom_p1
  }
  
  # Check if probabilities are valid (between 0 and 1)
  if (!is.na(p1_prob1) && !is.na(p2_prob1) && 
      p1_prob1 >= 0 && p1_prob1 <= 1 && 
      p2_prob1 >= 0 && p2_prob1 <= 1) {
    
    # Calculate expected payoffs
    p1_expected <- p1_prob1 * p2_prob1 * p1_matrix[1,1] + 
                   p1_prob1 * (1-p2_prob1) * p1_matrix[1,2] +
                   (1-p1_prob1) * p2_prob1 * p1_matrix[2,1] +
                   (1-p1_prob1) * (1-p2_prob1) * p1_matrix[2,2]
    
    p2_expected <- p1_prob1 * p2_prob1 * p2_matrix[1,1] + 
                   p1_prob1 * (1-p2_prob1) * p2_matrix[1,2] +
                   (1-p1_prob1) * p2_prob1 * p2_matrix[2,1] +
                   (1-p1_prob1) * (1-p2_prob1) * p2_matrix[2,2]
    
    return(list(
      player1_prob_strategy1 = p1_prob1,
      player2_prob_strategy1 = p2_prob1,
      player1_expected_payoff = p1_expected,
      player2_expected_payoff = p2_expected
    ))
  } else {
    return(NULL)
  }
}

# =============================================================================
# SPECIFIC GAME IMPLEMENTATIONS
# =============================================================================

# Prisoner's Dilemma
prisoners_dilemma <- function() {
  # Classic Prisoner's Dilemma payoff matrix
  # (Cooperate, Cooperate): (3,3)
  # (Cooperate, Defect): (0,5)  
  # (Defect, Cooperate): (5,0)
  # (Defect, Defect): (1,1)
  
  # Create payoff matrix correctly for Prisoner's Dilemma:
  # Row = Player 1's strategy, Col = Player 2's strategy
  # (Cooperate, Cooperate): (3,3), (Cooperate, Defect): (0,5)
  # (Defect, Cooperate): (5,0), (Defect, Defect): (1,1)
  payoff <- create_payoff_matrix(3, 0, 5, 1, 3, 5, 0, 1)
  
  cat("=== PRISONER'S DILEMMA ===\n")
  cat("Strategy 1: Cooperate, Strategy 2: Defect\n\n")
  
  cat("Player 1 Payoff Matrix:\n")
  print(payoff$player1)
  cat("\nPlayer 2 Payoff Matrix:\n")
  print(payoff$player2)
  
  equilibria <- find_nash_equilibria(payoff)
  cat("\nPure Strategy Nash Equilibria:\n")
  if (length(equilibria) > 0) {
    for (i in 1:length(equilibria)) {
      eq <- equilibria[[i]]
      strat1 <- ifelse(eq$player1_strategy == 1, "Cooperate", "Defect")
      strat2 <- ifelse(eq$player2_strategy == 1, "Cooperate", "Defect")
      cat(sprintf("Equilibrium %d: Player 1 plays %s, Player 2 plays %s\n", 
                  i, strat1, strat2))
      cat(sprintf("Payoffs: Player 1 = %d, Player 2 = %d\n\n", 
                  eq$player1_payoff, eq$player2_payoff))
    }
  } else {
    cat("No pure strategy Nash equilibria found.\n\n")
  }
  
  mixed_eq <- find_mixed_nash(payoff)
  if (!is.null(mixed_eq)) {
    cat("Mixed Strategy Nash Equilibrium:\n")
    cat(sprintf("Player 1 cooperates with probability %.3f\n", mixed_eq$player1_prob_strategy1))
    cat(sprintf("Player 2 cooperates with probability %.3f\n", mixed_eq$player2_prob_strategy1))
    cat(sprintf("Expected payoffs: Player 1 = %.3f, Player 2 = %.3f\n\n", 
                mixed_eq$player1_expected_payoff, mixed_eq$player2_expected_payoff))
  }
  
  return(payoff)
}

# Rock-Paper-Scissors
rock_paper_scissors <- function() {
  # Rock-Paper-Scissors as a zero-sum game
  # Win = 1, Lose = -1, Tie = 0
  
  cat("=== ROCK-PAPER-SCISSORS ===\n")
  cat("Strategy 1: Rock, Strategy 2: Paper, Strategy 3: Scissors\n\n")
  
  # Create 3x3 payoff matrices for Rock-Paper-Scissors
  p1_matrix <- matrix(c(0, -1, 1, 1, 0, -1, -1, 1, 0), nrow = 3, ncol = 3,
                      dimnames = list(c("Rock", "Paper", "Scissors"), 
                                    c("Rock", "Paper", "Scissors")))
  p2_matrix <- -p1_matrix  # Zero-sum game
  
  cat("Player 1 Payoff Matrix:\n")
  print(p1_matrix)
  cat("\nPlayer 2 Payoff Matrix:\n")
  print(p2_matrix)
  
  cat("\nIn Rock-Paper-Scissors, the Nash equilibrium is for each player\n")
  cat("to play each strategy with probability 1/3.\n")
  cat("Expected payoff for both players: 0\n\n")
  
  return(list(player1 = p1_matrix, player2 = p2_matrix))
}

# Battle of the Sexes (Coordination Game)
battle_of_sexes <- function() {
  # Battle of the Sexes coordination game
  # Both prefer to coordinate, but have different preferences
  
  payoff <- create_payoff_matrix(2, 0, 0, 1, 1, 0, 0, 2)
  
  cat("=== BATTLE OF THE SEXES ===\n")
  cat("Strategy 1: Opera, Strategy 2: Football\n")
  cat("Both players prefer to be together, but have different preferences\n\n")
  
  cat("Player 1 Payoff Matrix (prefers Opera):\n")
  print(payoff$player1)
  cat("\nPlayer 2 Payoff Matrix (prefers Football):\n")
  print(payoff$player2)
  
  equilibria <- find_nash_equilibria(payoff)
  cat("\nPure Strategy Nash Equilibria:\n")
  if (length(equilibria) > 0) {
    for (i in 1:length(equilibria)) {
      eq <- equilibria[[i]]
      strat1 <- ifelse(eq$player1_strategy == 1, "Opera", "Football")
      strat2 <- ifelse(eq$player2_strategy == 1, "Opera", "Football")
      cat(sprintf("Equilibrium %d: Both go to %s\n", i, strat1))
      cat(sprintf("Payoffs: Player 1 = %d, Player 2 = %d\n\n", 
                  eq$player1_payoff, eq$player2_payoff))
    }
  }
  
  mixed_eq <- find_mixed_nash(payoff)
  if (!is.null(mixed_eq)) {
    cat("Mixed Strategy Nash Equilibrium:\n")
    cat(sprintf("Player 1 chooses Opera with probability %.3f\n", mixed_eq$player1_prob_strategy1))
    cat(sprintf("Player 2 chooses Opera with probability %.3f\n", mixed_eq$player2_prob_strategy1))
    cat(sprintf("Expected payoffs: Player 1 = %.3f, Player 2 = %.3f\n\n", 
                mixed_eq$player1_expected_payoff, mixed_eq$player2_expected_payoff))
  }
  
  return(payoff)
}

# =============================================================================
# INTERACTIVE GAME THEORY ANALYZER
# =============================================================================

# Function to analyze a custom 2x2 game
analyze_custom_game <- function(a11, a12, a21, a22, b11, b12, b21, b22) {
  payoff <- create_payoff_matrix(a11, a12, a21, a22, b11, b12, b21, b22)
  
  cat("=== CUSTOM GAME ANALYSIS ===\n\n")
  
  cat("Player 1 Payoff Matrix:\n")
  print(payoff$player1)
  cat("\nPlayer 2 Payoff Matrix:\n")
  print(payoff$player2)
  
  equilibria <- find_nash_equilibria(payoff)
  cat("\nPure Strategy Nash Equilibria:\n")
  if (length(equilibria) > 0) {
    for (i in 1:length(equilibria)) {
      eq <- equilibria[[i]]
      cat(sprintf("Equilibrium %d: Player 1 plays Strategy %d, Player 2 plays Strategy %d\n", 
                  i, eq$player1_strategy, eq$player2_strategy))
      cat(sprintf("Payoffs: Player 1 = %d, Player 2 = %d\n\n", 
                  eq$player1_payoff, eq$player2_payoff))
    }
  } else {
    cat("No pure strategy Nash equilibria found.\n\n")
  }
  
  mixed_eq <- find_mixed_nash(payoff)
  if (!is.null(mixed_eq)) {
    cat("Mixed Strategy Nash Equilibrium:\n")
    cat(sprintf("Player 1 plays Strategy 1 with probability %.3f\n", mixed_eq$player1_prob_strategy1))
    cat(sprintf("Player 2 plays Strategy 1 with probability %.3f\n", mixed_eq$player2_prob_strategy1))
    cat(sprintf("Expected payoffs: Player 1 = %.3f, Player 2 = %.3f\n\n", 
                mixed_eq$player1_expected_payoff, mixed_eq$player2_expected_payoff))
  } else {
    cat("No mixed strategy Nash equilibrium found.\n\n")
  }
  
  return(payoff)
}

# =============================================================================
# MAIN MENU SYSTEM
# =============================================================================

# Main menu function
main_menu <- function() {
  cat("=========================================\n")
  cat("     GAME THEORY ANALYZER IN R\n")
  cat("=========================================\n\n")
  
  cat("Choose a game to analyze:\n")
  cat("1. Prisoner's Dilemma\n")
  cat("2. Rock-Paper-Scissors\n")
  cat("3. Battle of the Sexes\n")
  cat("4. Custom 2x2 Game\n")
  cat("5. Exit\n\n")
  
  choice <- readline(prompt = "Enter your choice (1-5): ")
  
  switch(choice,
    "1" = prisoners_dilemma(),
    "2" = rock_paper_scissors(),
    "3" = battle_of_sexes(),
    "4" = {
      cat("\nEnter payoff values for a 2x2 game:\n")
      cat("Player 1 payoffs:\n")
      a11 <- as.numeric(readline("Player 1 payoff when both play Strategy 1: "))
      a12 <- as.numeric(readline("Player 1 payoff when P1=Strategy 1, P2=Strategy 2: "))
      a21 <- as.numeric(readline("Player 1 payoff when P1=Strategy 2, P2=Strategy 1: "))
      a22 <- as.numeric(readline("Player 1 payoff when both play Strategy 2: "))
      
      cat("\nPlayer 2 payoffs:\n")
      b11 <- as.numeric(readline("Player 2 payoff when both play Strategy 1: "))
      b12 <- as.numeric(readline("Player 2 payoff when P1=Strategy 1, P2=Strategy 2: "))
      b21 <- as.numeric(readline("Player 2 payoff when P1=Strategy 2, P2=Strategy 1: "))
      b22 <- as.numeric(readline("Player 2 payoff when both play Strategy 2: "))
      
      analyze_custom_game(a11, a12, a21, a22, b11, b12, b21, b22)
    },
    "5" = {
      cat("Thanks for using the Game Theory Analyzer!\n")
      return(FALSE)
    },
    {
      cat("Invalid choice. Please try again.\n\n")
    }
  )
  
  cat("\nPress Enter to continue...")
  readline()
  return(TRUE)
}

# Run the interactive menu system
run_game_theory_app <- function() {
  if (interactive()) {
    continue <- TRUE
    while (continue) {
      continue <- main_menu()
    }
  } else {
    # Non-interactive mode - run demos
    cat("Running Game Theory Analyzer in demo mode...\n\n")
    prisoners_dilemma()
    cat("\n" , rep("=", 50), "\n\n")
    rock_paper_scissors()
    cat("\n" , rep("=", 50), "\n\n")
    battle_of_sexes()
  }
}

# =============================================================================
# ENTRY POINT
# =============================================================================

# Check if this script is being run directly
if (sys.nframe() == 0) {
  run_game_theory_app()
}