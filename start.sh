#!/bin/bash

# Use PORT environment variable if set, otherwise use 8080
PORT=${PORT:-8080}

# Start Streamlit app
exec streamlit run Hello.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false