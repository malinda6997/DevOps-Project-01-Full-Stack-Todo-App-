# Manual EC2 Setup Instructions

Since your AWS infrastructure is working (load balancer URL: http://todo-app-alb-1282445744.us-east-1.elb.amazonaws.com), let's manually set up Jenkins and Docker on your EC2 instances.

## Current Status

✅ AWS Infrastructure: DEPLOYED
✅ Load Balancer: WORKING
✅ EC2 Instances: RUNNING (2 instances)
❌ Jenkins: NOT INSTALLED
❌ Docker: NOT INSTALLED

## EC2 Instance IPs

- Instance 1: 34.201.17.2
- Instance 2: 98.84.45.83

## Step 1: Connect to EC2 Instances

You'll need to SSH into each instance. If you don't have the SSH key locally, you can:

### Option A: Use AWS Console

1. Go to AWS Console → EC2 → Instances
2. Select your instance
3. Click "Connect" → "Session Manager"

### Option B: Download SSH Key

1. AWS Console → EC2 → Key Pairs
2. Find "malinda-aws-key"
3. Download the .pem file

## Step 2: Install Jenkins and Docker

Once connected to each instance, run these commands:

```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user

# Install Java for Jenkins
sudo yum install -y java-17-amazon-corretto-devel

# Install Jenkins
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo yum install -y jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins

# Get Jenkins initial password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

## Step 3: Access Jenkins

After installation, you can access Jenkins at:

- Instance 1: http://34.201.17.2:8080
- Instance 2: http://98.84.45.83:8080

## Step 4: Configure Jenkins

1. Enter the initial admin password from the command above
2. Install suggested plugins
3. Create your first admin user
4. Install additional plugins:
   - Git
   - Docker Pipeline
   - Blue Ocean
   - AWS Credentials
   - SSH Agent

## Alternative: Automated Setup

You can also run our automated setup script:

```bash
curl -fsSL https://raw.githubusercontent.com/malinda6997/DevOps-Project-01-Full-Stack-Todo-App-/main/scripts/setup-ec2.sh | bash
```

## Next Steps After Setup

1. Configure Jenkins credentials:

   - Docker Hub credentials
   - AWS credentials
   - SSH key for EC2 access

2. Create Jenkins pipeline job using our Jenkinsfile

3. Test the complete CI/CD pipeline

Would you like me to help you with any of these steps?
