Project 30: Persist Container Data Using Docker Volumes


Goal

Learn how to use a named Docker volume so that data persists even after the container is removed.


Step 1: Build the image
  
  #docker build -t flask-volume:v1 .

Step 2: Create a Docker volume

  #docker volume create flask-data

Step 3: Verify the volume

  #docker volume ls

Step 4: Run the container with the volume

  #docker run -d \
  --name flask-volume-container \
  -p 5000:5000 \
  -v flask-data:/data \
  flask-volume:v1

Step 5: Test persistence

  #http://localhost:5000

  Refresh the page several times.

  The Total Visits count should increase.

Step 6: Remove the container

  #docker stop flask-volume-container
  #docker rm flask-volume-container

Step 7: Start a new container using the same volume

  #docker run -d \
  --name flask-volume-container-2 \
  -p 5000:5000 \
  -v flask-data:/data \
  flask-volume:v1

  Open:

   http://localhost:5000
✅ Verify that the visit count continues from the previous value instead of starting at 1.

Step 8: Inspect the volume

  #docker volume inspect flask-data

Step 9: List volumes

  #docker volume ls

Step 10: Clean up

  #docker stop flask-volume-container-2
  #docker rm flask-volume-container-2


