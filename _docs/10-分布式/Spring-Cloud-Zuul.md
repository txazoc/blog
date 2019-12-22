### Spring-Cloud-Zuul

#### Zuul功能

* 鉴权
* 动态路由
* 负载均衡(Ribbon)
* Hystrix: 隔离、限流、熔断、降级
* 黑白名单
* 监控

#### Zuul Filter

* `ZuulServlet`
* `pre filters`
    * PreDecorationFilter: 路由查找
        * `serviceId`: 服务id路由 `-&gt;` RibbonRoutingFilter
        * `routeHost`: url路由 `-&gt;` SimpleHostRoutingFilter
* `route filters`
    * RibbonRoutingFilter: Ribbon `-&gt;` Hystrix `-&gt;` HttpClients转发请求)
    * SimpleHostRoutingFilter: HttpClient
* `post filters`
    * SendResponseFilter: 写response
* `error filters`
    * SendErrorFilter: 抛异常，forward到`error.path`

**服务id路由:**

```yaml
zuul:
  routes:
    user:
      path=/user/**
      serviceId=service-user
    trade:
      path=/trade/**
      serviceId=service-trade
```

**url路由:**

```yaml
zuul:
  routes:
    index:
      path=/index/**
      url=http://127.0.0.1:9999
```
