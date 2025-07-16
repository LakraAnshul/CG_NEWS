# Use Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy your code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run your app
CMD ["python", "main.py"]
