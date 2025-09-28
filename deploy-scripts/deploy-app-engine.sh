#!/bin/bash

# Deploy Game Theory Examples to Google App Engine
# Usage: ./deploy-app-engine.sh [PROJECT_ID]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying Game Theory Examples to Google App Engine${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project ID
if [ -n "$1" ]; then
    PROJECT_ID="$1"
    echo -e "${YELLOW}📋 Using provided project ID: $PROJECT_ID${NC}"
    gcloud config set project "$PROJECT_ID"
else
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ No project ID provided and no default project set.${NC}"
        echo "Usage: $0 [PROJECT_ID]"
        echo "Or set default project: gcloud config set project YOUR_PROJECT_ID"
        exit 1
    fi
    echo -e "${YELLOW}📋 Using current project: $PROJECT_ID${NC}"
fi

# Check if App Engine is enabled
echo -e "${YELLOW}🔍 Checking if App Engine is enabled...${NC}"
if ! gcloud app describe >/dev/null 2>&1; then
    echo -e "${YELLOW}⚙️  App Engine not initialized. Creating App Engine application...${NC}"
    echo "Please select a region when prompted (e.g., us-central)"
    gcloud app create
fi

# Deploy to App Engine
echo -e "${YELLOW}🔨 Deploying to App Engine...${NC}"
gcloud app deploy app.yaml --quiet

# Get the deployed URL
APP_URL=$(gcloud app browse --no-launch-browser 2>&1 | grep -o 'https://[^[:space:]]*')

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Your Game Theory Examples app is available at:${NC}"
echo -e "${GREEN}   $APP_URL${NC}"
echo ""
echo -e "${YELLOW}📊 To view logs:${NC} gcloud app logs tail -s default"
echo -e "${YELLOW}📈 To view in browser:${NC} gcloud app browse"