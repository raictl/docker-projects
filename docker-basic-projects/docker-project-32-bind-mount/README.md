Project 32: Bind Mount a Host Directory into a Container

Goal

Use a host directory as storage for a container and verify that changes made on the host are immediately visible inside the container.

Step 1: Build the image

  #docker build -t nginx-bind-mount:v1 .

Step 2: Run the container with a bind mount

  From inside the project directory:
  #docker run -d \
  --name nginx-bind-container \
  -p 8080:80 \
  -v "$(pwd)/website:/usr/share/nginx/html" \
  nginx-bind-mount:v1

Step 3: Verify the container

  #docker ps

Step 4: Test the website

  Open-
  #http://localhost:8080

Step 5: Modify the file on the host

  Edit:
  website/index.html

  <p>This website is stored on the Docker host.</p>

  to:

  <p>This content was changed directly on the Docker host.</p>

Step 6: Test again

  Refresh:
  http://localhost:8080

Step 7: Verify from inside the container

  #docker exec nginx-bind-container cat /usr/share/nginx/html/index.html

Step 8: Test container → host synchronization

  #docker exec nginx-bind-container sh -c 'echo "<p>Added from inside the container.</p>" >> /usr/share/nginx/html/index.html'

  Now check the host file:

  #cat website/index.html

Step 9: Stop and remove the container

  #docker stop nginx-bind-container
  #docker rm nginx-bind-container

Step 10: Verify the host data still exists

  #cat website/index.html

#The file should still contain your changes.





