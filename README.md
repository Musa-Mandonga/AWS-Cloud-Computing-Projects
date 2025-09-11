# Project 1: AWS Account Setup & Billing Alert

## 🎯 Learning Objectives
By completing this project, you will:
- Set up an AWS free tier account
- Understand AWS billing and cost management
- Configure billing alerts and notifications
- Learn basic CloudWatch alarm setup
- Familiarize yourself with the AWS Management Console

## 📋 Project Overview
This foundational project guides you through creating an AWS account and setting up essential billing monitoring. You'll learn how to configure cost alerts to avoid unexpected charges while exploring AWS services.

## 🏗️ Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AWS Account   │───▶│  CloudWatch      │───▶│  SNS Topic      │
│   (Free Tier)   │    │  Billing Alarm   │    │  (Optional)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🔧 AWS Services Used
- **AWS Account Management**: Free tier account setup
- **CloudWatch**: Billing alarms and monitoring
- **SNS (Simple Notification Service)**: Optional email notifications
- **Billing Dashboard**: Cost tracking and management

## 📝 Prerequisites
- Valid email address
- Credit or debit card for account verification
- Phone number for verification

## 🚀 Implementation Methods

### Method 1: AWS Management Console (Recommended for Learning)

#### Step 1: Create AWS Account
1. Navigate to [AWS Free Tier](https://aws.amazon.com/free/)
2. Click "Create a Free Account"
3. Provide email address, password, and account name
4. Complete contact information and payment verification
5. Verify email and phone number as instructed

#### Step 2: Initial Account Configuration
1. Sign in to [AWS Management Console](https://console.aws.amazon.com/)
2. Navigate to Billing Dashboard (search "Billing")
3. In left menu, select "Billing preferences"
4. Enable "Receive Free Tier Usage Alerts"
5. Save preferences

#### Step 3: Set Up Billing Alarm (Optional but Recommended)
1. Navigate to CloudWatch service
2. Go to "Alarms" → "Create alarm"
3. Select "EstimatedCharges" metric
4. Configure threshold (e.g., $5 or $10)
5. Set up SNS notification if desired

#### Step 4: Explore AWS Console
- Familiarize yourself with navigation bar
- Explore services menu
- Review account settings

### Method 2: CloudFormation Template

⚠️ **Note**: Account creation cannot be automated with CloudFormation. Use the template only after your account is set up.

```bash
# Deploy the billing alarm
aws cloudformation create-stack \
  --stack-name billing-alarm-stack \
  --template-body file://project1_set_up_aws_account.yaml
```

## 📁 Project Files

### `aws_ui_instructions.txt`
Detailed step-by-step instructions for AWS Console setup.

### `project1_set_up_aws_account.yaml`
CloudFormation template that creates:
- CloudWatch billing alarm
- Monitors estimated charges
- Triggers when charges exceed threshold

## 💰 Cost Estimation
- **AWS Account**: Free
- **CloudWatch Alarms**: First 10 alarms are free
- **SNS Notifications**: First 1,000 emails free per month
- **Total Estimated Cost**: $0 (within free tier limits)

## 🔍 Key Learning Points

### AWS Free Tier
- 12 months of free services for new accounts
- Always-free services (DynamoDB, Lambda, etc.)
- Trial services (free for short periods)

### Billing Best Practices
- Set up billing alerts immediately
- Monitor usage regularly
- Understand free tier limits
- Use AWS Cost Explorer for detailed analysis

### Security Considerations
- Enable MFA (Multi-Factor Authentication)
- Use strong passwords
- Review and understand AWS shared responsibility model

## 🧪 Testing & Validation

### Verification Steps
1. ✅ AWS account successfully created
2. ✅ Can access AWS Management Console
3. ✅ Billing preferences configured
4. ✅ CloudWatch billing alarm created (if using CloudFormation)
5. ✅ Free tier usage alerts enabled

### Expected Outcomes
- Functioning AWS account with billing monitoring
- Understanding of AWS console navigation
- Basic knowledge of cost management tools

## 🚨 Troubleshooting

### Common Issues
1. **Credit card verification fails**
   - Ensure card details are correct
   - Contact your bank if transactions are blocked
   - Try a different card if needed

2. **Phone verification issues**
   - Ensure phone number is entered correctly
   - Check for SMS/call blocking
   - Try automated call option

3. **CloudFormation stack fails**
   - Verify you're in correct AWS region
   - Check IAM permissions
   - Ensure SNS topic ARN is correct (if using notifications)

## 🧹 Cleanup Instructions
```bash
# Delete CloudFormation stack (if created)
aws cloudformation delete-stack --stack-name billing-alarm-stack

# Verify deletion
aws cloudformation describe-stacks --stack-name billing-alarm-stack
```

⚠️ **Important**: You cannot delete an AWS account immediately. If you want to close your account permanently, follow AWS account closure process in the billing console.

## 📚 Additional Resources
- [AWS Free Tier FAQ](https://aws.amazon.com/free/free-tier-faqs/)
- [AWS Billing and Cost Management User Guide](https://docs.aws.amazon.com/awsaccountbilling/)
- [AWS Well-Architected Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/)

## ➡️ Next Steps
After completing this project:
1. Proceed to [Project 2: IAM Users, Groups & Roles](../project2_iam_user_group_role/)
2. Explore the AWS console and familiarize yourself with different services
3. Review your billing dashboard regularly as you progress through projects

---
**🎓 Congratulations!** You've successfully set up your AWS account and implemented billing monitoring. This foundation will support all your future AWS learning endeavors.
