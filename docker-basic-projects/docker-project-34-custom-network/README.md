Project 34: Create a Custom Docker Network and Connect Containers

Goal

Create a custom Docker bridge network and run two containers on it so they can communicate with each other using container names.


Step 1: Build the Docker image

#docker build -t custom-network-demo:v1 .

Step 2: Create a custom Docker network

#docker network create custom-app-network

Verify:

#docker network ls

Step 3: Inspect the network

#docker network inspect custom-app-network

Initially, no application containers should be connected.

Step 4: Start the server container

#docker run -d \
  --name server-container \
  --network custom-app-network \
  custom-network-demo:v1 \
  python server.py

Verify:

#docker ps

Step 5: Start the client container

#docker run -d \
  --name client-container \
  --network custom-app-network \
  custom-network-demo:v1 \
  python client.py

Step 6: Verify both containers

# docker ps

Step 7: Check client logs

#docker logs client-container

Step 8: Test communication manually

Execute a command inside the client container:

#docker exec client-container python -c "import urllib.request; print(urllib.request.urlopen('http://server-container:8080').read().decode())"

Expected:

Hello from the server container!

Step 9: Verify the network members

#docker network inspect custom-app-network

Step 10: Test the server container's hostname

#docker exec client-container getent hosts server-container

Step 11: Stop the containers

#docker stop client-container server-container

Step 12: Remove the containers

#docker rm client-container server-container

Step 13: Remove the custom network

#docker network rm custom-app-network


