FROM nginx:alpine

LABEL maintainer="Ashutosh Rai"
LABEL project="Docker Project 28"
LABEL version="1.0.0"
LABEL description="Nginx image with Docker labels"

COPY index.html /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
