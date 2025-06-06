#!/bin/bash

# Set variables
API_ID="gy1uvk48di"  # Replace with your actual API ID
STAGE="prod"         # Your API stage
REGION="us-west-2"   # Your AWS region

# Export the OpenAPI 3.0 definition
aws apigateway get-export \
  --rest-api-id $API_ID \
  --stage-name $STAGE \
  --export-type oas30 \
  --accepts application/json \
  openapi.json

echo "Exported OpenAPI definition to openapi.json"

# Use API Gateway's Export Feature to Get OpenAPI Definition
# You can also generate the OpenAPI definition directly from API Gateway after it's deployed:
