#!/bin/bash

# Google Cloud Deployment Script for Streamlit App
# This script helps deploy the Streamlit application to Google App Engine

set -e  # Exit on any error

echo "🚀 Starting Google Cloud deployment..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK (gcloud) is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ You are not authenticated with Google Cloud."
    echo "Please run: gcloud auth login"
    exit 1
fi

# Get current project
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No Google Cloud project is set."
    echo "Please run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📋 Current project: $PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable appengine.googleapis.com

# Deploy to App Engine
echo "🌐 Deploying to Google App Engine..."
gcloud app deploy app.yaml --quiet

# Get the app URL
APP_URL=$(gcloud app browse --no-launch-browser)
echo "✅ Deployment complete!"
echo "🌍 Your app is available at: $APP_URL"

echo ""
echo "📚 Additional commands:"
echo "  View logs: gcloud app logs tail -s default"
echo "  Open app:  gcloud app browse"
echo "  Stop app:  gcloud app versions stop [VERSION]"