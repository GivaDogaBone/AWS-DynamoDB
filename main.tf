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
}