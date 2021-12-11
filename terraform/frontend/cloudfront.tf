locals {
  origins = {
    default = "S3-${local.static_bucket}"
  }
}

resource "aws_cloudfront_origin_access_identity" "default" {
  comment = "static content for ${local.static_bucket}"
}

resource "aws_cloudfront_distribution" "default" {
  aliases         = []
  comment         = local.static_bucket
  enabled         = false
  is_ipv6_enabled = true
  price_class     = var.price_class
  tags            = var.tags

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }

  origin {
    origin_id   = local.origins.default
    domain_name = module.static-bucket.output["bucket_domain_name"]
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.default.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true
    target_origin_id       = local.origins.default
    viewer_protocol_policy = "redirect-to-https"

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Host"]
      cookies {
        forward = "all"
      }
    }

    lambda_function_association {
      event_type   = "origin-request"
      lambda_arn   = module.default-lambda.output["qualified_arn"]
      include_body = true
    }

    lambda_function_association {
      event_type = "origin-response"
      lambda_arn = module.default-lambda.output["qualified_arn"]
    }
  }
}