module "nextjs-secret" {
  source = "../common/secret"
  name = "${var.prefix}-nextjs-${var.suffix}"
  tags = var.tags
  data = var.lambda_secrets
}

module "hello-secret" {
  source = "../common/secret"
  name   = "${var.prefix}-hello-${var.suffix}"
  tags   = var.tags
  data = {
    message = "hello world"
  }
}