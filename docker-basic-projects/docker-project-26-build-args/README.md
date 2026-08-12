Project 26: Build a Docker Image Using Build Arguments (ARG) Goal

Pass values to the Docker image at build time using ARG.

Step 1: Build the image

  #docker build \
  --build-arg APP_VERSION=2.5.1 \
  --build-arg APP_ENV=production \
  -t nginx-build-args:v1 .

Step 2: Run the container

  #docker run -d --name nginx-build-args-container -p 8080:80 nginx-build-args:v1

Step 3: Verify

  #docker ps

Step 4: Open in your browser

  #http://localhost:8080

Step 5: Inspect the image history

  #docker history nginx-build-args:v1

Step 6: Stop and remove the container

  #docker stop nginx-build-args-container
  #docker rm nginx-build-args-container


