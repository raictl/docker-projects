# Project 1 — Docker Multi-Stage Build

**Level:** Intermediate  
**Category:** Docker Image Optimization  
**Project Type:** Hands-on  
**Repository:** `ultimate-docker-roadmap`

## 1. Project Overview

In this project, we build a small Go web application using a Docker multi-stage build.

The first stage compiles the application using the Go toolchain. The second stage copies only the compiled binary into a smaller runtime image.

This demonstrates how to separate the build environment from the runtime environment and reduce unnecessary files in the final Docker image.

### Objectives

- Understand multi-stage Docker builds.
- Use named build stages with `AS`.
- Copy artifacts between stages using `COPY --from`.
- Compare multi-stage and single-stage image sizes.
- Verify the final image's contents.
- Inspect image layers and container configuration.
- Understand the security and maintenance benefits of smaller runtime images.

## 2. Architecture

```text
                Docker Build
                     |
                     v
        +--------------------------+
        | Stage 1: Builder         |
        | golang:1.23-alpine       |
        |                          |
        | Source code              |
        | Go compiler              |
        |                          |
        | go build -o app main.go  |
        +-------------+------------+
                      |
                      | COPY --from=builder
                      v
        +--------------------------+
        | Stage 2: Runtime         |
        | alpine:3.20              |
        |                          |
        | Compiled application     |
        | No Go compiler           |
        +-------------+------------+
                      |
                      v
               Container :8080
                      |
                      v
                 HTTP response
```

**Important:** The builder stage is used during the image build. The final image is based on the second `FROM` instruction and receives only the files explicitly copied into it.

## 3. Prerequisites

- Docker Engine or Docker Desktop installed and running.
- Git installed if you want to commit the project.
- Terminal access.
- Internet access to pull the base images on the first build.

Verify the environment:

```bash
docker --version
docker info
git --version
```

If `docker info` fails, check whether the Docker daemon is running and whether your account has permission to access it.

## 4. Create the Project Directory

```bash
cd ~/ultimate-docker-roadmap

mkdir -p project-01-multi-stage-build

cd project-01-multi-stage-build
```

Expected directory structure:

```text
project-01-multi-stage-build/
├── Dockerfile
├── Dockerfile.multistage
├── go.mod
├── main.go
└── README.md
```

`Dockerfile` will be the multi-stage build. `Dockerfile.multistage` is an optional copy used to demonstrate the single-stage comparison; despite its filename, it contains the single-stage Dockerfile in this exercise.

## 5. Create the Go Module

Create `go.mod`:

```go
module docker-intermediate-project-01

go 1.23
```

The `module` directive identifies the Go module. The `go` directive declares the minimum Go language version expected by the module.

## 6. Create the Application

Create `main.go`:

```go
package main

import (
    "fmt"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintln(w, "Hello from Docker Multi-Stage Build!")
}

func main() {
    http.HandleFunc("/", handler)

    fmt.Println("Server running on port 8080")

    if err := http.ListenAndServe(":8080", nil); err != nil {
        fmt.Println("Server error:", err)
    }
}
```

The application exposes an HTTP endpoint on port `8080`.

The application binds to `:8080`, which means it listens on all container interfaces rather than only on the loopback interface.

## 7. Create the Multi-Stage Dockerfile

Create `Dockerfile`:

```dockerfile
# Stage 1: Build the application
FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod .
COPY main.go .

RUN go build -o app main.go

# Stage 2: Runtime image
FROM alpine:3.20

WORKDIR /app

COPY --from=builder /app/app .

EXPOSE 8080

CMD ["./app"]
```

### Important instructions explained

| Instruction | Purpose |
|---|---|
| `FROM golang:1.23-alpine AS builder` | Starts the build stage and names it `builder`. |
| `WORKDIR /app` | Sets the working directory for subsequent instructions. |
| `COPY go.mod .` | Copies the Go module file into the build context. |
| `COPY main.go .` | Copies the application source code. |
| `RUN go build -o app main.go` | Compiles the application into a binary named `app`. |
| `FROM alpine:3.20` | Starts a separate final runtime stage. |
| `COPY --from=builder /app/app .` | Copies the compiled binary from the builder stage. |
| `EXPOSE 8080` | Documents the application's listening port. It does not publish the port on the host. |
| `CMD ["./app"]` | Runs the compiled application when the container starts. |

**Key concept:** Multiple `FROM` instructions create multiple stages. The final stage is the default output image unless another target is explicitly selected.

## 8. Build the Multi-Stage Image

Run:

```bash
docker build -t docker-intermediate-01:1.0 .
```

Check the image:

```bash
docker images docker-intermediate-01:1.0
```

Inspect the image metadata:

```bash
docker image inspect docker-intermediate-01:1.0
```

Inspect its build history:

```bash
docker history docker-intermediate-01:1.0
```

The image history can help explain the final image's layers. It does not necessarily show every operation from every discarded build stage.

## 9. Run the Container

```bash
docker run -d \
  --name multi-stage-app \
  --publish 8080:8080 \
  docker-intermediate-01:1.0
```

Check its status:

```bash
docker ps --filter name=multi-stage-app
```

Check its logs:

```bash
docker logs multi-stage-app
```

Expected application log:

```text
Server running on port 8080
```

Test the application:

```bash
curl -i http://localhost:8080/
```

Expected response body:

```text
Hello from Docker Multi-Stage Build!
```

The `-i` option displays HTTP response headers as well as the response body.

## 10. Verify the Runtime Image

List the files in the application directory:

```bash
docker exec multi-stage-app ls -la /app
```

You should see the compiled `app` binary. The Go source files and Go compiler are not copied into the final stage by this Dockerfile.

Check the executable's file type:

```bash
docker exec multi-stage-app ls -l /app/app
```

Check the final image's configured command and working directory:

```bash
docker image inspect \
  --format='WorkingDir={{.Config.WorkingDir}} Cmd={{json .Config.Cmd}}' \
  docker-intermediate-01:1.0
```

The expected working directory is `/app`, and the command should be `["./app"]`.

## 11. Compare with a Single-Stage Build

Create a second Dockerfile:

```bash
cp Dockerfile Dockerfile.multistage
```

Replace the contents of `Dockerfile.multistage` with:

```dockerfile
FROM golang:1.23-alpine

WORKDIR /app

COPY go.mod .
COPY main.go .

RUN go build -o app main.go

EXPOSE 8080

CMD ["./app"]
```

This version uses the Go image for both compilation and runtime. The compiler and other tools in that base image remain available in the resulting image.

Build the single-stage image:

```bash
docker build \
  -f Dockerfile.multistage \
  -t docker-intermediate-01-single:1.0 .
```

Compare the image sizes:

```bash
docker images \
  --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}' \
  | grep docker-intermediate-01
```

### How to interpret the results

The multi-stage image should generally be smaller because it starts from the Alpine runtime image rather than the Go build image.

Record the sizes displayed on your own system. Do not expect a fixed size: base-image updates, architecture, image metadata, and build configuration affect the result.

The single-stage image is not inherently broken or always unsuitable. It is simply less optimized for this particular runtime-only application.

## 12. Understand Build Stages

To build only the named builder stage:

```bash
docker build --target builder -t docker-intermediate-01-builder:1.0 .
```

This is useful for debugging compilation problems or inspecting build artifacts. The builder-target image is not the final runtime image.

The normal build:

```bash
docker build -t docker-intermediate-01:1.0 .
```

builds the default final stage.

## 13. Troubleshooting

### Problem A: Port 8080 is already in use

Check the port:

```bash
ss -lntp | grep ':8080'
```

Alternatively, use a different host port:

```bash
docker run -d \
  --name multi-stage-app \
  -p 8081:8080 \
  docker-intermediate-01:1.0
```

Then test:

```bash
curl http://localhost:8081/
```

### Problem B: Container exits immediately

Check its status:

```bash
docker ps -a --filter name=multi-stage-app
```

Read the logs:

```bash
docker logs multi-stage-app
```

Inspect the exit code and state:

```bash
docker inspect \
  --format='Status={{.State.Status}} ExitCode={{.State.ExitCode}} Error={{.State.Error}}' \
  multi-stage-app
```

### Problem C: Image build fails

Run:

```bash
docker build --no-cache --progress=plain \
  -t docker-intermediate-01:1.0 .
```

`--no-cache` forces build instructions to be executed without using the existing build cache. It is useful for diagnosis but is not required for routine builds.

### Problem D: Cannot connect using curl

Check:

```bash
docker ps
docker logs multi-stage-app
docker port multi-stage-app
```

Verify that the container is running, that the application listens on port `8080`, and that the host port mapping is correct.

## 14. Cleanup

Stop and remove the container:

```bash
docker rm -f multi-stage-app
```

Remove the lab images when they are no longer needed:

```bash
docker rmi \
  docker-intermediate-01:1.0 \
  docker-intermediate-01-single:1.0 \
  docker-intermediate-01-builder:1.0
```

If the builder-target image was not built, Docker will report that it cannot find that image; this is harmless.

Check remaining project images:

```bash
docker images | grep docker-intermediate-01
```

Avoid broad cleanup commands such as `docker system prune -a` on shared or production systems because they can remove resources unrelated to this lab.

## 15. Important Interview Questions and Answers

### Q1. What is a multi-stage Docker build?

A multi-stage build uses multiple `FROM` instructions in one Dockerfile. Each stage can have its own base image and purpose. Files from earlier stages can be selectively copied into later stages, allowing the final image to exclude build tools and other unnecessary files.

### Q2. Why use multi-stage builds?

They help reduce final image size, separate build dependencies from runtime dependencies, reduce the software footprint in the final image, and make it easier to create purpose-built runtime images.

### Q3. What does `AS builder` mean?

It assigns the name `builder` to that build stage. The name can be referenced later:

```dockerfile
COPY --from=builder /app/app .
```

### Q4. What does `COPY --from=builder` do?

It copies files from the filesystem of the named builder stage into the current stage. It can also copy from another image or an external build stage when configured appropriately.

### Q5. Does Docker run the builder stage when the container starts?

No. The build stages run as part of building the image. When the container starts, Docker runs the configured command from the final image. The builder stage is not running alongside the application.

### Q6. Is the builder stage included in the final image?

Not as a complete filesystem stage in this example. Only the specified binary is copied into the final stage. Docker may retain build cache and intermediate build data separately, depending on the builder and cache configuration.

### Q7. Why is the final image smaller?

The final stage starts from `alpine:3.20` and copies only the compiled binary. It does not inherit the Go compiler, source code, or other files from `golang:1.23-alpine`.

### Q8. Does `EXPOSE 8080` publish the port?

No. `EXPOSE` documents the port the application is expected to use. Host access requires a port mapping, such as:

```bash
docker run -p 8080:8080 docker-intermediate-01:1.0
```

### Q9. What is the difference between `RUN` and `CMD`?

`RUN` executes during the image build and contributes to the image filesystem or metadata. `CMD` specifies the default command or arguments used when a container starts; it can be overridden at runtime.

### Q10. What is the difference between `CMD` and `ENTRYPOINT`?

`CMD` provides a default command or default arguments. `ENTRYPOINT` configures the executable that the container runs. They can be combined: `ENTRYPOINT` defines the main executable while `CMD` supplies default arguments.

### Q11. Can I use a different build and runtime base image?

Yes. This is one of the main advantages of multi-stage builds. The build stage can contain compilers and development tools, while the runtime stage contains only what is needed to execute the application.

The runtime image must still provide any required shared libraries and runtime components.

### Q12. Can a multi-stage build improve security?

It can reduce the number of tools and packages available in the runtime image, reducing the attack surface. However, multi-stage builds alone do not guarantee security. The application, base image, dependencies, permissions, secrets handling, and vulnerability management still matter.

### Q13. Does a smaller image always mean a faster application?

No. A smaller image often reduces image transfer and storage costs and can improve pull times. Application performance depends on the code, runtime, CPU and memory, I/O, and workload.

### Q14. Does `COPY --from=builder` copy the entire builder image?

No. It copies only the specified path or paths. In this project, it copies `/app/app`, not the builder's entire filesystem.

### Q15. How would you debug a failed multi-stage build?

I would inspect the failing build step, review the build output, validate file paths and build context, and verify that the artifact exists in the source stage. I could build the named stage using `--target builder` to isolate compilation problems.

### Q16. What should be considered when using Alpine as the runtime image?

Alpine uses musl libc rather than glibc. Some precompiled applications and dynamically linked binaries may require libraries or compatibility adjustments. Test the application in the actual runtime image rather than assuming a binary built elsewhere will work.

This Go example normally produces a binary that works in the chosen Alpine runtime, but applications with CGO or external library dependencies may need additional configuration.

### Q17. Can multi-stage builds help with secret management?

They can help prevent build-only files from being copied into the final image, but simply using multiple stages does not guarantee that secrets are safe. Avoid passing secrets through Dockerfile `ARG` or persistent image layers. Use BuildKit secret mounts when build-time access to secrets is required, and do not copy secret files into the final stage.

### Q18. What is the difference between image layers and build stages?

A layer represents filesystem changes associated with image build instructions. A stage is a logical build environment starting from a `FROM` instruction. A Dockerfile can have multiple stages, and only the selected final stage's resulting filesystem becomes the default output image.

### Q19. How do you select a specific build stage?

Use the `--target` option:

```bash
docker build --target builder -t my-builder-image .
```

This is useful for debugging or producing a specific intermediate artifact.

### Q20. How would you optimize this project further for production?

I would consider:

- Pinning base images to approved versions or digests.
- Using a non-root runtime user.
- Minimizing runtime packages.
- Scanning images and dependencies for vulnerabilities.
- Using BuildKit cache mounts where appropriate.
- Adding appropriate health checks and graceful shutdown handling.
- Testing the final runtime image in CI.
- Measuring actual image size and startup behavior rather than assuming improvements.

