FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf

COPY ssl/ /etc/nginx/ssl/

COPY website/ /usr/share/nginx/html/

EXPOSE 443

CMD ["nginx","-g","daemon off;"]
