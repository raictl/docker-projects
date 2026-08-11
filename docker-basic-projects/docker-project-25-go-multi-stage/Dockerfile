# ---------- Build Stage ----------
FROM golang:1.24-alpine AS builder

WORKDIR /app

COPY . .

ENV CGO_ENABLED=0

RUN go build -o server .

# ---------- Runtime Stage ----------
FROM alpine:3.22

WORKDIR /app

COPY --from=builder /app/server .

EXPOSE 8080

CMD ["./server"]
