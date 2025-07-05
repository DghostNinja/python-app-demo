# Dockerfile for FauxMart - lightweight and production-friendly
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN apk add --no-cache gcc musl-dev libffi-dev sqlite && \
    pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
