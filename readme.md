## Hello Okta

#### tool versions
- python 3.8.12
- node 16.13.0

#### useful commands
- initialize frontend code
```sh
npx create-next-app frontend-nextjs
cd frontend-nextjs
touch tsconfig.json
npm install --save-dev typescript @types/react @types/node
npm run dev
```

### okta notes

#### group naming convention
I've opted for the following pattern to avoid name collisions between teams:
{namespace}-{project}-{name}

The main purpose of the namespace is to organize the groups by department or team name. It also distinguishes between
the default okta groups like "Everyone". I would use the company name or top level domain (`tld`) as the namespace.

Examples:
- tld-devops-blue
- tld-devops-green
- tld-cloud-purple

#### include groups in access token
After creating an application configure it under the "Sign On" tab to set the `groups` claim on the token. We want to
include only the groups that are relevant to our application / project. 
- group claims type: filter
- group claims filter: starts with `namespace-project`

The default config for the authorization servers does not include groups in the access token.
In the okta admin ui you can navigate to the config under security -> api or go to the following url:
https://{company}-admin.okta.com/admin/oauth2/as

Edit the default authorization server by adding a `claim` for `groups`. The only other claim that should exist is `sub`.
The `groups` claim should have the following settings:
- name: groups
- include in token type: access Token
- value type: groups
- filter: starts with `namespace`
- include in: any scope

Test the config using the Token Preview tab in the UI. The form has four inputs to fill out:
- oauth/oidc client: {client} i.e: HelloWorld
- grant type: authorization code
- user: {email}
- scopes: openid

The preview should show two tabs for the `id_token` and `token`. The `token` should include the `groups` claim.

#### links
- https://developer.okta.com/docs/guides/protect-your-api/python/before-you-begin/
- https://github.com/okta/samples-python-flask
- https://github.com/oktadev/okta-fastapi
- https://nextjs.org/learn/basics/create-nextjs-app
- https://github.com/vercel/next-learn
- https://github.com/serverless-nextjs/serverless-next.js
- https://developer.okta.com/blog/2020/11/13/nextjs-typescript
- https://developer.okta.com/blog/2020/12/17/build-and-secure-an-api-in-python-with-fastapi
- https://developer.okta.com/blog/2017/07/25/oidc-primer-part-1
