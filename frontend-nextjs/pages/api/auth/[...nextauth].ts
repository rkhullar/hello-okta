import NextAuth from 'next-auth'
import Providers from 'next-auth/providers'
import { NextApiRequest, NextApiResponse } from 'next'

const providers = [
  Providers.Okta({
    clientId: process.env.OKTA_CLIENT_ID,
    clientSecret: process.env.OKTA_CLIENT_SECRET,
    domain: `${process.env.OKTA_DOMAIN}/oauth2/default`
  })
]

const callbacks = {
  async jwt(token, user, account, profile, isNewUser) {
    if (account?.accessToken)
      token.accessToken = account.accessToken
    return token
  },
  async session(session, token) {
    session.accessToken = token.accessToken
    return session
  }
}

export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, {providers, callbacks})