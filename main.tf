# main.tf
provider "aws" {
  region = var.aws_region
}

resource "aws_dynamodb_table" "venues" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST" # On-demand capacity mode
  hash_key     = "venueID"

  attribute {
    name = "venueID"
    type = "S" # String type
  }

  tags = {
    Name        = "${var.table_name}-table"
    Environment = var.environment
  }

  # Add this lifecycle block to prevent Terraform from trying to recreate the table
  lifecycle {
    # This prevents Terraform from attempting to recreate the resource if it already exists
    # but was created outside of Terraform
    ignore_changes = all
  }
}