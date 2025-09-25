#!/usr/bin/env python3
"""
Main entry point for Google App Engine deployment.
This file starts the Streamlit application server.
"""

import os
import subprocess
import signal
import sys
from threading import Thread
import time

def run_streamlit():
    """Run the Streamlit application."""
    # Set environment variables for Streamlit
    os.environ["STREAMLIT_SERVER_PORT"] = os.environ.get("PORT", "8080")
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    # Start Streamlit
    cmd = [
        sys.executable, "-m", "streamlit", "run", "Hello.py",
        "--server.port", os.environ.get("PORT", "8080"),
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ]
    
    try:
        # Start the Streamlit process
        process = subprocess.Popen(cmd)
        
        # Handle shutdown gracefully
        def signal_handler(signum, frame):
            print("Shutting down Streamlit server...")
            process.terminate()
            process.wait()
            sys.exit(0)
            
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        # Wait for the process to complete
        process.wait()
        
    except Exception as e:
        print(f"Error starting Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_streamlit()