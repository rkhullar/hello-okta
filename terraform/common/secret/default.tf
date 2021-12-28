resource "aws_secretsmanager_secret" "default" {
  name                    = var.name
  tags                    = var.tags
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "default" {
  for_each      = toset([random_uuid.default.id])
  secret_id     = aws_secretsmanager_secret.default.id
  secret_string = jsonencode(var.data)
  lifecycle {
    ignore_changes = [secret_string]
  }
}

resource "random_uuid" "default" {
  keepers = { for key in local.keys_to_keep : key => var.data[key] }
}

locals {
  keys_from_data   = keys(var.data)
  keys_to_preserve = coalesce(var.preserve, [])
  keys_to_ignore   = coalesce(var.ignore, [])
  keys_from_ignore = setsubtract(local.keys_from_data, local.keys_to_ignore)
  keys_to_keep_1   = var.ignore == null ? local.keys_to_preserve : local.keys_from_ignore
  keys_to_keep     = setunion(local.keys_to_preserve, local.keys_to_keep_1)
}