# Project 04: Docker Image Tagging and Version Management

## 1. Objective

Learn how to tag, version, inspect, test, and roll back Docker images.

This project covers:

- Docker image tags and image IDs
- Multiple tags pointing to the same image
- Application versioning
- Running multiple image versions simultaneously
- Updating the `latest` tag
- Image metadata and filesystem layers
- Rollback to a previous image version
- Container cleanup and release-management practices

## 2. Project Structure

```text
project-04-image-tagging-versioning/
├── Dockerfile
├── README.md
└── app.py
```

## 3. Application

The application is a small Python HTTP server that returns its version.

Example:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_VERSION = "1.0.0"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = f"Application version: {APP_VERSION}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print(f"Application listening on port 8000, version {APP_VERSION}")
server.serve_forever()
```

## 4. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY app.py .

EXPOSE 8000

CMD ["python", "app.py"]
```

`EXPOSE 8000` documents the application's listening port. It does not publish the port to the host.

## 5. Build Version 1.0.0

```bash
docker build -t image-version-demo:1.0.0 .
```

Verify:

```bash
docker image ls image-version-demo
```

## 6. Add Additional Tags

```bash
docker tag image-version-demo:1.0.0 image-version-demo:1.0
docker tag image-version-demo:1.0.0 image-version-demo:latest
```

Inspect the references:

```bash
docker image inspect image-version-demo:1.0.0 image-version-demo:1.0 image-version-demo:latest --format '{{.RepoTags}} {{.Id}}'
```

The tags should reference the same image ID.

A tag is a mutable reference; retagging does not rebuild the image.

## 7. Run Version 1.0.0

```bash
docker run -d --name image-version-test -p 8000:8000 image-version-demo:1.0.0
```

Verify:

```bash
docker ps --filter name=image-version-test
curl -i http://localhost:8000
docker logs image-version-test
```

Expected response body:

```text
Application version: 1.0.0
```

## 8. Build Version 1.1.0

Update `APP_VERSION` in `app.py`:

```python
APP_VERSION = "1.1.0"
```

Build the new image:

```bash
docker build -t image-version-demo:1.1.0 .
```

Compare image IDs:

```bash
docker image inspect image-version-demo:1.0.0 image-version-demo:1.1.0 --format '{{.RepoTags}} {{.Id}}'
```

The changed application contents should result in a different image ID.

Building the new image does not update existing containers.

## 9. Run Both Versions

Run version 1.1.0 on a different host port:

```bash
docker run -d --name image-version-test-v1-1 -p 8001:8000 image-version-demo:1.1.0
```

Test both releases:

```bash
curl -s http://localhost:8000
curl -s http://localhost:8001
```

Expected responses:

```text
Application version: 1.0.0
Application version: 1.1.0
```

## 10. Update the Latest Tag

```bash
docker tag image-version-demo:1.1.0 image-version-demo:latest
```

Verify:

```bash
docker image inspect image-version-demo:1.0.0 image-version-demo:1.1.0 image-version-demo:latest --format '{{.RepoTags}} {{.Id}}'
```

The `latest` tag should now reference the same image ID as `1.1.0`.

**Important:** `latest` is not automatically the newest image. It is an ordinary tag whose target can be changed.

## 11. Inspect Image Metadata and Layers

Inspect the image:

```bash
docker image inspect image-version-demo:1.1.0
```

Display its image ID:

```bash
docker image inspect image-version-demo:1.1.0 --format '{{.Id}}'
```

Inspect filesystem layers:

```bash
docker image inspect image-version-demo:1.1.0 --format '{{json .RootFS.Layers}}'
```

Compare versions:

```bash
docker image inspect image-version-demo:1.0.0 --format '{{json .RootFS.Layers}}'
docker image inspect image-version-demo:1.1.0 --format '{{json .RootFS.Layers}}'
```

Unchanged base layers may be shared, while the changed application file results in changed filesystem content.

An image ID is not the same as a registry manifest digest.

## 12. Rollback to Version 1.0.0

Start a rollback test container:

```bash
docker run -d --name image-version-rollback -p 8002:8000 image-version-demo:1.0.0
```

Verify the response:

```bash
curl -i http://localhost:8002
```

Expected response body:

```text
Application version: 1.0.0
```

A production rollback usually requires updating the deployment to use the previous image and recreating or replacing the affected workload. Database migrations, configuration, and persistent data must also be considered.

## 13. Cleanup

Remove the lab containers:

```bash
docker rm -f image-version-test image-version-test-v1-1 image-version-rollback
```

Verify:

```bash
docker ps -a --filter name=image-version
```

Optionally remove the test images when they are no longer required:

```bash
docker image rm image-version-demo:1.0.0 image-version-demo:1.0 image-version-demo:1.1.0 image-version-demo:latest
```

Docker may report that some references share the same image ID. Remove only these project images, not unrelated images.

## 14. Production Best Practices

- Use explicit, meaningful version tags.
- Avoid relying on `latest` as a release identifier.
- Keep known-good images available for rollback.
- Use image digests when you need to pin exact registry content.
- Test the new image before promoting it.
- Coordinate application rollback with database and configuration changes.
- Avoid overwriting release tags in registries when immutable release history is required.
- Scan images for vulnerabilities before production deployment.

## 15. Interview Questions and Answers

### Q1. What does `docker tag` do?

It creates another tag reference for an image. It does not rebuild the image or push it to a registry.

### Q2. Can multiple tags point to the same image?

Yes. For example, `1.0.0`, `1.0`, and `latest` can all reference the same image ID.

### Q3. Does `latest` always mean the newest release?

No. It is an ordinary mutable tag and can reference any image.

### Q4. What happens to a running container when a new image is built?

The container continues running from the image it was created from. Building a new image does not update existing containers.

### Q5. What is the difference between an image tag and image ID?

A tag is a human-readable reference that can be moved. An image ID identifies the local image configuration.

### Q6. What is an image digest?

A digest is a content-addressed identifier for registry content, such as an image manifest. It helps pin a deployment to specific content.

### Q7. Why keep previous image versions?

They support controlled rollback when a release introduces a defect, provided application dependencies and data remain compatible.

### Q8. Is running two image versions side by side a blue-green deployment?

Not by itself. It is a useful testing technique. A blue-green deployment also requires traffic routing and a controlled switch between environments.

### Q9. Does deleting a container delete its image?

No. Containers and images are separate Docker objects.

### Q10. Is rolling back an image always sufficient to restore a service?

No. Database migrations, persistent data, external dependencies, and configuration changes can prevent a simple image rollback from restoring the previous behavior.

## Key Takeaways

- Tags make image versions easier to manage.
- Multiple tags can reference the same image.
- New application content requires a new build.
- Existing containers do not automatically switch to a newly built image.
- Explicit versions and image digests improve deployment control.
- Retaining known-good images supports rollback.

**Project status:** Docker Intermediate Project 4 — Image Tagging and Version Management.

