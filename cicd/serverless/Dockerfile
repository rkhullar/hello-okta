ARG NODE_VERSION='16.13.1'
FROM node:${NODE_VERSION}-alpine
WORKDIR /root
RUN npm install -g serverless
ENTRYPOINT ["serverless"]
