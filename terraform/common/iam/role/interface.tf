variable "name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "principals" {
  type    = list(object({ type = string, identifiers = list(string) }))
  default = []
}

variable "trust" {
  type    = string
  default = null
}

variable "policies" {
  type    = map(string)
  default = {}
}

variable "managed_policies" {
  type    = list(string)
  default = []
}

variable "inline_policies" {
  type    = map(string)
  default = {}
}

variable "instance_profile" {
  type    = bool
  default = false
}

output "default" {
  value = aws_iam_role.default
}

output "profile" {
  value = var.instance_profile ? aws_iam_instance_profile.default[0] : null
}