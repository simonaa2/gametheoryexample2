#!/usr/bin/env python3
"""
Main entry point for Google App Engine deployment.
This script handles the Streamlit app startup with proper configuration for GAE.
"""
import os
import subprocess
import sys

def main():
    """Start the Streamlit application with proper configuration for App Engine."""
    
    # Get port from environment (App Engine sets this)
    port = os.environ.get('PORT', '8080')
    
    # Streamlit command with App Engine compatible settings
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'Hello.py',
        '--server.port', port,
        '--server.address', '0.0.0.0',
        '--server.headless', 'true',
        '--server.fileWatcherType', 'none',
        '--browser.gatherUsageStats', 'false',
        '--server.enableCORS', 'false',
        '--server.enableXsrfProtection', 'false'
    ]
    
    # Start the Streamlit app
    subprocess.run(cmd)

if __name__ == '__main__':
    main()