Project 43: Docker Restart Policies

Goal: Learn how Docker automatically restarts containers when they stop or when the Docker daemon restarts.

By the end of this project, you will understand and test all four restart policies:

no

on-failure

always

unless-stopped

1. Build the image

docker build -t restart-demo:1.0 .

Verify:

docker images restart-demo

2. Test restart policy: no

This is the default policy. Docker will not automatically restart the container after it exits.

Start the container:

docker run -d \
  --name restart-no \
  --restart=no \
  restart-demo:1.0

Check its policy:

docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' restart-no

Stop the container's main process abruptly:

docker kill restart-no

Check its status:

docker ps -a --filter name=restart-no

Expected: The container exits and remains stopped.

3. Test restart policy: on-failure

Docker restarts the container when its main process exits with a non-zero exit code.

docker run -d \
  --name restart-on-failure \
  --restart=on-failure:3 \
  restart-demo:1.0

Kill its main process:

docker kill restart-on-failure

Inspect the result:

docker inspect -f \
'Status={{.State.Status}} RestartCount={{.RestartCount}} ExitCode={{.State.ExitCode}}' \
restart-on-failure

Because docker kill normally causes exit code 137, Docker should attempt to restart the container, up to the configured retry limit. The restart count can increase asynchronously, so inspect again after a few seconds.

Production use: Useful when an application should be restarted after a failure, with a finite retry limit if required.

4. Test restart policy: always

Docker attempts to restart the container whenever its main process exits, subject to Docker's restart-policy behavior.

docker run -d \
  --name restart-always \
  --restart=always \
  restart-demo:1.0

Kill the main process:

docker kill restart-always

Wait a few seconds, then check:

docker ps --filter name=restart-always

Inspect the restart count:

docker inspect -f \
'Status={{.State.Status}} RestartCount={{.RestartCount}}' \
restart-always

Expected: The container starts again, and its restart count increases.

Important: manually stopping a container with docker stop suppresses automatic restarts until you manually start it again or the Docker daemon restarts.

5. Test restart policy: unless-stopped

This policy restarts a container after an unexpected exit, but respects an explicit manual stop across Docker daemon restarts.

docker run -d \
  --name restart-unless-stopped \
  --restart=unless-stopped \
  restart-demo:1.0

Kill the main process:

docker kill restart-unless-stopped

Verify that Docker restarts it:

docker ps --filter name=restart-unless-stopped

Now stop it intentionally:

docker stop restart-unless-stopped

Check its status:

docker ps -a --filter name=restart-unless-stopped

Expected: It remains stopped. Docker will not automatically restart it merely because the daemon restarts.


Compare the policies

Policy            Restarts after a non-zero exit?            Key behavior

no                       No                         Never automatically restart
on-failure:3             Yes                        Retry up to the configured limit
always                   Yes                        Restart after exit; manual stops suppress restarts temporarily
unless-stopped           Yes                        Respect an intentional stop, including across daemon restarts

These policies manage container restarts; they do not repair application errors or guarantee application health.

6. Change a restart policy on an existing container

You do not need to rebuild the image.

docker update --restart=unless-stopped restart-no

Verify:

docker inspect -f '{{.HostConfig.RestartPolicy.Name}}' restart-no

Expected:

unless-stopped

Update an Existing Container
docker update --restart=unless-stopped restart-no

7. Cleanup

docker rm -f restart-no restart-on-failure restart-always restart-unless-stopped
docker rmi restart-demo:1.0

8. Key Learning

Restart policies control what Docker does when a container exits. They do not fix application failures or replace health checks and monitoring.




