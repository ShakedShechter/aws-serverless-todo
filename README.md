# Serverless Todo App with AWS

A fully serverless, secure, and scalable Todo List web application built entirely with native AWS services. This project demonstrates modern cloud-native architecture patterns without any server management requirements.

![AWS Serverless Architecture](https://img.shields.io/badge/AWS-Serverless-orange?style=flat-square&logo=amazon-aws)
![React](https://img.shields.io/badge/React-18-blue?style=flat-square&logo=react)
![Python](https://img.shields.io/badge/Python-Lambda-green?style=flat-square&logo=python)
![DynamoDB](https://img.shields.io/badge/Database-DynamoDB-yellow?style=flat-square&logo=amazon-dynamodb)

## 🎯 Project Overview

This project showcases the development of a production-ready serverless application that includes:
- **User Authentication** with JWT tokens
- **Secure CRUD operations** for todo management  
- **Real-time UI updates** with dynamic feedback
- **Multi-tenant data isolation** per user
- **Comprehensive monitoring** and logging

## 🏗️ Architecture

The application follows a modern serverless architecture leveraging fully managed AWS services:

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│   React     │───▶│   Amazon     │───▶│   Amazon    │───▶│   AWS        │───▶│   Amazon    │
│   Frontend  │    │   Cognito    │    │   API       │    │   Lambda     │    │   DynamoDB  │
│  (Amplify)  │    │ (Auth & JWT) │    │   Gateway   │    │  (Python)    │    │   (NoSQL)   │
└─────────────┘    └──────────────┘    └─────────────┘    └──────────────┘    └─────────────┘
```

### Component Breakdown

- **Frontend**: React SPA hosted on AWS Amplify with SSL and CDN
- **Authentication**: Amazon Cognito User Pools with hosted UI and JWT tokens
- **API Layer**: Amazon API Gateway (HTTP API) with JWT authorizers
- **Compute**: AWS Lambda functions (Python) for all business logic
- **Database**: Amazon DynamoDB with user-based data partitioning
- **Monitoring**: Amazon CloudWatch for logs and application insights
- **Security**: AWS IAM with least-privilege access policies

## 🚀 Features

- ✅ **Secure Authentication**: Cognito-managed sign-in/sign-out with JWT
- ✅ **CRUD Operations**: Create, read, update, and delete todos
- ✅ **User Isolation**: Each user sees only their own todos
- ✅ **Real-time Updates**: Dynamic UI with immediate feedback
- ✅ **Token Management**: Automatic session validation and renewal
- ✅ **CORS Handling**: Proper cross-origin request management
- ✅ **Error Handling**: Graceful degradation and user-friendly messages
- ✅ **Responsive Design**: Works across desktop and mobile devices

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React (Vite) | Modern UI framework with fast build tooling |
| **Hosting** | AWS Amplify | Serverless static site hosting with SSL |
| **Authentication** | Amazon Cognito | Managed user authentication and JWT tokens |
| **API** | API Gateway (HTTP API) | RESTful API endpoints with JWT authorization |
| **Compute** | AWS Lambda (Python) | Serverless function execution |
| **Database** | Amazon DynamoDB | NoSQL database with automatic scaling |
| **Monitoring** | Amazon CloudWatch | Centralized logging and application monitoring |
| **Security** | AWS IAM | Identity and access management |

## 📋 Prerequisites

- AWS Account with appropriate permissions
- Node.js 18+ and npm/yarn
- Python 3.9+ for Lambda development
- AWS CLI configured (optional, for advanced deployment)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/serverless-todo-app.git
cd serverless-todo-app
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. AWS Infrastructure Setup

#### DynamoDB Table
Create a DynamoDB table with:
- **Table Name**: `TodoItems`
- **Partition Key**: `user_id` (String)
- **Sort Key**: `todo_id` (String)

#### Lambda Functions
Deploy the following Python Lambda functions:
- `create-todo` - Creates new todo items
- `get-todos` - Retrieves user's todo list
- `delete-todo` - Removes specific todo items

#### API Gateway
Configure HTTP API with routes:
- `POST /create-todo`
- `GET /get-todos`
- `DELETE /delete-todo/{todoId}`

#### Cognito Setup
1. Create User Pool with hosted UI
2. Configure app client with appropriate OAuth flows
3. Set up JWT authorizer in API Gateway

### 4. Environment Configuration
Update your React app with the correct AWS resource endpoints and IDs.

## 🔐 Security Features

- **JWT Authentication**: All API calls require valid Cognito tokens
- **User Data Isolation**: DynamoDB partition key ensures user separation
- **Least Privilege IAM**: Lambda functions have minimal required permissions
- **CORS Protection**: API Gateway configured for specific origin access
- **Token Validation**: Frontend validates token expiry before API calls
- **Secure Headers**: Proper HTTPS and security headers implementation

## 🐛 Common Issues & Solutions

### CORS Errors
- Ensure API Gateway has proper CORS configuration
- Verify OPTIONS method is configured for preflight requests
- Check that Lambda responses include proper `application/json` content-type

### JWT Authentication Failures
- Validate token format and expiration in frontend
- Confirm Cognito User Pool configuration matches API Gateway authorizer
- Check CloudWatch logs for detailed error messages

### DynamoDB Access Issues
- Verify IAM role has proper DynamoDB permissions
- Ensure table name matches in Lambda environment variables
- Check that partition key (`user_id`) is correctly extracted from JWT

## 📊 Monitoring & Debugging

The application includes comprehensive logging via Amazon CloudWatch:

- **Lambda Logs**: Function execution, errors, and performance metrics
- **API Gateway Logs**: Request/response tracking and integration errors  
- **DynamoDB Metrics**: Read/write capacity and throttling alerts

Access logs through:
```bash
# View Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/"

# Tail specific function logs  
aws logs tail /aws/lambda/your-function-name --follow
```

## 🔮 Future Improvements

- [ ] **Infrastructure as Code**: Migrate to AWS CDK or CloudFormation
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Enhanced Monitoring**: AWS X-Ray tracing and custom CloudWatch dashboards
- [ ] **Secrets Management**: AWS Systems Manager Parameter Store integration
- [ ] **Multi-Region**: DynamoDB Global Tables for geographic distribution
- [ ] **Advanced Features**: Due dates, categories, search functionality
- [ ] **Notifications**: SNS/SES integration for reminders
- [ ] **Mobile App**: React Native or native mobile clients

## 📈 Performance & Scalability

This serverless architecture automatically scales to handle varying loads:

- **Lambda**: Automatic concurrency scaling up to account limits
- **DynamoDB**: On-demand billing with automatic scaling
- **API Gateway**: Built-in scalability for millions of requests
- **Amplify**: Global CDN distribution for fast content delivery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS Documentation and best practices
- React and Vite communities
- Serverless architecture patterns and examples

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) page for existing solutions
2. Review AWS CloudWatch logs for detailed error information
3. Consult AWS documentation for service-specific troubleshooting
4. Create a new issue with detailed reproduction steps

---

**Built with ❤️ using AWS Serverless Services**
