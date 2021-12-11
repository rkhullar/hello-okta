locals {
  origins = {
    default = "S3-${local.static_bucket}"
  }
  time = {
    hour = 3600
    day  = 3600 * 24
    year = 3600 * 24 * 365
  }
}

resource "aws_cloudfront_origin_access_identity" "default" {
  comment = "static content for ${local.static_bucket}"
}

resource "aws_cloudfront_distribution" "default" {
  aliases         = []
  comment         = local.static_bucket
  enabled         = var.enable_cloudfront
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
    target_origin_id       = local.origins.default
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      headers      = ["Authorization", "Host"]
      query_string = true
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

  ordered_cache_behavior {
    path_pattern           = "_next/static/*"
    target_origin_id       = local.origins.default
    compress               = true
    viewer_protocol_policy = "https-only"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    default_ttl            = local.time.day
    max_ttl                = local.time.year

    forwarded_values {
      headers      = []
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }
}