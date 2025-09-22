# Game Theory Analyzer in R

A comprehensive game theory application built in R that analyzes strategic games and finds Nash equilibria. This interactive tool helps users understand fundamental game theory concepts through classic examples and custom game analysis.

## 🎯 Features

### Core Game Theory Analysis
- **Nash Equilibrium Detection**: Finds both pure and mixed strategy Nash equilibria
- **Payoff Matrix Analysis**: Analyzes 2x2 strategic games
- **Custom Game Support**: Create and analyze your own games
- **Interactive Web Interface**: User-friendly HTML interface with real-time calculations

### Included Classic Games
1. **Prisoner's Dilemma** - Demonstrates dominant strategies and suboptimal outcomes
2. **Rock-Paper-Scissors** - Shows mixed strategy equilibria in zero-sum games  
3. **Battle of the Sexes** - Illustrates coordination problems with multiple equilibria

### Technical Implementation
- **Pure R Implementation**: Uses base R for all calculations
- **Mathematical Accuracy**: Implements proper Nash equilibrium algorithms
- **Educational Focus**: Clear explanations and step-by-step analysis
- **Web Interface**: Interactive HTML/JavaScript frontend

## 🚀 Getting Started

### Prerequisites
- R (version 4.0 or higher)
- Web browser for the interactive interface

### Installation
1. Clone this repository
2. Ensure R is installed on your system
3. No additional R packages required - uses base R only

### Running the Application

#### Command Line Interface
```bash
# Run the interactive R application
Rscript game_theory.R

# Or start R and source the file
R
> source("game_theory.R")
> run_game_theory_app()
```

#### Web Interface
1. Open `index.html` in your web browser
2. Interact with the game theory examples
3. Use the custom game analyzer to create your own scenarios

## 📊 Game Theory Concepts

### Nash Equilibrium
A strategy profile where no player can improve their payoff by unilaterally changing their strategy.

### Pure vs Mixed Strategies
- **Pure Strategy**: Playing a single strategy with certainty
- **Mixed Strategy**: Randomizing between strategies with specific probabilities

### Game Types Demonstrated
- **Coordination Games**: Players benefit from coordinating (Battle of the Sexes)
- **Prisoner's Dilemmas**: Individual rationality leads to collective irrationality
- **Zero-Sum Games**: One player's gain equals another's loss (Rock-Paper-Scissors)

## 🔬 Technical Details

### Nash Equilibrium Algorithm
The application implements the standard algorithm for finding Nash equilibria in 2x2 games:

1. **Pure Strategy Equilibria**: Check each strategy profile to see if any player wants to deviate
2. **Mixed Strategy Equilibria**: Solve the indifference conditions for each player

### Mathematical Foundation
For a 2x2 game with payoff matrices:
- Player 1's mixed strategy probability: Derived from Player 2's indifference condition
- Player 2's mixed strategy probability: Derived from Player 1's indifference condition
- Expected payoffs calculated using probability distributions

## 📝 Examples

### Prisoner's Dilemma Analysis
```
Strategy 1: Cooperate, Strategy 2: Defect

Player 1 Payoffs:         Player 2 Payoffs:
     C    D                    C    D  
C   [3]  [0]               C   [3]  [5]
D   [5]  [1]               D   [0]  [1]

Nash Equilibrium: (Defect, Defect) = (1, 1)
```

### Custom Game Creation
Use the web interface or R commands to create custom games:
```r
# Create a custom game
payoff <- create_payoff_matrix(2, 0, 0, 1, 1, 0, 0, 2)
equilibria <- find_nash_equilibria(payoff)
mixed_eq <- find_mixed_nash(payoff)
```

## 🎓 Educational Applications

This tool is designed for:
- **Economics Students**: Learning fundamental game theory concepts
- **Researchers**: Quick analysis of strategic interactions
- **Educators**: Teaching Nash equilibria and strategic thinking
- **Game Designers**: Understanding player incentives and balance

## 🔧 Advanced Features

### Interactive Analysis
- Real-time Nash equilibrium calculation
- Dynamic payoff matrix updates
- Visual representation of equilibria
- Step-by-step solution explanations

### Extensibility
The modular R code structure allows for easy extension:
- Add new game types
- Implement n-player games
- Include evolutionary game theory concepts
- Add advanced solution concepts

## 🌐 Web Interface Features

- **Responsive Design**: Works on desktop and mobile devices
- **Interactive Calculations**: Real-time analysis as you modify payoffs
- **Educational Content**: Built-in explanations of game theory concepts
- **Visual Matrices**: Clear payoff matrix displays

## 📚 Further Reading

- Game Theory basics: Nash equilibria and strategic thinking
- Applications in economics, politics, and biology
- Advanced topics: Evolutionary game theory, mechanism design
- Computational approaches to game theory

## 🤝 Contributing

This is an educational tool focused on demonstrating game theory concepts in R. 
Feel free to extend the functionality or suggest improvements!

## 📄 License

This project maintains the same license structure as the original Streamlit demo application.

---

**Built with R and mathematical rigor for educational excellence! 🎯📊**
