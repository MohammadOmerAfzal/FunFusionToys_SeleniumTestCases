FROM selenium/standalone-chrome:latest

USER root

# Install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all tests
COPY test ./test

# Debug: verify test structure
RUN echo "=== DEBUG: contents of /app/test ===" && ls -R /app/test

# Create startup script with connection verification
RUN echo '#!/bin/bash\n\
echo "=== Verifying Selenium connection ==="\n\
for i in $(seq 1 30); do\n\
  if curl -s http://selenium-node-ci:4444/status > /dev/null 2>&1; then\n\
    echo "✓ Connected to Selenium Grid"\n\
    break\n\
  fi\n\
  echo "Waiting for Selenium... ($i/30)"\n\
  sleep 2\n\
done\n\
\n\
echo "=== Running pytest ==="\n\
pytest /app/test --maxfail=1 --disable-warnings -v\n\
' > /app/run_tests.sh && chmod +x /app/run_tests.sh

CMD ["/app/run_tests.sh"]
