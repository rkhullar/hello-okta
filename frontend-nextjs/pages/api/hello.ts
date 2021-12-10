import { NextApiRequest, NextApiResponse } from 'next'

function setEnv(key: string, val: string) {
  process.env[key] = val
}

// setEnv('TEST_ENV', 'dev')

export default (req: NextApiRequest, res: NextApiResponse) => {
  res.status(200).json({ message: 'hello world', environment: process.env.TEST_ENV })
}