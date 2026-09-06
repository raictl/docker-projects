Project 37: Connect Nginx to a Backend Application

Goal

Build a simple application where:

Nginx will act as a reverse proxy and forward requests to the backend.

We will use:

    Nginx

    Python backend

    Custom Docker network

    Docker CLI

    Dockerfiles for both containers


1. Build Backend Image

#docker build -t nginx-backend-app:1.0 ./backend

Verify:

#docker images nginx-backend-app

2. Build Nginx Image

#docker build -t nginx-backend-proxy:1.0 ./nginx

Verify:

#docker images nginx-backend-proxy

3. Create Network

#docker network create nginx-backend-net

Verify:

#docker network ls

4. Start Backend

#docker run -d \
  --name backend \
  --network nginx-backend-net \
  nginx-backend-app:1.0

Verify:

#docker ps

Test backend directly:

#docker exec backend wget -qO- http://localhost:5000/

Expected:

Hello from Backend Application!

Test health endpoint:

#docker exec backend wget -qO- http://localhost:5000/health

Expected:

Backend is healthy!

5. Start Nginx

#docker run -d \
  --name nginx \
  --network nginx-backend-net \
  -p 8080:80 \
  nginx-backend-proxy:1.0

Check:

#docker ps

You should see:

nginx
backend

6. Test Nginx → Backend

From your host:

#curl http://localhost:8080

Expected:

Hello from Backend Application!

The request flow is:

Browser/curl
     |
     | :8080
     ↓
 Nginx :80
     |
     | Docker DNS
     ↓
backend :5000
     |
     ↓
Python Application

7. Test Health Endpoint Through Nginx

#curl http://localhost:8080/health

Expected:

Backend is healthy!

Notice that the client is communicating with Nginx, not directly with the backend.
8. Verify Backend Is Not Exposed to Host

Run:

#docker ps

You should see something similar to:

nginx     0.0.0.0:8080->80/tcp
backend   5000/tcp

The backend does not have:

0.0.0.0:5000->5000/tcp

So port 5000 is not published on the host.

You can verify:

#curl http://localhost:5000

This should fail.

But:

#curl http://localhost:8080

should work.

This is an important pattern:

Internet/Client
      ↓
  Nginx
      ↓
  Backend

Only Nginx is exposed to the host.

9. Verify Docker DNS

Check:

#docker exec nginx getent hosts backend

You should get an IP address for backend.

This confirms that Nginx can resolve:

backend

through the Docker network.

10. Check Nginx Logs

docker logs nginx

Generate a request:

#curl http://localhost:8080

Then:

#docker logs nginx

You should see the request in the access log.

11. Check Backend Logs

#docker logs backend

You should see:

Backend application running on port 5000

12. Test Backend Failure

Stop the backend:

#docker stop backend

Now:

#curl http://localhost:8080

The request should fail because Nginx cannot reach the backend.

Start it again:

#docker start backend

Test:

#curl http://localhost:8080

Expected:

Hello from Backend Application!

13. Cleanup

Stop containers:

#docker stop nginx backend

Remove containers:

#docker rm nginx backend

Remove network:

#docker network rm nginx-backend-net

Remove images:

#docker rmi nginx-backend-proxy:1.0
#docker rmi nginx-backend-app:1.0
