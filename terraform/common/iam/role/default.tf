resource "aws_iam_role" "default" {
  name                  = var.name
  tags                  = var.tags
  assume_role_policy    = coalesce(var.trust, data.aws_iam_policy_document.trust.json)
  force_detach_policies = true
}

resource "aws_iam_role_policy_attachment" "default" {
  for_each   = var.policies
  role       = aws_iam_role.default.name
  policy_arn = each.value
}

resource "aws_iam_role_policy_attachment" "managed" {
  for_each   = toset(var.managed_policies)
  role       = aws_iam_role.default.name
  policy_arn = "arn:aws:iam::aws:policy/${each.value}"
}

resource "aws_iam_role_policy" "managed" {
  for_each = var.inline_policies
  name     = each.key
  policy   = each.value
  role     = aws_iam_role.default.name
}

resource "aws_iam_instance_profile" "default" {
  count = var.instance_profile ? 1 : 0
  name  = aws_iam_role.default.name
  role  = aws_iam_role.default.name
}

data "aws_iam_policy_document" "trust" {
  statement {
    actions = ["sts:AssumeRole"]
    dynamic "principals" {
      for_each = var.principals
      content {
        type        = principals.value.type
        identifiers = principals.value.identifiers
      }
    }
  }
}