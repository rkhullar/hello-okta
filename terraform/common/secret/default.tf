resource "aws_secretsmanager_secret" "default" {
  name                    = var.name
  tags                    = var.tags
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "default" {
  for_each      = toset(var.enable ? [random_uuid.default.id] : [])
  secret_id     = aws_secretsmanager_secret.default.id
  secret_string = jsonencode(var.data)
  lifecycle {
    ignore_changes = [secret_string]
  }
}

resource "random_uuid" "default" {
  keepers = { for key in local.keys_to_track : key => var.data[key] }
}

locals {
  keys_to_track_1 = var.tracking == "preserve" ? var.preserve : keys(var.data)
  keys_to_track_2 = setunion(local.keys_to_track_1, var.preserve)
  keys_to_track   = setsubtract(local.keys_to_track_2, var.ignore)
}