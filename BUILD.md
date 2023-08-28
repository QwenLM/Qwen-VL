## build

```
docker build -t qwen-vl-chat:latest --platform linux/amd64 . 
```

## run

```
docker run -it --gpus all -d --restart always -v /var/run/docker.sock:/var/run/docker.sock --name qwen-vl-chat -p 8000:8000 --user=20001:20001 --platform linux/amd64 qwen-vl-chat:latest
```
