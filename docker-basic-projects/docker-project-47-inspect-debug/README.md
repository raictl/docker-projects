# Project 47: Inspect and Debug Containers

## Goal

Learn how to inspect Docker containers and perform basic troubleshooting using Docker CLI.

## Build

```bash
docker build -t inspect-demo:1.0 .
```

## Run

```bash
docker run -d \
  --name inspect-demo \
  -p 8080:80 \
  --memory=128m \
  --cpus=0.5 \
  inspect-demo:1.0
```

## Test

```bash
curl http://localhost:8080
```

## Basic Inspect

```bash
docker inspect inspect-demo
```

## Inspect State

```bash
docker inspect -f '{{json .State}}' inspect-demo
```

Useful fields include:

```text
Status
Running
Pid
ExitCode
OOMKilled
Error
StartedAt
FinishedAt
```

## Check Environment

```bash
docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' inspect-demo
```

## Check Ports

```bash
docker port inspect-demo
```

## Check Network

```bash
docker inspect -f '{{json .NetworkSettings}}' inspect-demo
```

## Check Container IP

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inspect-demo
```

## Check Mounts

```bash
docker inspect -f '{{json .Mounts}}' inspect-demo
```

## Check Resource Limits

```bash
docker inspect -f '{{.HostConfig.Memory}}' inspect-demo

docker inspect -f '{{.HostConfig.NanoCpus}}' inspect-demo
```

## Check Processes

```bash
docker top inspect-demo
```

## Check Logs

```bash
docker logs --tail 50 inspect-demo
```

## Check Live Resources

```bash
docker stats inspect-demo
```

## Check Filesystem Changes

```bash
docker diff inspect-demo
```

Create a test file:

```bash
docker exec inspect-demo sh -c 'echo "debug file" > /tmp/debug.txt'
```

Then:

```bash
docker diff inspect-demo
```

## Troubleshooting Flow

When a container has a problem:

```text
1. docker ps -a
2. docker inspect
3. docker logs
4. docker port
5. docker inspect network
6. docker stats
7. docker top
8. docker diff
```

Do not immediately restart or recreate the container. First collect evidence.

## Important Commands

```bash
docker inspect CONTAINER
docker logs CONTAINER
docker stats CONTAINER
docker top CONTAINER
docker diff CONTAINER
docker port CONTAINER
```

## Command Purpose

| Command          | Purpose                           |
| ---------------- | --------------------------------- |
| `docker inspect` | Configuration, metadata and state |
| `docker logs`    | Container stdout/stderr logs      |
| `docker stats`   | Live resource usage               |
| `docker top`     | Existing container processes      |
| `docker diff`    | Filesystem changes                |
| `docker port`    | Published port mappings           |

## Cleanup

```bash
docker rm -f inspect-demo
docker rmi inspect-demo:1.0
```

## Key Learning

Effective Docker troubleshooting starts with evidence.

Use `inspect`, `logs`, `stats`, `top`, `port`, and `diff` to understand what is actually happening before making changes.

