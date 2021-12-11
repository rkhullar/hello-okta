resource "aws_s3_bucket" "default" {
  bucket        = var.name
  tags          = var.tags
  force_destroy = true
}

resource "aws_s3_bucket_policy" "default" {
  count  = var.attach_policy ? 1 : 0
  bucket = aws_s3_bucket.default.id
  policy = var.policy
}

resource "aws_s3_bucket_public_access_block" "default" {
  bucket                  = aws_s3_bucket.default.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}