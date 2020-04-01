FROM node:13-alpine

RUN npm install -g serve

ADD ./src/frontend /app

WORKDIR /app

ARG apiBaseUrl
ENV REACT_APP_API_BASE_URL=$apiBaseUrl

ARG siteUrl
ENV REACT_APP_SITE_URL=$siteUrl

RUN yarn install
RUN yarn build

CMD ["serve", "-s", "build", "-l", "3000"]
