# Streamlit Demo App - Google Cloud Deployment

This is a Streamlit demonstration app with multiple interactive demos including animations, plotting, mapping, and data visualization.

## 🚀 Google Cloud Deployment

This application is configured for deployment to Google App Engine. Follow these steps to deploy:

### Prerequisites

1. **Google Cloud Account**: Create an account at [Google Cloud Console](https://console.cloud.google.com/)
2. **Google Cloud SDK**: Install from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
3. **Google Cloud Project**: Create a new project or use an existing one

### Deployment Steps

1. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   ```

2. **Set your project ID**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Deploy using the provided script**:
   ```bash
   ./deploy.sh
   ```

   Or deploy manually:
   ```bash
   gcloud app deploy app.yaml
   ```

4. **View your deployed app**:
   ```bash
   gcloud app browse
   ```

### Configuration Files

- **`app.yaml`**: Google App Engine configuration
- **`main.py`**: Entry point for the application server
- **`.gcloudignore`**: Files to exclude from deployment
- **`requirements.txt`**: Python dependencies
- **`deploy.sh`**: Automated deployment script

### App Features

The application includes several demo pages:
- **Animation Demo**: Interactive fractal visualization
- **Plotting Demo**: Real-time data plotting
- **Mapping Demo**: Geographic data visualization
- **DataFrame Demo**: Data analysis and visualization

### Local Development

To run the app locally:

```bash
pip install -r requirements.txt
streamlit run Hello.py
```

### Monitoring and Management

After deployment, you can:
- **View logs**: `gcloud app logs tail -s default`
- **Manage versions**: `gcloud app versions list`
- **Stop the app**: `gcloud app versions stop [VERSION]`

### Cost Optimization

The app is configured with:
- Automatic scaling (0-2 instances)
- CPU-based scaling
- Minimal resource allocation for cost efficiency

### Troubleshooting

If you encounter issues:
1. Ensure all required APIs are enabled
2. Check that your Google Cloud project has billing enabled
3. Verify that you have the necessary permissions for App Engine deployment
