# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Set environment variable for port
ENV PORT=8080

# Expose the port
EXPOSE $PORT

# Set the command to run the Streamlit app using the startup script
CMD ["./start.sh"]