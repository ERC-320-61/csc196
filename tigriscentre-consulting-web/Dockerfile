# Use a Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y curl && apt-get clean

# Create the logs directory and set permissions
RUN mkdir -p /app/logs && chmod -R 755 /app/logs

# Copy the requirements file from the current directory (relative to Docker context)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source files into the container
# Adjust the relative path based on your current file structure
COPY . .

# Set environment variables for the container
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
