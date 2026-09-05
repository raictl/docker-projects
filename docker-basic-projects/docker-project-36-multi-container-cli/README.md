Project 36: Multi-Container Application Using Only Docker CLI


Goal

Build a simple multi-container application using only Docker CLI.

We will create:

Client
  ↓
Web Container (Nginx)
  ↓
Backend Container (Python)

You will manually create the network and containers using docker commands.


Directory Structure:

project-36-multi-container-cli/
├── backend/
│   ├── app.py
│   └── Dockerfile
├── nginx/
│   ├── nginx.conf
│   └── Dockerfile
└── README.md

1. Build Backend Image

From the project directory:

#docker build -t multi-container-backend:1.0 ./backend

Verify:

#docker images multi-container-backend

2. Build Nginx Image

#docker build -t multi-container-nginx:1.0 ./nginx

Verify:

#docker images multi-container-nginx

3. Create Docker Network

#docker network create multi-container-net

Verify:

#docker network ls

4. Start Backend Container

#docker run -d \
  --name backend \
  --network multi-container-net \
  multi-container-backend:1.0

Check:

#docker ps

Test backend directly:

#docker exec backend wget -qO- http://localhost:5000

Expected:

Hello from Python Backend!

5. Start Nginx Container

#docker run -d \
  --name nginx \
  --network multi-container-net \
  -p 8080:80 \
  multi-container-nginx:1.0

Check:

#docker ps

You should have:

backend
nginx

running.

6. Test the Complete Application

From the host:

#curl http://localhost:8080

Expected:

Hello from Python Backend!

The request flow is:

localhost:8080
      ↓
   nginx:80
      ↓
backend:5000
      ↓
Python application

7. Verify Container Communication

Check the network:

#docker network inspect multi-container-net

You should see:

backend
nginx

Now verify that Nginx can resolve the backend container:

docker exec nginx getent hosts backend

Expected output similar to:

172.18.0.2    backend

8. Check Nginx Logs

#docker logs nginx

Generate another request:

#curl http://localhost:8080

Then check:

#docker logs nginx

You should see the HTTP request in the logs.

9. Check Backend Logs

#docker logs backend

You should see:

Backend server running on port 5000

10. Test Failure Scenario

Stop the backend:

#docker stop backend

Now test:

#curl http://localhost:8080

The request should fail because Nginx cannot reach the backend.

Start the backend again:

#docker start backend

Test again:

#curl http://localhost:8080

Expected:

Hello from Python Backend!

This is a useful real-world troubleshooting exercise.

12. Cleanup

Stop containers:

#docker stop nginx backend

Remove containers:

#docker rm nginx backend

Remove network:

#docker network rm multi-container-net

Remove images:

#docker rmi multi-container-nginx:1.0
#docker rmi multi-container-backend:1.0
