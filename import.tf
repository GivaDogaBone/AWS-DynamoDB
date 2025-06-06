# import.tf
# This file allows Terraform to manage an existing DynamoDB table
# without attempting to create it again

terraform {
  # Add this import block to tell Terraform about existing resources
  # This is a new feature in Terraform 1.5+
  # If you're using an older version, you'll need to use the terraform import command manually
  
  required_version = ">= 1.5.0"
  
  # If your Terraform version doesn't support import blocks, comment this out
  # and use manual import with: terraform import aws_dynamodb_table.venues venues
  # import {
  #   to = aws_dynamodb_table.venues
  #   id = "venues"
  # }
}