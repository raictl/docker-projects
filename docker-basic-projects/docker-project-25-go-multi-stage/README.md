Project 25: Build a Multi-Stage Docker Image for a Go Application
Goal

Use a multi-stage build to compile a Go application and produce a small runtime image.


Step 1: Build the image

  #docker build -t go-multistage:v1 .

Step 2: Verify the image

  #docker images

Step 3: Run the container

  #docker run -d \
  --name go-multistage-container \
  -p 8080:8080 \
  go-multistage:v1

Step 4: Test the application

  #http://localhost:8080

Step 5: View logs

  #docker logs go-multistage-container

Step 6: Stop and remove the container

  #docker stop go-multistage-container
  #docker rm go-multistage-container


