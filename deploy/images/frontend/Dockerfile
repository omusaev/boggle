FROM node:13-alpine

RUN npm install -g serve

ADD ./src/frontend /app

WORKDIR /app

RUN yarn install
RUN yarn build

CMD ["serve", "-s", "build", "-l", "3000"]
