# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required port for Cloud Run (8080)
EXPOSE 8080

# Create a script to run both FastAPI (Gunicorn) and Streamlit
RUN echo '#!/bin/bash\n\
# Run FastAPI (Gunicorn with Uvicorn Worker) on port 8080\n\
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend:app --bind 0.0.0.0:8080 &\n\
# Run Streamlit on port 8501\n\
streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0\n' > /app/start.sh && chmod +x /app/start.sh

# Command to run the script
CMD ["bash", "/app/start.sh"]

