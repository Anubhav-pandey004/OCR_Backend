# Base Python image
FROM python:3.13-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system packages including tesseract
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      tesseract-ocr \
      libtesseract-dev \
      build-essential \
      && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Environment variable for Render port
ENV PORT 10000

# Start Django with Gunicorn
CMD ["sh", "-c", "gunicorn ocr_backend.wsgi:application --bind 0.0.0.0:${PORT}"]
