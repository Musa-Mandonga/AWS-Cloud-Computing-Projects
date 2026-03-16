# Project 3: AWS CLI Installation & S3 Operations

## 🎯 Learning Objectives
By completing this project, you will:
- Install and configure AWS CLI (Command Line Interface)
- Understand AWS credentials and profiles
- Create and manage S3 buckets programmatically
- Perform basic S3 operations (upload, download, list, delete)
- Learn S3 bucket policies and access controls
- Understand the difference between console and programmatic access

## 📋 Project Overview
This project introduces you to AWS CLI and Amazon S3 (Simple Storage Service). You'll learn how to interact with AWS services programmatically and manage object storage in the cloud.

## 🏗️ Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Local Machine │───▶│    AWS CLI       │───▶│   Amazon S3     │
│   (Your Computer)    │   (Configured)   │    │   (Buckets)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌──────────────────┐    ┌─────────────────┐
         └─────────────▶│  IAM Credentials │    │  S3 Objects     │
                        │  (Access Keys)   │    │  (Files)        │
                        └──────────────────┘    └─────────────────┘
```

## 🔧 AWS Services Used
- **Amazon S3**: Object storage service
- **IAM**: For access credentials and policies
- **CloudFormation**: Infrastructure as Code deployment

## 📝 Prerequisites
- Completed Project 2 (IAM setup)
- Computer with command line access (Windows, macOS, or Linux)
- Python 3.6+ (recommended for AWS CLI v2)
- IAM user with programmatic access

## 🚀 Implementation Methods

### Method 1: Manual Setup (Recommended for Learning)

#### Step 1: Install AWS CLI
```bash
# Windows (using installer)
# Download from: https://awscli.amazonaws.com/AWSCLIV2.msi

# macOS
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Verify installation
aws --version
```

#### Step 2: Configure AWS CLI
```bash
# Configure with your IAM user credentials
aws configure

# You'll be prompted for:
# AWS Access Key ID: [Your access key]
# AWS Secret Access Key: [Your secret key]
# Default region name: us-east-1
# Default output format: json
```

#### Step 3: Create S3 Bucket via AWS Console
1. Navigate to S3 service in AWS Console
2. Click "Create bucket"
3. Bucket name: `my-learning-bucket-[random-suffix]`
4. Choose region (e.g., us-east-1)
5. Configure settings (keep defaults for learning)
6. Create bucket

#### Step 4: S3 Operations via CLI
```bash
# List all buckets
aws s3 ls

# Create a test file
echo "Hello AWS CLI!" > test-file.txt

# Upload file to S3
aws s3 cp test-file.txt s3://my-learning-bucket-[suffix]/

# List objects in bucket
aws s3 ls s3://my-learning-bucket-[suffix]/

# Download file from S3
aws s3 cp s3://my-learning-bucket-[suffix]/test-file.txt downloaded-file.txt

# Delete object
aws s3 rm s3://my-learning-bucket-[suffix]/test-file.txt

# Sync directory to S3
mkdir test-directory
echo "File 1" > test-directory/file1.txt
echo "File 2" > test-directory/file2.txt
aws s3 sync test-directory/ s3://my-learning-bucket-[suffix]/test-folder/
```

### Method 2: CloudFormation Template

```bash
# Create S3 bucket using CloudFormation
aws cloudformation create-stack \
  --stack-name s3-learning-stack \
  --template-body file://project3_install_aws_cli_and_s3_api.yaml \
  --parameters ParameterKey=BucketName,ParameterValue=my-cf-bucket-$(date +%s)
```

## 📁 Project Files

### `aws_ui_instructions3.txt`
Step-by-step instructions for AWS Console S3 operations.

### `project3_install_aws_cli_and_s3_api.yaml`
CloudFormation template that creates:
- S3 bucket with proper configuration
- Bucket policy for secure access
- Output values for reference

## 💰 Cost Estimation
- **S3 Storage**: $0.023 per GB/month (Standard)
- **S3 Requests**: $0.0004 per 1,000 PUT requests
- **Data Transfer**: Free for first 1 GB out per month
- **Total Estimated Cost**: <$1/month for learning purposes

## 🔍 Key Learning Points

### AWS CLI Fundamentals
- **Profiles**: Manage multiple sets of credentials
- **Regions**: Different geographic locations for resources
- **Output Formats**: JSON, table, text
- **Configuration Files**: Located in ~/.aws/

### S3 Concepts
- **Buckets**: Containers for objects (globally unique names)
- **Objects**: Files stored in buckets (up to 5TB each)
- **Keys**: Object names/paths within buckets
- **Storage Classes**: Different cost/performance tiers

### S3 Security
- **Bucket Policies**: JSON policies for bucket-level access
- **ACLs**: Access Control Lists for object-level permissions
- **Encryption**: Data protection at rest and in transit
- **Versioning**: Keep multiple versions of objects

## 🧪 Testing & Validation

### Verification Steps
1. ✅ AWS CLI installed and configured
2. ✅ Can list S3 buckets using CLI
3. ✅ Successfully upload files to S3
4. ✅ Successfully download files from S3
5. ✅ Can delete objects and manage bucket contents
6. ✅ Understand S3 pricing and storage classes

### CLI Command Tests
```bash
# Test AWS CLI configuration
aws sts get-caller-identity

# Test S3 access
aws s3 ls

# Test file operations
aws s3 cp --help
aws s3 sync --help

# Check AWS CLI configuration
aws configure list
```

## 🚨 Troubleshooting

### Common Issues
1. **AWS CLI not found**
   - Check installation path
   - Restart terminal/command prompt
   - Verify Python installation

2. **Access denied errors**
   - Check IAM user permissions
   - Verify access keys are correct
   - Ensure S3 permissions are granted

3. **Bucket name already exists**
   - S3 bucket names must be globally unique
   - Add random suffix or timestamp
   - Check bucket naming conventions

4. **Region mismatch**
   - Ensure CLI region matches bucket region
   - Use --region flag to override

### Best Practices
- Never commit AWS credentials to version control
- Use IAM roles instead of access keys when possible
- Enable MFA for sensitive operations
- Regularly rotate access keys

## 🧹 Cleanup Instructions

### Manual Cleanup
```bash
# Delete all objects in bucket
aws s3 rm s3://my-learning-bucket-[suffix] --recursive

# Delete bucket
aws s3 rb s3://my-learning-bucket-[suffix]

# Remove local test files
rm test-file.txt downloaded-file.txt
rm -rf test-directory/
```

### CloudFormation Cleanup
```bash
# Empty bucket first (CloudFormation can't delete non-empty buckets)
aws s3 rm s3://[bucket-name] --recursive

# Delete stack
aws cloudformation delete-stack --stack-name s3-learning-stack
```

## 📚 Additional Resources
- [AWS CLI User Guide](https://docs.aws.amazon.com/cli/latest/userguide/)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/s3/latest/userguide/)
- [S3 Pricing](https://aws.amazon.com/s3/pricing/)
- [S3 Best Practices](https://docs.aws.amazon.com/s3/latest/userguide/best-practices.html)

## 🔧 Advanced CLI Operations
```bash
# Create multiple profiles
aws configure --profile development
aws configure --profile production

# Use specific profile
aws s3 ls --profile development

# Set environment variables
export AWS_PROFILE=development
export AWS_DEFAULT_REGION=us-west-2

# Batch operations
aws s3 cp . s3://my-bucket/ --recursive --exclude "*.tmp"

# Presigned URLs (temporary access)
aws s3 presign s3://my-bucket/file.txt --expires-in 3600
```

## 🔐 Security Best Practices
- **Principle of Least Privilege**: Only grant necessary S3 permissions
- **Bucket Policies**: Use for fine-grained access control
- **Encryption**: Enable server-side encryption
- **Access Logging**: Monitor bucket access
- **MFA Delete**: Require MFA for object deletion

## ➡️ Next Steps
After completing this project:
1. Proceed to [Project 4: Custom VPC & EC2 Web App](../project4_custom_vpc_ec2_webapp/)
2. Explore S3 advanced features (lifecycle policies, cross-region replication)
3. Learn about S3 storage classes and cost optimization
4. Practice with AWS SDK in your preferred programming language

---
**🎓 Congratulations!** You've successfully mastered AWS CLI and S3 fundamentals. You can now interact with AWS services programmatically and manage cloud storage efficiently.
