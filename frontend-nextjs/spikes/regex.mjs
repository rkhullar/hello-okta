function parse_lambda_function_name(name) {
  const pattern = /^(?<region>[\w-]+)\.(?<prefix>[\w-]+)-(?<base>api|default)-(?<suffix>[\w-]+)$/s
  const match_object = name.match(pattern)
  if (!match_object)
    throw {detail: 'bad name', example: 'serverless-poc-api-sbx', found: text}
  return match_object.groups
}

try {
  const test_input = 'us-east-1.serverless-poc-api-sbx'
  const result = parse_lambda_function_name(test_input)
  console.log(result)
  const secret_target = `${result.prefix}-nextjs-${result.suffix}`
  console.log(secret_target)
} catch (err) {
  console.log(err)
}