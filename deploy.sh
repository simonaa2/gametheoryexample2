#!/bin/bash

# Deployment script for Google Cloud Platform
# Usage: ./deploy.sh [cloud-run|app-engine]

set -e

DEPLOYMENT_TYPE=${1:-cloud-run}
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}

if [ -z "$PROJECT_ID" ]; then
    echo "Error: Please set GOOGLE_CLOUD_PROJECT environment variable or configure gcloud project"
    exit 1
fi

echo "Deploying to $DEPLOYMENT_TYPE for project: $PROJECT_ID"

case $DEPLOYMENT_TYPE in
    "cloud-run")
        echo "Building and deploying to Cloud Run..."
        gcloud builds submit --config cloudbuild.yaml
        echo "✅ Deployment to Cloud Run completed!"
        echo "Access your app at: https://streamlit-app-$(gcloud config get-value project).a.run.app"
        ;;
    
    "app-engine")
        echo "Deploying to App Engine..."
        gcloud app deploy app.yaml --quiet
        echo "✅ Deployment to App Engine completed!"
        gcloud app browse
        ;;
    
    *)
        echo "Usage: $0 [cloud-run|app-engine]"
        echo "  cloud-run   - Deploy to Google Cloud Run (default)"
        echo "  app-engine  - Deploy to Google App Engine"
        exit 1
        ;;
esac