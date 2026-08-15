import time
from datetime import datetime

FILE = "/shared/messages.txt"

while True:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(FILE, "a") as file:
        file.write(f"Writer container: {timestamp}\n")

    print(f"Written: {timestamp}")

    time.sleep(5)
