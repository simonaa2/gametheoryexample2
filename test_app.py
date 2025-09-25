#!/usr/bin/env python3
"""
Simple test script to verify the application works correctly.
"""

import sys
import importlib.util

def test_imports():
    """Test that all required modules can be imported."""
    required_modules = [
        'streamlit',
        'pandas', 
        'numpy',
        'altair',
        'pydeck'
    ]
    
    print("🧪 Testing module imports...")
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} imported successfully")
        except ImportError as e:
            print(f"❌ Failed to import {module}: {e}")
            return False
    
    return True

def test_app_files():
    """Test that main application files can be imported."""
    print("\n🧪 Testing application files...")
    
    files_to_test = [
        'Hello.py',
        'utils.py',
        'pages/0_Animation_Demo.py',
        'pages/1_Plotting_Demo.py', 
        'pages/2_Mapping_Demo.py',
        'pages/3_DataFrame_Demo.py'
    ]
    
    for file_path in files_to_test:
        try:
            # Convert file path to module name
            module_name = file_path.replace('/', '.').replace('.py', '')
            if module_name.startswith('pages.'):
                # Handle pages directory
                module_name = module_name.replace('pages.', '')
            
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"✅ {file_path} loaded successfully")
            else:
                print(f"❌ Could not load spec for {file_path}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to load {file_path}: {e}")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Running application tests...\n")
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test application files
    if not test_app_files():
        success = False
    
    if success:
        print("\n✅ All tests passed! Application is ready for deployment.")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())