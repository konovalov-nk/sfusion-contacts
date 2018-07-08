FROM node:alpine
MAINTAINER Nikolay Konovalov <konovalov.nk@gmail.com>

WORKDIR /usr/app

COPY ./package.json ./
RUN npm install --quiet

COPY ./ ./

EXPOSE 8004