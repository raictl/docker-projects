Project 23: Containerize a Java Servlet Application Using Tomcat
Goal

Deploy a simple Java web application (.war) on an Apache Tomcat container.


Step 1: Build the image

  #docker build -t tomcat-webapp:v1 .

Step 2: Run the container

  #docker run -d \
  --name tomcat-webapp-container \
  -p 8080:8080 \
  tomcat-webapp:v1

Step 3: Verify

  #docker ps

Step 4: Test the application

  #http://localhost:8080

Step 4: View logs

  #docker logs tomcat-webapp-container

Step 5: Verify Tomcat process

  #docker exec tomcat-webapp-container ps -ef

Step 6: Stop and remove the container

  #docker stop tomcat-webapp-container
  #docker rm tomcat-webapp-container


