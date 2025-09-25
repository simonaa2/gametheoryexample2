# 🚀 Quick Start - Deploy to Google Cloud

Get your Streamlit app running on Google Cloud in just a few minutes!

## ⚡ Fastest Deploy (App Engine)

1. **Install Google Cloud SDK**
   ```bash
   # On macOS
   brew install google-cloud-sdk
   
   # On Windows
   # Download from: https://cloud.google.com/sdk/docs/install
   
   # On Linux
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

2. **Setup Google Cloud**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud app create --region=us-central1
   ```

3. **Deploy**
   ```bash
   ./deploy.sh
   ```

That's it! Your app will be live at `https://YOUR_PROJECT_ID.appspot.com`

## 🐳 Deploy with Docker (Cloud Run)

If you prefer containers:

```bash
./deploy-cloud-run.sh
```

## 🧪 Test Locally First

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run Hello.py

# Or test with our entry point
python main.py
```

## 📋 Prerequisites Checklist

- [ ] Google Cloud account created
- [ ] Project created in Google Cloud Console
- [ ] Billing enabled for your project
- [ ] Google Cloud SDK installed
- [ ] Authenticated with `gcloud auth login`

## 💡 Pro Tips

- **First time?** Use App Engine (easier setup)
- **Need more control?** Use Cloud Run (Docker-based)
- **Production app?** Consider using custom domains and HTTPS
- **Multiple environments?** Set up separate projects for dev/staging/prod

## 🆘 Need Help?

- Check our detailed [DEPLOYMENT.md](DEPLOYMENT.md) guide
- Run `python test_app.py` to verify your setup
- View logs: `gcloud app logs tail -s default`

## 💰 Costs

- **App Engine**: ~$0-20/month for small apps (has free tier)
- **Cloud Run**: ~$0-10/month for small apps (generous free tier)

Both options scale to zero when not in use! 🎉