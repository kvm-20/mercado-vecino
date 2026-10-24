# syntax=docker/dockerfile:1

# ---------- Etapa 1: compilación ----------
# Node solo se usa para compilar; no llega a la imagen final.
FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
# npm ci instala exactamente lo que dice package-lock.json (reproducible)
RUN npm ci
COPY . .
# Las variables VITE_* quedan incrustadas en el JavaScript público: nunca un secreto
ARG VITE_API_URL=/api
ENV VITE_API_URL=${VITE_API_URL}
RUN npm run build

# ---------- Etapa 2: servidor estático ----------
# nginx-unprivileged corre como usuario no root y escucha en 8080
FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
