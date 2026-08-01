FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/site1 /var/www/site2

COPY websites/site1/ /var/www/site1/
COPY websites/site2/ /var/www/site2/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
