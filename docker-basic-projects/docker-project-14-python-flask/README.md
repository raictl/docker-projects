Project 14: Containerize a Python Flask Application
Goal

Build and run a simple Python Flask web application using Docker.

Step 1: Build the image

docker build -t python-flask:v1 .

Step 2: Verify the image

docker images

Step 3: Run the container

docker run -d --name python-flask-container -p 5000:5000 python-flask:v1

Step 4: Verify

docker ps

Step 5: Open in your browser

http://localhost:5000

Expected output:

Docker Project 15

Hello from Flask!

Step 6: View logs

docker logs python-flask-container

Step 7: Stop and remove the container

docker stop python-flask-container
docker rm python-flask-container
