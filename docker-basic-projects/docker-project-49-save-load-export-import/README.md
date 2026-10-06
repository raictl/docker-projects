# Project 48: Docker Image Save/Load and Container Export/Import

## Goal

Learn the difference between:

* `docker save` / `docker load`
* `docker export` / `docker import`

## Key Concept

### Image transfer

```text
Docker Image
    ↓
docker save
    ↓
.tar
    ↓
docker load
    ↓
Docker Image
```

### Container filesystem export

```text
Container
    ↓
docker export
    ↓
.tar
    ↓
docker import
    ↓
New Docker Image
```

---

## Part A: docker save/load

### Build

```bash
docker build -t save-load-demo:1.0 .
```

### Inspect

```bash
docker inspect save-load-demo:1.0
docker history save-load-demo:1.0
```

### Save Image

```bash
docker save -o save-load-demo.tar save-load-demo:1.0
```

Verify:

```bash
ls -lh save-load-demo.tar
```

### Remove Image

```bash
docker rmi save-load-demo:1.0
```

### Load Image

```bash
docker load -i save-load-demo.tar
```

Verify:

```bash
docker images save-load-demo
```

### Run Loaded Image

```bash
docker run -d \
  --name save-load-demo-container \
  save-load-demo:1.0
```

Verify:

```bash
docker exec save-load-demo-container cat /message.txt
```

---

## Part B: docker export/import

### Create Container

```bash
docker run -d \
  --name export-demo \
  alpine:3.22 \
  sh -c 'while true; do sleep 10; done'
```

### Modify Container Filesystem

```bash
docker exec export-demo sh -c \
  'echo "Created after container startup" > /export-demo.txt'
```

Verify:

```bash
docker exec export-demo cat /export-demo.txt
```

### Export Container

```bash
docker export -o export-demo.tar export-demo
```

### Remove Container

```bash
docker rm -f export-demo
```

### Import Filesystem

```bash
docker import export-demo.tar export-import-demo:1.0
```

Verify:

```bash
docker images export-import-demo
```

### Run Imported Image

```bash
docker run -d \
  --name export-import-container \
  export-import-demo:1.0 \
  sh -c 'while true; do sleep 10; done'
```

Check the exported file:

```bash
docker exec export-import-container cat /export-demo.txt
```

---

## Save/Load vs Export/Import

| Feature                               | save/load             | export/import     |
| ------------------------------------- | --------------------- | ----------------- |
| Source                                | Image                 | Container         |
| Preserves layers                      | Yes                   | No                |
| Preserves image history               | Yes                   | No                |
| Preserves image metadata              | Yes                   | No                |
| Captures container filesystem changes | Not directly          | Yes               |
| Typical use                           | Image transfer/backup | Filesystem export |

## Production Rule

For transferring a Docker image between hosts:

```bash
docker save -o image.tar image:tag
docker load -i image.tar
```

Do not use `docker export/import` as a replacement for normal image transfer.

## Useful Commands

```bash
docker save -o image.tar image:tag
docker load -i image.tar

docker export -o container.tar container-name
docker import container.tar image:tag

docker history image:tag
docker inspect image:tag
```

## Cleanup

```bash
docker rm -f \
  save-load-demo-container \
  export-import-container

docker rmi \
  save-load-demo:1.0 \
  export-import-demo:1.0

rm -f \
  save-load-demo.tar \
  export-demo.tar
```

## Key Learning

`docker save/load` works with **Docker images** and preserves image structure.

`docker export/import` works with a **container filesystem** and does not preserve the original image's layer history.

