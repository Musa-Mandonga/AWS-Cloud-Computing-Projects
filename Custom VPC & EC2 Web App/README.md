# Project 4: Custom VPC & EC2 Web Application

## 🎯 Learning Objectives
By completing this project, you will:
- Design and create a custom Virtual Private Cloud (VPC)
- Understand networking concepts: subnets, route tables, gateways
- Configure security groups and Network ACLs (NACLs)
- Launch EC2 instances in a custom network environment
- Deploy a simple web application on EC2
- Learn the difference between public and private subnets
- Understand AWS networking security layers

## 📋 Project Overview
This project teaches you AWS networking fundamentals by building a custom VPC from scratch. You'll create public and private subnets, configure routing, set up security controls, and deploy a web application on an EC2 instance.

## 🏗️ Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                          Custom VPC                             │
│                        (10.0.0.0/16)                           │
│  ┌─────────────────────────────┐  ┌─────────────────────────────┐ │
│  │       Public Subnet         │  │      Private Subnet         │ │
│  │      (10.0.1.0/24)         │  │      (10.0.2.0/24)         │ │
│  │  ┌─────────────────────┐   │  │  ┌─────────────────────┐   │ │
│  │  │    EC2 Instance     │   │  │  │    EC2 Instance     │   │ │
│  │  │   (Web Server)      │   │  │  │   (Database)        │   │ │
│  │  └─────────────────────┘   │  │  └─────────────────────┘   │ │
│  └─────────────────────────────┘  └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Internet Gateway   │
                    └─────────────────────┘
                              │
                              ▼
                         [ Internet ]
```

## 🔧 AWS Services Used
- **VPC (Virtual Private Cloud)**: Isolated network environment
- **EC2 (Elastic Compute Cloud)**: Virtual servers
- **Security Groups**: Instance-level firewall
- **Network ACLs**: Subnet-level firewall
- **Internet Gateway**: Internet access for VPC
- **Route Tables**: Network traffic routing

## 📝 Prerequisites
- Completed Projects 1-3
- Understanding of basic networking concepts
- Knowledge of IP addresses and CIDR notation
- Familiarity with Linux command line
- SSH client installed

## 🚀 Implementation Methods

### Method 1: AWS Management Console (Recommended for Learning)

#### Step 1: Create Custom VPC
1. Navigate to VPC Dashboard
2. Go to "Your VPCs" → "Create VPC"
3. Configuration:
   - Name: `CustomVPC`
   - IPv4 CIDR block: `10.0.0.0/16`
   - IPv6 CIDR block: No IPv6 CIDR block
   - Tenancy: Default
4. Create VPC

#### Step 2: Create Subnets
**Public Subnet:**
1. Go to "Subnets" → "Create subnet"
2. Select your VPC
3. Configuration:
   - Name: `PublicSubnet`
   - Availability Zone: `us-east-1a`
   - IPv4 CIDR block: `10.0.1.0/24`

**Private Subnet:**
1. Create another subnet
2. Configuration:
   - Name: `PrivateSubnet`
   - Availability Zone: `us-east-1b`
   - IPv4 CIDR block: `10.0.2.0/24`

#### Step 3: Set Up Internet Gateway
1. Go to "Internet Gateways" → "Create internet gateway"
2. Name: `CustomIGW`
3. Create and attach to your VPC

#### Step 4: Configure Route Tables
**Public Route Table:**
1. Go to "Route Tables"
2. Find the route table associated with your VPC
3. Add route:
   - Destination: `0.0.0.0/0`
   - Target: Your Internet Gateway
4. Associate with PublicSubnet

#### Step 5: Create Security Group
1. Go to "Security Groups" → "Create security group"
2. Name: `WebServerSG`
3. VPC: Select your custom VPC
4. Inbound rules:
   - HTTP (80): Source `0.0.0.0/0`
   - SSH (22): Source `Your IP/32`
5. Outbound rules: Allow all traffic

#### Step 6: Create Network ACL (Optional)
1. Go to "Network ACLs" → "Create network ACL"
2. Name: `PublicNACL`
3. VPC: Select your custom VPC
4. Add inbound rules:
   - HTTP (80): Source `0.0.0.0/0`
   - SSH (22): Source `Your IP/32`
   - Ephemeral ports (1024-65535): Source `0.0.0.0/0`
5. Associate with PublicSubnet

#### Step 7: Launch EC2 Instance
1. Go to EC2 → "Launch Instance"
2. Configuration:
   - AMI: Amazon Linux 2
   - Instance type: `t2.micro`
   - Network: Your custom VPC
   - Subnet: PublicSubnet
   - Auto-assign Public IP: Enable
   - Security Group: WebServerSG
   - Key Pair: Create new or use existing

#### Step 8: Deploy Web Application
```bash
# SSH into your instance
ssh -i your-key.pem ec2-user@<public-ip>

# Update system
sudo yum update -y

# Install Apache web server
sudo yum install -y httpd

# Start and enable Apache
sudo systemctl start httpd
sudo systemctl enable httpd

# Create simple web page
sudo tee /var/www/html/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html>
<head>
    <title>My Custom VPC Web App</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .success { color: green; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">🎉 Success!</h1>
        <h2>Custom VPC Web Application</h2>
        <p>This web server is running on:</p>
        <ul>
            <li>Custom VPC: 10.0.0.0/16</li>
            <li>Public Subnet: 10.0.1.0/24</li>
            <li>EC2 Instance with Apache HTTP Server</li>
        </ul>
        <p>Instance metadata:</p>
        <pre id="metadata"></pre>
    </div>
    <script>
        fetch('http://169.254.169.254/latest/meta-data/instance-id')
            .then(response => response.text())
            .then(data => {
                document.getElementById('metadata').innerHTML = 'Instance ID: ' + data;
            })
            .catch(error => console.log('Metadata not available'));
    </script>
</body>
</html>
EOF

# Test web server
curl localhost
```

### Method 2: CloudFormation Template

```bash
# Deploy complete infrastructure
aws cloudformation create-stack \
  --stack-name custom-vpc-webapp \
  --template-body file://project4_custom_vpc_ec2_webapp.yaml \
  --parameters ParameterKey=KeyName,ParameterValue=your-key-pair \
  --capabilities CAPABILITY_IAM
```

## 📁 Project Files

### `aws_ui_instructions.txt`
Detailed step-by-step AWS Console instructions.

### `project4_custom_vpc_ec2_webapp.yaml`
CloudFormation template that creates:
- Custom VPC with public and private subnets
- Internet Gateway and route tables
- Security Groups and NACLs
- EC2 instance with web server
- All necessary networking components

## 💰 Cost Estimation
- **VPC Components**: Free (VPC, subnets, route tables, IGW)
- **EC2 t2.micro**: Free tier eligible (750 hours/month)
- **Data Transfer**: 1 GB free per month
- **Total Estimated Cost**: $0 (within free tier limits)

## 🔍 Key Learning Points

### VPC Fundamentals
- **CIDR Blocks**: IP address ranges for VPC and subnets
- **Availability Zones**: Physical locations within regions
- **Route Tables**: Control network traffic routing
- **Internet Gateway**: VPC connection to internet

### Subnet Types
- **Public Subnet**: Has route to Internet Gateway
- **Private Subnet**: No direct internet access
- **Database Subnet**: Typically private for security

### Security Layers
- **Security Groups**: Stateful firewall at instance level
- **NACLs**: Stateless firewall at subnet level
- **Both work together**: Defense in depth approach

### Networking Concepts
- **Public IP**: Internet-routable address
- **Private IP**: Internal VPC address
- **Elastic IP**: Static public IP address
- **DNS Resolution**: Name to IP address translation

## 🧪 Testing & Validation

### Verification Steps
1. ✅ Custom VPC created with correct CIDR
2. ✅ Public and private subnets in different AZs
3. ✅ Internet Gateway attached and routing configured
4. ✅ Security Group allows HTTP and SSH
5. ✅ EC2 instance launched in public subnet
6. ✅ Web application accessible from internet
7. ✅ SSH access works from your IP

### Network Testing
```bash
# Test web application
curl http://<public-ip>

# Test SSH connectivity
ssh -i your-key.pem ec2-user@<public-ip>

# From EC2 instance, test internet connectivity
ping -c 4 google.com

# Check instance metadata
curl http://169.254.169.254/latest/meta-data/instance-id
```

## 🚨 Troubleshooting

### Common Issues
1. **Cannot access web application**
   - Check Security Group allows port 80
   - Verify instance has public IP
   - Ensure route table has internet gateway route

2. **SSH connection refused**
   - Check Security Group allows port 22 from your IP
   - Verify you're using correct key pair
   - Check instance is in running state

3. **No internet from private subnet**
   - Private subnets need NAT Gateway for internet
   - Check route table configuration

4. **Website not loading**
   - Verify Apache is running: `sudo systemctl status httpd`
   - Check if port 80 is listening: `sudo netstat -tlnp`

### Security Considerations
- Limit SSH access to your IP only
- Use jump boxes for private subnet access
- Regularly update security groups
- Monitor VPC Flow Logs for unusual traffic

## 🧹 Cleanup Instructions

### Manual Cleanup (in order)
1. Terminate EC2 instances
2. Delete NAT Gateways (if created)
3. Release Elastic IPs
4. Delete route table associations
5. Delete subnets
6. Detach and delete Internet Gateway
7. Delete Security Groups (except default)
8. Delete VPC

### CloudFormation Cleanup
```bash
aws cloudformation delete-stack --stack-name custom-vpc-webapp
```

## 📚 Additional Resources
- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [VPC Security Best Practices](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html)
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/latest/userguide/)
- [VPC Peering](https://docs.aws.amazon.com/vpc/latest/peering/)

## 🔗 Advanced Concepts to Explore
- **NAT Gateway**: Internet access for private subnets
- **VPC Endpoints**: Private access to AWS services
- **VPC Peering**: Connect multiple VPCs
- **Transit Gateway**: Centralized connectivity hub
- **Direct Connect**: Dedicated network connection to AWS

## ➡️ Next Steps
After completing this project:
1. Proceed to [Project 5: Database Connectivity](../project5_db_connect_write_read/)
2. Experiment with multi-AZ deployments
3. Learn about load balancers and auto scaling
4. Explore VPC Flow Logs for network monitoring

---
**🎓 Congratulations!** You've successfully built a custom AWS network infrastructure and deployed a web application. You now understand the fundamentals of AWS networking and security.
