FROM python:3.10-alpine

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Start the application
CMD ["flask", "run", "--host", "0.0.0.0"]
