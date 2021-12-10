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