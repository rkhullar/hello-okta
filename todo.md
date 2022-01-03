## High Level TODOs
- [x] dockerize fastapi backend
- [x] deploy nextjs to AWS cloudfront and lambda via [serverless-nextjs][]
  - look into sls-core
- [ ] look more into keeping the user session active with refresh tokens
- [ ] improve nextjs project structure
  - move code under `src`
  - set build output to `dist` instead of `_next`
- [ ] try django implementation or remove
- [ ] archive `learn-nextjs` or move to its own repo
- [ ] revisit terraform secret manager module
  - try to work around unknown value error without enable flag
  - or only use enable flag without ignore / preserve logic



[serverless-nextjs]: https://github.com/serverless-nextjs/serverless-next.js