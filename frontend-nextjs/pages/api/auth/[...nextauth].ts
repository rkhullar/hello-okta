import NextAuth from 'next-auth'
import OktaProvider from 'next-auth/providers/okta'
import GoogleProvider from 'next-auth/providers/google'
import { NextApiRequest, NextApiResponse } from 'next'

const providers = [
  OktaProvider({
    clientId: process.env.OKTA_CLIENT_ID,
    clientSecret: process.env.OKTA_CLIENT_SECRET,
    issuer: `https://${process.env.OKTA_DOMAIN}/oauth2/default`
  }),
  GoogleProvider({
    clientId: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET
  })
]

const callbacks = {
  async jwt({token, account}) {
    // TODO: add types?
    if (account)
      token.access_token = account.access_token
    return token
  },
  async session({session, token, user}) {
    // TODO: add types?
    session.access_token = token.access_token
    return session
  }
}

const secret = process.env.NEXTAUTH_SECRET

export default NextAuth({providers, secret})
// export default NextAuth({providers, callbacks, secret})
// export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, {providers, callbacks, secret})
