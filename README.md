# Streamlit Game Theory Example

This is a Streamlit application demonstrating various interactive visualizations and data analysis capabilities.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run Hello.py
```

## Google Cloud Deployment

This application is configured for deployment on Google Cloud Platform using multiple deployment options:

### Option 1: Cloud Run (Recommended)

1. Build and deploy using Google Cloud Build:
```bash
gcloud builds submit --config cloudbuild.yaml
```

2. Or deploy manually:
```bash
# Build the Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/streamlit-app .

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/streamlit-app

# Deploy to Cloud Run
gcloud run deploy streamlit-app \
    --image gcr.io/YOUR_PROJECT_ID/streamlit-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080
```

### Option 2: App Engine

1. Deploy to App Engine:
```bash
gcloud app deploy app.yaml
```

2. View your application:
```bash
gcloud app browse
```

### Configuration Files

- `Dockerfile`: Container configuration for Cloud Run
- `app.yaml`: App Engine configuration
- `cloudbuild.yaml`: Cloud Build configuration for CI/CD
- `.gcloudignore`: Files to exclude from deployment
- `main.py`: Entry point for App Engine deployment

### Requirements

- Python 3.11+
- Google Cloud SDK
- Docker (for Cloud Run deployment)
