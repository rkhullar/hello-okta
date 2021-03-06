module "nextjs-secret" {
  source   = "../common/secret"
  name     = "${var.prefix}-nextjs-${var.suffix}"
  tags     = var.tags
  data     = var.lambda_secrets
  tracking = "ignore"
  ignore   = var.secrets_ignore
  enable   = var.enable_secrets
}