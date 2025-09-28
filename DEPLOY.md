# Google Cloud Deployment Guide

This guide explains how to deploy the Game Theory Examples application to Google Cloud Platform.

## Prerequisites

1. **Google Cloud Account**: Sign up at [cloud.google.com](https://cloud.google.com)
2. **Google Cloud SDK**: Install from [cloud.google.com/sdk](https://cloud.google.com/sdk/docs/install)
3. **Docker** (for Cloud Run): Install from [docker.com](https://docs.docker.com/get-docker/)

## Quick Setup

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Create or select a project**:
   ```bash
   # Create new project
   gcloud projects create YOUR_PROJECT_ID
   
   # Or select existing project
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Enable billing** for your project in the [Google Cloud Console](https://console.cloud.google.com)

## Deployment Options

### Option 1: Google App Engine (Recommended for beginners)

App Engine is the simplest option with automatic scaling and no container management.

**Deploy using script**:
```bash
./deploy-scripts/deploy-app-engine.sh YOUR_PROJECT_ID
```

**Or deploy manually**:
```bash
gcloud app deploy app.yaml
```

**Features**:
- ✅ Automatic scaling (0 to 10 instances)
- ✅ Custom domain support
- ✅ SSL certificates included
- ✅ No server management
- 💰 Pay per use (free tier available)

### Option 2: Google Cloud Run

Cloud Run offers more control and can be more cost-effective for variable traffic.

**Deploy using script**:
```bash
./deploy-scripts/deploy-cloud-run.sh YOUR_PROJECT_ID us-central1
```

**Or deploy manually**:
```bash
# Build and push image
docker build -t gcr.io/YOUR_PROJECT_ID/gametheory-app .
docker push gcr.io/YOUR_PROJECT_ID/gametheory-app

# Deploy to Cloud Run
gcloud run deploy gametheory-app \
    --image=gcr.io/YOUR_PROJECT_ID/gametheory-app \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated \
    --port=8501 \
    --memory=1Gi \
    --cpu=1 \
    --max-instances=10
```

**Features**:
- ✅ Container-based deployment
- ✅ Pay per request
- ✅ Scale to zero when not in use
- ✅ Custom domains and SSL
- ✅ More configuration options

### Option 3: Automated CI/CD with Cloud Build

For continuous deployment when you push code changes.

1. **Enable Cloud Build API**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Connect your repository** in the [Cloud Build Console](https://console.cloud.google.com/cloud-build)

3. **Set up trigger** to use `cloudbuild.yaml` for automatic deployments

**Features**:
- ✅ Automatic deployment on code changes
- ✅ Build history and logs
- ✅ Integration with GitHub/GitLab
- ✅ Rollback capabilities

## Configuration

### Environment Variables

The application uses these environment variables for Google Cloud:

```yaml
STREAMLIT_SERVER_HEADLESS: "true"
STREAMLIT_SERVER_PORT: "8501"  # 8080 for App Engine
STREAMLIT_SERVER_ADDRESS: "0.0.0.0"
STREAMLIT_BROWSER_GATHER_USAGE_STATS: "false"
```

### Health Checks

The application includes health check endpoints at `/_stcore/health` for:
- App Engine readiness and liveness checks
- Cloud Run health monitoring
- Load balancer verification

## Cost Optimization

### App Engine
- Uses automatic scaling with min 0 instances
- Scales down when not in use
- Free tier: 28 instance hours per day

### Cloud Run
- Scales to zero when not in use
- Pay only for actual requests
- Free tier: 2 million requests per month

## Monitoring and Logs

### View Application Logs
```bash
# App Engine
gcloud app logs tail -s default

# Cloud Run
gcloud run logs tail --service=gametheory-app --region=us-central1
```

### Monitor Performance
- Visit [Google Cloud Console](https://console.cloud.google.com)
- Navigate to your service (App Engine or Cloud Run)
- View metrics, logs, and performance data

## Troubleshooting

### Common Issues

1. **Build failures**: Check `cloudbuild.yaml` configuration
2. **Memory errors**: Increase memory allocation in configuration files
3. **Port issues**: Ensure STREAMLIT_SERVER_PORT matches exposed port
4. **Permission errors**: Check IAM roles and API enablement

### Debug Commands
```bash
# Check deployment status
gcloud app versions list  # App Engine
gcloud run services list  # Cloud Run

# View detailed logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50
```

## Security Best Practices

1. **Use least privilege IAM roles**
2. **Enable audit logging**
3. **Use HTTPS only** (enabled by default)
4. **Regular security updates** of dependencies
5. **Monitor access patterns**

## Custom Domains

### App Engine
```bash
gcloud app domain-mappings create DOMAIN_NAME
```

### Cloud Run
1. Map domain in Cloud Run console
2. Update DNS records as instructed
3. SSL certificate will be provisioned automatically

## Scaling Configuration

### App Engine (app.yaml)
```yaml
automatic_scaling:
  min_instances: 0
  max_instances: 10
  target_cpu_utilization: 0.6
```

### Cloud Run (cloudbuild.yaml)
```yaml
--max-instances=10
--memory=1Gi
--cpu=1
```

## Next Steps

1. **Custom Domain**: Set up your own domain name
2. **Analytics**: Add Google Analytics for usage tracking
3. **Monitoring**: Set up alerts for performance and errors
4. **CDN**: Use Cloud CDN for global performance
5. **Database**: Add Cloud Firestore for user data persistence

## Support

- [Google Cloud Documentation](https://cloud.google.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [App Engine Python Runtime](https://cloud.google.com/appengine/docs/standard/python3)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

---

*This application is optimized for Google Cloud Platform with proper health checks, security, and scaling configurations.*