Project 29: Use .dockerignore to Exclude Files from the Docker Build Context

Goal

Prevent unnecessary files from being sent to the Docker daemon during image builds using .dockerignore.

Step 1: Build the image

  #docker build -t dockerignore-demo:v1 .

Step 2: Run the container

  #docker run -d --name dockerignore-container -p 8080:80 dockerignore-demo:v1

Step 3: Verify

  #docker ps

Step 4: Verify ignored files

  #docker exec dockerignore-container ls -R /usr/share/nginx/html

  Verify:

✅ Present:

    index.html

❌ Not present:

    secret.txt

    notes.md

    temp/


Step 5: Open the application

  #http://localhost:8080

Step 6: Stop and remove the container

  #docker stop dockerignore-container
  #docker rm dockerignore-container


