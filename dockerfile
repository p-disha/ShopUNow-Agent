FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["sh", "-c", "python -m voila ShopUNow.ipynb --no-browser --VoilaApp.ip=0.0.0.0 --VoilaApp.port=${PORT}"]
