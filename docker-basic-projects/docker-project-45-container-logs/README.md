Project 45: Docker Container Logs

Goal: Learn how to view, follow, filter, and troubleshoot container logs using Docker CLI.

You will practice:

docker logs
--follow
--tail
--timestamps
--since
--until
stdout/stderr behavior
log inspection during troubleshooting

1. Project structure

project-46-docker-container-logs/
├── Dockerfile
└── README.md

2. Create Dockerfile

FROM alpine:3.22

CMD ["sh", "-c", "i=1; while true; do echo \"INFO: application request $i\"; sleep 2; i=$((i+1)); done"]

This continuously writes messages to stdout, allowing us to practice Docker logging.

3. Build the image

docker build -t logs-demo:1.0 .

Verify:

docker images logs-demo

4. Run the container

docker run -d --name logs-demo logs-demo:1.0

Check:

docker ps

5. View container logs

docker logs logs-demo

You should see messages similar to:

INFO: application request 1
INFO: application request 2
INFO: application request 3
...

The command retrieves logs produced by the container's configured logging mechanism.
6. Follow logs in real time

This is one of the most important commands for production troubleshooting:

docker logs -f logs-demo

You should see new messages appearing every two seconds.

Press:

Ctrl+C

This stops log following, not the container.

Verify:

docker ps --filter name=logs-demo

The container should still be running.

7. Show only the last N lines

Show the last 5 lines:

docker logs --tail 5 logs-demo

This is very useful when a container has generated thousands of log lines.

For example:

docker logs --tail 20 logs-demo

8. Add timestamps

docker logs -t logs-demo

You should see timestamps before each message.

Example:

2026-10-04T15:30:01.123456789Z INFO: application request 10

This is particularly useful when correlating container events with:

    application events

    system logs

    monitoring alerts

    incidents

9. Combine --tail and --timestamps

docker logs -t --tail 10 logs-demo

This gives you the latest 10 log entries with timestamps.

10. View logs from a specific time

Docker allows time-based filtering.

For example:

docker logs --since 1m logs-demo

This shows logs generated during approximately the last minute.

Try:

docker logs --since 30s logs-demo

You can also specify an absolute timestamp:

docker logs --since "2026-10-04T15:00:00" logs-demo

Use a timestamp appropriate for your environment.

11. Use --until

You can define both boundaries.

Example:

docker logs \
  --since 2m \
  --until 30s \
  logs-demo

This requests logs from approximately two minutes ago until approximately thirty seconds ago.
12. Combine useful options

A very practical troubleshooting command:

docker logs \
  --timestamps \
  --tail 20 \
  logs-demo

Another:

docker logs \
  --since 5m \
  --timestamps \
  logs-demo

And real-time troubleshooting:

docker logs \
  --follow \
  --timestamps \
  logs-demo

13. Understand stdout and stderr

Docker's default docker logs behavior is based on what the container writes to stdout and stderr.

Let's create a second container that writes to both.

Run:

docker run -d \
  --name stdout-stderr-demo \
  alpine:3.22 \
  sh -c 'while true; do echo "INFO: stdout message"; echo "ERROR: stderr message" >&2; sleep 3; done'

View the logs:

docker logs stdout-stderr-demo

You should see both:

INFO: stdout message
ERROR: stderr message

Docker collects both streams.

14. Follow stdout/stderr logs

docker logs -f stdout-stderr-demo

Press:

Ctrl+C

Again, this only exits log-following.

15. Check container logging configuration

Inspect the container:

docker inspect logs-demo

Look for:

LogConfig

A cleaner command:

docker inspect -f '{{json .HostConfig.LogConfig}}' logs-demo

On a default Docker installation, you will commonly see:

{"Type":"json-file","Config":{}}

The exact result can vary depending on the Docker daemon configuration.

16. Production troubleshooting scenario

Imagine an application container is showing errors.

First check whether it is running:

docker ps -a

Then check the latest logs:

docker logs --tail 100 container-name

Add timestamps:

docker logs --timestamps --tail 100 container-name

Check recent logs:

docker logs --since 10m container-name

Follow new messages:

docker logs --follow container-name

This is a common first step before entering the container or changing anything.

17. Important distinction

docker logs does not mean Docker can automatically read every log file inside a container.

For example, if an application writes:

/var/log/application.log

inside the container, that file is not automatically equivalent to Docker's container log stream.

For docker logs to show application messages, the application should normally write them to:

stdout
stderr

This distinction is important in real production environments.

18. Cleanup

Stop and remove the containers:

docker rm -f logs-demo stdout-stderr-demo

Remove the image:

docker rmi logs-demo:1.0


