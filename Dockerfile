FROM selenium/standalone-chrome:latest

USER root

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy test files
COPY test ./test

# Verify test structure
RUN echo "=== Test files ===" && ls -la /app/test

# Run tests with pytest
CMD ["pytest", "/app/test", "--maxfail=1", "--disable-warnings", "-v"]
