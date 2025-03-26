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

# Expose ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Create a script to run both FastAPI and Streamlit
RUN echo '#!/bin/bash\n\
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend:app --bind 0.0.0.0:8000 &\n\
streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0\n' > /app/start.sh && chmod +x /app/start.sh

# Command to run the script
CMD ["bash", "/app/start.sh"]


# Command to run the script
CMD ["bash", "/app/start.sh"]
