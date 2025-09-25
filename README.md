# Welcome to streamlit

This is the app you get when you run `streamlit hello`, extracted as its own app.

Edit [Hello.py](./Hello.py) to customize this app to your heart's desire. ❤️

Check it out on [Streamlit Community Cloud](https://st-hello-app.streamlit.app/)

## Deployment to Google Cloud Run

This app is configured for deployment to Google Cloud Run with the following files:

- `Dockerfile` - Container configuration that runs the app on port 8080
- `start.sh` - Startup script that respects the PORT environment variable
- `cloudbuild.yaml` - Google Cloud Build configuration
- `app.yaml` - Additional Cloud Run deployment settings
- `.dockerignore` - Optimizes Docker builds by excluding unnecessary files

### Local Development

Run the app locally:
```bash
streamlit run Hello.py
```

### Docker Deployment

Build and run with Docker:
```bash
docker build -t streamlit-app .
docker run -p 8080:8080 -e PORT=8080 streamlit-app
```

The app will be available at http://localhost:8080
