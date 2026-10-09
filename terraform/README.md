# The Cloud Infrastrucutr

Terraform is used to deploy the containerised webapp on AWS. With the docker compose file and bash script it sets up the machine to deploy the app. The code will be extended to set up CloudFront, mainly as a reverse proxy.

To test the code, install `aws cli` and `terraform` first. Then:

```bash
aws configure # Configure AWS CLI with an access token
terraform init # Pulls necessary dependency packages for the terraform code and inits the backend
terraform apply # Set up the infrastructure
# Terraform will output the ip address where the webapp is reachable on (http port 80)
terraform destroy # to tear down the deployment
```

A known issue is that the s3 backend isn't used correctly, instead, terraform use the default local backend.

A note of warning is that the ec2 security group allows tcp/80 and tcp/22 from any ip curently.

## The Terraform Code

There are some things of interest in the design of the IoC.

### The Terraform Backend

For Terraform to correctly plan/modify the infrastructure it manages, it needs to know what the current state is. To do so, it tracks the state in a file called the backend. By default the backend is stored in a local file, however, this is an issue if we want to manage the infrastructure through our CI/CD pipe.

A (popular) solution to this problem is to store the backend in a S3 bucket. In that way, we enable collaboration amongst users on the same infrastructure. Though, then comes the question to how terraform can first create the S3 backend if it need it in the first place to function. The answer is that it can't. Instead, we need to manually prepare the S3 backend as a one-time setup.

# EC2 Instance

The EC2 Instance is currently set up to Allow HTTP and SSH from any ip but will soon be closed down to only allow http from CloudFront and managment traffic through Sesion Manager.

# VPC
Nothing special going on with the VPC Really. Instances are given DNS names, including publicly resolvable names.