# https://registry.terraform.io/modules/terraform-aws-modules/ec2-instance/aws/6.4.1

module "tomo_ec2" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 6.4"

  name = "${var.project_name}-instance"

  ami = data.aws_ami.ubuntu.id
  instance_type = "t3.small"

  subnet_id = module.vpc.public_subnets[0]

  create_security_group         = true
  security_group_description    = "Security group for ${var.project_name} EC2 instance"
  security_group_egress_rules   = {"allow-all": { "cidr_ipv4": "0.0.0.0/0", "description": "Allow all", "ip_protocol": "-1" }}
  security_group_ingress_rules  = {"http-from-cloudfront": { "prefix_list_id": data.aws_ec2_managed_prefix_list.cloudfront.id, "description": "HTTP from CloudFront", "from_port": 80, "to_port": 80, "ip_protocol": "tcp" } }

  # Session Manager instead of ssh
  create_iam_instance_profile = true
  iam_role_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }

  user_data = templatefile("${path.module}/user_data.sh.tftpl", {
    docker_compose_file = file("${path.module}/compose.yaml")
  })

  root_block_device = {
    type = "gp3"
    size = 16
    encrypted = true    # Defaults to AWS managed keys
  }
}