FROM node as build

WORKDIR /pier
COPY ./package.json /pier/package.json

RUN yarn install
COPY . .
RUN yarn build --prod --aot=true

FROM nginx:alpine

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /pier/dist/pier /usr/share/nginx/html