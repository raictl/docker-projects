FROM busybox:1.37

COPY website/ /www/

EXPOSE 8080

CMD ["httpd","-f","-v","-p","8080","-h","/www"]
