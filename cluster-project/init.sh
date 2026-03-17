#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y git vim htop btop wget neofetch build-essential \
  python3 python3-pip python3-venv redis-tools net-tools

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Check firewall and allow cluster traffic
sudo ufw allow from 10.0.1.0/24
sudo ufw status

echo "Setup complete on $(hostname)"

