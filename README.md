# Serverless-Web-Application
Build a web-based interface for managing security controls by perform CRUD operations (Create, Read, Update, Delete) on a list of controls stored in dynamodb, with API calls handled via frontend interactions and DynamoDB manipulation facilitated by Lambda functions and API Gateway endpoints.

## Architecture
![Serverless App](https://github.com/MiguelAngelHorta/Serverless-Web-Application/assets/106134627/16d45e9a-b8bf-4b8c-9d49-a70e995af126)

## API Endpoints
- Endpoint: https://9ookpuq4tk.execute-api.us-east-1.amazonaws.com/prod/items
- Stage: Prod
- Routes: 
  - /items
    - GET
    - PUT
  - /items/{mainID}
    - POST
    - DELETE
    - GET

## Features

- **Add Control**: Users can add new security controls with details such as control ID, description, domain, and scope.
- **Update Control**: Existing security controls can be updated with revised information.
- **Delete Control**: Users have the ability to delete security controls from the inventory.
- **Fetch Controls**: The application provides an API to fetch all security controls stored in the database.
- **Download CSV**: Users can download the security controls data in CSV format for offline analysis.

## Technology Stack

The project utilizes the following technologies:

- **AWS Lambda**: Serverless compute service to execute backend logic for handling API requests.
- **DynamoDB**: Fully managed NoSQL database service for storing security controls data.
- **API Gateway**: Service for creating, publishing, maintaining, monitoring, and securing APIs.
- **S3**: Object storage service used for hosting the web interface files.
- **CloudFront**: Content delivery network (CDN) service for fast and secure delivery of web content globally.
- **Certificate Manager**: Manages SSL/TLS certificates for enabling HTTPS connections.
- **CloudWatch Logs**: Logging and monitoring of exceeded thresholds.
-  **Simple Notification Service (SNS)**: Email notification of exceeded thresholds.


