# Get Bun image and install dependencies from lockfile
FROM oven/bun:1 AS build
WORKDIR /src
COPY package.json bun.lock ./
RUN bun install --frozen-lockfile

# Build static site using Bun
COPY . .
RUN bun run build

# Serve site with nginx, proxying /api to the backend
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /src/dist /usr/share/nginx/html
EXPOSE 80
