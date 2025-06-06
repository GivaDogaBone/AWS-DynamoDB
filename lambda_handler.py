# lambda_handler.py
import json
import logging
from mangum import Mangum
from main import app

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create Mangum handler with proper configuration for API Gateway
handler = Mangum(app, lifespan="off")

# Log environment variables for debugging
logger.info(f"Environment variables: AWS_REGION={os.environ.get('AWS_REGION')}, "
            f"CUSTOM_AWS_REGION={os.environ.get('CUSTOM_AWS_REGION')}, "
            f"DYNAMODB_TABLE_NAME={os.environ.get('DYNAMODB_TABLE_NAME')}")

def log_request(event, context):
    """Log request details for debugging"""
    logger.info(f"Event: {json.dumps(event)}")
    logger.info(f"Context: {str(context.__dict__)}")
    return event

def lambda_entrypoint(event, context):
    """
    Lambda function entrypoint with additional logging.
    """
    logger.info(f"Received event: {json.dumps(event)}")
    return handler(event, context)

# Additional initialization can be done here
# This code runs once when the Lambda container initializes
logger.info("Lambda handler initialized")
