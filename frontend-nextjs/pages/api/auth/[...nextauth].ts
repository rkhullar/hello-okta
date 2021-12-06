import NextAuth from 'next-auth'
import OktaProvider from 'next-auth/providers/okta'
import { NextApiRequest, NextApiResponse } from 'next'

const providers = [
  OktaProvider({
    clientId: process.env.OKTA_CLIENT_ID,
    clientSecret: process.env.OKTA_CLIENT_SECRET,
    issuer: `https://${process.env.OKTA_DOMAIN}/oauth2/default`
  })
]

const callbacks = {
  async jwt({token, user, account, profile, isNewUser}) {
    console.log("inside jwt callback")
    console.log('token', token)
    console.log('user', user)
    console.log('account', account)
    console.log('profile', profile)
    console.log('isNewUser', isNewUser)
    if (account?.accessToken)
      token.accessToken = account.accessToken
    return token
  },
  async session({session, token, user}) {
    console.log("inside session callback")
    console.log('session', session)
    console.log('token', token)
    console.log('user', user)
    session.accessToken = token.accessToken
    return session
  }
}

const secret = process.env.NEXTAUTH_SECRET

// export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, {providers, callbacks, secret})
// export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, {providers, secret})

export default NextAuth({providers, callbacks, secret})
