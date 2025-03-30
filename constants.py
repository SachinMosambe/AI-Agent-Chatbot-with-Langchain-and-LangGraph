import os
# Load environment variables
HOST=os.environ.get("HOST")
BACKEND_PORT=int(os.environ.get("BACKEND_PORT", 8000))
FRONTEND_PORT=int(os.environ.get("FRONTEND_PORT", 8501))
