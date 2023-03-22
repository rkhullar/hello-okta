import { NextApiRequest, NextApiResponse } from 'next'

export default (req: NextApiRequest, res: NextApiResponse) => {
  res.status(200).json({ message: 'hello world', fastapi_url: process.env.FASTAPI_URL })
}