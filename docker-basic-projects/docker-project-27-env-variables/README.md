Project 27: Build a Docker Image Using Environment Variables (ENV)

Goal

Use Docker environment variables to configure a container at runtime.

Step 1: Build the image

  #docker build -t flask-env:v1 .

Step 2: Run the container

Override the default environment variables:

  #docker run -d \
  --name flask-env-container \
  -p 5000:5000 \
  -e APP_NAME="My Docker App" \
  -e APP_ENV="production" \
  -e APP_VERSION="2.0.0" \
  flask-env:v1


Step 3: Verify

  #docker ps


Step 4: Test the application

  #http://localhost:5000

Step 5: Verify environment variables inside the container

  #docker exec flask-env-container env

Step 6: Stop and remove the container

  #docker stop flask-env-container
  #docker rm flask-env-container



