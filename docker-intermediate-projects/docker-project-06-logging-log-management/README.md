# Docker Intermediate Project 6: Logging and Log Management

## Project Overview

This project demonstrates how to collect, inspect, monitor, and manage
application logs from Docker containers.

It uses a Python HTTP application and Docker's `json-file` logging driver
to demonstrate practical logging and log rotation.

## Objectives

- Understand Docker container logging.
- Read logs with `docker logs`.
- Filter logs by time and line count.
- Monitor logs in real time.
- Inspect Docker logging drivers and configuration.
- Configure log rotation to control disk usage.
- Troubleshoot application errors using logs.
- Practice safe container cleanup.

## Technologies

- Docker
- Python 3
- Linux
- Docker CLI
- Docker `json-file` logging driver
- Git and GitHub

## Project Structure

```text
docker-project-06-logging-log-management/
├── app.py
├── Dockerfile
└── README.md
```

## Application Endpoints

| Endpoint | Expected HTTP status | Purpose |
|---|---:|---|
| `/` | 200 | Normal application request |
| `/health` | 200 | Simulated health check |
| `/error` | 500 | Generates a simulated application error |

The `/error` endpoint intentionally returns HTTP 500 for troubleshooting
practice. It does not indicate a Docker failure.

## Step 1: Validate the Application

Check Python syntax:

```bash
python3 -m py_compile app.py
```

No output indicates that the syntax check passed.

Inspect the Dockerfile:

```bash
cat Dockerfile
```

## Step 2: Build the Image

```bash
docker build -t docker-logging-demo:1.0 .
```

Verify the image:

```bash
docker images docker-logging-demo
```

## Step 3: Start the Application Container

Check whether the container name is already in use:

```bash
docker ps -a --filter name=^/logging-demo$
```

If the name is available, start the container:

```bash
docker run -d \
  --name logging-demo \
  -p 8000:8000 \
  docker-logging-demo:1.0
```

Verify its status:

```bash
docker ps --filter name=^/logging-demo$
```

## Step 4: Generate Application Logs

Run these commands individually:

```bash
curl -i http://localhost:8000/
curl -i http://localhost:8000/health
curl -i http://localhost:8000/error
```

Expected results:

- `/` returns HTTP 200.
- `/health` returns HTTP 200.
- `/error` returns HTTP 500 and generates an error log.

## Step 5: Inspect Container Logs

Display all available logs:

```bash
docker logs logging-demo
```

Display the last five lines:

```bash
docker logs --tail 5 logging-demo
```

Display logs from the last five minutes:

```bash
docker logs --since 5m logging-demo
```

Include timestamps:

```bash
docker logs --timestamps logging-demo
```

Monitor logs continuously:

```bash
docker logs --follow logging-demo
```

Press `Ctrl+C` to stop following logs. This does not stop the container.

## Step 6: Inspect the Logging Driver

Check the Docker daemon's default logging driver:

```bash
docker info --format '{{.LoggingDriver}}'
```

Inspect the driver used by the application container:

```bash
docker inspect --format \
  '{{.HostConfig.LogConfig.Type}}' logging-demo
```

Inspect its logging options:

```bash
docker inspect --format \
  '{{json .HostConfig.LogConfig.Config}}' logging-demo
```

Inspect the Docker-reported log path:

```bash
docker inspect --format '{{.LogPath}}' logging-demo
```

The default driver and the driver configured for a particular container
are related but distinct settings.

## Step 7: Configure Log Rotation

Create a separate test container so the original application container
remains unchanged.

Check that the test container name is available:

```bash
docker ps -a --filter name=^/logging-rotation-test$
```

If no container appears, create the test container:

```bash
docker run -d \
  --name logging-rotation-test \
  --log-driver json-file \
  --log-opt max-size=1m \
  --log-opt max-file=3 \
  docker-logging-demo:1.0
```

### Understand the options

- `--log-driver json-file`: uses the JSON-file logging driver.
- `--log-opt max-size=1m`: rotates the log file at approximately 1 MB.
- `--log-opt max-file=3`: retains up to three log files, including the
  current file.

These limits apply to this container, not automatically to every
container on the host.

Verify the configuration:

```bash
docker inspect --format \
  '{{.HostConfig.LogConfig.Type}}' logging-rotation-test
```

```bash
docker inspect --format \
  '{{json .HostConfig.LogConfig.Config}}' logging-rotation-test
```

Expected configuration:

```json
{"max-file":"3","max-size":"1m"}
```

The order of the JSON keys may differ.

## Step 8: Generate Logs in the Rotation Test Container

The test container does not publish port 8000 on the host. Generate
requests from inside the container instead:

```bash
docker exec logging-rotation-test python -c '
import urllib.request

for i in range(1000):
    with urllib.request.urlopen("http://127.0.0.1:8000/") as response:
        response.read()
'
```

Inspect recent logs:

```bash
docker logs --tail 10 logging-rotation-test
```

Inspect the log path:

```bash
docker inspect --format '{{.LogPath}}' logging-rotation-test
```

Inspect the directory containing the log files:

```bash
sudo ls -lh "$(dirname "$(docker inspect --format '{{.LogPath}}' logging-rotation-test)")"
```

Rotation occurs only when the configured size threshold is reached.
A small test may not generate enough output to trigger rotation.

Do not manually edit or delete Docker-managed log files.

## Troubleshooting

### Container is not running

```bash
docker ps -a
docker inspect logging-demo
docker logs logging-demo
```

### Application returns HTTP 500

```bash
curl -i http://localhost:8000/error
docker logs --tail 20 logging-demo
```

The `/error` endpoint intentionally generates this response.

### Port 8000 is already in use

Check the container publishing that port:

```bash
docker ps --filter publish=8000
```

Inspect the application container before changing port mappings.

### Logs are missing or delayed

```bash
docker ps -a
docker logs --timestamps logging-demo
docker inspect --format '{{.HostConfig.LogConfig.Type}}' logging-demo
```

Check that the application is running and writing logs to standard
output or standard error.

## Production Best Practices

1. Configure log rotation to prevent unbounded local log growth.
2. Send application logs to standard output and standard error when
   appropriate for the container runtime.
3. Use timestamps to correlate events during incident investigations.
4. Monitor disk usage and log volume.
5. Use centralized logging for multi-host production environments.
6. Avoid blindly changing the Docker daemon's logging configuration.
7. Recreate containers when necessary to apply changed container-level
   logging settings.
8. Never delete Docker-managed log files manually as a routine cleanup
   method.
9. Avoid logging passwords, access tokens, or other sensitive data.
10. Keep production log retention aligned with security and compliance
    requirements.

## Interview Questions and Answers

### 1. What is Docker logging?

Docker logging collects output written by a containerized application
to standard output and standard error.

### 2. How do you view container logs?

Use `docker logs CONTAINER_NAME`.

### 3. How do you follow logs in real time?

Use `docker logs -f CONTAINER_NAME`.

### 4. How do you display only the last 100 lines?

Use `docker logs --tail 100 CONTAINER_NAME`.

### 5. What is a Docker logging driver?

It determines how Docker collects and routes container logs.

### 6. What is the `json-file` logging driver?

It stores container logs in JSON-formatted files on the Docker host.

### 7. Why is log rotation important?

It limits log storage growth and helps prevent disk exhaustion.

### 8. What does `max-size=10m` mean?

It configures log-file rotation at approximately 10 MB per file.

### 9. What does `max-file=3` mean?

It retains up to three log files, including the current file.

### 10. How do you inspect a container's logging driver?

Use:

```bash
docker inspect --format \
  '{{.HostConfig.LogConfig.Type}}' CONTAINER_NAME
```

### 11. Does changing a moving image tag update a running container?

No. A running container continues using its existing image. It must be
recreated to use a different image version.

### 12. What would you investigate if Docker logs consume too much disk?

Check the logging driver, rotation settings, disk usage, application log
volume, and any external log collection or retention policies.

### 13. Why should application logs go to standard output?

Docker can collect them through its logging system, making them easier
to inspect with `docker logs` and route to logging backends.

### 14. Should you manually truncate Docker's JSON log file?

No. Use supported Docker logging configuration and retention mechanisms.

## Cleanup

Remove only the test containers created for this project.

First, inspect their status:

```bash
docker ps -a --filter name=^/logging-demo$
docker ps -a --filter name=^/logging-rotation-test$
```

After confirming these are the project containers, stop them:

```bash
docker stop logging-demo logging-rotation-test
```

Remove the containers:

```bash
docker rm logging-demo logging-rotation-test
```

Verify cleanup:

```bash
docker ps -a --filter name=^/logging-demo$
docker ps -a --filter name=^/logging-rotation-test$
```

The image is intentionally retained for future practice. Remove it only
if you no longer need it:

```bash
docker image rm docker-logging-demo:1.0
```

Do not run cleanup commands against unrelated containers.

## Learning Outcomes

After completing this project, you should be able to:

- Inspect Docker container logs.
- Follow and filter logs during troubleshooting.
- Identify a container's logging driver and options.
- Configure per-container log rotation.
- Explain why log management matters in production.
- Apply safe cleanup practices.

## Practice Checklist

- [ ] Build the application image.
- [ ] Start the application container.
- [ ] Test all three endpoints.
- [ ] Inspect logs with `docker logs`.
- [ ] Follow logs in real time.
- [ ] Inspect the logging driver and configuration.
- [ ] Configure rotation on the separate test container.
- [ ] Generate test logs and inspect the results.
- [ ] Review troubleshooting and interview questions.
- [ ] Clean up the test containers safely.
