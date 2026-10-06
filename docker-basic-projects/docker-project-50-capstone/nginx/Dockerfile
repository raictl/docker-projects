FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/default.conf

HEALTHCHECK --interval=10s \
            --timeout=3s \
            --start-period=5s \
            --retries=3 \
            CMD wget -qO- http://127.0.0.1/ || exit 1

EXPOSE 80
