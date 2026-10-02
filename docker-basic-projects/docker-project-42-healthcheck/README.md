Project 42: Docker HEALTHCHECK

 Goal

Create a Docker container with a built-in health check and learn how to verify whether an application is healthy.

We will use Nginx and Docker CLI only.

By the end, you will know how to:

Configure HEALTHCHECK in a Dockerfile.

Build and run the container.

Check healthy and unhealthy status.

Inspect health-check results.

Troubleshoot a failed health check.


* Directory Structure
project-42-docker-healthcheck/
├── Dockerfile
└── README.md

1. Build the Image

docker build -t healthcheck-nginx:1.0 .

Verify:

docker images healthcheck-nginx

2. Run the Container

docker run -d \
  --name healthcheck-web \
  -p 8080:80 \
  healthcheck-nginx:1.0

Verify:

docker ps

Initially, the container may show health: starting. Wait a few seconds for the first checks to run.

3. Verify the Application

Run:

curl -I http://localhost:8080

Expected output includes:

HTTP/1.1 200 OK
Server: nginx

Your exact headers may differ slightly.

4. Check Container Health

Run:

docker ps

Expected status after successful checks:

Up ... (healthy)

Check the health status directly:

docker inspect \
  --format '{{.State.Health.Status}}' \
  healthcheck-web

Expected:

healthy

5. Inspect Health-Check Results

Run:

docker inspect \
  --format '{{json .State.Health}}' \
  healthcheck-web

The output contains the health status, recent check results, exit codes, and output from the health-check command.

For readable output, if jq is installed:

docker inspect healthcheck-web \
  --format '{{json .State.Health}}' | jq .

Check the last few health-check results:

docker inspect \
  --format '{{range .State.Health.Log}}{{println .ExitCode .Output}}{{end}}' \
  healthcheck-web

A successful check normally has exit code 0.

Important: Docker health status does not automatically restart an unhealthy container. Restart policies and health checks are separate features.

6. Test a Failed Health Check

We will temporarily make the health-check command fail without stopping Nginx.

Create a second image that uses an invalid health-check URL:

docker build \
  --tag healthcheck-nginx-fail:1.0 \
  --file - . <<'EOF'
FROM healthcheck-nginx:1.0

HEALTHCHECK --interval=5s \
            --timeout=2s \
            --start-period=2s \
            --retries=2 \
            CMD curl -fsS http://127.0.0.1:9999/ || exit 1
EOF

Stop and remove the first container:

docker rm -f healthcheck-web

Run the test container:

docker run -d \
  --name healthcheck-fail \
  -p 8080:80 \
  healthcheck-nginx-fail:1.0

Wait approximately 15–20 seconds, then inspect:

docker inspect \
  --format '{{.State.Health.Status}}' \
  healthcheck-fail

Expected:

unhealthy

Now check whether Nginx itself is still serving requests:

curl -I http://localhost:8080

You should still receive an HTTP response, usually 200 OK.

What did we prove? The health check is failing, but the main application process is still running. A health check tests the condition you define; it does not prove every aspect of the application is working.

7. Check the Failed Health-Check Logs

docker inspect \
  --format '{{range .State.Health.Log}}{{println .ExitCode .Output}}{{end}}' \
  healthcheck-fail

You should see non-zero exit codes and errors related to connecting to port 9999.
8. Cleanup

docker rm -f healthcheck-fail
docker rmi healthcheck-nginx:1.0 healthcheck-nginx-fail:1.0

