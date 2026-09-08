from flask import Flask
import redis
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")

client = redis.Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)


@app.route("/")
def home():
    return "Hello from Flask + Redis!"


@app.route("/count")
def count():
    value = client.incr("visits")

    return f"Visitor count: {value}"


@app.route("/health")
def health():
    try:
        client.ping()
        return "Flask and Redis are healthy!"
    except Exception:
        return "Redis connection failed!", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
