### Spring-Cloud-Zuul

> Zuul，微服务网关

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
    * RibbonRoutingFilter: Ribbon `-&gt;` Hystrix `-&gt;` HttpClient转发请求
    * SimpleHostRoutingFilter: HttpClient
* `post filters`
    * SendResponseFilter: 写response
* `error filters`
    * SendErrorFilter: 抛异常，forward到`${error.path}`

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

#### Zuul架构图

![Zuul Filter](../_media/distribution/zuul-filter.png)(60%)

![Zuul Lifecycle](../_media/distribution/zuul-lifecycle.png)(60%)

#### Zuul初始化

ZuulProxyAutoConfiguration

* 

#### Zuul配置

* zuul.ribbon.eager-load.enabled = true，开启Ribbon的饥饿加载模式
