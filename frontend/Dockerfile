# Multi-stage build: this project uses Yarn (see package.json's
# "packageManager" field and the "resolutions" block, which npm ignores —
# installing with npm instead of yarn silently breaks dependency resolution).
FROM node:20-slim AS build
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
# REACT_APP_BACKEND_URL is baked in at build time (CRA convention) — set it
# as a build ARG/env var on your host before building, not at container run time.
ARG REACT_APP_BACKEND_URL
ENV REACT_APP_BACKEND_URL=${REACT_APP_BACKEND_URL}
RUN yarn build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
