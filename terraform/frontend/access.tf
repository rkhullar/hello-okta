resource "aws_iam_role" "lambda" {
  name               = "${var.project}-lambda"
  tags               = local.common_tags
  assume_role_policy = data.aws_iam_policy_document.lambda-trust.json
}

resource "aws_iam_role_policy" "lambda-default" {
  # inline
  role   = aws_iam_role.lambda.id
  name   = "default"
  policy = data.aws_iam_policy_document.lambda-default.json
}

data "aws_iam_policy_document" "lambda-trust" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com", "edgelambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "lambda-default" {
  statement {
    actions   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
    resources = ["*"]
  }
}
