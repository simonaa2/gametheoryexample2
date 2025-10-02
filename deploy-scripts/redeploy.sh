#!/bin/bash

# Redeploy Game Theory Examples to Google Cloud
# This script helps redeploy the application after fixing issues
# Usage: ./redeploy.sh [app-engine|cloud-run] [PROJECT_ID] [REGION]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}🔄 Game Theory Examples - Redeployment Script${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check deployment type
DEPLOY_TYPE="${1:-cloud-run}"

if [ "$DEPLOY_TYPE" != "app-engine" ] && [ "$DEPLOY_TYPE" != "cloud-run" ]; then
    echo -e "${RED}❌ Invalid deployment type: $DEPLOY_TYPE${NC}"
    echo "Usage: $0 [app-engine|cloud-run] [PROJECT_ID] [REGION]"
    echo ""
    echo "Examples:"
    echo "  $0 cloud-run my-project us-central1"
    echo "  $0 app-engine my-project"
    exit 1
fi

echo -e "${YELLOW}📋 Deployment type: ${GREEN}$DEPLOY_TYPE${NC}"
echo ""

# Pre-deployment checks
echo -e "${YELLOW}🔍 Running pre-deployment checks...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed.${NC}"
    echo "Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
echo -e "${GREEN}✓ gcloud CLI is installed${NC}"

# Check if docker is installed (needed for Cloud Run)
if [ "$DEPLOY_TYPE" == "cloud-run" ]; then
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker is not installed.${NC}"
        echo "Install it from: https://docs.docker.com/get-docker/"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker is installed${NC}"
fi

# Check if required files exist
echo -e "${YELLOW}📁 Checking required files...${NC}"
REQUIRED_FILES=("Hello.py" "requirements.txt" "Dockerfile")
if [ "$DEPLOY_TYPE" == "app-engine" ]; then
    REQUIRED_FILES+=("app.yaml")
fi

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}❌ Required file not found: $file${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Found $file${NC}"
done

echo ""
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ All pre-deployment checks passed!${NC}"
echo -e "${YELLOW}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Deploy based on type
if [ "$DEPLOY_TYPE" == "cloud-run" ]; then
    echo -e "${BLUE}🚀 Starting Cloud Run deployment...${NC}"
    echo ""
    PROJECT_ID="${2}"
    REGION="${3:-us-central1}"
    
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${YELLOW}No project ID provided. Using current gcloud project...${NC}"
        PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
        if [ -z "$PROJECT_ID" ]; then
            echo -e "${RED}❌ No project ID set. Please provide one:${NC}"
            echo "Usage: $0 cloud-run PROJECT_ID [REGION]"
            exit 1
        fi
    fi
    
    echo -e "${YELLOW}📋 Project ID: ${GREEN}$PROJECT_ID${NC}"
    echo -e "${YELLOW}📍 Region: ${GREEN}$REGION${NC}"
    echo ""
    
    exec ./deploy-scripts/deploy-cloud-run.sh "$PROJECT_ID" "$REGION"
    
elif [ "$DEPLOY_TYPE" == "app-engine" ]; then
    echo -e "${BLUE}🚀 Starting App Engine deployment...${NC}"
    echo ""
    PROJECT_ID="${2}"
    
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${YELLOW}No project ID provided. Using current gcloud project...${NC}"
        PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    fi
    
    if [ -n "$PROJECT_ID" ]; then
        echo -e "${YELLOW}📋 Project ID: ${GREEN}$PROJECT_ID${NC}"
        echo ""
    fi
    
    exec ./deploy-scripts/deploy-app-engine.sh "$PROJECT_ID"
fi
