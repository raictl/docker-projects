Project 31: Share Data Between Two Containers Using the Same Docker Volume

Goal

Run two containers that use the same Docker named volume and verify that both containers can read and modify the same data.

Step 1: Build the image

  #docker build -t shared-volume:v1 .

Step 2: Create the Docker volume

  #docker volume create shared-data

Verify:

  #docker volume ls

Expected:

  shared-data

Step 3: Start the writer container

  #docker run -d \
  --name writer-container \
  -v shared-data:/shared \
  shared-volume:v1 \
  python writer.py

Step 4: Start the reader container

  #docker run -d \
  --name reader-container \
  -v shared-data:/shared \
  shared-volume:v1 \
  python reader.py

Step 5: Verify both containers

  #docker ps

Step 6: Check writer logs

  #docker logs writer-container

Step 6: Check reader logs

  #docker logs reader-container

Step 7: Verify the shared file directly

  #docker exec writer-container cat /shared/messages.txt

Now verify from the reader container:

  #docker exec reader-container cat /shared/messages.txt

Both commands should return the same content.

Step 8: Add data from the reader container

  #docker exec reader-container sh -c 'echo "Message added by reader container" >> /shared/messages.txt'

Now check from the writer container:

  #docker exec writer-container cat /shared/messages.txt

You should see:

Message added by reader container

This confirms both containers are accessing the same volume.

Step 9: Stop the containers

  #docker stop writer-container reader-container

Step 10: Remove the containers

  #docker rm writer-container reader-container

Step 11: Verify the volume still exists

  #docker volume ls

You should still see:

shared-data


