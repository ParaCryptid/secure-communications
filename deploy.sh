#!/bin/bash
echo "Deploying secure-communications..."

# Navigate to the repository directory
cd /var/www/secure-communications

# Pull latest changes
git pull origin main

# Install dependencies (modify as per project needs)
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "package.json" ]; then
    npm install
fi

# Restart service (modify based on actual setup)
sudo systemctl restart secure-communications.service

echo "secure-communications deployed successfully!"
