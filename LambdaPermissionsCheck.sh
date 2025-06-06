#!/bin/bash
# This is a script you can run locally or add to your GitHub Actions to check Lambda permissions

# Set your variables
LAMBDA_NAME="venues-api"
ROLE_NAME=$(aws lambda get-function --function-name $LAMBDA_NAME --query 'Configuration.Role' --output text | awk -F '/' '{print $NF}')

echo "Lambda function $LAMBDA_NAME uses role $ROLE_NAME"

# Check the role's policies
echo "Checking role policies..."
aws iam list-attached-role-policies --role-name $ROLE_NAME

# Check if the role has DynamoDB access
echo "Checking for DynamoDB access..."
POLICY_ARN=$(aws iam list-attached-role-policies --role-name $ROLE_NAME --query "AttachedPolicies[?contains(PolicyName, 'DynamoDB')].PolicyArn" --output text)

if [ -z "$POLICY_ARN" ]; then
  echo "WARNING: No DynamoDB policy found! This might cause access issues."
  
  echo "Attaching AmazonDynamoDBFullAccess policy..."
  aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
else
  echo "DynamoDB policy is attached: $POLICY_ARN"
fi

# Check Lambda timeout
TIMEOUT=$(aws lambda get-function-configuration --function-name $LAMBDA_NAME --query 'Timeout' --output text)
echo "Lambda timeout is set to $TIMEOUT seconds"

if [ $TIMEOUT -lt 10 ]; then
  echo "WARNING: Lambda timeout is less than 10 seconds, which may cause timeouts for cold starts."
fi

# Check Lambda memory
MEMORY=$(aws lambda get-function-configuration --function-name $LAMBDA_NAME --query 'MemorySize' --output text)
echo "Lambda memory is set to $MEMORY MB"

if [ $MEMORY -lt 256 ]; then
  echo "WARNING: Lambda memory is less than 256 MB, which may cause performance issues."
fi