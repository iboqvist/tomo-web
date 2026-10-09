variable "region" {
  type    = string
  default = "eu-north-1"  # Stockholm
}

variable "availability_zone" {
  type    = string
  description = "The AZ in which to deploy everything"
  default = "eu-north-1a"
}

variable "project_name" {
  type    = string
  default = "tomoweb"
}

variable "vpc_cidr" {
  type    = string
  description = "The CIDR block for the EC2 instance network, must be free in the region"
  default = "10.10.0.0/16"
}

variable "public_subnet_cidr" {
  type    = string
  default = "10.10.10.0/24"
}