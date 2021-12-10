resource "aws_secretsmanager_secret" "default" {
  name                    = "${var.prefix}-${var.suffix}"
  tags                    = var.tags
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "default" {
  secret_id     = aws_secretsmanager_secret.default.id
  secret_string = jsonencode(var.lambda_secrets)
}