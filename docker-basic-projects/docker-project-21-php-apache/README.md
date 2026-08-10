Project 22: Containerize a PHP + Apache Web Application
Goal

Build and run a simple PHP web application using the official PHP-Apache Docker image.



Step 1: Build the image

  #docker build -t php-apache:v1 .

Step 2: Run the container

  #docker run -d \
  --name php-apache-container \
  -p 8080:80 \
  php-apache:v1

Step 3: Verify

  #docker ps

Step 4: Test the application

  http://localhost:8080

Step 5: View logs

  #docker logs php-apache-container

Step 6: Verify Apache is running

  #docker exec php-apache-container ps -ef

Step 7: Stop and remove the container

  #docker stop php-apache-container
  #docker rm php-apache-container


