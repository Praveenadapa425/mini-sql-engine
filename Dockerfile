# Use Python 3.7+ as base image
FROM python:3.7-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variable for Python path
ENV PYTHONPATH=/app

# Expose port for web application
EXPOSE 8000

# Default command to run the web application
CMD ["python", "-m", "src.web_app"]