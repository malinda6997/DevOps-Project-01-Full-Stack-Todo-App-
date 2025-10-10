# Docker Hub Setup Instructions

To complete your CI/CD pipeline, you need to set up Docker Hub repositories for your container images.

## Step 1: Create Docker Hub Account

If you don't have one already:

1. Go to https://hub.docker.com
2. Sign up for a free account
3. Verify your email

## Step 2: Create Repositories

You need to create two repositories:

### Repository 1: Backend API

1. Go to Docker Hub → Create Repository
2. Name: `todo-app-backend`
3. Visibility: Public (for free tier)
4. Description: "Todo App Flask Backend API"

### Repository 2: Frontend App

1. Go to Docker Hub → Create Repository
2. Name: `todo-app-frontend`
3. Visibility: Public (for free tier)
4. Description: "Todo App React Frontend"

## Step 3: Get Access Token

1. Go to Docker Hub → Account Settings → Security
2. Click "New Access Token"
3. Name: `jenkins-pipeline`
4. Permissions: Read, Write, Delete
5. Generate and save the token (you won't see it again!)

## Step 4: Update Jenkinsfile

Your current Jenkinsfile uses `DOCKER_REGISTRY = 'todoapp'`. You need to update this to your Docker Hub username.

For example, if your Docker Hub username is `yourusername`, change line in Jenkinsfile:

```groovy
DOCKER_REGISTRY = 'yourusername'  // Change this to your Docker Hub username
```

## Step 5: Configure Jenkins Credentials

When you set up Jenkins, add these credentials:

### Docker Hub Credentials

- Kind: Username with password
- ID: `docker-hub-credentials`
- Username: Your Docker Hub username
- Password: The access token from Step 3

## Step 6: Test Docker Build Locally

You can test building the images locally:

```bash
# Build backend
cd backend
docker build -t yourusername/todo-app-backend:test .

# Build frontend
cd ../frontend
docker build -t yourusername/todo-app-frontend:test .

# Test push (optional)
docker login
docker push yourusername/todo-app-backend:test
docker push yourusername/todo-app-frontend:test
```

## Your Repository URLs

After setup, your repositories will be:

- Backend: `https://hub.docker.com/r/yourusername/todo-app-backend`
- Frontend: `https://hub.docker.com/r/yourusername/todo-app-frontend`

## Alternative: AWS ECR

If you prefer using AWS ECR instead of Docker Hub:

```bash
# Create ECR repositories
aws ecr create-repository --repository-name todo-app-backend
aws ecr create-repository --repository-name todo-app-frontend

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 222634388891.dkr.ecr.us-east-1.amazonaws.com
```

## What's your Docker Hub username?

Once you provide your Docker Hub username, I can:

1. Update the Jenkinsfile with the correct registry
2. Provide exact repository URLs
3. Give you the exact commands to test locally

Please share your Docker Hub username so we can continue!
