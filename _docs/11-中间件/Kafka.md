### Kafka

参考资料: https://juejin.im/post/5de36418e51d4532e871ada3

#### Kafka概念

* `Broker`: Kafka实例节点
* `Controller`: 控制器，Kafka集群中的一个`Broker`，负责监听`Zookeeper`，管理Kafka集群的元数据
* `Topic`: 消息主题
* `Partition`: 分区，一个`Topic`有多个分区
* `Replication`: 副本，一个分区有多个副本
* `Offset`: 消息偏移量
* `Record`: 消息记录
* `Producer`: 生产者，发送消息到Kafka
* `Consumer`: 消费者，消费Kafka中的消息
* `Consumer Group`: 消费者组，一个消费者组中同一条消息只会被消费一次

#### Kafka高性能

* 磁盘顺序IO: 顺序写、顺序读
* 零拷贝

#### Kafka集群搭建

**启动Zookeeper:**

```bash
> bin/zkServer.sh start
```

***修改Kafka配置文件***

```bash
> cp config/server.properties config/server-1.properties
> cp config/server.properties config/server-2.properties
> cp config/server.properties config/server-3.properties
```

**config/server-1.properties:**

```console
broker.id=1
listeners=PLAINTEXT://:9081
log.dir=/tmp/kafka-logs-1
```

**config/server-2.properties:**

```console
broker.id=2
listeners=PLAINTEXT://:9082
log.dir=/tmp/kafka-logs-2
```

**config/server-3.properties:**

```console
broker.id=3
listeners=PLAINTEXT://:9083
log.dir=/tmp/kafka-logs-3
```

**启动Kafka:**

```bash
> bin/kafka-server-start.sh config/server-1.properties &
> bin/kafka-server-start.sh config/server-2.properties &
> bin/kafka-server-start.sh config/server-3.properties &
```

#### Broker

#### Controller

```bash
> get /controller
{"version":1,"brokerid":1,"timestamp":"1579342747527"}
```

#### Topic

**创建多分区和多副本的Topic:**

```bash
> bin/kafka-topics.sh --create --zookeeper 127.0.0.1:2181 --replication-factor 2 --partitions 5 --topic test
```

**查看Topic:**

```bash
> bin/kafka-topics.sh --describe --zookeeper 127.0.0.1:2181 --topic test
Topic:test	PartitionCount:5	ReplicationFactor:2	Configs:
	Topic: test	Partition: 0	Leader: 2	Replicas: 2,1	Isr: 2,1
	Topic: test	Partition: 1	Leader: 3	Replicas: 3,2	Isr: 3,2
	Topic: test	Partition: 2	Leader: 1	Replicas: 1,3	Isr: 1,3
	Topic: test	Partition: 3	Leader: 2	Replicas: 2,3	Isr: 2,3
	Topic: test	Partition: 4	Leader: 3	Replicas: 3,1	Isr: 3,1
```

* `Topic`: 消息主题
* `PartitionCount`: 分区数
* `ReplicationFactor`: 副本数
* `Partition`: 分区id
* `Leader`: 分区主节点id
* `Replicas`: 分区副本节点id列表(包含Leader)
* `Isr`: 
* `Leader`
* `Follower`: 同步`Leader`的数据

```bash
// Broker 1
/tmp/kafka-logs-1/test-0    Follower
/tmp/kafka-logs-1/test-2    Leader
/tmp/kafka-logs-1/test-4    Follower

// Broker 2
/tmp/kafka-logs-2/test-0    Leader
/tmp/kafka-logs-2/test-1    Follower
/tmp/kafka-logs-2/test-3    Leader

// Broker 3
/tmp/kafka-logs-3/test-1    Leader
/tmp/kafka-logs-3/test-2    Follower
/tmp/kafka-logs-3/test-3    Follower
/tmp/kafka-logs-3/test-4    Leader
```

#### Partition

**Partition日志存储:**

```bash
> ll /tmp/kafka-logs-1/test-0
00000000000000000000.index
00000000000000000000.log
00000000000000000000.timeindex
00000000000000645287.index
00000000000000645287.log
00000000000000645287.timeindex
00000000000001354234.index
00000000000001354234.log
00000000000001354234.timeindex
```

* `.index`: offset索引文件
* `.log`: 日志文件
* `.timeindex`: 时间戳索引文件

`稀松索引`

#### Offset

`consumer_offset`

#### Zookeeper

#### Producer

##### KafkaProducer初始化

* 解析Kafka生产者配置(`ProducerConfig`)
* 创建消息缓冲区(`RecordAccumulator`)
* 创建元数据(`Metadata`)
    * `bootstrap.servers`: Broker节点列表，提供建立到Kafka集群的初始连接
* 创建并启动消息发送线程(`Sender`)

##### 生产者发送消息

* 构建消息(`ProducerRecord`)
    * `topic`: 主题
    * `partition`: 分区id
    * `key`: 消息的key
    * `value`: 消息内容
* 发送消息
    * `KafkaProducer.send(ProducerRecord<K, V> record, Callback callback)`
        * `record`: 消息记录
        * `callback`: 消息回调
* 消息拦截器链(`ProducerInterceptors`)
    * `ProducerInterceptor.onSend()`
* 元数据(`Metadata`)更新
    * 无topic分区信息或无效的`partition`，更新元数据
    * `metadata.max.age.ms`: 元数据强制刷新的间隔数据，默认为`5分钟`
    * 元数据更新流程
        * 设置`needUpdate`标识，唤醒`Sender`线程，`Metadata.wait()`等待
        * `Sender`线程发送请求拉取元数据，更新元数据，`Metadata.notifyAll()`唤醒消息发送线程
* key/value序列化
    * `key.serializer`: key序列化器，org.apache.kafka.common.serialization.StringSerializer
    * `value.serializer`: value序列化器，org.apache.kafka.common.serialization.StringSerializer
* 分区(`Partitioner`)
    * 消息已分配了`partition`，使用已分配好的`partition`，否则使用`分区器`选择分区
    * 分区器`partitioner.class`: 默认分区器`DefaultPartitioner`
        * key不为null，`partition = hash(key) % 分区数`
        * key为null，计数器`轮询`负载均衡，优先分配到可用分区
* 校验消息大小
    * `消息大小` = 消息头大小 + key大小 + value大小
    * `消息大小`不可超过`max.request.size`: 单个消息的最大大小，默认为`1M`
    * `消息大小`不可超过`buffer.memory`: 消息缓冲区(`RecordAccumulator`)的大小，默认为`32M`
* 绑定消息回调`InterceptorCallback`: `Callback` + `ProducerInterceptors`
* 消息追加到消息缓冲区(`RecordAccumulator`)
    * `RecordAccumulator`
        * `Map<TopicPartition, Deque<ProducerBatch>> batches`: 每个topic的每个分区对应一个`batch`队列
        * `ProducerBatch`: 一批消息`batch`
    * 创建`batch`
        * `batch.size`: 默认为`16k`
        * 消息大小不超过`batch.size`，`batch`大小为`batch.size`，`batch`中可以追加多条消息
        * 消息大小超过`batch.size`，`batch`大小为消息大小，一个`batch`中只包含一条消息
        * `batch`分配`ByteBuffer`
    * 消息追加到`batch`
        * 消息追加到`batch`的`ByteBuffer`中
        * 生成`future`，绑定`future`和回调`InterceptorCallback`
* 唤醒消息发送线程(`Sender`)
* 返回future(`FutureRecordMetadata`)
    * 异步发送: 默认发送方式
    * 同步发送: `future.get()`，等待`ack`
* 消息发送线程(`Sender`)

##### 生产者参数

参考`ProducerConfig`

* `bootstrap.servers`: Broker节点列表
* `metadata.max.age.ms`: 元数据强制刷新的间隔数据，默认为`5分钟`
* `batch.size`: `batch`大小，默认为`16k`
* `acks`: 消息确认
    * `0`: 消息发送即可
    * `1`: 确保Leader写入消息，默认值
    * `-1`: `all`，确保Leader和所有ISR写入消息
* `linger.ms`: `batch`未满时，延迟发送的时间，默认为0，无延迟
* `request.timeout.ms`: 请求发出后等待响应的超时时间，默认为30s
* `delivery.timeout.ms`: 消息发送交付的超时时间，`send()`同步返回的最长时间，默认为`120s`
    * 失败重试时判断是否已超时
* `send.buffer.bytes`: Socket发送缓冲区大小，默认为`128k`
* `receive.buffer.bytes`: Socket接收缓冲区大小，默认为`32k`
* `max.request.size`: 单个消息的最大大小，默认为`1M`
* `max.block.ms`: 消息发送时阻塞的最长时间，默认为60s
    * `阻塞时间` = 等待元数据更新的时间 + 等待有可用buffer的时间
    * `阻塞时间` &gt;= `max.block.ms`，抛出`TimeoutException`
* `buffer.memory`: 消息缓冲区大小，默认为`32M`
* `retry.backoff.ms`: 消息发送失败重试间隔时间，默认为`100ms`
* `compression.type`: 消息压缩类型
    * `none`: 不压缩，默认类型
    * `gzip`、`snappy`、`lz4``zstd`
* `max.in.flight.requests.per.connection`: 针对单个连接生产者继续发送前未确认的最大请求数，默认为`5`
    * 当前未确认请求数 >= `max.in.flight.requests.per.connection`: 阻塞
    * 大于1且`retries` &gt; 1时，重试可能导致消息乱序，设为1可以保证消息的顺序性
* `retries`: 消息发送失败重试次数，默认为int最大值
* `key.serializer`: key序列化器
* `value.serializer`: value序列化器
* `connections.max.idle.ms`: 空闲连接的超时时间，默认为`9分钟`
* `partitioner.class`: 分区器
* `interceptor.classes`: 消息拦截器列表
* `enable.idempotence`: 是否开启幂等，默认为`false`
    * `true`: 保证消息的幂等，此时必须符合以下条件
        * `retries` &gt; 0
        * `acks` == `-1`
        * `max.in.flight.requests.per.connection` &lt; 5

```java
Properties props = new Properties();
props.put("bootstrap.servers", "192.168.1.102:9081,192.168.1.102:9082,192.168.1.102:9083");
props.put("batch.size", 16 * 1024);
props.put("acks", "all");
props.put("linger.ms", 10);
props.put("send.buffer.bytes", 128 * 1024);
props.put("receive.buffer.bytes", 32 * 1024);
props.put("max.request.size", 1024 * 1024);
props.put("max.block.ms", 60 * 1000);
props.put("buffer.memory", 32 * 1024L * 1024L);
props.put("retry.backoff.ms", 100);
props.put("compression.type", "gzip");
props.put("max.in.flight.requests.per.connection", 1);
props.put("retries", 3);
props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
props.put("partitioner.class", "org.apache.kafka.clients.producer.internals.DefaultPartitioner");
props.put("interceptor.classes", Collections.singleton(LogProducerInterceptor.class.getName()));
Producer<String, String> producer = new KafkaProducer<>(props);
```

#### Consumer

##### Coordinator

#### Kafka源码编译调试

##### 环境和版本

* 操作系统: Mac
* Java: 1.8.0_131
* Scala: 2.12.2
* Gradle: 5.0
* Kafka: 2.1.1

##### 准备

修改`build.gradle`:

```js
buildscript {
  repositories {
    mavenCentral()
    jcenter()
    maven {
      url "https://plugins.gradle.org/m2/"
      // 新增下面两行
      url "https://maven.aliyun.com/nexus/content/groups/public/"
      url "https://maven.aliyun.com/repository/gradle-plugin/"
    }
  }
}
```

##### 编译

```bash
> gradle idea
Starting a Gradle Daemon (subsequent builds will be faster)

> Configure project :
Building project 'core' with Scala version 2.11.12
Building project 'streams-scala' with Scala version 2.11.12

> Task :idea
Generated IDEA project at file:///Users/txazo/GitHub/kafka-2.1.1/kafka-2.1.1.ipr

BUILD SUCCESSFUL in 17s
28 actionable tasks: 28 executed
```

##### IDEA运行

IDEA中安装`Scala`插件

Kafka项目导入到IDEA中

运行`kafka.Kafka`
