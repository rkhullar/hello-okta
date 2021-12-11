locals {
  static_bucket = "${var.prefix}-static-${var.suffix}"
}

module "static-bucket" {
  source        = "../common/s3/bucket"
  name          = local.static_bucket
  tags          = var.tags
  policy        = data.aws_iam_policy_document.static-bucket-policy.json
  attach_policy = true
}

data "aws_iam_policy_document" "static-bucket-policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["arn:aws:s3:::${local.static_bucket}/*"]
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.default.iam_arn]
    }
  }
}