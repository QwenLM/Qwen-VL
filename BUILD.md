## qwen web demo

### build

```
docker build -t qwen-vl-chat:webdemo --platform linux/amd64 -f Dockerfile.qwendemo . 
```

### run

```
docker run -it --gpus device=0 -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name qwen-vl-chat -p 8000:8000 --user=20001:20001 --platform linux/amd64 qwen-vl-chat:webdemo
```

## qwen openai api

### build

```
docker build -t qwen-vl-chat:openai --platform linux/amd64 -f Dockerfile.qwenopenai . 
```

### run

```
docker run -it --gpus device=0 -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name qwen-vl-chat -p 8080:8080 --user=20001:20001 --platform linux/amd64 qwen-vl-chat:openai
```

## qwen-int4 openai api

### build

```
docker build -t qwen-vl-chat:int4-openai --platform linux/amd64 -f Dockerfile.qwenint4openai . 
```

### run

```
docker run -it --gpus device=0 -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name qwen-vl-chat-int4 -p 8080:8080 --user=20001:20001 --platform linux/amd64 qwen-vl-chat:int4-openai
```
