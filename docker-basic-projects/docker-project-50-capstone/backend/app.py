import os
from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppassword")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    return jsonify({
        "application": "Docker Capstone",
        "status": "running"
    })


@app.route("/db")
def database():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT message FROM messages ORDER BY id LIMIT 1")
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "database": "PostgreSQL",
            "message": result[0]
        })

    except Exception as error:
        return jsonify({
            "database": "PostgreSQL",
            "status": "error",
            "error": str(error)
        }), 500


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
