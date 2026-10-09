provider "aws" {
  region = var.region

  default_tags {
    tags = {
      project = var.project_name
    }
  }
}

# AMIs can be searched for through the AWS console

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical #Should not have to be changed

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}