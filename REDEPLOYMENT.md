# Redeployment Guide

This guide helps you redeploy the Game Theory Examples application after fixing issues or making updates.

## Quick Redeployment

Use the unified redeployment script for a streamlined experience:

### Cloud Run (Recommended)
```bash
./deploy-scripts/redeploy.sh cloud-run YOUR_PROJECT_ID us-central1
```

### App Engine
```bash
./deploy-scripts/redeploy.sh app-engine YOUR_PROJECT_ID
```

The redeployment script will:
- ✅ Verify all prerequisites (gcloud, docker, required files)
- ✅ Check that all configuration files exist
- ✅ Automatically detect your current project if not specified
- ✅ Deploy to your chosen platform

## Manual Redeployment

If you prefer to deploy manually or need more control:

### Cloud Run Manual Redeployment

```bash
# 1. Ensure you're authenticated
gcloud auth login

# 2. Set your project
gcloud config set project YOUR_PROJECT_ID

# 3. Enable required services (if not already enabled)
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# 4. Build and deploy
./deploy-scripts/deploy-cloud-run.sh YOUR_PROJECT_ID us-central1
```

### App Engine Manual Redeployment

```bash
# 1. Ensure you're authenticated
gcloud auth login

# 2. Set your project
gcloud config set project YOUR_PROJECT_ID

# 3. Deploy
./deploy-scripts/deploy-app-engine.sh YOUR_PROJECT_ID
```

## Automated CI/CD Redeployment

For automatic redeployments on code push:

### Using Cloud Build

1. **Ensure Cloud Build is enabled**:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   ```

2. **Connect your GitHub repository**:
   - Go to [Cloud Build Console](https://console.cloud.google.com/cloud-build/triggers)
   - Click "Connect Repository"
   - Follow the prompts to connect your GitHub repo

3. **Create a trigger**:
   - Trigger type: Push to branch
   - Branch: `^main$` (or your preferred branch)
   - Build configuration: Cloud Build configuration file
   - Location: `/cloudbuild.yaml`

4. **Push changes to trigger deployment**:
   ```bash
   git add .
   git commit -m "Redeploy with fixes"
   git push origin main
   ```

Cloud Build will automatically:
- Build your Docker image
- Tag it with both commit SHA and `latest`
- Push to Google Container Registry
- Deploy to Cloud Run

## Troubleshooting Common Deployment Issues

### Issue 1: Build Failures

**Symptoms**: Docker build fails or times out

**Solutions**:
- Check your `requirements.txt` for incompatible package versions
- Ensure Docker has enough memory allocated (4GB+ recommended)
- Review build logs: `gcloud builds list --limit=5`

### Issue 2: Service Unavailable After Deployment

**Symptoms**: Deployment succeeds but service returns 502/503 errors

**Solutions**:
- Check that port 8501 is correctly configured
- Verify health check endpoint: `/_stcore/health`
- Review logs: `gcloud run logs tail --service=gametheory-app --region=us-central1`
- Increase startup timeout if app takes longer to initialize

### Issue 3: Permission Errors

**Symptoms**: "Permission denied" or "Forbidden" errors

**Solutions**:
- Verify you have the correct IAM roles:
  - `roles/run.admin` for Cloud Run
  - `roles/appengine.appAdmin` for App Engine
- Check service account permissions
- Run: `gcloud auth application-default login`

### Issue 4: Memory or CPU Issues

**Symptoms**: Service crashes or becomes unresponsive under load

**Solutions**:
- Increase memory allocation in deployment configuration:
  - Cloud Run: Edit `cloudbuild.yaml` or use `--memory=2Gi`
  - App Engine: Edit `app.yaml` resources section
- Monitor resource usage in Cloud Console
- Consider enabling autoscaling with more instances

### Issue 5: Environment Variables Not Set

**Symptoms**: Streamlit doesn't start correctly or has wrong configuration

**Solutions**:
- Verify environment variables in deployment configuration
- Check `cloudbuild.yaml` for Cloud Run
- Check `app.yaml` for App Engine
- Required variables:
  - `STREAMLIT_SERVER_HEADLESS=true`
  - `STREAMLIT_SERVER_PORT=8501` (or 8080 for App Engine)
  - `STREAMLIT_SERVER_ADDRESS=0.0.0.0`
  - `STREAMLIT_BROWSER_GATHER_USAGE_STATS=false`

## Rollback Procedures

### Cloud Run Rollback

```bash
# List recent revisions
gcloud run revisions list --service=gametheory-app --region=us-central1

# Rollback to a specific revision
gcloud run services update-traffic gametheory-app \
    --to-revisions=REVISION_NAME=100 \
    --region=us-central1
```

### App Engine Rollback

```bash
# List versions
gcloud app versions list

# Route traffic to previous version
gcloud app services set-traffic default --splits=PREVIOUS_VERSION=1
```

## Viewing Deployment Status

### Cloud Run
```bash
# Get service details
gcloud run services describe gametheory-app --region=us-central1

# View recent logs
gcloud run logs tail --service=gametheory-app --region=us-central1

# List revisions
gcloud run revisions list --service=gametheory-app --region=us-central1
```

### App Engine
```bash
# Get app details
gcloud app describe

# View logs
gcloud app logs tail -s default

# List versions
gcloud app versions list
```

## Health Check Verification

After deployment, verify the health endpoint:

```bash
# For Cloud Run
SERVICE_URL=$(gcloud run services describe gametheory-app --region=us-central1 --format="value(status.url)")
curl "$SERVICE_URL/_stcore/health"

# For App Engine
APP_URL=$(gcloud app browse --no-launch-browser 2>&1 | grep -o 'https://[^[:space:]]*')
curl "$APP_URL/_stcore/health"
```

Expected response: `{"status": "ok"}` or similar healthy status

## Cost Optimization for Redeployment

To minimize costs during redeployment testing:

1. **Use Cloud Run** (scales to zero when not in use)
2. **Set minimum instances to 0** in production
3. **Delete old container images** to save storage:
   ```bash
   # List old images
   gcloud container images list-tags gcr.io/PROJECT_ID/gametheory-app
   
   # Delete specific tag
   gcloud container images delete gcr.io/PROJECT_ID/gametheory-app:OLD_TAG
   ```

## Getting Help

- Check deployment logs in Cloud Console
- Review [DEPLOY.md](DEPLOY.md) for detailed deployment instructions
- Visit [Google Cloud Documentation](https://cloud.google.com/docs)
- Check [Streamlit Cloud Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud)

---

## Quick Reference

| Task | Command |
|------|---------|
| Quick redeploy Cloud Run | `./deploy-scripts/redeploy.sh cloud-run PROJECT_ID` |
| Quick redeploy App Engine | `./deploy-scripts/redeploy.sh app-engine PROJECT_ID` |
| View Cloud Run logs | `gcloud run logs tail --service=gametheory-app` |
| View App Engine logs | `gcloud app logs tail` |
| Check deployment status | `gcloud run services describe gametheory-app` |
| Rollback Cloud Run | `gcloud run services update-traffic gametheory-app --to-revisions=REV=100` |
| Delete service | `gcloud run services delete gametheory-app` |

---

*For initial deployment setup, see [DEPLOY.md](DEPLOY.md)*
