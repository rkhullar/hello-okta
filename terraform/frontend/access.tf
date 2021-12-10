module "lambda-role" {
  source     = "../common/iam/role"
  name       = "${var.prefix}-lambda-${var.suffix}"
  tags       = var.tags
  principals = [{ type = "Service", identifiers = ["lambda.amazonaws.com", "edgelambda.amazonaws.com"] }]
  inline_policies = {
    logs = data.aws_iam_policy_document.logs.json
  }
}

data "aws_iam_policy_document" "logs" {
  statement {
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}
