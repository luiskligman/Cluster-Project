# Setup of head to worker relationship

* configure passwordless sudo for each node
```bash
cd ~
sudo visudo
# Password
# Add this at the bottom of the file
    # Allow passwordless sudo
    luis ALL=(ALL) NOPASSWD: ALL

sudo reboot now
```

* allow the head node to ssh into each worker without a password
```bash
# Generate SSH key if not already present
ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519

# Copy to all workers
for i in {101..104}; do
  ssh-copy-id luis@10.0.1.$i
done

# Test
for i in {101..104}; do
  ssh luis@10.0.1.$i "echo Worker $i responding"
done
```

* install the base software on all of the nodes 
```bash
#init.sh

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
```

* run init.sh on head then use head-worker_init.sh to scp files from head to workers and install base software on each worker
```bash
# head-worker_init.sh

#!/bin/bash

for i in {101..104}; do
  ssh luis@10.0.1.$i "mkdir -p ~/files/"
  scp ~/files/init.sh luis@10.0.1.$i:~/files/
  ssh luis@10.0.1.$i "bash ~/files/init.sh"
done
```

* now reboot each machine to allow changes to take place
```bash
# reboot.sh

#!/bin/bash
for i in {100..104}; do
        ssh luis@10.0.1.$i "sudo reboot now"
done
```

* install redis on head node only
```bash
# on head node
sudo apt install -y redis-server

# configure Redis to listen on all interfaces
sudo sed -i 's/bind 127.0.0.1/bind 0.0.0.0' /etc/redis/redis.conf

# restart redis
sudo systemctl restart redis-server

# verify it is running
redis-cli ping # should return PONG
```

