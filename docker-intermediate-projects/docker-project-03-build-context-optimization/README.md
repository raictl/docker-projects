# Project 03: Docker Build Context Optimization

## 1. Objective

Optimize Docker builds by excluding unnecessary files from the build context using `.dockerignore`.

This project demonstrates how to:

- Reduce unnecessary build-context content.
- Prevent irrelevant files from being copied into container images.
- Avoid accidental inclusion of local configuration and secret files.
- Understand the relationship between build context, `COPY`, and Docker layer caching.
- Verify `.dockerignore` behavior through practical experiments.

## 2. Project Structure

```text
project-03-build-context-optimization/
├── Dockerfile
├── .dockerignore
├── README.md
├── app.py
├── requirements.txt
├── debug.log
├── .env
├── .git/
├── .venv/
└── __pycache__/
```

The files and directories above are used to demonstrate which items should be excluded from a Docker build context.

## 3. Dockerfile

```dockerfile
FROM alpine:3.22

WORKDIR /app

COPY . .

CMD ["sh"]
```

### Explanation

- `FROM alpine:3.22`: Uses Alpine Linux as the base image.
- `WORKDIR /app`: Sets the working directory inside the image.
- `COPY . .`: Copies files from the build context into `/app`, excluding files matched by `.dockerignore`.
- `CMD ["sh"]`: Starts a shell by default when the container runs.

**Important:** `COPY . .` does not mean every file on the host is copied. The build context and `.dockerignore` determine which files are available to this instruction.

## 4. Create `.dockerignore`

```dockerignore
.git
.venv/
__pycache__/
*.pyc
*.log
.env
```

### Explanation

| Pattern | Purpose |
|---|---|
| `.git` | Excludes Git repository metadata. |
| `.venv/` | Excludes the local Python virtual environment. |
| `__pycache__/` | Excludes Python bytecode cache directories. |
| `*.pyc` | Excludes Python compiled bytecode files. |
| `*.log` | Excludes files ending in `.log`. |
| `.env` | Excludes the root-level `.env` file. |

Patterns should be selected according to the application and build requirements. Do not exclude files that are genuinely required to build the image.

## 5. Build the Image

From the project directory:

```bash
docker build --progress=plain -t build-context-demo:v1 .
```

### Command breakdown

- `docker build`: Builds a Docker image.
- `--progress=plain`: Displays detailed build output.
- `-t build-context-demo:v1`: Assigns an image name and tag.
- `.`: Specifies the current directory as the build context.

The final dot is important: it tells Docker which directory supplies files for the build.

## 6. Verify the Image Contents

```bash
docker run --rm build-context-demo:v1 sh -c 'ls -la /app'
```

Expected results:

- `Dockerfile`, `app.py`, and `requirements.txt` may appear.
- `.git`, `.venv`, `__pycache__`, `debug.log`, and `.env` should not appear when the patterns match and the image was built with the intended `.dockerignore`.

The exact output depends on the files present in the directory.

### Command explanation

- `docker run`: Creates and runs a container.
- `--rm`: Removes the container after it exits.
- `build-context-demo:v1`: Selects the image.
- `sh -c`: Executes the supplied shell command.
- `ls -la /app`: Lists files, including hidden files, inside `/app`.

## 7. Experiment: Build Without `.dockerignore`

Temporarily rename the ignore file:

```bash
mv .dockerignore .dockerignore.bak
```

Rebuild:

```bash
docker build --progress=plain -t build-context-demo:v2 .
```

Inspect the image:

```bash
docker run --rm build-context-demo:v2 sh -c 'ls -la /app'
```

If the sample files exist and are not otherwise excluded, you should see previously excluded items such as `.env`, `debug.log`, `.git`, `.venv`, and `__pycache__`.

Restore the ignore file immediately:

```bash
mv .dockerignore.bak .dockerignore
```

Verify it:

```bash
cat .dockerignore
```

**Security warning:** Never put real credentials in the sample `.env` file. If a secret is copied into an image, removing it in a later Dockerfile layer does not reliably remove it from the image's earlier layers or history.

## 8. Build Context and Layer Caching

Consider this instruction:

```dockerfile
COPY . .
```

Without `.dockerignore`, unrelated files can be included in the build context and copied into the image.

With `.dockerignore`, matching files are excluded from the context used by the build.

This can improve build efficiency and reduce the chance that irrelevant file changes affect cache reuse. However, `.dockerignore` does not guarantee that every build layer will be cached.

For better cache behavior, copy dependency manifests separately from frequently changing source files when the application permits it.

Example:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
```

This allows the dependency-installation layer to remain cacheable when only `app.py` changes, provided the preceding build inputs and instructions remain unchanged and the cache is available.

## 9. Security Considerations

- Exclude local secret files and unnecessary credentials from the build context.
- Never rely on `.dockerignore` as the only security control.
- Do not bake secrets into image layers, Docker build arguments, or image configuration.
- Use an appropriate secrets-management mechanism for build-time and runtime secrets.
- Inspect the final image before publishing it to a registry.
- Remember that `.dockerignore` does not delete files from the host.
- A file excluded from the context cannot be copied by a normal `COPY` instruction from that context, but other mechanisms or separate build contexts may introduce files independently.

## 10. Troubleshooting

### Problem: An excluded file appears in the image

Check:

```bash
cat .dockerignore
docker run --rm build-context-demo:v1 sh -c 'ls -la /app'
```

Possible causes:

- The image was built before `.dockerignore` was restored.
- The wrong build-context directory was used.
- The pattern does not match the file as expected.
- The file was introduced by another Dockerfile instruction or build input.

Rebuild with the intended context and inspect the newly tagged image.

### Problem: Docker cannot find the Dockerfile

Check your current directory:

```bash
pwd
ls -la
```

Run `docker build` from the project directory or explicitly supply the correct Dockerfile and context paths.

### Problem: The image still contains a secret

Do not assume that removing a file in a later layer makes the secret safe. Stop publishing the affected image, rotate any exposed credentials, and rebuild from a clean image history.

## 11. Interview Questions and Answers

### Q1. What is a Docker build context?

The build context is the set of files made available to the Docker build. It is commonly specified by the final path argument in `docker build`, such as `.`.

### Q2. What is `.dockerignore`?

It is a file containing patterns that exclude matching files and directories from the local build context.

### Q3. Why should `.git` be excluded?

Git metadata is generally unnecessary for building an application image. Excluding it reduces unnecessary context content and prevents accidental inclusion in the image.

### Q4. Why exclude `.venv/`?

A local Python virtual environment may contain unnecessary packages, platform-specific binaries, and files that should not be shipped with the application.

### Q5. Does `.dockerignore` delete files from the host?

No. It controls which matching files are excluded from the build context; the files remain on the host.

### Q6. Does `.dockerignore` automatically reduce container memory usage?

No. Its primary purpose is to control build-context contents. Runtime memory usage depends on the application, its workload, and container configuration.

### Q7. Does `.dockerignore` guarantee Docker layer-cache reuse?

No. Cache reuse depends on the build instructions, their inputs, and cache availability. Excluding irrelevant files can help avoid unnecessary cache invalidation.

### Q8. What is the difference between `.dockerignore` and a multi-stage build?

`.dockerignore` excludes files from the build context. A multi-stage build uses multiple `FROM` stages so that the final image can contain only the required runtime artifacts, rather than all build tools and intermediate files.

### Q9. Is `.dockerignore` sufficient to protect secrets?

No. It reduces accidental exposure through the build context, but secrets must also be handled securely through appropriate build and runtime secret mechanisms.

### Q10. What should you check if an excluded file appears in an image?

Check the active build context, the `.dockerignore` patterns, the exact image tag being inspected, and whether another build instruction or source introduced the file.

## 12. Cleanup

Remove the test images when they are no longer required:

```bash
docker image rm build-context-demo:v1 build-context-demo:v2
```

This removes the two named image tags if Docker can remove them. If a running container or another dependency prevents removal, inspect the dependency before taking further action.


## 13. Key Takeaways

- The build context defines which files are available to the build.
- `.dockerignore` excludes matching files from that context.
- `COPY . .` copies available context contents, not every file on the host.
- Excluding unnecessary files can improve build efficiency and reduce accidental exposure.
- `.dockerignore` is not a substitute for secrets management.
- Multi-stage builds and `.dockerignore` solve different problems.

