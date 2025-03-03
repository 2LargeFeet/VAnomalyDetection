# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables
ENV API_KEY=${API_KEY}
ENV REPO_URL="https://github.com/2LargeFeet/VAnomalyDetection.git"
ENV SCRIPT_PATH="/app/detectAnomaly.py"

# Install dependencies
RUN apt-get update && apt-get install -y git cron && rm -rf /var/lib/apt/lists/*
RUN pip3 install requests

# Set up the working directory
WORKDIR /app

# Clone the repo
RUN git clone $REPO_URL /app

# Add the script to cron (runs every 5 minutes)
# RUN echo "*/5 * * * * root cd /app && git pull && /usr/local/bin/python3 $SCRIPT_PATH" > /etc/cron.d/mycron \
#     && chmod 0644 /etc/cron.d/mycron \
#     && crontab /etc/cron.d/mycron
RUN $SCRIPT_PATH


# Start cron and keep container running
CMD ["cron", "-f"]
