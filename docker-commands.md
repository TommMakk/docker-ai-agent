# Common Docker Commands

## Docker-specific
### Clear System

```bash
docker system prune -a
docker image prune -a
```

### Build and Run Locally

Container image tag: `pyapp`

```bash
docker build -f Dockerfile -t pyapp .
```

```bash
docker run -it pyapp
```

### Enter Container Command Line (like _ssh_)

```bash
docker run -it pyapp /bin/bash
```
> `/bin/bash` just runs the bash shell, you can also run `docker run -it pyapp python` or `docker run -it pyapp node` if those tools are avialable.

## Docker Compose

#### Build with Docker Compose

```bash
docker compose up
```

```bash
docker compose down
```

```bash
docker compose run <service_name> /bin/bash
```

## Check that its running
# 4. Test running the model directly
ollama run llama3.2
# Start the Ollama server in the foreground (Ctrl+C to stop)
ollama serve

## Docker Model Runner

_From host terminal_
```bash
curl http://localhost:11435/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": "Please write 500 words about the history of Italy" }
    ]
  }'
```


_From within a container_
```bash
docker compose exec backend curl http://ollama:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [
      { "role": "system", "content": "You are a helpful assistant." },
      { "role": "user", "content": "Please write 500 words about the history of Italy." }
    ]
  }'
```
