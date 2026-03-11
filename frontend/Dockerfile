# ---- Build stage ----
FROM node:20-slim AS build

WORKDIR /app

# Install dependencies first (better layer caching)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copy source (context is repo root)
COPY frontend/ .

ARG VITE_API_URL=""
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# ---- Production stage ----
FROM nginx:alpine

COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
