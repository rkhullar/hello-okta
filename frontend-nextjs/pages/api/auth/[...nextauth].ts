import NextAuth from 'next-auth'
import OktaProvider from 'next-auth/providers/okta'
import { NextApiRequest, NextApiResponse } from 'next'

const options = {
  providers: [
    OktaProvider({
      clientId: process.env.OKTA_CLIENT_ID,
      clientSecret: process.env.OKTA_CLIENT_SECRET,
      domain: `${process.env.OKTA_DOMAIN}/oauth2/default`
    })
  ]
}

export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, options)