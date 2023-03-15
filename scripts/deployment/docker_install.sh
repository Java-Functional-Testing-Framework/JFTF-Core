#!/bin/bash
# ©2023 JFTF
# JFTF Ubuntu 22.04 docker installation script
# Usage
# sudo ./docker_install.sh
# Version 1.0

if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root!"
  exit
fi

# Update the package index
sudo apt-get update

# Install the required packages to use the Docker repository over HTTPS
sudo apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add the Docker repository to APT sources
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the package index (again)
sudo apt-get update

# Install Docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Verify that Docker is installed correctly
sudo docker run hello-world
