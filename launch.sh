#!/bin/bash

# Game Theory Analyzer Launcher Script
# This script provides easy access to different modes of the application

echo "=========================================="
echo "    GAME THEORY ANALYZER LAUNCHER"
echo "=========================================="
echo ""
echo "Choose how to run the Game Theory Analyzer:"
echo ""
echo "1) Interactive R Console Mode"
echo "2) Demo Mode (Non-interactive)"
echo "3) Web Interface Mode"
echo "4) View Help"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "Starting Interactive R Console Mode..."
        echo "You can analyze games and create custom scenarios."
        echo ""
        Rscript game_theory.R
        ;;
    2)
        echo ""
        echo "Running Demo Mode..."
        echo "This will show examples of all supported games."
        echo ""
        Rscript demo.R
        ;;
    3)
        echo ""
        echo "Starting Web Interface..."
        echo "The web interface will be available at: http://localhost:8000"
        echo "Press Ctrl+C to stop the server."
        echo ""
        python3 -m http.server 8000
        ;;
    4)
        echo ""
        echo "GAME THEORY ANALYZER - HELP"
        echo "============================"
        echo ""
        echo "Files in this application:"
        echo "- game_theory.R    : Main R application with game theory functions"
        echo "- demo.R          : Demonstration script showing all features"
        echo "- index.html      : Interactive web interface"
        echo "- README.md       : Comprehensive documentation"
        echo ""
        echo "Usage modes:"
        echo "1. Interactive Console: Full R environment for custom analysis"
        echo "2. Demo Mode: Automated demonstration of all game types"
        echo "3. Web Interface: User-friendly browser-based interface"
        echo ""
        echo "Game types supported:"
        echo "- Prisoner's Dilemma"
        echo "- Rock-Paper-Scissors"  
        echo "- Battle of the Sexes"
        echo "- Custom 2x2 games"
        echo ""
        echo "Features:"
        echo "- Nash equilibrium detection (pure and mixed strategies)"
        echo "- Payoff matrix analysis"
        echo "- Educational explanations"
        echo "- Interactive game creation"
        ;;
    *)
        echo ""
        echo "Invalid choice. Please run the script again and choose 1-4."
        ;;
esac

echo ""
echo "Thank you for using the Game Theory Analyzer!"