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

output "name" {
  value = aws_s3_bucket.default.bucket
}

output "output" {
  value = aws_s3_bucket.default
}