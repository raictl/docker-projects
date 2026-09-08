Project 38: Connect Flask + Redis

Goal

Build a simple Flask + Redis application using only Docker CLI.

Architecture:

Client
   ↓
Flask Container
   ↓
Redis Container

The Flask application will store and retrieve a value from Redis.

1. Build Flask Image

#docker build -t flask-redis-app:1.0 .

Verify:

#docker images flask-redis-app

2. Create Docker Network

#docker network create flask-redis-net

Verify:

docker network ls

3. Start Redis Container

Use the official Redis image:

#docker run -d \
  --name redis \
  --network flask-redis-net \
  redis:8-alpine

Verify:

#docker ps

Test Redis:

#docker exec redis redis-cli ping

Expected:

PONG

4. Start Flask Container

#docker run -d \
  --name flask \
  --network flask-redis-net \
  -p 8080:5000 \
  flask-redis-app:1.0

Verify:

#docker ps

You should have:

flask
redis

5. Test Flask Application

Run:

#curl http://localhost:8080

Expected:

Hello from Flask + Redis!

6. Test Flask → Redis Communication

Run:

#curl http://localhost:8080/health

Expected:

Flask and Redis are healthy!

This confirms:

Flask → Redis

is working.

7. Test Redis Counter

Run:

#curl http://localhost:8080/count

Expected:

Visitor count: 1

Run again:

#curl http://localhost:8080/count

Expected:

Visitor count: 2

Again:

#curl http://localhost:8080/count

Expected:

Visitor count: 3

Redis is maintaining the counter.

8. Verify the Value Directly in Redis

Run:

#docker exec redis redis-cli GET visits

Expected:

3

Your number may be different depending on how many times you called /count.

9. Verify Docker DNS

The Flask application connects to:

redis:6379

Here redis is the container name.

Verify DNS from the Flask container:

#docker exec flask getent hosts redis

You should get an IP address similar to:

172.18.0.2    redis

10. Verify Environment Variable

Our application supports:

REDIS_HOST

Check the container:

#docker exec flask env | grep REDIS_HOST

You may not see it because we didn't explicitly set it.

The application therefore uses its default:

redis

11. Test Redis Failure

Stop Redis:

#docker stop redis

Now test:

#curl http://localhost:8080/health

Expected:

Redis connection failed!

The Flask application is running, but its dependency is unavailable.

Start Redis again:

#docker start redis

Test:

#curl http://localhost:8080/health

Expected:

Flask and Redis are healthy!

12. Check Logs

Flask logs:

#docker logs flask

Redis logs:

#docker logs redis

Follow Flask logs:

#docker logs -f flask

Press:

Ctrl+C

to stop following the logs.

13. Inspect the Network

#docker network inspect flask-redis-net

You should see both:

flask
redis

connected to the same network.

14. Cleanup

Stop containers:

#docker stop flask redis

Remove containers:

#docker rm flask redis

Remove network:

#docker network rm flask-redis-net

Remove your application image:

#docker rmi flask-redis-app:1.0


