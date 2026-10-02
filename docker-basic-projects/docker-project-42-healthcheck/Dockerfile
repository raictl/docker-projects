FROM nginx:alpine

RUN apk add --no-cache curl

HEALTHCHECK --interval=10s \
            --timeout=3s \
            --start-period=5s \
            --retries=3 \
            CMD curl -fsS http://127.0.0.1/ || exit 1

EXPOSE 80
