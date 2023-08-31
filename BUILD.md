## qwen web demo

### build

```
docker build -t qwen-vl-chat:webdemo --platform linux/amd64 -f Dockerfile.qwendemo . 
```

### run

```
docker run -it --gpus all -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name qwen-vl-chat -p 8000:8000 --user=20001:20001 --platform linux/amd64 qwen-vl-chat:webdemo
```

## qwen openai api

### build

```
docker build -t qwen-vl-chat:openai --platform linux/amd64 -f Dockerfile.qwenopenai . 
```

### run

```
docker run -it --gpus all -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name qwen-vl-chat -p 8080:8080 --user=20001:20001 --platform linux/amd64 qwen-vl-chat:openai
```

## whisper openai api

### build

```
todo
```

### run

```
docker run -it --gpus all -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name whisper -p 8080:8080 --user=20001:20001 --platform linux/amd64 whisper:openai
```

## dall-e openai api

### build

```
todo
```

### run

```
docker run -it --gpus all -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name dall-e -p 8080:8080 --user=20001:20001 --platform linux/amd64 dall-e:openai
```
