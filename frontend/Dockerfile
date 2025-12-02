FROM node:18-alpine as build
WORKDIR /app
COPY frontend/package.json .
COPY frontend/package-lock.json* ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
# default nginx config serves static files
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
