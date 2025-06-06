# AWS-DynamoDB
Create an AWS DynamoDB

### Important Notes:
1. This configuration creates a DynamoDB table with a simple primary key (venueID).
2. The other attributes you mentioned (venueDescription, accountID, accountDenomination, accountDescription) don't need to be explicitly defined in the Terraform configuration. In DynamoDB, you only need to define attributes used in key schemas or indexes.
3. DynamoDB is schema-less, so you can add these attributes to your items without declaring them in the table definition.
4. I've set the billing mode to on-demand capacity (PAY_PER_REQUEST), which is often simpler for getting started.
5. You may want to add a terraform.tfvars file if you need to customize the variable values.

To apply this configuration:
1. Save these files in your project directory
2. Run `terraform init` to initialize your project
3. Run `terraform plan` to see what will be created
4. Run `terraform apply` to create the resources

### How to use this API:
1. Install dependencies:
``` bash
   pip install -r requirements.txt
```
1. Set up AWS credentials: Make sure you have AWS credentials configured either through environment variables, AWS CLI, or IAM roles if running on AWS services.
2. Run the FastAPI application:
``` bash
   python run.py
```
1. Access the API documentation: Open your browser and go to `http://localhost:8000/docs` to see the interactive Swagger UI documentation.
2. Test the API endpoints:
    - POST `/venues/` - Create a new venue
    - GET `/venues/{venue_id}` - Get a specific venue by ID
    - GET `/venues/` - List all venues
    - PUT `/venues/{venue_id}` - Update a venue
    - DELETE `/venues/{venue_id}` - Delete a venue

This FastAPI application provides a complete REST API for interacting with the DynamoDB table you defined in Terraform. It handles CRUD operations for your venue data and includes proper error handling.

### Setting up GitHub Secrets
For this workflow to function correctly, you need to set up the following secrets in your GitHub repository:
1. `AWS_ACCESS_KEY_ID`: Your AWS access key
2. `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
3. : The AWS region where your resources are deployed `AWS_REGION`
4. `LAMBDA_EXECUTION_ROLE`: The ARN of the IAM role that Lambda will use (this needs appropriate permissions for DynamoDB and CloudWatch logs)

### Important Notes
1. **Lambda Setup**: This workflow assumes you're deploying to AWS Lambda. The FastAPI app needs minor adjustments to work with Lambda (which I've provided with the Mangum adapter).
2. **IAM Permissions**: Make sure the AWS credentials used have appropriate permissions to:
    - Deploy Terraform resources
    - Create/update Lambda functions
    - Manage API Gateway
    - Access DynamoDB

3. **API Gateway Integration**: This is a simplified example for API Gateway. Depending on your needs, you might need a more comprehensive setup.
4. **Testing**: The workflow includes a testing step, but you'll need to create actual tests for your application.
5. **Cost Considerations**: Remember that deploying resources to AWS can incur costs.
6. **Security**: This workflow uses GitHub Secrets to store sensitive information. Make sure you follow best practices for managing these secrets.

To use this workflow:
1. Create the `.github/workflows` directory in your repository
2. Add the `deploy.yml` file with the content provided
3. Set up the required GitHub secrets
4. Push to your repository
5. The workflow will run automatically on pushes to main/master or can be triggered manually via the GitHub Actions interface

# Setting Up GitHub Secrets for AWS Deployment
GitHub Secrets allow you to store sensitive information like API keys and access credentials securely in your repository. Here's a step-by-step guide on how to set up the required secrets:
## Required Secrets
Based on your workflow file, you need to set up these secrets:
1. : Your AWS access key `AWS_ACCESS_KEY_ID`
2. : Your AWS secret key `AWS_SECRET_ACCESS_KEY`
3. : The AWS region where resources are deployed (e.g., "us-west-2") `AWS_REGION`
4. : The ARN of the IAM role for Lambda execution `LAMBDA_EXECUTION_ROLE`

## Step-by-Step Guide
### 1. Create an AWS IAM User (if you don't already have one)
1. Log in to the AWS Management Console
2. Navigate to IAM (Identity and Access Management)
3. Click on "Users" in the left sidebar, then "Add user"
4. Enter a username (e.g., "github-workflow-user")
5. Select "Programmatic access" for access type
6. For permissions, you can:
    - Attach existing policies like `AmazonDynamoDBFullAccess`, `AWSLambdaFullAccess`, etc.
    - Or create a custom policy with just the permissions needed

7. Complete the user creation and save the Access Key ID and Secret Access Key

### 2. Create an IAM Role for Lambda (for LAMBDA_EXECUTION_ROLE)
1. In the AWS Management Console, go to IAM
2. Click on "Roles" in the left sidebar, then "Create role"
3. Select "AWS service" as the trusted entity, and "Lambda" as the service
4. Attach the following policies:
    - `AmazonDynamoDBFullAccess` (or a more restrictive custom policy)
    - `CloudWatchLogsFullAccess` (or a custom policy for logs)

5. Name the role (e.g., "venues-api-lambda-role") and create it
6. After creating, click on the role and copy its ARN (it looks like `arn:aws:iam::123456789012:role/venues-api-lambda-role`)

### 3. Add Secrets to GitHub Repository
1. Go to your GitHub repository
2. Click on "Settings" (tab at the top)
3. In the left sidebar, navigate to "Secrets and variables" → "Actions"
4. Click "New repository secret" to add each of the following:
**For AWS_ACCESS_KEY_ID:**
    - Name: `AWS_ACCESS_KEY_ID`
    - Value: Paste your AWS Access Key ID
    - Click "Add secret"

**For AWS_SECRET_ACCESS_KEY:**
    - Name: `AWS_SECRET_ACCESS_KEY`
    - Value: Paste your AWS Secret Access Key
    - Click "Add secret"

**For AWS_REGION:**
    - Name: `AWS_REGION`
    - Value: Enter your AWS region (e.g., as indicated in your terraform.tfvars file) `us-west-2`
    - Click "Add secret"

**For LAMBDA_EXECUTION_ROLE:**
    - Name: `LAMBDA_EXECUTION_ROLE`
    - Value: Paste the full ARN of the IAM role you created (e.g., `arn:aws:iam::123456789012:role/venues-api-lambda-role`)
    - Click "Add secret"

### 4. Verify Secret Configuration
1. Go to "Actions" tab in your repository
2. If you have any previous workflow runs, you can check if they're using the secrets correctly
3. Alternatively, you can manually trigger the workflow using the "Run workflow" button if your workflow supports `workflow_dispatch`

## Security Best Practices
1. **Least Privilege**: Ensure your AWS IAM user and role have only the permissions needed for the workflow
2. **Rotate Credentials**: Periodically rotate your AWS access keys
3. **Audit Access**: Regularly review who has access to your GitHub repository and can view workflow runs
4. **Environment Restrictions**: Consider using environment protection rules for production deployments

## Troubleshooting
If your workflow fails after setting up the secrets:
1. Check the workflow logs to see specific error messages
2. Verify that the AWS credentials have the necessary permissions
3. Ensure the region specified in matches the region in your file `AWS_REGION``terraform.tfvars`
4. Confirm that the Lambda execution role has the required permissions for DynamoDB and CloudWatch

These steps should help you successfully set up the GitHub Secrets required for your AWS deployment workflow.
