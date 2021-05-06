### Nginx

#### Nginx功能

* 反向代理: 代理内网服务器来接收internet上的请求
* 负载均衡

#### Nginx负载均衡算法

* round-robin: 轮询，默认的负载均衡算法
* ip_hash: ip哈希
* least-conn: 最少连接

#### Nginx配置

```conf
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
    # 日志格式
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    # 负载均衡
    upstream image.txazo.com {
        # 轮询
        round-robin;
        server 127.0.0.1:8080;
        server 127.0.0.1:8081;
    }
    
    # 负载均衡
    upstream blog.txazo.com {
        # ip哈希
        ip_hash;
        server 127.0.0.1:8082;
        server 127.0.0.1:8083;
    }
    
    server {
        # 监听端口
        listen 80;
        # 虚拟主机
        server_name image.txazo.com;
        # 访问日志
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
        # 监听端口
        listen 80;
        # 虚拟主机
        server_name blog.txazo.com;
        # 访问日志
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


[<< 上一篇: Redis](11-中间件/Redis.md)

[>> 下一篇: ElasticSearch权威指南](11-中间件/ElasticSearch权威指南.md)
