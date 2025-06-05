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
