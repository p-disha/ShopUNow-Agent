# Use a slim Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install any OS-level dependencies needed by faiss etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libopenblas-dev \
        liblapack-dev \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all code (including .py file, JSON/FAQ files, etc.)
COPY . .

# (Optional) Convert notebook to Python if you still have .ipynb — safe fallback
RUN jupyter nbconvert --to python ShopUNow.ipynb || true

# Expose port (Gunicorn will bind here)
EXPOSE 8000

# Launch with Gunicorn
# Adjust module name (“shopunow”) and variable (“flask_app”) as per your .py file
CMD ["gunicorn", "shopunow:flask_app", "--bind", "0.0.0.0:8000", "--workers", "2"]
