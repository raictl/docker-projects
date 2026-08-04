from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "project": "Docker Project 16",
        "message": "Welcome to the Flask REST API"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })

@app.route("/version")
def version():
    return jsonify({
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
