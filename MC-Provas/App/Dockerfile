# Use the official Python image with Alpine Linux
FROM python:3.9-alpine

# Install system dependencies, including default-libmysqlclient-dev
RUN apk update && apk add --no-cache mysql mysql-client mysql-dev build-base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 5000

# Command to run on container start
CMD ["python", "app.py"]
