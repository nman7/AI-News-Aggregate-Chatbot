# Stage 1: Build React app
FROM node:18-alpine AS build

WORKDIR /app

# Only copy what's needed for npm install first
COPY package*.json ./
RUN npm install

# Then copy the rest
COPY . .
RUN npm run build

# Stage 2: Serve with NGINX (tiny image)
FROM nginx:alpine

# Clean default nginx config (optional)
RUN rm -rf /usr/share/nginx/html/*

# Copy built React app
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
