# Use official Python base image
FROM python:3.10-slim

# Install system dependencies (Chrome + ChromeDriver)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set display for headless Chrome
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Flask app port
EXPOSE 5000

# Run Flask app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
