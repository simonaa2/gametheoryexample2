# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8080

# Set environment variables for Cloud Run
ENV PORT=8080

# Run the Streamlit app
CMD ["streamlit", "run", "Hello.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]