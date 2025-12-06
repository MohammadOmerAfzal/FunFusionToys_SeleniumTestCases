FROM selenium/standalone-chrome:latest

USER root

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all tests
COPY test ./test

# Debug: verify test structure
RUN echo "=== DEBUG: contents of /app/test ===" && ls -R /app/test

# Default command: run all tests using pytest
CMD ["pytest", "/app/test", "--maxfail=1", "--disable-warnings", "-q"]
