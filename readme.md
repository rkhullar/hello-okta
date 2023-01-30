## Hello Okta

#### tool versions
- python 3.8.13
- node 16.15.1
- terraform 1.2.5

#### useful commands
- initialize frontend code
```shell
npx create-next-app frontend-nextjs
cd frontend-nextjs
touch tsconfig.json
npm install --save-dev typescript @types/react @types/node
npm run dev
```

##### 2023-01-29
```shell
cd frontend
npx create-next-app nextjs --ts --use-npm --eslint
cd nextjs
npm install @okta/okta-auth-js
npm install @okta/okta-react
#npm install react-router-dom@5

```

- upgrade global npm
```shell
npm install -g npm
```

- install serverless framework
```shell
npm install -g @serverless/cli
# asdf reshim nodejs
```

### okta notes

#### oidc web app config
##### [2023-01-29]
- grant types
  - Authorization Code
  - Refresh Token
- allowed signin urls
  - http://localhost:8000/authorization-code/callback
  - http://localhost:3000/api/auth/callback/okta
- require PKCE: disabled

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
##### [2021-12-11]
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

##### [2022-01-03]
Unfortunately there are flaws with the previous approach of filtering the groups claim for each application. The config
under the sign on tab for the filter only applies to the id token, not the access token. The following walks through
another approach for the group filtering.

To start we still want to leverage our custom groups claim within the authorization server config. However, we will use
an expression instead of a simple filter.
```
Groups.startsWith("OKTA", ((app.profile.group_prefix != null) ? app.profile.group_prefix : "tld"), 64)
```

The above expression filters the okta groups via dynamic prefix and limits the result set. If the application level
`group_prefix` is available, then we use it. Otherwise, we default to a hardcoded org level prefix. `app.profile` refers
to a dynamic map of application properties that can be managed programmatically via api key. It doesn't seem like that
functionality currently exists on the UI, at least not at the time of this writing. Here's an example python script to
set the `app.profile` [[link](backend-fastapi/spikes/app-profile-1.py)].

Another option is the substitute `app.profile` with `appuser.profile` in the expression. The advantage would be that
the required configuration to actually set the application level group prefix is already available in the UI. So there's
no need to use an api token and script. The disadvantage is that this results in duplicate hard coded data between users.
It also seems hacky to me since this config is really supposed to be at the application level. Using `appuser.profile`
allows for the `group_prefix` to actually be changed for users accessing the same application.

To use `appuser.profile` navigate to the profile editor for the application. Add a custom attribute for `group_prefix`
and set the data type to `string`. For the display name I'd suggest `Group Prefix`. After creating the attribute, update
the mapping for "Okta User -> {App} User" with the value for the group prefix. `"namespace-project" -> group_prefix`
For reference here are two screenshots:
- [attribute](docs/images/hello-world-profile.png)
- [mapping](docs/images/group-prefix-example.png)

#### links
- https://developer.okta.com/blog/2017/07/25/oidc-primer-part-1
- https://developer.okta.com/blog/2020/11/13/nextjs-typescript
- https://developer.okta.com/blog/2020/12/17/build-and-secure-an-api-in-python-with-fastapi
- https://developer.okta.com/docs/guides/customize-tokens-groups-claim/main
- https://developer.okta.com/docs/guides/protect-your-api/python/before-you-begin
- https://github.com/okta/samples-python-flask
- https://github.com/oktadev/okta-fastapi
- https://github.com/serverless-nextjs/serverless-next.js
- https://github.com/serverless-nextjs/serverless-next.js/issues/184
- https://github.com/serverless-nextjs/serverless-next.js/pull/649
- https://github.com/serverless/components
- https://github.com/vercel/next-learn
- https://nextjs.org/learn/basics/create-nextjs-app
