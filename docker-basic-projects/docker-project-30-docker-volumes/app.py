from flask import Flask
import os

app = Flask(__name__)

DATA_DIR = "/data"
FILE_NAME = os.path.join(DATA_DIR, "visits.txt")

os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/")
def home():
    count = 0

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            count = int(f.read())

    count += 1

    with open(FILE_NAME, "w") as f:
        f.write(str(count))

    return f"""
    <h1>Docker Project 30</h1>
    <h2>Persistent Volume Demo</h2>
    <h3>Total Visits: {count}</h3>
    """

app.run(host="0.0.0.0", port=5000)
