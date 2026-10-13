# Project 2 — Docker BuildKit Cache Optimization

**Level:** Intermediate  
**Category:** Docker Build Performance  
**Technology:** Docker, BuildKit, Python, Flask, pip

## 1. Project Overview

This project demonstrates how to optimize Docker image builds using layer caching and BuildKit cache mounts.

We build a simple Flask application and perform experiments to understand when Docker reuses cached layers, when it rebuilds them, and how package-download caching can reduce unnecessary network downloads.

### Learning objectives

- Understand Docker layer caching.
- Understand cache invalidation.
- Order Dockerfile instructions for efficient caching.
- Enable BuildKit cache mounts.
- Reuse cached Python package downloads.
- Compare builds after source-code and dependency changes.
- Verify the application and troubleshoot build failures.
- Apply caching techniques to CI/CD pipelines.

## 2. Architecture

```text
             Docker BuildKit
                    |
                    v
        +------------------------+
        | Python base image      |
        +------------------------+
                    |
                    v
        +------------------------+
        | Copy requirements.txt  |
        +------------------------+
                    |
                    v
        +------------------------+
        | pip install            |
        |                        |
        | Layer cache            |
        | BuildKit pip cache     |
        +------------------------+
                    |
                    v
        +------------------------+
        | Copy app.py            |
        +------------------------+
                    |
                    v
        +------------------------+
        | Final Docker image     |
        +------------------------+
                    |
                    v
        +------------------------+
        | Flask container        |
        | Port 5000              |
        +------------------------+
```

## 3. Prerequisites

- Docker Engine or Docker Desktop.
- Docker Buildx or a Docker builder with BuildKit support.
- Terminal access.
- Internet access to download the base image and Python packages.

Verify your environment:

```bash
docker --version
docker info
docker buildx version
docker buildx ls
```

### Command explanation

| Command | Purpose |
|---|---|
| `docker --version` | Displays the Docker client version. |
| `docker info` | Shows Docker daemon and environment information. |
| `docker buildx version` | Checks the Buildx version. |
| `docker buildx ls` | Lists available builders. |

If Buildx is unavailable, check your Docker installation before changing daemon configuration.

## 4. Create the project

```bash
cd ~/ultimate-docker-roadmap

mkdir -p project-02-buildkit-cache

cd project-02-buildkit-cache
```

Check your location:

```bash
pwd
```

Expected directory:

```text
~/ultimate-docker-roadmap/project-02-buildkit-cache
```

Project structure:

```text
project-02-buildkit-cache/
├── Dockerfile
├── requirements.txt
├── app.py
└── README.md
```

## 5. Create requirements.txt

Create `requirements.txt`:

```text
Flask==3.1.2
```

This file lists the Python package required by the application.

Pinning the Flask version makes the dependency selection more predictable.

## 6. Create app.py

Create `app.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Docker Build Cache - Version 1!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### Application explanation

- `Flask(__name__)` creates the web application.
- `@app.route("/")` defines the root HTTP endpoint.
- The function returns a text response.
- `host="0.0.0.0"` allows connections through the container's network interface.
- `port=5000` sets the application listening port.

## 7. Create an optimized Dockerfile

Create `Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

### Important instructions

| Instruction | Explanation |
|---|---|
| `# syntax=docker/dockerfile:1` | Selects the Dockerfile frontend that supports BuildKit features. |
| `FROM python:3.12-slim` | Selects the Python base image. |
| `WORKDIR /app` | Sets the working directory. |
| `COPY requirements.txt .` | Copies dependency definitions first. |
| `RUN --mount=type=cache,...` | Uses a persistent BuildKit cache mount for pip's package cache. |
| `pip install -r requirements.txt` | Installs the declared dependencies. |
| `COPY app.py .` | Copies application code after dependency installation. |
| `EXPOSE 5000` | Documents the intended listening port. |
| `CMD ["python", "app.py"]` | Defines the default container command. |

### Why copy requirements.txt first?

Application code changes more frequently than dependency definitions in many projects.

When only `app.py` changes, Docker can reuse the dependency-installation layer, provided the earlier build inputs and configuration remain unchanged.

When `requirements.txt` changes, Docker normally reruns the installation step.

## 8. Build the Docker image

Build the image:

```bash
docker build --progress=plain \
  -t docker-cache-demo:1.0 .
```

### Command explanation

- `docker build` builds an image.
- `--progress=plain` displays detailed build output.
- `-t docker-cache-demo:1.0` assigns the image name and tag.
- `.` specifies the current directory as the build context.

Inspect the image:

```bash
docker images docker-cache-demo:1.0
```

Inspect its metadata:

```bash
docker image inspect docker-cache-demo:1.0
```

## 9. Experiment 1 — Build the image twice

Run the same build command again:

```bash
docker build --progress=plain \
  -t docker-cache-demo:1.0 .
```

Observe the output.

Depending on your builder and cache state, Docker should reuse previously cached build steps.

You may see output such as:

```text
CACHED
```

### Expected behavior

| Step | Expected behavior |
|---|---|
| Base image | Reused if available and applicable. |
| Copy requirements | Reused when inputs are unchanged. |
| Install dependencies | Reused when the layer cache is valid. |
| Copy application | Reused when application code is unchanged. |

**Note:** A cache hit depends on the instruction, its inputs, previous layers, build arguments, mounts, and other relevant configuration. Docker does not decide cache validity from the instruction text alone.

## 10. Experiment 2 — Change only app.py

Change the response in `app.py`:

```python
return "Hello from Docker Build Cache - Version 2!"
```

Rebuild:

```bash
docker build --progress=plain \
  -t docker-cache-demo:1.0 .
```

### Expected result

- The requirements-copy step can be reused.
- The pip installation layer can be reused.
- The application-copy step runs again because `app.py` changed.

This avoids reinstalling dependencies unnecessarily.

## 11. Experiment 3 — Change requirements.txt

Append a second dependency:

```text
Flask==3.1.2
requests==2.32.4
```

Rebuild:

```bash
docker build --progress=plain \
  -t docker-cache-demo:1.0 .
```

### Expected result

The dependency-installation step normally runs again because `requirements.txt` changed.

However, BuildKit can retain the pip cache mount between builds. Pip may reuse previously downloaded package files and download only the missing packages.

The cache mount does not eliminate the need to install or verify the required dependencies.

## 12. Understand BuildKit cache mounts

The important instruction is:

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

### Layer cache vs. cache mount

| Feature | Layer cache | BuildKit cache mount |
|---|---|---|
| What it stores | Reusable result of a build instruction | Data used by a build instruction |
| Example | Result of installing dependencies | Downloaded pip package files |
| When useful | When an entire step can be skipped | When a step must run but can reuse cached data |
| If requirements change | Installation layer normally rebuilds | Previously downloaded packages may still be reusable |
| Runtime availability | Part of the image when included in the resulting layer | Not automatically included in the final image |

### Important details

- Cache mounts are intended for performance, not as a source of truth.
- A cache mount can be empty or cleared at any time.
- Builds must still succeed without cached data.
- Cache contents may persist across builds using the same builder, subject to builder lifecycle and cache management.
- Avoid storing secrets in cache mounts.

## 13. Experiment 4 — Verify the running application

Start the container:

```bash
docker run -d \
  --name docker-cache-demo \
  --publish 5000:5000 \
  docker-cache-demo:1.0
```

Check its status:

```bash
docker ps --filter name=docker-cache-demo
```

View application logs:

```bash
docker logs docker-cache-demo
```

Test the endpoint:

```bash
curl -i http://localhost:5000/
```

The body should match the response currently defined in `app.py`.

For example:

```text
Hello from Docker Build Cache - Version 2!
```

Check the installed Requests package after adding it to `requirements.txt`:

```bash
docker exec docker-cache-demo \
  python -m pip show requests
```

The displayed version should be `2.32.4` if the updated image was successfully built and the running container was created from it.

## 14. Experiment 5 — Compare build times

You can measure approximate elapsed build time with the shell's `time` command:

```bash
time docker build -t docker-cache-demo:1.0 .
```

Run the command once, then run it again without changing the files.

Record the elapsed time for each build.

| Build | What to measure |
|---|---|
| First build | Base-image and dependency download/build time |
| Second build | Time when layers can be reused |
| After changing app.py | Time when only application-related steps need rebuilding |
| After changing requirements.txt | Time when dependencies must be processed again |

Times vary depending on network speed, CPU, builder cache state, and package availability. A single measurement is not a reliable benchmark.

## 15. Troubleshooting

### Problem A — BuildKit cache mount not recognized

Check the Dockerfile syntax directive:

```dockerfile
# syntax=docker/dockerfile:1
```

Check the available builder:

```bash
docker buildx ls
```

Then try:

```bash
docker buildx build \
  --progress=plain \
  --load \
  -t docker-cache-demo:1.0 .
```

`--load` loads the built image into the local Docker image store when supported by the selected builder.

### Problem B — Port 5000 is already in use

Inspect listening sockets:

```bash
ss -lntp | grep ':5000'
```

Alternatively, use a different host port:

```bash
docker run -d \
  --name docker-cache-demo \
  -p 5001:5000 \
  docker-cache-demo:1.0
```

Test:

```bash
curl http://localhost:5001/
```

### Problem C — Container exits

Inspect its status:

```bash
docker ps -a --filter name=docker-cache-demo
```

Read logs:

```bash
docker logs docker-cache-demo
```

Inspect its exit code:

```bash
docker inspect \
  --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}} Error={{.State.Error}}' \
  docker-cache-demo
```

### Problem D — Changes do not appear in the response

Remember that rebuilding an image does not update an already-running container.

Remove and recreate the container from the new image:

```bash
docker rm -f docker-cache-demo

docker run -d \
  --name docker-cache-demo \
  -p 5000:5000 \
  docker-cache-demo:1.0
```

Then test:

```bash
curl http://localhost:5000/
```

### Problem E — Build is unexpectedly slow

Check the detailed build output:

```bash
docker build --progress=plain \
  -t docker-cache-demo:1.0 .
```

Investigate:

- Whether an earlier instruction changed.
- Whether `requirements.txt` changed.
- Whether files are being copied too early.
- Whether the builder has retained cache.
- Whether dependencies require new downloads.
- Whether the network or package index is slow.

## 16. Cleanup

Remove the container:

```bash
docker rm -f docker-cache-demo
```

Remove the image if it is no longer required:

```bash
docker rmi docker-cache-demo:1.0
```

Check for remaining resources:

```bash
docker ps -a
docker images
```

Do not use broad cleanup commands such as `docker system prune -a` on a shared or production Docker host unless you have reviewed what will be removed.

BuildKit cache data is managed separately from the application image and may remain available after the image is deleted.

## 17. Important Interview Questions and Answers

### Q1. What is Docker layer caching?

Docker can reuse the result of a previous build instruction when its cache key remains valid. This avoids repeating work and can make image builds significantly faster.

### Q2. Why should dependencies be copied before application source code?

Dependency definitions often change less frequently than application source. Copying them first allows Docker to reuse the dependency-installation layer when only source files change.

### Q3. What invalidates the dependency-installation layer in this project?

Changing `requirements.txt` changes the input to the dependency-installation step. Docker normally reruns that step instead of reusing its previous layer.

### Q4. What is a BuildKit cache mount?

A cache mount is a directory provided to a build instruction that can retain data across builds. It is useful for reusable data such as downloaded packages or compiler caches.

### Q5. How does a pip cache mount help?

It allows pip to reuse cached package downloads when the installation step runs again. This can reduce repeated network downloads.

### Q6. Does a cache mount mean Docker skips pip installation?

No. The command still runs when the installation layer is invalidated. Pip may reuse cached downloads, but it must still resolve and install the required dependencies.

### Q7. What is the difference between layer caching and cache mounts?

Layer caching reuses the result of a whole build instruction. A cache mount retains data used by a build instruction so that the command can benefit from it when it executes again.

### Q8. What happens if the BuildKit cache is empty?

The build should still succeed by downloading or generating the required data again. Cache mounts should improve performance, not determine correctness.

### Q9. Why might Docker rebuild a layer even if the Dockerfile instruction looks unchanged?

Earlier layers or instruction inputs may have changed. Build arguments, copied files, mount configuration, relevant build options, and cache availability can also affect cache reuse.

### Q10. How do you inspect Docker build cache behavior?

Use:

```bash
docker build --progress=plain -t docker-cache-demo:1.0 .
```

Review which steps are cached and which execute again.

### Q11. What is the purpose of `--no-cache`?

It disables normal layer-cache reuse for the build. It can be useful for troubleshooting, but it does not automatically clear a BuildKit cache mount.

### Q12. Does deleting the final image always clear BuildKit cache data?

No. Build cache is managed separately and may remain available even when the resulting image is removed.

### Q13. Can cache mounts be used in CI/CD?

Yes. They can reduce repeated dependency downloads and compilation work. The pipeline must account for builder lifecycle, cache availability, concurrency, and cache isolation.

### Q14. Are cache mounts safe for secrets?

They should not be treated as a secret store. Cache data can persist and may be shared depending on configuration. Use dedicated BuildKit secret mounts for build-time secrets, and avoid writing secrets into cached output.

### Q15. Why shouldn't builds depend on cache contents for correctness?

Caches can be empty, evicted, or unavailable on another builder. A correct build must be able to obtain or generate all required inputs independently.

### Q16. Does a cached build always guarantee the same result?

Not necessarily. Mutable base-image tags, unpinned dependencies, external downloads, and nondeterministic build steps can produce different results. Reproducibility requires controlled inputs, pinned dependencies, and appropriate base-image management.

### Q17. How would you optimize Docker builds in production?

I would order instructions to maximize cache reuse, use BuildKit cache mounts for suitable package managers, keep the build context small, pin dependencies, use appropriate CI cache strategies, and measure build times before and after changes.

### Q18. Why is `.dockerignore` important for build performance?

It excludes unnecessary files from the build context. This can reduce context transfer and prevent irrelevant file changes from invalidating instructions that copy large portions of the context.

Example `.dockerignore`:

```text
.git
__pycache__/
*.pyc
.venv/
venv/
.env
```

Do not exclude files that are required to build the application. Never commit secrets into the repository.
