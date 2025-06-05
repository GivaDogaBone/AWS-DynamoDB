# variables.tf
variable "aws_region" {
  description = "AWS region where resources will be created"
  type        = string
  default     = "us-east-1"
}

variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "venues"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}