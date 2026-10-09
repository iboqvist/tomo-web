terraform {
  required_version = "~> 1.16"

  # https://registry.terraform.io/providers/hashicorp/aws/6.68.0
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "6.68.0"
    }
  }

  # https://developer.hashicorp.com/terraform/language/backend/s3#s3
  # The bucket needs to be created manually before terraform init, or we end up with a chicken or the egg problem
  backend "s3" {
    bucket        = "noizy87-a3-b"
    key           = "terraform.tfstate"
    region        = "eu-north-1"
    use_lockfile  = true
  }
}