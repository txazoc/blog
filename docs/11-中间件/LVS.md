### LVS

> Linux Virtual Server，Linux虚拟服务器

#### LVS三种工作模式

* VS/NAT

> 改写请求报文的`目标IP地址`，请求转发到真实服务器，真实服务器将响应返回给`调度器`，`调度器`将响应返回给`客户端`

* VS/TUN

> 请求报文通过`IP隧道技术`转发到真实服务器，真实服务器将响应直接返回给`客户端`

* VS/DR

> 改写请求报文的`目标MAC地址`，请求转发到真实服务器，真实服务器将响应直接返回给`客户端`

#### LVS调度算法

* 轮询
* 加权轮询
* 最少连接
* 加权最少连接
* ...


[<< 上一篇: ElasticSearch](11-中间件/ElasticSearch.md)

[>> 下一篇: 高可用](12-架构/高可用.md)
