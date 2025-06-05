# lambda_handler.py
import json
import logging
from mangum import Mangum
from main import app

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create Mangum handler
handler = Mangum(app, lifespan="off")

# Add additional context logging if needed
def log_request(event, context):
    """Log request details for debugging"""
    logger.info(f"Event: {json.dumps(event)}")
    logger.info(f"Context: {context}")
    return event

# You can use this as a wrapper around the handler if needed
def lambda_entrypoint(event, context):
    """
    Lambda function entrypoint with additional logging.
    Uncomment this function and change the handler in the GitHub Actions
    workflow to 'lambda_handler.lambda_entrypoint' if you need extra logging.
    """
    # log_request(event, context)
    return handler(event, context)

# Additional initialization can be done here
# This code runs once when the Lambda container initializes
logger.info("Lambda handler initialized")