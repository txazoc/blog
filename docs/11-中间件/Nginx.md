### Nginx

#### 反向代理

> 代理内网服务器来接收外部的请求

#### 负载均衡

#### Nginx配置

```console
user www www;
worker_processes auto;
pid logs/nginx.pid;

events {
    # 事件模型
    use epoll;
    # 最大连接数
    worker_connections 65535;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    # 负载均衡
    upstream image.txazo.com {
        server 127.0.0.1:8080;
        server 127.0.0.1:8081;
    }
    
    # 负载均衡
    upstream blog.txazo.com {
        server 127.0.0.1:8082;
        server 127.0.0.1:8083;
    }
    
    server {
        listen 80;
        # 虚拟主机
        server_name image.txazo.com;
        access_log logs/image_txazo_com.access.log main;
        
        location / {
            # 反向代理
            proxy_pass http://image.txazo.com;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    
    server {
        listen 80;
        # 虚拟主机
        server_name blog.txazo.com;
        access_log logs/blog_txazo_com.access.log main;
        
        location / {
            # 反向代理
            proxy_pass http://blog.txazo.com;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
}
```


[<< 上一篇: LVS](11-中间件/LVS.md)

[>> 下一篇: Redis](11-中间件/Redis.md)
