variable "prefix" {
  type = string
}

variable "suffix" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "price_class" {
  type    = string
  default = "PriceClass_100"
}

variable "lambda_secrets" {
  type    = map(string)
  default = {}
}

variable "lambda_handler" {
  type    = string
  default = "index.handler"
}

variable "lambda_memory" {
  type    = number
  default = 512
}

variable "lambda_timeout" {
  type    = number
  default = 10
}

variable "enable_cloudfront" {
  type    = bool
  default = false
}

output "buckets" {
  value = {
    static = module.static-bucket.name
  }
}

output "lambdas" {
  value = {
    default = module.default-lambda.name
    api     = module.api-lambda.name
  }
}

output "roles" {
  value = {
    lambda = module.lambda-role.name
  }
}

output "secrets" {
  value = {
    nextjs = module.nextjs-secret.name
  }
}

output "cloudfront" {
  value = {
    id     = aws_cloudfront_distribution.default.id
    domain = aws_cloudfront_distribution.default.domain_name
  }
}