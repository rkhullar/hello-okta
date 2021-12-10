/*
 * NOTE: attempt to inject environment vars from aws secret manager
 * https://github.com/serverless-nextjs/serverless-next.js/pull/649
 */

const originalLambda = require('./index')

process.env.TEST_ENV = 'sbx'

exports.handler = async function(event, context) {
  console.log("inside custom handler")
  context.callbackWaitsForEmptyEventLoop = false // TODO: verify needed
  return originalLambda.handler(event, context)
}