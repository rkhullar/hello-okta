resource "aws_cloudfront_origin_access_identity" "default" {
  comment = "static content for ${local.bucket_name}"
}

//resource "aws_cloudfront_distribution" "default" {
//  aliases         = []
//  comment         = var.prefix
//  enabled         = false
//  is_ipv6_enabled = true
//  price_class     = var.price_class
//  tags            = var.tags
//
//  origin {
//    domain_name = ""
//    origin_id   = ""
//  }
//}