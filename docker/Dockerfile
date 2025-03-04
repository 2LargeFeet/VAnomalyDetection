# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables
ENV API_KEY=${API_KEY}
ENV REPO_URL="https://github.com/2LargeFeet/VAnomalyDetection.git"
ENV SCRIPT_PATH="/app/detectAnomaly.py"

# Install dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip3 install requests

# Set up the working directory
WORKDIR /app

# Clone the repo
RUN git clone $REPO_URL /app

# Run app
CMD [ "python", detectAnomaly.py ]
