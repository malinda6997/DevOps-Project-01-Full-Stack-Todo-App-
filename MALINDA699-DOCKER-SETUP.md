# Docker Hub Setup for malinda699

## ✅ Your Docker Hub Configuration

Your Docker Hub username: **malinda699**

## 📦 Required Repositories

You need to create these two repositories on Docker Hub:

### 1. Backend Repository

- **Name**: `todo-app-backend`
- **Full Name**: `malinda699/todo-app-backend`
- **URL**: https://hub.docker.com/r/malinda699/todo-app-backend

### 2. Frontend Repository

- **Name**: `todo-app-frontend`
- **Full Name**: `malinda699/todo-app-frontend`
- **URL**: https://hub.docker.com/r/malinda699/todo-app-frontend

## 🔑 Setup Steps

### Step 1: Create Repositories

1. Go to https://hub.docker.com
2. Sign in with username: `malinda699`
3. Click "Create Repository"
4. Create `todo-app-backend` (Public)
5. Create `todo-app-frontend` (Public)

### Step 2: Get Access Token

1. Go to Account Settings → Security
2. Click "New Access Token"
3. Name: `jenkins-ci-cd`
4. Permissions: Read, Write, Delete
5. **Save the token** - you'll need it for Jenkins!

### Step 3: Test Local Build (Optional)

```bash
# Test building and pushing images
cd "D:\DEVOPS PRACTICES\Devops-Project-01\backend"
docker build -t malinda699/todo-app-backend:test .

cd "../frontend"
docker build -t malinda699/todo-app-frontend:test .

# Login and push (optional test)
docker login
docker push malinda699/todo-app-backend:test
docker push malinda699/todo-app-frontend:test
```

## 🔧 Jenkins Credentials Setup

When you configure Jenkins, add these credentials:

**Credential Type**: Username with password

- **ID**: `docker-hub-credentials`
- **Username**: `malinda699`
- **Password**: [Your access token from Step 2]
- **Description**: Docker Hub Credentials for CI/CD

## ✅ Jenkinsfile Updated

I've already updated your Jenkinsfile to use `malinda699` as the Docker registry.

## 🚀 Ready for Pipeline!

After you:

1. ✅ Create the Docker Hub repositories
2. ✅ Install Jenkins on EC2 (using the script)
3. ✅ Configure Jenkins credentials

Your CI/CD pipeline will automatically:

- Build Docker images tagged as `malinda699/todo-app-backend:BUILD_NUMBER`
- Push to your Docker Hub repositories
- Deploy to your EC2 instances
- Run health checks

## 📞 Current Status

- ✅ **Jenkinsfile**: Updated with malinda699
- ✅ **Installation Script**: Ready for EC2
- ⏳ **Docker Hub**: Need to create repositories
- ⏳ **Jenkins**: Need to install on EC2

**Next Action**: Create the Docker Hub repositories, then we'll install Jenkins!
