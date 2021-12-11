variable "name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "role" {
  type = string
}

variable "handler" {
  type = string
}

variable "runtime" {
  type = string
}

variable "template" {
  type = string
}

variable "memory" {
  type    = number
  default = 128
}

variable "timeout" {
  type    = number
  default = 3
}

output "name" {
  value = aws_lambda_function.default.function_name
}

output "output" {
  value = aws_lambda_function.default
}