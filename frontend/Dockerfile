# ---- build stage -----------------------------------------------------------
FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci 2>/dev/null || npm install

COPY . .

# Vite inlines env vars at BUILD time, so the API URL must be passed here.
# This is the URL the *browser* uses to reach the API (not a docker-internal
# hostname), hence the localhost default.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ---- serve stage ------------------------------------------------------------
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
