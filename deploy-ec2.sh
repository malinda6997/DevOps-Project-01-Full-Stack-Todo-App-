#!/bin/bash

# EC2 Deployment Script for Todo App
# EC2 IP: 107.20.98.202

echo "🚀 Deploying Todo App to EC2..."

# Update system
echo "📦 Updating system packages..."
sudo yum update -y

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    sudo yum install -y docker
    sudo systemctl start docker
    sudo systemctl enable docker
    sudo usermod -a -G docker ec2-user
fi

# Install Docker Compose if not already installed
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Clone or update repository
REPO_DIR="/home/ec2-user/todo-app"
if [ -d "$REPO_DIR" ]; then
    echo "📥 Updating repository..."
    cd "$REPO_DIR"
    git pull
else
    echo "📥 Cloning repository..."
    git clone https://github.com/malinda6997/DevOps-Project-01-Full-Stack-Todo-App-.git "$REPO_DIR"
    cd "$REPO_DIR"
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f docker-compose.ec2.yml down

# Build and start containers
echo "🏗️  Building and starting containers..."
docker-compose -f docker-compose.ec2.yml up -d --build

# Show status
echo "✅ Deployment complete!"
echo ""
echo "📊 Container Status:"
docker-compose -f docker-compose.ec2.yml ps
echo ""
echo "🌐 Access your app at:"
echo "   Frontend: http://107.20.98.202:3001"
echo "   Backend API: http://107.20.98.202:5000/api"
echo "   Grafana: http://107.20.98.202:3000"
echo ""
echo "📝 View logs with:"
echo "   docker-compose -f docker-compose.ec2.yml logs -f"
