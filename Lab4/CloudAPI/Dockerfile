# Use the official Python image from the DockerHub
FROM python:3.12-slim

# Set environment variables to prevent Python from writing .pyc files and for buffer output directly
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the Docker image
COPY . /code/

# Expose the port the app will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]