Project 35: Container-to-Container Communication

Goal

Create two Docker containers:

web → Nginx
app → simple HTTP backend

Connect both containers using a custom Docker network and verify that web can communicate with app using the container name.

1. Build Backend Image

#docker build -t container-communication-app:1.0 ./app

Verify:
#docker images container-communication-app

2. Create Docker Network

#docker network create communication-net

Verify:
#docker network ls

3. Start Backend Container

#docker run -d \
  --name app \
  --network communication-net \
  container-communication-app:1.0


Verify:
#docker ps

4. Start Nginx Container

#docker run -d \
  --name web \
  --network communication-net \
  nginx:alpine

Verify:
#docker ps

5. Test Container-to-Container Communication

#docker exec -it web sh

Inside the container, install curl:

#apk add --no-cache curl

Now communicate with the backend using its container name:

#curl http://app:5000

6. Test Using Container IP

#docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' app

Example:
172.18.0.2

You can also test using the IP:

#docker exec web curl http://172.18.0.2:5000

NOTE- The IP can change when the container is recreated. The container name app is better for this project.

7. Verify Network Membership

#docker network inspect communication-net

Look for both containers:
app
web

8. Verify DNS Resolution

Docker's custom network provides container-name resolution.
RUN:
#docker exec web getent hosts app

Example:

172.18.0.2    app

This confirms that:

web → app

can resolve the backend container by name.

9. Cleanup

#docker stop web app

#docker rm web app

Remove network:
#docker network rm communication-net

Remove image:
#docker rmi container-communication-app:1.0


