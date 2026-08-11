# Build Stage
FROM golang:1.24-alpine AS builder

WORKDIR /app

COPY . .

ENV CGO_ENABLED=0

RUN go build -o app .

# Runtime Stage
FROM scratch

COPY --from=builder /app/app /app

ENTRYPOINT ["/app"]
