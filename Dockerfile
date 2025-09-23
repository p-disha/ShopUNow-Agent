# Base image with Python 3.11 slim
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps needed for building / packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install deps as root
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app

# Create a non-root user and give it ownership of /app
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (optional, for documentation)
EXPOSE 10000

# Run Voilà binding to host 0.0.0.0 and dynamic port
CMD ["sh", "-c", "python -m voila ShopUNow.ipynb --no-browser --VoilaApp.ip=0.0.0.0 --VoilaApp.port=${PORT:-8866}"]
