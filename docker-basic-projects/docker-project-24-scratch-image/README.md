Project 24: Build a Minimal Docker Image Using scratch
Goal

Build your smallest possible Docker image using the scratch base image and a statically compiled Go application.


Step 1: Build the image

  #docker build -t scratch-app:v1 .

Step 2: Verify the image

  #docker images

Step 3: Run the container

  #docker run --name scratch-app-container scratch-app:v1

Step 4: Verify the container

  #docker ps -a

Step 5: Inspect the image

  #docker image inspect scratch-app:v1

Step 6: Remove the container

  #docker rm scratch-app-container


