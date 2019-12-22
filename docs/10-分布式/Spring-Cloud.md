## Spring Cloud

https://www.cnblogs.com/crazymakercircle/p/11674597.html

### Spring Cloud架构图

<p style="text-align: center;"><img src="_media/distribution/spring-cloud.png" alt="Spring Cloud" style="width: 100%"></p>

### Eureka

> 注册中心

#### Eureka Client

服务提供者:

* 启动时注册到Eureka Server: POST http://localhost:8761/eureka/apps/SPRING-CLOUD-ZUUL
    * eureka.client.register-with-eureka: true，是否将自己的实例信息注册到EurekaServer
* 发送心跳: HeartbeatThread
* 实例信息更新: InstanceInfoReplicator
    * eureka.client.instance-info-replication-interval-seconds: 30，同步实例信息变化到EurekaServer的间隔时间
    * eureka.client.initial-instance-info-replication-interval-seconds: 40，初始化实例信息到EurekaServer的间隔时间

* 服务下线时从Eureka Server摘除: DELETE http://localhost:8761/eureka/apps/SPRING-CLOUD-ZUUL

服务消费者:

* 启动时从Eureka Server拉取服务注册信息: GET http://localhost:8761/eureka/apps/
    * eureka.client.fetch-registry: true，是否从EurekaServer拉取注册信息
* 周期性拉取服务注册信息: CacheRefreshThread
    * eureka.client.registry-fetch-interval-seconds: 30，从EurekaServer拉取注册信息的间隔时间

#### Eureka Server

* 内存中维护一个注册表(ResponseCacheImpl)，保存各个服务的机器(ip + 端口号)列表
    * readOnlyCacheMap: ConcurrentMap，只读缓存
    * readWriteCacheMap: LoadingCache，读写缓存
* 集群节点对等，同步转发，保证最终一致性
* eureka.instance.lease-expiration-duration-in-seconds: 90，接收到上一次心跳后，EurekaServer等待下一次心跳的超时时间，超时则摘除实例
* eureka.instance.lease-renewal-interval-in-seconds: 30，EurekaClient向EurekaServer发送心跳的间隔时间

#### Eureka配置

* `register-with-eureka`: 是否向注册中心注册自己
* `fetch-registry`: 是否向注册中心拉取服务注册信息
* `eureka.client.registry-fetch-interval-seconds`: Eureka Client拉取服务注册信息的间隔时间，默认为30s
* `eureka.instance.lease-renewal-interval-in-seconds`: Eureka Client向Eureka Server发送心跳的频率，超过则可以摘除instance，默认为30s
* `eureka.instance.lease-expiration-duration-in-seconds`: Eureka Server收到上一次心跳后，等待下一次心跳的超时时间，超时则可以摘除instance，默认为90s

### Feign

> 声明式的HTTP客户端，简化HTTP调用

* 动态代理: ReflectiveFeign$FeignInvocationHandler
* 构造请求地址
    * `@FeignClient`: `ip:port`
        * Eureka: 获取服务机器列表
        * Ribbon: 选择一台机器
    * `@RequestMapping`、`@RequestParam`: `uri`、`参数`
* httpclient/okhttp发送请求

### Ribbon

> 客户端负载均衡

* RoundRobinRule(轮询)，默认策略
* RandomRule(随机)
* WeightedResponseTimeRule(平均响应时间权重)，权重=总的平均响应时间-实例的平均响应时间
* BestAvailableRule(排除熔断后选择并发数最小的Server)

### Hystrix

> 断路器，提供资源隔离、熔断、限流、降级的功能

Request -&gt; `HystrixCommand` -&gt; `请求缓存` -&gt; `熔断开关` -&gt; `线程池/信号量` -&gt; Remote Call

<p style="text-align: center;"><img src="_media/distribution/hystrix.png" alt="Hystrix" style="width: 100%"></p>

#### HystrixCommand

* commandKey
* commandGroup

#### 请求缓存

> 在一个请求上下文中

#### 断路器

断路器状态:

* CLOSED
* HALF_OPEN: 快速恢复
* OPEN: fail-fast(快速失败) -&gt; `fallback`

HystrixCircuitBreaker.allowRequest():

* circuitBreaker.enabled: 断路器开关
* circuitBreaker.forceOpen，是否强制开启中断
* circuitBreaker.forceClosed，是否强制关闭中断
* metrics.rollingStats.timeInMilliseconds: 10000，滑动窗口的统计时间，默认为10s
* circuitBreaker.requestVolumeThreshold: 20，滑动窗口内触发熔断的最少请求阀值，默认为20
* circuitBreaker.errorThresholdPercentage: 50，触发熔断的错误比例，默认为50%
* circuitBreaker.sleepWindowInMilliseconds: 5000，熔断后多长时间，断路器进入HALF_OPEN状态，尝试重试

#### 资源隔离

线程池/信号量满 -&gt; `fallback`

* 线程池: 对依赖服务进行隔离、限流、超时控制
    * execution.isolation.strategy: THREAD，线程池隔离策略
    * HystrixContextScheduler$HystrixContextSchedulerWorker.schedule()
    * HystrixThreadPoolDefault: Hystrix线程池
    * hystrix.threadpool.default.coreSize=10
    * hystrix.threadpool.default.maximumSize=10，allowMaximumSizeToDivergeFromCoreSize为true时才生效，否则maximumSize=coreSize
    * hystrix.threadpool.default.keepAliveTimeMinutes=1，默认存活时间1分钟
    * hystrix.threadpool.default.allowMaximumSizeToDivergeFromCoreSize=false
    * hystrix.threadpool.default.queueSizeRejectionThreshold=5
    * hystrix.threadpool.default.maxQueueSize=-1
        * 不大于0时，workQueue=SynchronousQueue，线程池的拒绝策略
        * 否则，workQueue=LinkedBlockingQueue(maxQueueSize)，queueSize &lt; queueSizeRejectionThreshold
* 信号量: 限流
    * execution.isolation.strategy: SEMAPHORE，信号量隔离策略
    * execution.isolation.semaphore.maxConcurrentRequests: 10，信号量隔离时的最大并发数

#### 超时/异常

* 超时 -&gt; `fallback`
    * executionTimeoutEnabled: 超时开关
    * executionTimeoutInMilliseconds: 超时时间
* 异常 -&gt; `fallback`

#### 降级

* `fallback`


[<< 上一篇: Spring-Cloud-Zuul](10-分布式/Spring-Cloud-Zuul.md)

[>> 下一篇: Zookeeper](10-分布式/Zookeeper.md)
