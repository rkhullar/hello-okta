resource "aws_lambda_function" "default" {
  function_name    = var.name
  tags             = var.tags
  role             = data.aws_iam_role.default.arn
  handler          = var.handler
  runtime          = var.runtime
  memory_size      = var.memory
  timeout          = var.timeout
  publish          = var.publish
  filename         = data.archive_file.template.output_path
  source_code_hash = data.archive_file.template.output_base64sha256

  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}

data "aws_iam_role" "default" {
  name = var.role
}

data "archive_file" "template" {
  type        = "zip"
  source_dir  = "${path.module}/templates/${var.template}"
  output_path = "${path.module}/local/${var.template}.zip"
}