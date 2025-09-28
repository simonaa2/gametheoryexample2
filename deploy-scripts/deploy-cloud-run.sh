#!/bin/bash

# Deploy Game Theory Examples to Google Cloud Run
# Usage: ./deploy-cloud-run.sh [PROJECT_ID] [REGION]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Deploying Game Theory Examples to Google Cloud Run${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.docker.com/get-docker/"
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
        echo "Usage: $0 [PROJECT_ID] [REGION]"
        echo "Or set default project: gcloud config set project YOUR_PROJECT_ID"
        exit 1
    fi
    echo -e "${YELLOW}📋 Using current project: $PROJECT_ID${NC}"
fi

# Set region
REGION="${2:-us-central1}"
echo -e "${YELLOW}📍 Using region: $REGION${NC}"

# Service and image names
SERVICE_NAME="gametheory-app"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Enable required services
echo -e "${YELLOW}⚙️  Enabling required Google Cloud services...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build and push the Docker image
echo -e "${YELLOW}🔨 Building Docker image...${NC}"
docker build -t "$IMAGE_NAME" .

echo -e "${YELLOW}📤 Pushing image to Google Container Registry...${NC}"
docker push "$IMAGE_NAME"

# Deploy to Cloud Run
echo -e "${YELLOW}🚀 Deploying to Cloud Run...${NC}"
gcloud run deploy "$SERVICE_NAME" \
    --image="$IMAGE_NAME" \
    --region="$REGION" \
    --platform=managed \
    --allow-unauthenticated \
    --port=8501 \
    --memory=1Gi \
    --cpu=1 \
    --max-instances=10 \
    --set-env-vars="STREAMLIT_SERVER_HEADLESS=true,STREAMLIT_SERVER_PORT=8501,STREAMLIT_SERVER_ADDRESS=0.0.0.0,STREAMLIT_BROWSER_GATHER_USAGE_STATS=false"

# Get the deployed URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region="$REGION" --format="value(status.url)")

echo -e "${GREEN}✅ Deployment successful!${NC}"
echo -e "${GREEN}🌐 Your Game Theory Examples app is available at:${NC}"
echo -e "${GREEN}   $SERVICE_URL${NC}"
echo ""
echo -e "${YELLOW}📊 To view logs:${NC} gcloud run logs tail --service=$SERVICE_NAME --region=$REGION"
echo -e "${YELLOW}🔧 To update:${NC} Re-run this script"
echo -e "${YELLOW}🗑️  To delete:${NC} gcloud run services delete $SERVICE_NAME --region=$REGION"