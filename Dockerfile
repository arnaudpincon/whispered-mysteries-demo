# Dockerfile.standard
FROM python:3.13

WORKDIR /app

# Install additional dependencies if needed
RUN apt-get update && apt-get install -y \
ca-certificates \
openssl

# Update
RUN update-ca-certificates

# Update pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Install python-dotenv if necessary
RUN pip install python-dotenv

# Expose the Gradio port
EXPOSE 7860

# SSL environment variables
ENV SSL_CERT_DIR=/etc/ssl/certs
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# Start command
CMD ["python", "main.py"]