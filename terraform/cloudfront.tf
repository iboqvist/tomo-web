# https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/cloudfront_distribution


data "aws_cloudfront_cache_policy" "cache_policy" {
  name = "Managed-CachingDisabled"
}

data "aws_cloudfront_origin_request_policy" "all_except_host" {
  name = "Managed-AllViewerExceptHostHeader"  # Header is not needed
}

resource "aws_cloudfront_distribution" "tomo_ec2" {
  enabled = true
  comment = "Cloudfront Proxy for tomoweb"
  price_class = "PriceClass_100"

  origin {
    origin_id = "${var.project_name}-ec2"
    domain_name = module.tomo_ec2.public_dns

    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "http-only"  # https -> Cloudfront -> http -> ec2
      origin_ssl_protocols = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    target_origin_id = "${var.project_name}-ec2"
    viewer_protocol_policy = "redirect-to-https"

    # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/DownloadDistValuesCacheBehavior.html
    allowed_methods = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods = ["GET", "HEAD"]  # For some reason terraform requires this while caching is disabled

    cache_policy_id = data.aws_cloudfront_cache_policy.cache_policy.id
    origin_request_policy_id = data.aws_cloudfront_origin_request_policy.all_except_host.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}