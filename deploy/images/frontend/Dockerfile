FROM node:13-alpine

ADD ./src/frontend /app

WORKDIR /app

RUN yarn install

CMD ["yarn", "start"]
