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