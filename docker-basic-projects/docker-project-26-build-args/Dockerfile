FROM nginx:alpine

ARG APP_VERSION=1.0.0
ARG APP_ENV=development

COPY index.html /usr/share/nginx/html/index.html

RUN sed -i "s/APP_VERSION/${APP_VERSION}/g" /usr/share/nginx/html/index.html && \
    sed -i "s/APP_ENV/${APP_ENV}/g" /usr/share/nginx/html/index.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
