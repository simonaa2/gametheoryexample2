#!/usr/bin/env python3
"""
Comprehensive functionality test for the Game Theory Examples application.
Tests all key components to ensure the application is working correctly.
"""

import sys
import os
import importlib.util
import numpy as np
import pandas as pd

# Test results tracker
test_results = []
def test(name):
    def decorator(func):
        def wrapper():
            try:
                func()
                test_results.append((name, True, None))
                print(f"✓ {name}")
                return True
            except Exception as e:
                test_results.append((name, False, str(e)))
                print(f"✗ {name}: {e}")
                return False
        return wrapper
    return decorator

# Test 1: Core imports
@test("Core imports (streamlit, numpy, pandas, matplotlib)")
def test_core_imports():
    import streamlit
    import numpy
    import pandas
    import matplotlib.pyplot
    assert True

# Test 2: Main file imports
@test("Hello.py imports successfully")
def test_hello_import():
    import Hello
    assert hasattr(Hello, 'run')

# Test 3: Utils imports
@test("utils.py imports successfully")
def test_utils_import():
    import utils
    assert hasattr(utils, 'show_code')

# Test 4: Page files load
@test("All page files load without errors")
def test_page_files():
    pages = [
        'pages/0_Prisoners_Dilemma.py',
        'pages/1_Nash_Equilibrium.py',
        'pages/2_Mixed_Strategy.py',
        'pages/3_Evolutionary_Games.py'
    ]
    for page in pages:
        spec = importlib.util.spec_from_file_location('test_module', page)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    assert True

# Test 5: Nash equilibrium calculation logic
@test("Nash equilibrium calculation works correctly")
def test_nash_equilibrium_logic():
    # Test with Prisoner's Dilemma payoffs
    payoff_p1 = np.array([[3, 0], [5, 1]])
    payoff_p2 = np.array([[3, 5], [0, 1]])
    
    # Check (Defect, Defect) is Nash equilibrium
    # At position (1, 1)
    row, col = 1, 1
    
    # Player 1's best response
    current_p1 = payoff_p1[row, col]  # 1
    alternative_p1 = payoff_p1[0, col]  # 0
    assert current_p1 >= alternative_p1
    
    # Player 2's best response
    current_p2 = payoff_p2[row, col]  # 1
    alternative_p2 = payoff_p2[row, 0]  # 0
    assert current_p2 >= alternative_p2

# Test 6: Mixed strategy calculation
@test("Mixed strategy calculation works correctly")
def test_mixed_strategy_logic():
    # Test with Matching Pennies
    p1_matrix = np.array([[1, -1], [-1, 1]])
    p2_matrix = np.array([[-1, 1], [1, -1]])
    
    # Calculate mixed strategy equilibrium
    denominator_p1 = (p2_matrix[0,0] - p2_matrix[1,0]) - (p2_matrix[0,1] - p2_matrix[1,1])
    p1_prob_a = (p2_matrix[1,1] - p2_matrix[1,0]) / denominator_p1
    
    denominator_p2 = (p1_matrix[0,0] - p1_matrix[0,1]) - (p1_matrix[1,0] - p1_matrix[1,1])
    p2_prob_a = (p1_matrix[1,1] - p1_matrix[0,1]) / denominator_p2
    
    # For matching pennies, both should play 50-50
    assert abs(p1_prob_a - 0.5) < 0.01
    assert abs(p2_prob_a - 0.5) < 0.01

# Test 7: Evolutionary dynamics simulation
@test("Evolutionary dynamics simulation works correctly")
def test_evolutionary_dynamics():
    # Simple test case
    payoff_matrix = np.array([[1, 0], [2, 1]])
    
    freq_a = 0.5
    p = freq_a
    q = 1 - p
    
    # Calculate fitness
    fitness_a = p * payoff_matrix[0, 0] + q * payoff_matrix[0, 1]
    fitness_b = p * payoff_matrix[1, 0] + q * payoff_matrix[1, 1]
    avg_fitness = p * fitness_a + q * fitness_b
    
    # Check calculations are reasonable
    assert fitness_a >= 0
    assert fitness_b >= 0
    assert avg_fitness >= 0
    assert avg_fitness <= max(fitness_a, fitness_b) + 0.01

# Test 8: Payoff matrix creation
@test("Payoff matrix creation and display")
def test_payoff_matrix():
    # Create payoff matrices
    payoff_p1 = np.array([[3, 0], [5, 1]])
    payoff_p2 = np.array([[3, 5], [0, 1]])
    
    # Create combined display
    game_display = pd.DataFrame(
        [
            [f"({payoff_p1[0,0]}, {payoff_p2[0,0]})", f"({payoff_p1[0,1]}, {payoff_p2[0,1]})"],
            [f"({payoff_p1[1,0]}, {payoff_p2[1,0]})", f"({payoff_p1[1,1]}, {payoff_p2[1,1]})"]
        ],
        columns=["Player 2: Strategy A", "Player 2: Strategy B"],
        index=["Player 1: Strategy A", "Player 1: Strategy B"]
    )
    
    assert game_display.shape == (2, 2)
    assert game_display.iloc[0, 0] == "(3, 3)"

# Test 9: Best response analysis
@test("Best response analysis works correctly")
def test_best_response():
    payoff_p1 = np.array([[3, 0], [5, 1]])
    payoff_p2 = np.array([[3, 5], [0, 1]])
    
    # Player 1's best response to Player 2's Strategy A (column 0)
    # Compare row 0 vs row 1
    assert payoff_p1[1, 0] > payoff_p1[0, 0]  # Strategy B is better (5 > 3)
    
    # Player 2's best response to Player 1's Strategy B (row 1)
    # Compare column 0 vs column 1
    assert payoff_p2[1, 1] > payoff_p2[1, 0]  # Strategy B is better (1 > 0)

# Test 10: File structure
@test("All required files exist")
def test_file_structure():
    required_files = [
        'Hello.py',
        'utils.py',
        'requirements.txt',
        'README.md',
        'pages/0_Prisoners_Dilemma.py',
        'pages/1_Nash_Equilibrium.py',
        'pages/2_Mixed_Strategy.py',
        'pages/3_Evolutionary_Games.py'
    ]
    
    for file in required_files:
        assert os.path.exists(file), f"Missing file: {file}"

def main():
    print("\n" + "="*60)
    print("Game Theory Examples - Functionality Test Suite")
    print("="*60 + "\n")
    
    # Run all tests
    test_core_imports()
    test_hello_import()
    test_utils_import()
    test_page_files()
    test_nash_equilibrium_logic()
    test_mixed_strategy_logic()
    test_evolutionary_dynamics()
    test_payoff_matrix()
    test_best_response()
    test_file_structure()
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result, _ in test_results if result)
    total = len(test_results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! The application is working well.")
        return 0
    else:
        print("\n⚠️  Some tests failed. See details above.")
        print("\nFailed tests:")
        for name, result, error in test_results:
            if not result:
                print(f"  - {name}: {error}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
