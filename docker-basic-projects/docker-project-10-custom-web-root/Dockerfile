FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/html

COPY website/ /var/www/html/

EXPOSE 80

CMD ["nginx","-g","daemon off;"]
