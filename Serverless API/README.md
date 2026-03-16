# Project 8: Serverless API with Lambda & API Gateway

## 🎯 Learning Objectives
By completing this project, you will:
- Understand serverless computing concepts and benefits
- Create and deploy AWS Lambda functions
- Build RESTful APIs using Amazon API Gateway
- Learn about event-driven architecture
- Implement serverless authentication and authorization
- Understand Lambda pricing and optimization
- Monitor serverless applications with CloudWatch

## 📋 Project Overview
This project introduces you to serverless computing by building a REST API using AWS Lambda and API Gateway. You'll create Lambda functions that respond to HTTP requests, eliminating the need to manage servers while achieving automatic scaling and high availability.

## 🏗️ Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│    Internet     │───▶│   API Gateway    │───▶│  Lambda Function│
│   (HTTP Client) │    │  (REST API)      │    │ (hello_world.py)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       ▼                       ▼
         │              ┌──────────────────┐    ┌─────────────────┐
         └─────────────▶│   CloudWatch     │    │   Execution     │
                        │   (Logs/Metrics) │    │   Environment   │
                        └──────────────────┘    └─────────────────┘
```

## 🔧 AWS Services Used
- **AWS Lambda**: Serverless compute service
- **Amazon API Gateway**: Managed API service
- **CloudWatch**: Monitoring and logging
- **IAM**: Identity and access management
- **CloudFormation**: Infrastructure as Code

## 📝 Prerequisites
- Completed Projects 1-3
- Basic understanding of REST APIs
- Familiarity with Python programming
- Understanding of HTTP methods and status codes
- AWS CLI configured

## 🚀 Implementation Methods

### Method 1: AWS Management Console (Recommended for Learning)

#### Step 1: Create Lambda Function
1. Navigate to AWS Lambda Console
2. Click "Create function"
3. Configuration:
   - Function name: `HelloWorldFunction`
   - Runtime: Python 3.11
   - Architecture: x86_64
   - Execution role: Create new role with basic Lambda permissions

4. Replace default code with:
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"message": "Hello, world! This is a Lambda function exposed via API Gateway."}'
    }
```

5. Deploy the function

#### Step 2: Test Lambda Function
1. Create test event with API Gateway proxy template
2. Test the function and verify response
3. Check CloudWatch logs for execution details

#### Step 3: Create API Gateway
1. Navigate to API Gateway Console
2. Choose "REST API" (not private)
3. Configuration:
   - API name: `HelloWorldAPI`
   - Endpoint type: Regional
4. Create API

#### Step 4: Create API Resource and Method
1. In API Gateway, create new resource:
   - Resource path: `/hello`
   - Enable CORS if needed

2. Create GET method:
   - Integration type: Lambda Function
   - Lambda Region: Same as your function
   - Lambda Function: HelloWorldFunction
   - Grant permission when prompted

#### Step 5: Deploy API
1. Click "Deploy API"
2. Create new deployment stage:
   - Stage name: `prod`
   - Description: Production stage
3. Deploy and note the invoke URL

#### Step 6: Test API Endpoint
```bash
# Test the API endpoint
curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello

# Expected response:
# {"message": "Hello, world! This is a Lambda function exposed via API Gateway."}
```

#### Step 7: Add More Functionality (Optional)
Create additional Lambda functions for different operations:

**User Management Function:**
```python
import json

def lambda_handler(event, context):
    http_method = event['httpMethod']
    
    if http_method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'users': [
                    {'id': 1, 'name': 'John Doe'},
                    {'id': 2, 'name': 'Jane Smith'}
                ]
            })
        }
    elif http_method == 'POST':
        body = json.loads(event['body'])
        return {
            'statusCode': 201,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': f"User {body.get('name', 'Unknown')} created successfully"
            })
        }
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'})
        }
```

### Method 2: CloudFormation Template

```bash
# Deploy serverless API infrastructure
aws cloudformation create-stack \
  --stack-name serverless-api-stack \
  --template-body file://project8_lambda_apigateway.yaml \
  --capabilities CAPABILITY_IAM
```

## 📁 Project Files

### `hello_world_lambda.py`
```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '{"message": "Hello, world! This is a Lambda function exposed via API Gateway."}'
    }
```

### `aws_ui_instructions.txt`
Step-by-step AWS Console instructions for manual setup.

### `project8_lambda_apigateway.yaml`
CloudFormation template that creates:
- Lambda function with execution role
- API Gateway REST API
- API Gateway deployment and stage
- CloudWatch log groups
- Necessary permissions

## 💰 Cost Estimation
- **Lambda Requests**: 1M free requests/month, then $0.20 per 1M requests
- **Lambda Duration**: 400,000 GB-seconds free/month, then $0.0000166667 per GB-second
- **API Gateway**: 1M API calls free/month, then $3.50 per million calls
- **CloudWatch Logs**: $0.50 per GB ingested
- **Total Estimated Cost**: $0 for moderate usage (within free tier)

## 🔍 Key Learning Points

### Serverless Benefits
- **No Server Management**: AWS handles infrastructure
- **Automatic Scaling**: From zero to thousands of concurrent executions
- **Pay-per-Use**: Only pay for actual compute time
- **High Availability**: Built-in fault tolerance and redundancy

### Lambda Fundamentals
- **Event-Driven**: Functions triggered by events
- **Stateless**: Each invocation is independent
- **Runtime Support**: Multiple programming languages
- **Cold Starts**: Initial latency for new containers

### API Gateway Features
- **Request/Response Transformation**: Modify data in transit
- **Authentication**: Built-in authorization options
- **Rate Limiting**: Control API usage
- **Monitoring**: Built-in metrics and logging

### Event Structure
Understanding the event object passed to Lambda:
```json
{
  "httpMethod": "GET",
  "path": "/hello",
  "queryStringParameters": {},
  "headers": {
    "Content-Type": "application/json"
  },
  "body": null,
  "isBase64Encoded": false
}
```

## 🧪 Testing & Validation

### Verification Steps
1. ✅ Lambda function created and deployed
2. ✅ Function executes successfully in test console
3. ✅ API Gateway REST API created
4. ✅ API method configured and deployed
5. ✅ API endpoint responds to HTTP requests
6. ✅ CloudWatch logs capture function execution
7. ✅ API Gateway logs show request/response details

### Testing Commands
```bash
# Test basic endpoint
curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello

# Test with verbose output
curl -v https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello

# Test POST request (if implemented)
curl -X POST \
  https://<api-id>.execute-api.<region>.amazonaws.com/prod/users \
  -H 'Content-Type: application/json' \
  -d '{"name": "Test User"}'

# Load testing with ab (Apache Bench)
ab -n 100 -c 10 https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello
```

### Monitoring and Debugging
```bash
# View Lambda logs
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/HelloWorldFunction
aws logs tail /aws/lambda/HelloWorldFunction --follow

# Check Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=HelloWorldFunction \
  --start-time 2025-01-01T00:00:00Z \
  --end-time 2025-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## 🚨 Troubleshooting

### Common Issues
1. **Lambda function times out**
   - Check function execution time
   - Increase timeout in function configuration
   - Optimize code for better performance

2. **API Gateway returns 500 error**
   - Check Lambda function logs
   - Verify function permissions
   - Ensure proper response format

3. **CORS errors in browser**
   - Enable CORS in API Gateway
   - Add proper headers in Lambda response
   - Deploy API after CORS changes

4. **Cold start latency**
   - Implement provisioned concurrency
   - Optimize function initialization
   - Consider connection pooling

### Debugging Tips
```python
# Add logging to Lambda function
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Your function logic here
        result = {"message": "Success"}
        logger.info(f"Function completed successfully")
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(result)
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal server error'})
        }
```

## 🧹 Cleanup Instructions

### Manual Cleanup
1. Delete API Gateway deployment and API
2. Delete Lambda function
3. Delete CloudWatch log groups
4. Delete IAM roles created for Lambda

### CloudFormation Cleanup
```bash
aws cloudformation delete-stack --stack-name serverless-api-stack
```

### Verification
```bash
# Verify resources are deleted
aws lambda list-functions
aws apigateway get-rest-apis
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/
```

## 📚 Additional Resources
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/)
- [Serverless Application Model (SAM)](https://docs.aws.amazon.com/serverless-application-model/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

## 🔧 Advanced Concepts to Explore
- **Lambda Layers**: Share code between functions
- **Step Functions**: Orchestrate Lambda functions
- **EventBridge**: Event-driven architectures
- **Lambda@Edge**: Run functions at CloudFront edge locations
- **API Gateway WebSocket APIs**: Real-time communication

## 🔐 Security Best Practices
- **Least Privilege**: Minimal IAM permissions
- **API Keys**: Control API access
- **WAF Integration**: Protect against common attacks
- **VPC Integration**: Access private resources securely
- **Secrets Manager**: Manage sensitive configuration

## 📊 Performance Optimization
```python
# Connection pooling example
import json
import boto3
from botocore.exceptions import ClientError

# Initialize outside handler for connection reuse
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):
    # Function logic here
    pass
```

## 🚀 Scaling Considerations
- **Concurrent Executions**: Default limit of 1,000
- **Memory Allocation**: 128MB to 10,008MB
- **Timeout**: Maximum 15 minutes
- **Provisioned Concurrency**: Reduce cold starts
- **Reserved Concurrency**: Limit function scaling

## ➡️ Next Steps
After completing this project:
1. Proceed to [Project 9: Load Balancer Analytics](../project9_alb_logs_athena/)
2. Build more complex APIs with database integration
3. Explore serverless frameworks (SAM, Serverless Framework)
4. Implement authentication with Amazon Cognito
5. Learn about event-driven architectures with EventBridge

---
**🎓 Congratulations!** You've successfully built a serverless API using AWS Lambda and API Gateway. You now understand the fundamentals of serverless computing and can build scalable, cost-effective APIs without managing servers.
