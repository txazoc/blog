### Zookeeper

Zookeeper，是一个高性能的分布式协调服务

#### Zookeeper角色

* Leader
* Follow: 参入投票
* Observer: 不参入投票，扩展系统

#### Zookeeper节点

* `持久节点`(PERSISTENT): 节点被创建后就一直存在，直到主动调用删除操作来删除节点
* `临时节点`(EPHEMERAL): 节点的生命周期同Session相关联，没有子节点
* `顺序节点`(SEQUENTIAL)
    * `持久顺序节点`(PERSISTENT_SEQUENTIAL)
    * `临时顺序节点`(EPHEMERAL_SEQUENTIAL)

#### Zookeeper选举

`epoch(选举周期)` &gt; `zxid(事务id)` &gt; `sid(Server ID)`

#### Zookeeper应用

* 命名服务: 文件系统
* 配置管理: 持久节点 + watch
* 集群管理: 临时节点 + watch
* 分布式锁: 临时顺序节点 + watch
* 分布式队列: 持久顺序节点 + watch


[<< 上一篇: CAP](10-分布式/CAP.md)

[>> 下一篇: 监控中心](10-分布式/监控中心.md)
