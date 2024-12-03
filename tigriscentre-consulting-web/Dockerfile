# Use a Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y curl && apt-get clean

# Create the logs directory and set permissions
RUN mkdir -p /app/logs && chmod -R 755 /app/logs

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files to the container
COPY . .

# Set environment variables (for secure configuration)
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
