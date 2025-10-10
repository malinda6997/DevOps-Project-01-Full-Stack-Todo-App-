#!/bin/bash

# Complete Todo App Deployment Script for EC2
# This script deploys the containerized applications with proper nginx configuration

echo "🚀 Starting Todo App Deployment..."

# Set variables
DOCKER_REGISTRY="malinda699"
IMAGE_TAG="latest"
APP_DIR="/opt/todo-app"

# Create application directory
sudo mkdir -p $APP_DIR
cd $APP_DIR

echo "📦 Pulling Docker images..."
# Pull latest images from Docker Hub
docker pull $DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG || {
    echo "❌ Failed to pull backend image. Please ensure the image exists on Docker Hub."
    echo "Build and push the image first:"
    echo "docker build -t $DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG ./backend"
    echo "docker push $DOCKER_REGISTRY/todo-app-backend:$IMAGE_TAG"
    exit 1
}

docker pull $DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG || {
    echo "❌ Failed to pull frontend image. Please ensure the image exists on Docker Hub."
    echo "Build and push the image first:"
    echo "docker build -t $DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG ./frontend"
    echo "docker push $DOCKER_REGISTRY/todo-app-frontend:$IMAGE_TAG"
    exit 1
}

echo "🛑 Stopping existing containers..."
# Stop and remove existing containers
docker-compose down 2>/dev/null || true
docker stop todo-nginx todo-backend todo-frontend 2>/dev/null || true
docker rm todo-nginx todo-backend todo-frontend 2>/dev/null || true

echo "📝 Creating docker-compose.yml..."
# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'

services:
  backend:
    image: ${DOCKER_REGISTRY}/todo-app-backend:${IMAGE_TAG}
    container_name: todo-backend
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
      - MONGO_URI=mongodb+srv://admin:nh7bcbRYQtHiHN0q@todo-devops-01.7dlpitt.mongodb.net/todoapp?retryWrites=true&w=majority&appName=Todo-devops-01
      - DATABASE_NAME=todoapp
      - COLLECTION_NAME=todos
      - HOST=0.0.0.0
      - PORT=5000
    ports:
      - "5000:5000"
    networks:
      - todo-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  frontend:
    image: ${DOCKER_REGISTRY}/todo-app-frontend:${IMAGE_TAG}
    container_name: todo-frontend
    restart: unless-stopped
    environment:
      - REACT_APP_API_URL=/api
      - NODE_ENV=production
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - todo-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  nginx:
    image: nginx:alpine
    container_name: todo-nginx
    restart: unless-stopped
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
      - frontend
    networks:
      - todo-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  todo-network:
    driver: bridge
    name: todo-network
EOF

echo "🔧 Creating nginx configuration..."
# Create nginx configuration
cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    # Basic Settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 10M;

    # Gzip Settings
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # Upstream Services
    upstream backend {
        server todo-backend:5000;
    }

    upstream frontend {
        server todo-frontend:3000;
    }

    # Main Server Block
    server {
        listen 80;
        server_name _;

        # Security Headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;

        # Health Check Endpoint
        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # API Routes
        location /api {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # CORS Headers for API
            add_header Access-Control-Allow-Origin "*" always;
            add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
            add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization" always;
            
            # Handle preflight requests
            if ($request_method = 'OPTIONS') {
                add_header Access-Control-Allow-Origin "*";
                add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS";
                add_header Access-Control-Allow-Headers "DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization";
                add_header Content-Length 0;
                add_header Content-Type text/plain;
                return 204;
            }
        }

        # Static Assets and Frontend
        location / {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Support for React Router
            proxy_intercept_errors on;
            error_page 404 = @fallback;
        }

        # Fallback for React Router
        location @fallback {
            proxy_pass http://frontend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}
EOF

echo "🚀 Starting containers..."
# Start the containers
docker-compose up -d

echo "⏳ Waiting for containers to be healthy..."
# Wait for containers to be healthy
sleep 30

echo "🔍 Checking container status..."
# Check container status
docker-compose ps

echo "🏥 Checking health status..."
# Check health status
for container in todo-nginx todo-backend todo-frontend; do
    health=$(docker inspect --format='{{.State.Health.Status}}' "$container" 2>/dev/null || echo "no-healthcheck")
    echo "$container: $health"
done

echo "🌐 Testing endpoints..."
# Test endpoints
echo "Testing nginx health endpoint..."
curl -f http://localhost/health || echo "❌ Nginx health check failed"

echo "Testing backend API..."
curl -f http://localhost/api/health || echo "❌ Backend API health check failed"

echo "Testing frontend..."
curl -f http://localhost/ -I || echo "❌ Frontend health check failed"

echo "📊 Application Status:"
echo "✅ Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/"
echo "✅ API: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)/api/health"
echo "✅ Load Balancer: http://todo-app-alb-1282445744.us-east-1.elb.amazonaws.com"

echo "🎉 Deployment completed!"
echo ""
echo "📋 Quick Commands:"
echo "- View logs: docker-compose logs -f"
echo "- Restart: docker-compose restart"
echo "- Stop: docker-compose down"
echo "- Status: docker-compose ps"
EOF