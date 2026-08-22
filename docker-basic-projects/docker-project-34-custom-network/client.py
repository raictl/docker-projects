import urllib.request
import time

SERVER_URL = "http://server-container:8080"

while True:
    try:
        response = urllib.request.urlopen(SERVER_URL)
        message = response.read().decode()

        print(f"Response from server: {message}")

    except Exception as error:
        print(f"Connection failed: {error}")

    time.sleep(5)


