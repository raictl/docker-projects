# -------------------------
# Stage 1: Builder
# -------------------------
FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod .
COPY main.go .

RUN go build -o app main.go


# -------------------------
# Stage 2: Runtime
# -------------------------
FROM alpine:3.20

WORKDIR /app

COPY --from=builder /app/app .

EXPOSE 8080

CMD ["./app"]
