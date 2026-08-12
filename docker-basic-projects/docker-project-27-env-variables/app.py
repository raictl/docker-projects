from flask import Flask
import os

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Unknown")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

@app.route("/")
def home():
    return f"""
    <h1>{APP_NAME}</h1>
    <p>Environment: {APP_ENV}</p>
    <p>Version: {APP_VERSION}</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
