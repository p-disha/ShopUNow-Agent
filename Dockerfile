FROM python:3.11-slim

WORKDIR /app

# Install system deps if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app

# Must bind to all interfaces and use the Render provided $PORT
CMD ["sh", "-c", "python -m voila ShopUNow.ipynb --no-browser --VoilaApp.ip=0.0.0.0 --VoilaApp.port=${PORT}"]
