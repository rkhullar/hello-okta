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

output "default" {
  value = aws_secretsmanager_secret.default
}