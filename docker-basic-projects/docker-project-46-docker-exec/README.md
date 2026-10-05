# Project 46: Execute Commands Inside Running Containers

## Goal

Learn how to execute commands inside a running Docker container using `docker exec`.

## Build

```bash
docker build -t exec-demo:1.0 .
```

## Run

```bash
docker run -d --name exec-demo exec-demo:1.0
```

## Execute Commands

Run `ls`:

```bash
docker exec exec-demo ls
```

Check working directory:

```bash
docker exec exec-demo pwd
```

Read a file:

```bash
docker exec exec-demo cat /app/message.txt
```

Check environment variable:

```bash
docker exec exec-demo printenv APP_NAME
```

## Interactive Shell

```bash
docker exec -it exec-demo sh
```

Exit:

```bash
exit
```

## Run Commands Using `sh -c`

```bash
docker exec exec-demo sh -c 'cd /app && pwd && ls -l'
```

## Change Working Directory

```bash
docker exec -w /tmp exec-demo pwd
```

The `-w` option applies only to that exec process.

## Run as Another User

Check current identity:

```bash
docker exec exec-demo id
```

Run as root:

```bash
docker exec -u root exec-demo id
```

## Inspect Processes

```bash
docker exec exec-demo ps
```

Compare with:

```bash
docker top exec-demo
```

`docker exec` starts a new process inside the container, while `docker top` displays existing container processes.

## Production Troubleshooting

A common investigation sequence is:

```bash
docker ps
docker logs --tail 100 container-name
docker exec container-name ps
docker exec container-name df -h
docker exec container-name free -m
docker exec container-name ls -lah /app
```

Enter the container only when required:

```bash
docker exec -it container-name sh
```

## Important Concept

`docker exec` starts an additional process inside an already-running container.

It does not replace the container's main process.

For example:

```text
Container
│
├── PID 1 → Main application
│
└── docker exec → Additional process
```

Exiting an interactive `docker exec` shell does not stop the container.

## Production Caution

Avoid undocumented manual modifications inside production containers. Containers are normally treated as immutable deployment units and should be rebuilt/redeployed when application or configuration changes are required.

## Cleanup

```bash
docker rm -f exec-demo
docker rmi exec-demo:1.0
```

## Key Commands

```bash
docker exec CONTAINER COMMAND
docker exec -it CONTAINER sh
docker exec -w /path CONTAINER COMMAND
docker exec -u USER CONTAINER COMMAND
```

