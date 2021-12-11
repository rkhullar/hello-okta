module "default-lambda" {
  source   = "../common/lambda/function"
  name     = "${var.prefix}-default-${var.suffix}"
  tags     = var.tags
  role     = module.lambda-role.name
  handler  = var.lambda_handler
  runtime  = "nodejs14.x"
  template = "nodejs/default"
  publish  = true
  memory   = var.lambda_memory
  timeout  = var.lambda_timeout
}

module "api-lambda" {
  source   = "../common/lambda/function"
  name     = "${var.prefix}-api-${var.suffix}"
  tags     = var.tags
  role     = module.lambda-role.name
  handler  = var.lambda_handler
  runtime  = "nodejs14.x"
  template = "nodejs/default"
  publish  = true
  memory   = var.lambda_memory
  timeout  = var.lambda_timeout
}