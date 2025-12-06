# Use Python 3.12 slim
FROM python:3.12-slim

# Install Chrome dependencies
RUN apt-get update && \
    apt-get install -y wget unzip gnupg curl xvfb && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && apt-get install -y /tmp/google-chrome.deb && \
    rm /tmp/google-chrome.deb

# Install ChromeDriver that matches Chrome version dynamically
RUN CHROME_MAJOR=$(google-chrome --version | grep -oP '\d+' | head -1) && \
    echo "Detected Chrome major version: $CHROME_MAJOR" && \
    LATEST=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAJOR) && \
    echo "Latest ChromeDriver version: $LATEST" && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Set display for headless mode
ENV DISPLAY=:99

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Selenium tests
COPY . .

# Run all tests via test_main.py
CMD ["python", "test/test_main.py"]
