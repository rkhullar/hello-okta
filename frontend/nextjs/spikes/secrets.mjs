import { SecretsManager } from "@aws-sdk/client-secrets-manager"
const secrets_manager = new SecretsManager({region: 'us-east-1'});

async function read_meta() {
  const params = {
    MaxResults: 1
  }
  const response = await secrets_manager.listSecrets(params)
  const secret_data = response.SecretList[0]
  return {arn: secret_data.ARN, name: secret_data.Name}
}

async function read_secret_arn(name) {
  const filter = {Key: 'name', Values: [name]}
  const response = await secrets_manager.listSecrets({MaxResults: 1, Filters: [filter]})
  const secret_data = response.SecretList[0]
  return secret_data.ARN
}

async function load_secret(target) {
  const response = await secrets_manager.getSecretValue({SecretId: target})
  return JSON.parse(response.SecretString)
}

/*
const meta = await read_meta()
console.log(meta)

const result = await load_secret(meta.arn)
console.log(result)
*/

const name = 'serverless-poc-hello-sbx'
const secret_arn = await read_secret_arn(name)
const result = await load_secret(secret_arn)
console.log(result)
