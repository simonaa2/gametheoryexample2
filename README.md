# Streamlit Demo App - Game Theory Example

This is a fully functional Streamlit application with multiple interactive demos including animations, data visualization, mapping and plotting examples.

## 🚀 Live Demo

You can view the live application at: [Streamlit Community Cloud](https://st-hello-app.streamlit.app/)

## 📋 Features

- **Animation Demo**: Interactive fractal animations based on the Julia Set
- **Plotting Demo**: Real-time data plotting with progress visualization  
- **Mapping Demo**: Geospatial data visualization using PyDeck
- **DataFrame Demo**: Data analysis and visualization with Altair charts

## 🛠️ Local Development

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/simonaa2/gametheoryexample2.git
cd gametheoryexample2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run Hello.py
```

The app will be available at `http://localhost:8501`

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - Free)

**Streamlit Community Cloud is the easiest and free way to deploy your app online.**

1. **Fork this repository** to your GitHub account
2. **Sign up** at [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account** 
4. **Deploy your app** by selecting your forked repository
5. **Set the main file** to `Hello.py`
6. Your app will be live at `https://[your-app-name].streamlit.app`

**Requirements for Streamlit Cloud:**
- ✅ Public GitHub repository
- ✅ `requirements.txt` file (included)
- ✅ Main Python file (`Hello.py`)

### Option 2: Heroku Deployment

1. **Install Heroku CLI** and create an account at [heroku.com](https://heroku.com)

2. **Login to Heroku:**
```bash
heroku login
```

3. **Create a new Heroku app:**
```bash
heroku create your-app-name
```

4. **Deploy to Heroku:**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

Your app will be available at `https://your-app-name.herokuapp.com`

### Option 3: Docker Deployment

1. **Create a Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Hello.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run:**
```bash
docker build -t streamlit-app .
docker run -p 8501:8501 streamlit-app
```

### Option 4: Other Cloud Platforms

- **Google Cloud Run**
- **AWS EC2 with Docker**
- **Azure Container Instances**
- **DigitalOcean App Platform**

## 📁 Project Structure

```
├── Hello.py                 # Main application file
├── requirements.txt         # Python dependencies
├── utils.py                # Utility functions
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── pages/                  # Multi-page app structure
│   ├── 0_Animation_Demo.py
│   ├── 1_Plotting_Demo.py
│   ├── 2_Mapping_Demo.py
│   └── 3_DataFrame_Demo.py
├── Procfile               # Heroku deployment config
└── setup.sh              # Heroku setup script
```

## 🔧 Configuration

The app includes configuration files for various deployment scenarios:

- `.streamlit/config.toml` - Streamlit-specific settings
- `Procfile` - Heroku deployment configuration
- `setup.sh` - Setup script for Heroku deployment

## 📖 Dependencies

- **streamlit**: Web app framework
- **numpy**: Numerical computing
- **pandas**: Data manipulation and analysis
- **altair**: Statistical visualization
- **pydeck**: WebGL-powered data visualization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `streamlit run Hello.py`
5. Submit a pull request

## 📄 License

Licensed under the Apache License, Version 2.0. See the original Streamlit license headers in the source files.

## 🆘 Troubleshooting

**Common Issues:**

1. **Import errors**: Make sure all dependencies are installed via `pip install -r requirements.txt`
2. **Port conflicts**: Change the port in `.streamlit/config.toml` if 8501 is occupied
3. **Permission errors**: On Unix systems, ensure `setup.sh` is executable: `chmod +x setup.sh`

**Need Help?**
- Check the [Streamlit Documentation](https://docs.streamlit.io)
- Visit [Streamlit Community Forum](https://discuss.streamlit.io)
- Review [Deployment Guide](https://docs.streamlit.io/streamlit-community-cloud)
