#!/bin/bash
echo "Installing secure-communications..."

# Move to appropriate directory
sudo mkdir -p /var/www/secure-communications
sudo chown $USER:$USER /var/www/secure-communications
cd /var/www/secure-communications

# Clone the repository
git clone https://github.com/ParaCryptid/secure-communications.git .

# Install dependencies
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
elif [ -f "package.json" ]; then
    npm install
fi

# Create systemd service file
sudo bash -c 'cat <<EOF > /etc/systemd/system/secure-communications.service
[Unit]
Description=secure-communications Service
After=network.target

[Service]
ExecStart=/var/www/secure-communications/start.sh
Restart=always
User=$USER
WorkingDirectory=/var/www/secure-communications

[Install]
WantedBy=multi-user.target
EOF'

# Enable and start service
sudo systemctl enable secure-communications.service
sudo systemctl start secure-communications.service

echo "secure-communications installed and running!"
