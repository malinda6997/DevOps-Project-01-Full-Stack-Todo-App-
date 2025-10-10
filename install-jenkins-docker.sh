#!/bin/bash

# EC2 Jenkins and Docker Installation Script
# Run this script on your EC2 instances via AWS Console Session Manager

echo "Starting Jenkins and Docker installation..."

# Update system
echo "Updating system packages..."
sudo yum update -y

# Install Docker
echo "Installing Docker..."
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Java 17 for Jenkins
echo "Installing Java 17..."
sudo yum install -y java-17-amazon-corretto-devel

# Add Jenkins repository and install
echo "Adding Jenkins repository..."
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key

echo "Installing Jenkins..."
sudo yum install -y jenkins

# Start and enable Jenkins
echo "Starting Jenkins service..."
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Install Docker Compose
echo "Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Wait for Jenkins to start
echo "Waiting for Jenkins to start..."
sleep 30

# Get Jenkins initial password
echo "============================================"
echo "Jenkins installation completed!"
echo "============================================"
echo "Jenkins URL: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8080"
echo ""
echo "Initial Admin Password:"
sudo cat /var/lib/jenkins/secrets/initialAdminPassword 2>/dev/null || echo "Password file not found - Jenkins may still be starting"
echo ""
echo "============================================"
echo "Next steps:"
echo "1. Access Jenkins at the URL above"
echo "2. Enter the initial admin password"
echo "3. Install suggested plugins"
echo "4. Create your admin user"
echo "============================================"

# Test Docker installation
echo "Testing Docker installation..."
docker --version
docker-compose --version

echo "Installation script completed!"
echo "Please check Jenkins access at the URL provided above."