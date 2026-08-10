Project 23: Containerize a Static Website Using BusyBox HTTP Server
Goal

Serve a static website using the lightweight BusyBox HTTP server.

Step 1: Build the image

  #docker build -t busybox-httpd:v1 .

Step 2: Run the container

  #docker run -d \
  --name busybox-httpd-container \
  -p 8080:8080 \
  busybox-httpd:v1

Step 3: Verify

  #docker ps

Step 4: est the application

  #http://localhost:8080

Step 5: View logs

  #docker logs busybox-httpd-container

Step 6: Verify website files
  
  #docker exec busybox-httpd-container ls -l /www

Step 7: Stop and remove the container

  #docker stop busybox-httpd-container
  #docker rm busybox-httpd-container




