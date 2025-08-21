FROM python:3.10-slim

# Install Chrome + Driver
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:99

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Nhost sets PORT automatically
CMD gunicorn -w 1 -t 120 -b 0.0.0.0:$PORT app:app
