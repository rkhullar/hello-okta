/*
 * NOTE: attempt to inject environment vars from aws secret manager
 * https://github.com/serverless-nextjs/serverless-next.js/pull/649
 */

const AWS = require('aws-sdk')
const originalLambda = require('./index')

// START - Secrets Lib - # without TS
const secrets_manager = new AWS.SecretsManager({region: 'us-east-1'})

async function read_secret_arn(name) {
  const filter = {Key: 'name', Values: [name]}
  const response = await secrets_manager.listSecrets({MaxResults: 1, Filters: [filter]})
  const secret_data = response.SecretList[0]
  return secret_data.ARN
}

async function load_secret_arn(arn) {
  const response = await secrets_manager.getSecretValue({SecretId: arn})
  return JSON.parse(response.SecretString)
}

async function load_secret(name) {
  const arn = await read_secret_arn(name)
  return await load_secret_arn(arn)
}
// END - Secrets Lib

function set_env(key, val) {
  process.env[key] = val
}

function inject_envs(data) {
  // TODO: cleanup with loop?
  set_env('OKTA_DOMAIN', data.okta_domain)
  set_env('OKTA_DOMAIN', data.okta_domain)
  set_env('OKTA_CLIENT_ID', data.okta_client_id)
  set_env('OKTA_CLIENT_SECRET', data.okta_client_secret)
  set_env('NEXTAUTH_URL', data.next_auth_url)
  set_env('NEXTAUTH_SECRET', data.next_auth_secret)
  set_env('FASTAPI_URL', data.fast_api_url)
  // TODO: inject metadata: project and environment
}

let state_counter = 0

exports.handler = async function(event, context) {
  console.log("inside custom handler")
  console.log(context)

  // TODO: dynamically infer secret name somehow; should work with multiple environments
  const secret_name = 'serverless-poc-nextjs-sbx'
  if (!state_counter) {
    const secret_data = await load_secret(secret_name)
    inject_envs(secret_data)
  }

  context.callbackWaitsForEmptyEventLoop = false // TODO: verify needed
  return originalLambda.handler(event, context)
}