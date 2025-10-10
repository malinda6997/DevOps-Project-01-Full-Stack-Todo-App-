# Build and Push Docker Images to Docker Hub (PowerShell)
# Run this script locally to build and push your images

$DOCKER_REGISTRY = "malinda699"
$IMAGE_TAG = "latest"

Write-Host "🔐 Please login to Docker Hub first:" -ForegroundColor Yellow
Write-Host "docker login" -ForegroundColor Cyan
Write-Host "Enter your Docker Hub credentials when prompted" -ForegroundColor Yellow
Write-Host ""

$response = Read-Host "Have you logged into Docker Hub? (y/n)"
if ($response -ne "y" -and $response -ne "Y") {
    Write-Host "Please run 'docker login' first, then re-run this script" -ForegroundColor Red
    exit 1
}

Write-Host "🏗️ Building Docker images..." -ForegroundColor Green

# Build backend image
Write-Host "Building backend image..." -ForegroundColor Cyan
Set-Location backend
docker build -t "$DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG" .
docker tag "$DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG" "$DOCKER_REGISTRY/todo-app-backend:latest"

# Build frontend image  
Write-Host "Building frontend image..." -ForegroundColor Cyan
Set-Location ../frontend
docker build -t "$DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG" .
docker tag "$DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG" "$DOCKER_REGISTRY/todo-app-frontend:latest"

Write-Host "📤 Pushing images to Docker Hub..." -ForegroundColor Green

# Push backend image
Write-Host "Pushing backend image..." -ForegroundColor Cyan
docker push "$DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG"
docker push "$DOCKER_REGISTRY/todo-app-backend:latest"

# Push frontend image
Write-Host "Pushing frontend image..." -ForegroundColor Cyan
docker push "$DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG"
docker push "$DOCKER_REGISTRY/todo-app-frontend:latest"

Write-Host "✅ Images successfully built and pushed!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Your repositories:" -ForegroundColor Yellow
Write-Host "- Backend: https://hub.docker.com/r/$DOCKER_REGISTRY/todo-app-backend" -ForegroundColor Cyan
Write-Host "- Frontend: https://hub.docker.com/r/$DOCKER_REGISTRY/todo-app-frontend" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Now you can deploy to EC2 using the deploy-todo-app.sh script" -ForegroundColor Green

# Return to project root
Set-Location ..