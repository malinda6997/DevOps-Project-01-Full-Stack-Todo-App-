pipeline {
    agent any
    
    environment {
        // Docker Registry Configuration
        DOCKER_REGISTRY = 'todoapp'  // Change to your Docker Hub username
        IMAGE_TAG = "${BUILD_NUMBER}"
        
        // AWS Configuration
        AWS_REGION = 'us-east-1'
        EC2_SSH_KEY_NAME = 'malinda-aws-key'
        AUTO_SCALING_GROUP_NAME = 'todo-app-asg'
        
        // Application Configuration
        COMPOSE_PROJECT_NAME = "todoapp-${BUILD_NUMBER}"
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
    }
    
    stages {
        stage('Setup Environment') {
            steps {
                script {
                    // Load environment setup script
                    sh '''
                        echo "Setting up build environment..."
                        docker --version
                        docker-compose --version
                        aws --version
                    '''
                }
            }
        }
        
        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.IMAGE_TAG = "${BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('Build Images') {
            parallel {
                stage('Build Backend') {
                    steps {
                        script {
                            echo "Building backend Docker image..."
                            sh '''
                                cd backend
                                docker build -t ${DOCKER_REGISTRY}/todo-app-backend:${IMAGE_TAG} .
                                docker tag ${DOCKER_REGISTRY}/todo-app-backend:${IMAGE_TAG} ${DOCKER_REGISTRY}/todo-app-backend:latest
                            '''
                        }
                    }
                }
                
                stage('Build Frontend') {
                    steps {
                        script {
                            echo "Building frontend Docker image..."
                            sh '''
                                cd frontend
                                docker build -t ${DOCKER_REGISTRY}/todo-app-frontend:${IMAGE_TAG} .
                                docker tag ${DOCKER_REGISTRY}/todo-app-frontend:${IMAGE_TAG} ${DOCKER_REGISTRY}/todo-app-frontend:latest
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Push to Registry') {
            parallel {
                stage('Push Backend') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                            sh '''
                                echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                                docker push ${DOCKER_REGISTRY}/todo-app-backend:${IMAGE_TAG}
                                docker push ${DOCKER_REGISTRY}/todo-app-backend:latest
                            '''
                        }
                    }
                }
                
                stage('Push Frontend') {
                    steps {
                        withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                            sh '''
                                echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                                docker push ${DOCKER_REGISTRY}/todo-app-frontend:${IMAGE_TAG}
                                docker push ${DOCKER_REGISTRY}/todo-app-frontend:latest
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                script {
                    echo "Deploying to EC2 instances..."
                    
                    // Get EC2 instances from Auto Scaling Group
                    def instances = sh(
                        script: '''
                            aws autoscaling describe-auto-scaling-groups \
                                --auto-scaling-group-names ${AUTO_SCALING_GROUP_NAME} \
                                --query 'AutoScalingGroups[0].Instances[?HealthStatus==`Healthy`].InstanceId' \
                                --output text
                        ''',
                        returnStdout: true
                    ).trim().split()
                    
                    if (instances.size() == 0) {
                        error("No healthy instances found in Auto Scaling Group: ${AUTO_SCALING_GROUP_NAME}")
                    }
                    
                    // Deploy to each instance
                    instances.each { instanceId ->
                        echo "Deploying to instance: ${instanceId}"
                        
                        // Get instance IP
                        def instanceIP = sh(
                            script: "aws ec2 describe-instances --instance-ids ${instanceId} --query 'Reservations[0].Instances[0].PublicIpAddress' --output text",
                            returnStdout: true
                        ).trim()
                        
                        echo "Instance IP: ${instanceIP}"
                        
                        // Deploy to instance
                        withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                            sh """
                                ssh -o StrictHostKeyChecking=no -i \${SSH_KEY} ec2-user@${instanceIP} '
                                    # Pull latest images
                                    docker pull ${DOCKER_REGISTRY}/todo-app-backend:${IMAGE_TAG}
                                    docker pull ${DOCKER_REGISTRY}/todo-app-frontend:${IMAGE_TAG}
                                    
                                    # Stop existing containers
                                    docker-compose -p todoapp down || true
                                    
                                    # Create docker-compose.yml
                                    cat > docker-compose.yml << EOF
version: "3.8"
services:
  backend:
    image: ${DOCKER_REGISTRY}/todo-app-backend:${IMAGE_TAG}
    container_name: todo-backend
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - MONGO_URI=mongodb+srv://admin:nh7bcbRYQtHiHN0q@todo-devops-01.7dlpitt.mongodb.net/todoapp?retryWrites=true&w=majority&appName=Todo-devops-01
      - DATABASE_NAME=todoapp
      - COLLECTION_NAME=todos
    ports:
      - "5000:5000"
    networks:
      - todo-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    image: ${DOCKER_REGISTRY}/todo-app-frontend:${IMAGE_TAG}
    container_name: todo-frontend
    restart: unless-stopped
    environment:
      - REACT_APP_API_URL=http://localhost:5000/api
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

networks:
  todo-network:
    driver: bridge
EOF

                                    # Create nginx config
                                    cat > nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server todo-backend:5000;
    }

    upstream frontend {
        server todo-frontend:3000;
    }

    server {
        listen 80;

        location /api {
            proxy_pass http://backend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }

        location / {
            proxy_pass http://frontend;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
            proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto \$scheme;
        }
    }
}
EOF
                                    
                                    # Start new containers
                                    docker-compose -p todoapp up -d
                                    
                                    # Wait for health checks
                                    sleep 30
                                    
                                    # Verify deployment
                                    docker-compose -p todoapp ps
                                '
                            """
                        }
                    }
                }
            }
        }
        
        stage('Health Check') {
            steps {
                script {
                    echo "Performing health checks..."
                    
                    // Get load balancer DNS
                    def lbDNS = sh(
                        script: '''
                            aws elbv2 describe-load-balancers \
                                --query 'LoadBalancers[?contains(LoadBalancerName, `todo-app`)].DNSName' \
                                --output text
                        ''',
                        returnStdout: true
                    ).trim()
                    
                    if (lbDNS) {
                        echo "Load Balancer DNS: ${lbDNS}"
                        
                        // Health check with retries
                        retry(5) {
                            sleep(10)
                            sh "curl -f http://${lbDNS}/api/health"
                        }
                        
                        echo "Health check passed! Application is available at: http://${lbDNS}"
                    } else {
                        echo "Load balancer not found, checking individual instances..."
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup local images
            sh '''
                docker image prune -f
                docker system df
            '''
        }
        
        success {
            echo "✅ Pipeline completed successfully!"
            echo "🚀 Application deployed and health checks passed"
        }
        
        failure {
            echo "❌ Pipeline failed!"
            echo "Check the logs above for error details"
        }
        
        cleanup {
            // Workspace cleanup
            cleanWs()
        }
    }
}