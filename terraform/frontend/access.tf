module "lambda-role" {
  source     = "../common/iam/role"
  name       = "${var.prefix}-lambda-${var.suffix}"
  tags       = var.tags
  principals = [{ type = "Service", identifiers = ["lambda.amazonaws.com", "edgelambda.amazonaws.com"] }]
  inline_policies = {
    logs = data.aws_iam_policy_document.logs.json
    s3   = data.aws_iam_policy_document.s3.json
  }
}

data "aws_iam_policy_document" "logs" {
  statement {
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "s3" {
  statement {
    actions   = ["s3:GetObject", "s3:PutObject"]
    resources = ["arn:aws:s3:::${local.bucket_name}/*", "arn:aws:s3:::rk-serverless-test-01-static/*"]
  }
}

data "aws_iam_policy_document" "lambda-secrets" {
  statement {
    actions   = ["secretsmanager:ListSecrets"]
    resources = ["*"]
  }
  statement {
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [module.nextjs-secret.default["arn"]]
  }
}