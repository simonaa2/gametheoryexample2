# Google Cloud Deployment Guide

This guide provides multiple options for deploying the Streamlit application to Google Cloud Platform.

## 🎯 Deployment Options

### Option 1: Google App Engine (Recommended for beginners)
**Best for**: Simple deployment, automatic scaling, minimal configuration

#### Quick Deploy
```bash
./deploy.sh
```

#### Manual Deploy
```bash
gcloud app deploy app.yaml
```

**Pros**:
- Zero server management
- Automatic scaling to zero
- Built-in load balancing
- Integrated with Google Cloud services

**Cons**:
- Less control over infrastructure
- Limited to specific runtimes

---

### Option 2: Google Cloud Run (Recommended for Docker users)
**Best for**: Containerized applications, more control, pay-per-use

#### Quick Deploy
```bash
./deploy-cloud-run.sh
```

#### Manual Deploy
```bash
# Build and push image
docker build -t gcr.io/PROJECT_ID/streamlit-app .
docker push gcr.io/PROJECT_ID/streamlit-app

# Deploy to Cloud Run
gcloud run deploy streamlit-app \
    --image gcr.io/PROJECT_ID/streamlit-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

**Pros**:
- Container-based deployment
- More flexible scaling options
- Better for microservices architecture
- Support for custom domains

**Cons**:
- Requires Docker knowledge
- Slightly more complex setup

---

### Option 3: Google Kubernetes Engine (GKE)
**Best for**: Large-scale applications, complex orchestration needs

#### Prerequisites
```bash
# Create a GKE cluster
gcloud container clusters create streamlit-cluster \
    --num-nodes=3 \
    --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials streamlit-cluster --zone=us-central1-a
```

#### Deploy
```bash
# Build and push image
docker build -t gcr.io/PROJECT_ID/streamlit-app .
docker push gcr.io/PROJECT_ID/streamlit-app

# Create Kubernetes deployment
kubectl create deployment streamlit-app --image=gcr.io/PROJECT_ID/streamlit-app
kubectl expose deployment streamlit-app --type=LoadBalancer --port=80 --target-port=8080
```

**Pros**:
- Full container orchestration
- High availability and scalability
- Advanced networking and security features

**Cons**:
- Most complex setup
- Higher costs for small applications
- Requires Kubernetes knowledge

---

## 📋 Prerequisites

### 1. Google Cloud Setup
1. Create a Google Cloud account
2. Create a new project or select existing one
3. Enable billing for your project
4. Install Google Cloud SDK

### 2. Authentication
```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Verify setup
gcloud config list
```

### 3. Required APIs
Enable these APIs in your Google Cloud Console:
- App Engine Admin API (for App Engine)
- Cloud Build API (for Cloud Run/GKE)
- Cloud Run API (for Cloud Run)
- Container Registry API (for Docker images)
- Kubernetes Engine API (for GKE)

---

## 💰 Cost Considerations

### App Engine
- **Free tier**: 28 hours per day
- **Pricing**: Pay for instance hours
- **Scaling**: Automatic (0 to N instances)

### Cloud Run
- **Free tier**: 2 million requests per month
- **Pricing**: Pay per request and CPU time
- **Scaling**: 0 to 1000 instances

### GKE
- **Cluster management**: $0.10 per hour per cluster
- **Node pricing**: Based on Compute Engine pricing
- **Minimum**: 3 nodes recommended

---

## 🔧 Configuration Files

| File | Purpose | Deployment Option |
|------|---------|-------------------|
| `app.yaml` | App Engine configuration | App Engine |
| `Dockerfile` | Container definition | Cloud Run, GKE |
| `docker-compose.yml` | Local development | Development |
| `main.py` | App Engine entry point | App Engine |
| `.gcloudignore` | Exclude files from deployment | All |

---

## 🚨 Troubleshooting

### Common Issues

1. **"Project not found" error**
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   gcloud projects list
   ```

2. **Permission denied**
   ```bash
   gcloud auth login
   gcloud auth list
   ```

3. **API not enabled**
   ```bash
   gcloud services enable appengine.googleapis.com
   gcloud services enable run.googleapis.com
   ```

4. **Docker authentication issues**
   ```bash
   gcloud auth configure-docker
   ```

### Getting Help
- View deployment logs: `gcloud app logs tail -s default`
- Check service status: `gcloud app versions list`
- Monitor resources: Google Cloud Console

---

## 🔒 Security Best Practices

1. **Environment Variables**: Store sensitive data in environment variables
2. **IAM Roles**: Use least privilege principle
3. **HTTPS**: Enable HTTPS for production deployments
4. **Authentication**: Consider adding authentication for sensitive applications
5. **Monitoring**: Set up monitoring and alerting

---

## 📊 Monitoring and Logging

### App Engine
```bash
# View logs
gcloud app logs tail -s default

# View metrics in Console
https://console.cloud.google.com/appengine
```

### Cloud Run
```bash
# View logs
gcloud run services logs tail streamlit-app --region us-central1

# View metrics in Console
https://console.cloud.google.com/run
```

---

## 🔄 CI/CD Integration

For automated deployments, consider integrating with:
- Google Cloud Build
- GitHub Actions
- GitLab CI/CD
- Jenkins

Example GitHub Actions workflow available in `.github/workflows/` directory.