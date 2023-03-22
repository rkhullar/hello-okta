import NextAuth from 'next-auth'
import OktaProvider from 'next-auth/providers/okta'
import { NextApiRequest, NextApiResponse } from 'next'

function read_issuer_url() {
  const default_issuer = `https://${process.env.OKTA_DOMAIN}/oauth2/default`
  const custom_issuer = process.env.OKTA_ISSUER_URL
  if (custom_issuer !== undefined)
    return custom_issuer
  return default_issuer
}

const providers = [
  OktaProvider({
    clientId: process.env.OKTA_CLIENT_ID,
    clientSecret: '',
    // wellKnown: 'https://auth.nydev.me/oauth2/default/.well-known/openid-configuration',
    issuer: read_issuer_url(),
    authorization: { params: { scope: 'openid email profile offline_access' } },
    idToken: true,
    checks: ['pkce', 'state'],
    client: {
      token_endpoint_auth_method: 'none'
    }
  })
]

const callbacks = {
  async jwt({token, account}) {
    // TODO: add types?
    console.log('inside jwt hook')
    if (account) {
      token.id_token = account.id_token
      token.access_token = account.access_token
    }
    return token
  },
  async session({session, token, user}) {
    // TODO: add types?
    console.log('inside session hook')
    session.id_token = token.id_token
    session.access_token = token.access_token
    console.log(token)
    return session
  }
}

const secret = process.env.NEXTAUTH_SECRET

export default NextAuth({providers, callbacks, secret})
// export default (req: NextApiRequest, res: NextApiResponse) => NextAuth(req, res, {providers, callbacks, secret})
