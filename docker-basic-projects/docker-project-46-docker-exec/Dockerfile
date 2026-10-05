FROM alpine:3.22

ENV APP_NAME="docker-exec-demo"

WORKDIR /app

RUN echo "Hello from Docker container" > /app/message.txt

CMD ["sh", "-c", "while true; do echo 'Application is running'; sleep 10; done"]
