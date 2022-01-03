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

variable "enable" {
  type    = bool
  default = true
}

variable "tracking" {
  type    = string
  default = "preserve"
  validation {
    condition     = contains(["preserve", "ignore"], var.tracking)
    error_message = "The tracking value must be within [preserve, ignore]."
  }
}

variable "preserve" {
  type     = list(string)
  nullable = false
  default  = []
}

variable "ignore" {
  type     = list(string)
  nullable = false
  default  = []
}

output "name" {
  value = aws_secretsmanager_secret.default.name
}

output "output" {
  value = aws_secretsmanager_secret.default
}