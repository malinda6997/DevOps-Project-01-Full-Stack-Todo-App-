# EC2 Deployment Guide

## EC2 Server Details

- **IP Address:** 107.20.98.202
- **Deployment Method:** Docker Compose

## Prerequisites on EC2

1. Docker installed
2. Docker Compose installed
3. Security Group allows:
   - Port 3001 (Frontend - avoiding Grafana port 3000 conflict)
   - Port 5000 (Backend API)
   - Port 3000 (Grafana)
   - Port 22 (SSH)
   - Port 27017 (MongoDB - optional, only if external access needed)

## Quick Deploy

### Option 1: Automated Script

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@107.20.98.202

# Run deployment script
curl -o deploy.sh https://raw.githubusercontent.com/malinda6997/DevOps-Project-01-Full-Stack-Todo-App-/main/deploy-ec2.sh
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Manual Deployment

```bash
# SSH into EC2
ssh -i your-key.pem ec2-user@107.20.98.202

# Install Docker and Docker Compose
sudo yum update -y
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone repository
git clone https://github.com/malinda6997/DevOps-Project-01-Full-Stack-Todo-App-.git
cd DevOps-Project-01-Full-Stack-Todo-App-

# Deploy with EC2 config
docker-compose -f docker-compose.ec2.yml up -d --build
```

## Access Your Application

- **Frontend:** http://107.20.98.202:3001
- **Backend API:** http://107.20.98.202:5000/api
- **Health Check:** http://107.20.98.202:5000/api/health
- **Grafana:** http://107.20.98.202:3000 (if installed)

## Manage Deployment

### View Logs

```bash
docker-compose -f docker-compose.ec2.yml logs -f
```

### Restart Services

```bash
docker-compose -f docker-compose.ec2.yml restart
```

### Stop Services

```bash
docker-compose -f docker-compose.ec2.yml down
```

### Update and Redeploy

```bash
git pull
docker-compose -f docker-compose.ec2.yml up -d --build
```

## Troubleshooting

### Check Container Status

```bash
docker-compose -f docker-compose.ec2.yml ps
```

### Check Individual Container Logs

```bash
docker logs todo-mongodb
docker logs todo-backend
docker logs todo-frontend
```

### Test Backend Connection

```bash
curl http://107.20.98.202:5000/api/health
```

## Security Group Configuration

Ensure your EC2 security group allows:

| Type               | Protocol | Port  | Source       |
| ------------------ | -------- | ----- | ------------ |
| Custom TCP         | TCP      | 3001  | 0.0.0.0/0    |
| Custom TCP         | TCP      | 5000  | 0.0.0.0/0    |
| Custom TCP         | TCP      | 3000  | 0.0.0.0/0    |
| SSH                | TCP      | 22    | Your IP      |
| MongoDB (optional) | TCP      | 27017 | 127.0.0.1/32 |

## Environment Variables

The deployment uses:

- Frontend: `.env.production` with EC2 IP
- Backend: `backend/.env` with MongoDB Atlas or local MongoDB
- Docker Compose overrides MONGO_URI to use local MongoDB container

## Notes

- Frontend runs on port 3001 (mapped from container port 3000 to avoid Grafana conflict)
- Backend runs on port 5000
- Grafana runs on port 3000 (standard Grafana port)
- MongoDB runs on port 27017 (not exposed externally)
- All data persists in Docker volumes
