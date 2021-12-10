/*
 * NOTE: attempt to inject environment vars from aws secret manager
 * https://github.com/serverless-nextjs/serverless-next.js/pull/649
 */

const originalLambda = require('./index')
import { load_secret } from '$lib/secrets'

// TODO: dynamically infer secret name somehow; should work with multiple environments
const secret_name = 'serverless-poc-hello-sbx'
const secret_data = load_secret(secret_name)

process.env.OKTA_DOMAIN = secret_data.okta_domain
process.env.OKTA_CLIENT_ID = secret_data.okta_client_id
process.env.OKTA_CLIENT_SECRET = secret_data.okta_client_secret
process.env.NEXTAUTH_URL = secret_data.next_auth_url
process.env.NEXTAUTH_SECRET = secret_data.next_auth_secret
process.env.FASTAPI_URL = secret_data.fast_api_url

exports.handler = async function(event, context) {
  console.log("inside custom handler")
  context.callbackWaitsForEmptyEventLoop = false // TODO: verify needed
  return originalLambda.handler(event, context)
}