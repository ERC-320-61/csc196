# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Set environment variables (if necessary)
ENV PYTHONUNBUFFERED=1

# Expose the port your app will run on
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
