# Use Selenium prebuilt Chrome image
FROM selenium/standalone-chrome:latest

# Set working directory
WORKDIR /app

# Install Python 3 and pip
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all Selenium tests
COPY . .

# Run the main test suite
CMD ["pytest", "test_main.py"]
