# Project 50: Beginner Docker Capstone

## Goal

Build a complete multi-container application using Docker CLI only.

## Architecture

```text
Browser
   |
   | :8080
   v
Nginx
   |
   | HTTP :5000
   v
Flask Backend
   |
   | PostgreSQL :5432
   v
PostgreSQL
   |
   v
Docker Volume
```

## Components

* Nginx reverse proxy
* Flask backend
* PostgreSQL database
* Custom Docker network
* Persistent Docker volume

## Build Images

```bash
docker build -t capstone-backend:1.0 ./backend

docker build -t capstone-nginx:1.0 ./nginx
```

## Create Network

```bash
docker network create docker-capstone-net
```

## Create Volume

```bash
docker volume create capstone-postgres-data
```

## Start PostgreSQL

```bash
docker run -d \
  --name postgres \
  --network docker-capstone-net \
  --restart=unless-stopped \
  --memory=256m \
  --cpus=0.5 \
  -e POSTGRES_DB=appdb \
  -e POSTGRES_USER=appuser \
  -e POSTGRES_PASSWORD=apppassword \
  -v capstone-postgres-data:/var/lib/postgresql/data \
  -v "$(pwd)/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro" \
  postgres:17-alpine
```

Verify:

```bash
docker exec postgres \
  pg_isready -U appuser -d appdb
```

## Start Backend

```bash
docker run -d \
  --name backend \
  --network docker-capstone-net \
  --restart=unless-stopped \
  --memory=256m \
  --cpus=0.5 \
  -e DB_HOST=postgres \
  -e DB_NAME=appdb \
  -e DB_USER=appuser \
  -e DB_PASSWORD=apppassword \
  capstone-backend:1.0
```

Test:

```bash
docker exec backend \
  wget -qO- http://127.0.0.1:5000/

docker exec backend \
  wget -qO- http://127.0.0.1:5000/db
```

## Start Nginx

```bash
docker run -d \
  --name nginx \
  --network docker-capstone-net \
  --restart=unless-stopped \
  --memory=128m \
  --cpus=0.25 \
  -p 8080:80 \
  capstone-nginx:1.0
```

## Test Application

```bash
curl http://localhost:8080/
```

```bash
curl http://localhost:8080/health
```

```bash
curl http://localhost:8080/db
```

## Verify Network

```bash
docker network inspect docker-capstone-net
```

The network should contain:

```text
nginx
backend
postgres
```

## Check Health

```bash
docker inspect -f '{{.Name}} -> {{.State.Health.Status}}' nginx

docker inspect -f '{{.Name}} -> {{.State.Health.Status}}' backend
```

PostgreSQL:

```bash
docker exec postgres \
  pg_isready -U appuser -d appdb
```

## Logs

```bash
docker logs nginx

docker logs backend

docker logs postgres
```

Follow backend logs:

```bash
docker logs -f backend
```

## Inspect Containers

```bash
docker inspect nginx
docker inspect backend
docker inspect postgres
```

## Resource Monitoring

```bash
docker stats
```

## Execute Commands

```bash
docker exec backend pwd

docker exec backend printenv DB_HOST

docker exec postgres \
  psql -U appuser -d appdb \
  -c "SELECT * FROM messages;"
```

## Persistent Storage Test

Remove PostgreSQL:

```bash
docker rm -f postgres
```

Do not remove the volume.

Start PostgreSQL again using the same volume and verify:

```bash
docker exec postgres \
  psql -U appuser -d appdb \
  -c "SELECT * FROM messages;"
```

The database data should remain because it is stored in the Docker volume.

## Troubleshooting Flow

If the application does not work:

```text
1. docker ps -a
2. docker logs nginx
3. docker logs backend
4. docker logs postgres
5. docker network inspect docker-capstone-net
6. docker inspect backend
7. docker inspect postgres
8. docker stats
9. docker exec backend ...
10. docker exec postgres ...
```

Do not immediately restart or recreate everything. Collect evidence first.

## Cleanup

```bash
docker rm -f nginx backend postgres

docker rmi capstone-nginx:1.0 capstone-backend:1.0

docker network rm docker-capstone-net

docker volume rm capstone-postgres-data
```

**Warning:** Removing `capstone-postgres-data` permanently deletes the PostgreSQL data from this lab.

## Key Learning

This project demonstrates a complete Docker application using Docker CLI only.

The application contains:

```text
Nginx
  ↓
Flask
  ↓
PostgreSQL
  ↓
Persistent Volume
```

The containers communicate through a custom Docker network and are managed using Docker CLI.

