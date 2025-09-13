FROM python:3.9-slim

WORKDIR /app/

# Install system dependencies
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ./requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY ./app /app/app/
COPY ./entrypoint.sh /app/

# Create data directory for SQLite
RUN mkdir -p /app/data

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
