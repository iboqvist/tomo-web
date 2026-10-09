# https://registry.terraform.io/modules/terraform-aws-modules/ec2-instance/aws/6.4.1

module "tomo_ec2" {
  source = "terraform-aws-modules/ec2-instance/aws"
  version = "~> 6.4"

  name = "${var.project_name}-instance"

  ami = data.aws_ami.ubuntu.id
  instance_type = "t4g.small"

  subnet_id = module.vpc.public_subnets[0]

  create_eip = true

  create_security_group         = true
  security_group_description    = "HTTP and SSH in all out"
  security_group_egress_rules   = {"allow-all": { "cidr_ipv4": "0.0.0.0/0", "description": "Allow all", "ip_protocol": "-1" }}
  security_group_ingress_rules  = {"http": { "cidr_ipv4": "0.0.0.0/0", "description": "HTTP from any", "from_port": 80, "to_port": 80, "ip_protocol": "tcp" },
                                  "allow-ssh": { "cidr_ipv4": "0.0.0.0/0", "description": "SSH-From-Any", "from_port": 22, "to_port": 22, "ip_protocol": "tcp" }}

  key_name = "sigstore-kyverno-aws-playground"

  root_block_device = {
    type = "gp3"
    size = 16
    encrypted = true    # Defaults to AWS managed keys
  }
}