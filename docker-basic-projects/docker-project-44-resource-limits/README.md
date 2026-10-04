Project 44: Docker CPU and Memory Resource Limits

Goal: Learn how to limit CPU and memory available to a container.

1. Project structure

project-45-docker-resource-limits/
├── Dockerfile
└── README.md

2. Create Dockerfile

FROM alpine:3.22

CMD ["sh", "-c", "while true; do :; done"]

This creates a container that continuously consumes CPU, which makes CPU limiting easy to observe.

3. Build the image

docker build -t resource-demo:1.0 .

Verify:

docker images resource-demo

4. Test CPU limit

Run the container with 0.5 CPU:

docker run -d \
  --name cpu-limited \
  --cpus="0.5" \
  resource-demo:1.0

Check the configured limit:

docker inspect -f '{{.HostConfig.NanoCpus}}' cpu-limited

Check live resource usage:

docker stats cpu-limited

You should see the container's CPU usage constrained compared with an unrestricted CPU-bound container.

Press:

Ctrl+C

to exit docker stats.

5. Compare with an unlimited container

Start another container without a CPU limit:

docker run -d \
  --name cpu-unlimited \
  resource-demo:1.0

Monitor both:

docker stats cpu-limited cpu-unlimited

You should see a significant difference in CPU consumption.

6. Test memory limit

First remove the CPU test containers:

docker rm -f cpu-limited cpu-unlimited

Now run a container with 128 MB memory:

docker run -d \
  --name memory-limited \
  --memory="128m" \
  alpine:3.22 \
  sh -c 'while true; do sleep 5; done'

Check the configured memory limit:

docker inspect -f '{{.HostConfig.Memory}}' memory-limited

Monitor it:

docker stats memory-limited

7. Test memory + swap limit

Run:

docker run -d \
  --name memory-swap-limited \
  --memory="128m" \
  --memory-swap="128m" \
  alpine:3.22 \
  sh -c 'while true; do sleep 5; done'

Check:

docker inspect -f \
'Memory={{.HostConfig.Memory}} MemorySwap={{.HostConfig.MemorySwap}}' \
memory-swap-limited

Here:

--memory=128m
--memory-swap=128m

means the container has a combined memory+swap limit of 128 MB, so it does not get an additional 128 MB of swap on top of that limit.

8. Test CPU shares concept

Docker also provides CPU weighting with:

--cpu-shares

For example:

docker run -d \
  --name cpu-low-priority \
  --cpu-shares=256 \
  resource-demo:1.0

Another container:

docker run -d \
  --name cpu-high-priority \
  --cpu-shares=1024 \
  resource-demo:1.0

Check:

docker inspect -f '{{.HostConfig.CpuShares}}' cpu-low-priority

and:

docker inspect -f '{{.HostConfig.CpuShares}}' cpu-high-priority

Important: --cpu-shares is a relative CPU weight. It is different from --cpus.

For this project, remember:

--cpus
    Hard CPU quota

--memory
    Hard memory limit

--cpu-shares
    Relative CPU scheduling weight

9. Change resource limits on an existing container

You can modify limits without rebuilding the image.

For example:

docker update --cpus="1.0" cpu-low-priority

Check:

docker inspect -f '{{.HostConfig.NanoCpus}}' cpu-low-priority

You can also change memory:

docker update --memory="256m" memory-limited

Verify:

docker inspect -f '{{.HostConfig.Memory}}' memory-limited

10. Check all resource limits

Use:

docker inspect cpu-low-priority

Look under:

HostConfig

Useful fields include:

NanoCpus
CpuShares
Memory
MemorySwap

For a cleaner check:

docker inspect -f \
'CPU={{.HostConfig.NanoCpus}} Shares={{.HostConfig.CpuShares}} Memory={{.HostConfig.Memory}} Swap={{.HostConfig.MemorySwap}}' \
cpu-low-priority

11. Monitor containers

The most useful command for this project:

docker stats

For a specific container:

docker stats memory-limited

Useful columns include:

CPU %
MEM USAGE / LIMIT
MEM %
NET I/O
BLOCK I/O
PIDS

12. Cleanup

Remove all containers:

docker rm -f \
  cpu-low-priority \
  cpu-high-priority \
  memory-limited \
  memory-swap-limited

Remove the image:

docker rmi resource-demo:1.0


