variable "prefix" {
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