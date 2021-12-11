variable "name" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}

variable "policy" {
  type    = string
  default = null
}

variable "attach_policy" {
  type    = bool
  default = false
}

output "output" {
  value = aws_s3_bucket.default
}