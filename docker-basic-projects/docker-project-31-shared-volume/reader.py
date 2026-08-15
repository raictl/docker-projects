import time

FILE = "/shared/messages.txt"

while True:
    print("\n===== Shared File Content =====")

    try:
        with open(FILE, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("File does not exist yet.")

    print("==============================")

    time.sleep(5)
