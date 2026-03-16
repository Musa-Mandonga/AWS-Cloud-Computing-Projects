# Project 7: Containerized Django Application with ECR & ECS

## 🎯 Learning Objectives
By completing this project, you will:
- Understand containerization concepts and Docker
- Build and containerize a Django web application
- Use Amazon ECR (Elastic Container Registry) for image storage
- Deploy containers using Amazon ECS (Elastic Container Service)
- Learn about AWS Fargate for serverless containers
- Understand container orchestration and service management
- Implement load balancing for containerized applications

## 📋 Project Overview
This project demonstrates modern application deployment using containers. You'll containerize a Django application with Docker, store the image in ECR, and deploy it using ECS with Fargate for a fully managed containerized solution.

## 🏗️ Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Developer     │───▶│     Docker       │───▶│   Amazon ECR    │
│   (Local Dev)   │    │   (Build Image)  │    │ (Image Registry)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    Internet     │◀───│ Application Load │◀───│   Amazon ECS    │
│    (Users)      │    │    Balancer      │    │   (Fargate)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                         │
                                ▼                         ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Target Group   │    │  Django Tasks   │
                       │   (Health Check) │    │  (Containers)   │
                       └──────────────────┘    └─────────────────┘
```

## 🔧 AWS Services Used
- **Amazon ECR**: Managed Docker container registry
- **Amazon ECS**: Container orchestration service
- **AWS Fargate**: Serverless compute for containers
- **Application Load Balancer**: Distribute traffic to containers
- **VPC**: Network isolation and security
- **CloudWatch**: Container monitoring and logging

## 📝 Prerequisites
- Completed Projects 1-4
- Docker installed on local machine
- Basic understanding of Python/Django
- Familiarity with containerization concepts
- AWS CLI configured

## 🚀 Implementation Methods

### Method 1: Manual Setup (Recommended for Learning)

#### Step 1: Prepare Django Application
The project includes a simple Django application with the following structure:
```
mysite/
├── manage.py
├── settings.py
├── urls.py
└── wsgi.py
```

Review the application files:
- **settings.py**: Basic Django configuration
- **urls.py**: URL routing
- **wsgi.py**: WSGI application entry point

#### Step 2: Build and Test Docker Image Locally
```bash
# Navigate to project directory
cd project7_django_ecr_ecs

# Build Docker image
docker build -t django-app .

# Test locally
docker run -p 8000:8000 django-app

# Verify application works
curl http://localhost:8000
```

#### Step 3: Create ECR Repository
```bash
# Create ECR repository
aws ecr create-repository --repository-name django-app --region us-east-1

# Get login token and authenticate Docker
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

#### Step 4: Push Image to ECR
```bash
# Tag image for ECR
docker tag django-app:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/django-app:latest

# Push to ECR
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/django-app:latest
```

#### Step 5: Create ECS Cluster
1. Navigate to ECS Console
2. Create Cluster:
   - Name: `django-cluster`
   - Infrastructure: AWS Fargate (serverless)
3. Create cluster

#### Step 6: Create Task Definition
1. Go to "Task Definitions" → "Create new Task Definition"
2. Configuration:
   - Family: `django-task`
   - Launch type: Fargate
   - Operating system: Linux
   - CPU: 0.25 vCPU
   - Memory: 0.5 GB
3. Container Definition:
   - Name: `django-container`
   - Image: `<account-id>.dkr.ecr.us-east-1.amazonaws.com/django-app:latest`
   - Port mappings: 8000 (HTTP)
4. Create task definition

#### Step 7: Create ECS Service
1. From cluster, create service:
   - Launch type: Fargate
   - Task Definition: django-task
   - Service name: `django-service`
   - Number of tasks: 2
   - VPC: Use default or custom VPC from Project 4
   - Subnets: Public subnets
   - Security Group: Allow HTTP (port 8000) and ALB access
   - Auto-assign public IP: Enabled

#### Step 8: Create Application Load Balancer
1. Go to EC2 → Load Balancers → Create Load Balancer
2. Choose Application Load Balancer
3. Configuration:
   - Name: `django-alb`
   - Scheme: Internet-facing
   - IP address type: IPv4
   - VPC: Same as ECS service
   - Subnets: Public subnets in multiple AZs
4. Security Group: Allow HTTP (port 80)
5. Target Group:
   - Target type: IP
   - Protocol: HTTP
   - Port: 8000
   - Health check: HTTP /
6. Create load balancer

#### Step 9: Update ECS Service with Load Balancer
1. Update ECS service to use the load balancer
2. Attach target group to service
3. Verify healthy targets in target group

### Method 2: CloudFormation Template

```bash
# First, build and push image to ECR manually, then deploy infrastructure
aws cloudformation create-stack \
  --stack-name django-ecs-stack \
  --template-body file://project7_django_ecr_ecs.yaml \
  --parameters ParameterKey=ImageURI,ParameterValue=<account-id>.dkr.ecr.us-east-1.amazonaws.com/django-app:latest \
  --capabilities CAPABILITY_IAM
```

## 📁 Project Files

### `Dockerfile`
```dockerfile
# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Run Django app
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]
```

### `requirements.txt`
```
Django>=4.0
```

### `mysite/` Directory
Contains a simple Django application with:
- Basic Django project structure
- Simple URL routing
- Basic views and templates

### `aws_ui_instructions.txt`
Step-by-step AWS Console instructions for ECS setup.

### `project7_django_ecr_ecs.yaml`
CloudFormation template that creates:
- ECR repository
- ECS cluster with Fargate
- Task definition and service
- Application Load Balancer
- Security groups and networking

## 💰 Cost Estimation
- **ECR Storage**: $0.10 per GB/month
- **Fargate vCPU**: $0.04048 per vCPU/hour
- **Fargate Memory**: $0.004445 per GB/hour
- **ALB**: $0.0225 per hour + $0.008 per LCU-hour
- **Data Transfer**: First 1 GB free
- **Total Estimated Cost**: ~$15-25/month for 2 tasks running 24/7

## 🔍 Key Learning Points

### Containerization Benefits
- **Consistency**: Same environment across dev/test/prod
- **Scalability**: Easy horizontal scaling
- **Isolation**: Applications run in isolated environments
- **Portability**: Run anywhere Docker is supported

### Docker Fundamentals
- **Images**: Read-only templates for containers
- **Containers**: Running instances of images
- **Dockerfile**: Instructions to build images
- **Layers**: Images built in layers for efficiency

### Amazon ECR
- **Private Registry**: Secure container image storage
- **Integration**: Native integration with ECS/EKS
- **Vulnerability Scanning**: Built-in security scanning
- **Lifecycle Policies**: Automated image cleanup

### Amazon ECS Concepts
- **Clusters**: Logical grouping of compute resources
- **Tasks**: Running containers based on task definition
- **Services**: Maintain desired number of tasks
- **Task Definitions**: Blueprint for containers

### AWS Fargate
- **Serverless**: No EC2 instances to manage
- **Right-sizing**: Pay only for resources you use
- **Security**: Built-in isolation between tasks
- **Simplicity**: Focus on applications, not infrastructure

## 🧪 Testing & Validation

### Verification Steps
1. ✅ Docker image builds successfully
2. ✅ Image pushed to ECR repository
3. ✅ ECS cluster created with Fargate
4. ✅ Task definition created with correct configuration
5. ✅ ECS service running desired number of tasks
6. ✅ Load balancer distributing traffic to healthy targets
7. ✅ Application accessible via ALB DNS name

### Testing Commands
```bash
# Test local Docker build
docker build -t django-app .
docker run -p 8000:8000 django-app
curl http://localhost:8000

# Check ECR repository
aws ecr describe-repositories --repository-names django-app

# Check ECS cluster
aws ecs describe-clusters --clusters django-cluster

# Check running tasks
aws ecs list-tasks --cluster django-cluster

# Test load balancer
curl http://<alb-dns-name>

# Check logs
aws logs describe-log-groups
aws logs tail /ecs/django-task --follow
```

## 🚨 Troubleshooting

### Common Issues
1. **Docker build fails**
   - Check Dockerfile syntax
   - Verify base image availability
   - Ensure all files are in build context

2. **Cannot push to ECR**
   - Authenticate Docker with ECR
   - Check repository exists
   - Verify IAM permissions

3. **ECS tasks fail to start**
   - Check task definition CPU/memory limits
   - Verify image URI is correct
   - Check CloudWatch logs for errors

4. **Load balancer health checks fail**
   - Verify application responds on correct port
   - Check security group rules
   - Ensure health check path exists

5. **Tasks stop unexpectedly**
   - Check application logs in CloudWatch
   - Verify resource limits
   - Check for application crashes

### Debugging Tips
```bash
# Check task status
aws ecs describe-tasks --cluster django-cluster --tasks <task-id>

# View container logs
aws logs get-log-events --log-group-name /ecs/django-task --log-stream-name <stream-name>

# Check service events
aws ecs describe-services --cluster django-cluster --services django-service
```

## 🧹 Cleanup Instructions

### Manual Cleanup (in order)
1. Update ECS service desired count to 0
2. Delete ECS service
3. Delete load balancer
4. Delete target groups
5. Delete ECS cluster
6. Delete task definitions
7. Delete ECR repository (and images)
8. Delete CloudWatch log groups

### CloudFormation Cleanup
```bash
# Delete ECR images first (if not handled by template)
aws ecr batch-delete-image \
  --repository-name django-app \
  --image-ids imageTag=latest

# Delete stack
aws cloudformation delete-stack --stack-name django-ecs-stack
```

### Docker Cleanup
```bash
# Remove local images
docker rmi django-app
docker rmi <account-id>.dkr.ecr.us-east-1.amazonaws.com/django-app:latest

# Clean up Docker system
docker system prune -f
```

## 📚 Additional Resources
- [Docker Documentation](https://docs.docker.com/)
- [Amazon ECR User Guide](https://docs.aws.amazon.com/ecr/)
- [Amazon ECS Developer Guide](https://docs.aws.amazon.com/ecs/)
- [AWS Fargate User Guide](https://docs.aws.amazon.com/fargate/)
- [Django Documentation](https://docs.djangoproject.com/)

## 🔧 Advanced Concepts to Explore
- **Auto Scaling**: Scale containers based on metrics
- **Service Discovery**: Connect services using AWS Cloud Map
- **Secrets Management**: Use AWS Secrets Manager for sensitive data
- **Blue/Green Deployments**: Zero-downtime deployments
- **Container Insights**: Enhanced monitoring and observability

## 🔐 Security Best Practices
- **Least Privilege**: Minimal IAM permissions for tasks
- **Network Security**: Use private subnets when possible
- **Image Scanning**: Enable vulnerability scanning in ECR
- **Secrets**: Never hardcode credentials in images
- **Updates**: Regularly update base images and dependencies

## 📊 Monitoring and Logging
```bash
# Enable Container Insights
aws ecs put-cluster --cluster django-cluster --settings name=containerInsights,value=enabled

# View metrics in CloudWatch
# - CPU and memory utilization
# - Network I/O
# - Task and service metrics

# Structured logging
# Configure application to log in JSON format
# Use CloudWatch Logs Insights for analysis
```

## ➡️ Next Steps
After completing this project:
1. Proceed to [Project 8: Serverless API with Lambda](../project8_lambda_apigateway/)
2. Experiment with ECS auto scaling
3. Learn about EKS (Kubernetes on AWS)
4. Explore CI/CD pipelines with containers
5. Implement blue/green deployments

---
**🎓 Congratulations!** You've successfully containerized and deployed a Django application using modern AWS container services. You now understand container orchestration and can deploy scalable, containerized applications in the cloud.
