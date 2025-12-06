FROM selenium/standalone-chrome:latest

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the test folder exactly as-is
COPY test ./test

# Debug: show the test structure
RUN echo "=== DEBUG: contents of /app/test ===" && ls -R /app/test

# Run your custom test suite
CMD ["python3", "test/test_main.py"]
