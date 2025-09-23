# Use Python 3.11 slim base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for numpy, pandas, faiss)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the repo
COPY . /app

# Expose port (Render sets $PORT automatically)
EXPOSE 10000

# Run Voilà on the correct host and port
CMD ["sh", "-c", "python -m voila ShopUNow.ipynb --no-browser --VoilaApp.ip=0.0.0.0 --VoilaApp.port=${PORT}"]
