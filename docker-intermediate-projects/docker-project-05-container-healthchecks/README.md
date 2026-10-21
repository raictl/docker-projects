# Docker Intermediate Project 5: Container Health Checks

## 1. Project Overview

**Objective:** Configure Docker HEALTHCHECK to monitor application health and distinguish a running container from a healthy application.

### Tools
- Docker
- Python 3.12
- Linux
- HTTP
- Git

## 2. Learning Objectives

- Understand Docker container health states.
- Configure HEALTHCHECK in a Dockerfile.
- Inspect health-check status and execution logs.
- Simulate healthy and unhealthy application responses.
- Understand why an unhealthy container is not automatically restarted.
- Practise the project repeatedly without rewriting application code.

## 3. Project Files

- `app.py` — Python HTTP server with a configurable health endpoint.
- `Dockerfile` — builds the image and defines the health check.
- `README.md` — documentation and repeat-practice guide.

## 4. How the Application Works

The application exposes two endpoints:

| Endpoint | Normal response | Failure mode |
|---|---|---|
| `/` | HTTP 200 | HTTP 200 |
| `/health` | HTTP 200 | HTTP 500 |

The `HEALTH_FAIL` environment variable controls the health endpoint:

- Unset or not equal to `1`: the endpoint returns HTTP 200.
- Set to `1`: the endpoint returns HTTP 500.

This is a test mechanism for learning. It is not intended as a production failure switch.

## 5. Docker Health-Check Configuration

The Dockerfile uses:

```dockerfile
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
```

- `--interval=10s`: runs the check every 10 seconds.
- `--timeout=3s`: allows 3 seconds for a check to finish.
- `--start-period=5s`: provides a startup grace period.
- `--retries=3`: consecutive failures can cause the status to become unhealthy.
- `CMD`: executes the health-check command.

The health check uses Python's standard library, so installing `curl` inside the image is unnecessary.

## 6. Build the Image

From this directory:

```bash
docker build -t healthcheck-demo:1.1 .
```

The tag `1.1` identifies the image built with the configurable health endpoint.

## 7. Test the Healthy Scenario

Start the container:

```bash
docker run -d --name health-healthy \
  -p 8000:8000 healthcheck-demo:1.1
```

Test the health endpoint:

```bash
curl -i http://localhost:8000/health
```

Expected: HTTP 200 and `OK`.

Inspect the health status:

```bash
docker inspect --format='{{.State.Health.Status}}' health-healthy
```

Wait for the first health check to finish. Expected status: `healthy`.

## 8. Test the Unhealthy Scenario

Start another container with the failure enabled:

```bash
docker run -d --name health-failure \
  -p 8001:8000 \
  -e HEALTH_FAIL=1 \
  healthcheck-demo:1.1
```

Test the endpoint:

```bash
curl -i http://localhost:8001/health
```

Expected: HTTP 500 and `UNHEALTHY`.

Wait for consecutive checks to fail, then inspect the status:

```bash
docker inspect --format='{{.State.Health.Status}}' health-failure
```

Expected status: `unhealthy`.

The exact time to reach this status depends on check timing and startup behavior.

## 9. Compare Both Containers

```bash
docker ps
```

Inspect detailed health-check results:

```bash
docker inspect --format='{{json .State.Health}}' health-healthy
docker inspect --format='{{json .State.Health}}' health-failure
```

Review the recent health-check log entries, exit codes, and failure streak.

Check application logs:

```bash
docker logs health-healthy
docker logs health-failure
```

**Important:** A container can remain `Up` while its health status is `unhealthy`.

## 10. Repeat-Practice Procedure

You can repeat this project whenever you want without replacing `app.py`.

### A. Check the source files

```bash
cd ~/ultimate-docker-roadmap/project-05-container-healthchecks
ls -l
```

### B. Rebuild the image

```bash
docker build -t healthcheck-demo:1.1 .
```

### C. Run both scenarios

Use the commands in Sections 7 and 8.

### D. Inspect and compare

Use the commands in Section 9.

### E. Clean up the test containers

```bash
docker rm -f health-healthy health-failure
```

You can now repeat the exercise. The source files and image remain available.

## 11. Source-Code and Version Preservation

- `app.py` supports both test scenarios through an environment variable.
- Healthy and unhealthy tests use the same image.
- Changing a source file does not modify an image that has already been built.
- Rebuilding an image does not update existing containers.
- Git commits preserve recorded source-code versions.
- Avoid replacing working files without first reviewing the change or preserving the previous version.

To review project changes:

```bash
git status
git diff
```

## 12. Important Production Lessons

- `Up` means the container is running; it does not guarantee application health.
- `healthy` means the configured health check is passing.
- `unhealthy` means the configured health check has repeatedly failed.
- HEALTHCHECK reports status; it does not itself restart an unhealthy container.
- A restart policy normally responds to container-process exits, not health status alone.
- Production recovery may require an orchestrator, monitoring, alerting, or a suitable remediation mechanism.
- Health checks should measure meaningful application behavior and avoid unnecessary load.

## 13. Interview Questions and Answers

### Q1. What is Docker HEALTHCHECK?
It periodically runs a test to determine whether an application is functioning as expected.

### Q2. What are the Docker health states?
`starting`, `healthy`, and `unhealthy`.

### Q3. Does Docker automatically restart an unhealthy container?
No. An unhealthy status alone does not trigger a restart.

### Q4. What is the difference between `Up` and `healthy`?
`Up` describes the container's execution state. `healthy` describes the result of its configured health check.

### Q5. Why use a dedicated health endpoint?
It provides a consistent way to test whether an application is responding as expected.

### Q6. Does rebuilding an image update an existing container?
No. The existing container continues using the image from which it was created.

### Q7. How can you inspect health-check history?
Use `docker inspect` to review the health status and recent check logs.

### Q8. Does HTTP 200 always guarantee that an application is healthy?
No. It confirms the tested endpoint returned success. It does not necessarily prove that every application function or dependency works correctly.

## 14. Cleanup

Remove the practice containers:

```bash
docker rm -f health-healthy health-failure
```

Verify:

```bash
docker ps -a
```

The image and source files are retained for future practice.
