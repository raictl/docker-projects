Project 28: Build a Docker Image with Labels (LABEL)

Goal

Add metadata to a Docker image using the LABEL instruction and inspect it.

Step 1: Build the image

  #docker build -t nginx-labels:v1 .

Step 2: Run the container

  #docker run -d --name nginx-labels-container -p 8080:80 nginx-labels:v1

Step 3: Verify

  #docker ps

Step 4: Test the application

  #http://localhost:8080

Step 5: Inspect the labels

  #docker image inspect nginx-labels:v1
OR
  #docker image inspect nginx-labels:v1

Step 6: Stop and remove the container

  #docker stop nginx-labels-container
  #docker rm nginx-labels-container


