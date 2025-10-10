#!/bin/bash

# Build and Push Docker Images to Docker Hub
# Run this script locally to build and push your images

set -e

DOCKER_REGISTRY="malinda699"
IMAGE_TAG="latest"

echo "🔐 Please login to Docker Hub first:"
echo "docker login"
echo "Enter your Docker Hub credentials when prompted"
echo ""

read -p "Have you logged into Docker Hub? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Please run 'docker login' first, then re-run this script"
    exit 1
fi

echo "🏗️ Building Docker images..."

# Build backend image
echo "Building backend image..."
cd backend
docker build -t $DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG .
docker tag $DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG $DOCKER_REGISTRY/todo-app-backend:latest

# Build frontend image  
echo "Building frontend image..."
cd ../frontend
docker build -t $DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG .
docker tag $DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG $DOCKER_REGISTRY/todo-app-frontend:latest

echo "📤 Pushing images to Docker Hub..."

# Push backend image
echo "Pushing backend image..."
docker push $DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG
docker push $DOCKER_REGISTRY/todo-app-backend:latest

# Push frontend image
echo "Pushing frontend image..."
docker push $DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG
docker push $DOCKER_REGISTRY/todo-app-frontend:latest

echo "✅ Images successfully built and pushed!"
echo ""
echo "📦 Your repositories:"
echo "- Backend: https://hub.docker.com/r/$DOCKER_REGISTRY/todo-app-backend"
echo "- Frontend: https://hub.docker.com/r/$DOCKER_REGISTRY/todo-app-frontend"
echo ""
echo "🚀 Now you can deploy to EC2 using the deploy-todo-app.sh script"