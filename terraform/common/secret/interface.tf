variable "name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "data" {
  type = map(string)
}

variable "preserve" {
  type    = list(string)
  default = null
}

variable "ignore" {
  type    = list(string)
  default = null
}

output "name" {
  value = aws_secretsmanager_secret.default.name
}

output "output" {
  value = aws_secretsmanager_secret.default
}