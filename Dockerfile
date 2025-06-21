# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port (Railway will set $PORT automatically)
EXPOSE 8000

# Copy start script and make it executable
COPY start.sh .
RUN chmod +x start.sh

# Run the application using the start script
CMD ["./start.sh"]