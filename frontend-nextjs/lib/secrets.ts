import { SecretsManager } from "@aws-sdk/client-secrets-manager"
const secrets_manager = new SecretsManager({region: 'us-east-1'});

async function read_secret_arn(name: string): string {
  const filter = {Key: 'name', Values: [name]}
  const response = await secrets_manager.listSecrets({MaxResults: 1, Filters: [filter]})
  const secret_data = response.SecretList[0]
  return secret_data.ARN
}

async function load_secret_arn(arn: string) {
  const response = await secrets_manager.getSecretValue({SecretId: arn})
  return JSON.parse(response.SecretString)
}

async function load_secret(name: string) {
  arn = await read_secret_arn(name)
  return await load_secret_arn(arn)
}