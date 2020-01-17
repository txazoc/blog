### Kafka

参考资料: https://juejin.im/post/5de36418e51d4532e871ada3

#### Kafka概念

* `Broker`: Kafka实例节点
* `Topic`: 消息主题
* `Partition`: 分区
* `Replication`: 副本
* `Offset`: 消息偏移量
* `Record`: 消息记录
* `Producer`: 生产者
* `Consumer`: 消费者
* `Consumer Group`: 消费者组

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
* `Follower`

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

**分区文件存储:**

```bash
> ll /tmp/kafka-logs-1/test-0
00000000000000000000.index
00000000000000000000.log
00000000000000645287.index
00000000000000645287.log
00000000000001354234.index
00000000000001354234.log
```

#### Offset

#### Zookeeper

#### Producer

##### KafkaProducer初始化

* 解析Kafka生产者配置(`ProducerConfig`)
* 创建消息缓冲区(`RecordAccumulator`)
* 创建元数据(`Metadata`)
    * `bootstrap.servers`: Broker节点列表，提供建立到Kafka集群的初始连接
* 创建并启动消息发送线程(`Sender`)

##### 生产者发送消息

* 发送消息: `KafkaProducer.send()`
* 消息拦截器链(`ProducerInterceptors`)
    * `ProducerInterceptor.onSend()`
* 元数据(`Metadata`)更新
    * 无topic分区信息或无效的`partition`，更新元数据
    * `metadata.max.age.ms`: 元数据强制刷新的间隔数据，默认为`5分钟`
    * 元数据更新流程
        * 设置`needUpdate`标识，唤醒`Sender`线程，`Metadata.wait()`等待
        * `Sender`线程发送请求拉取元数据，更新元数据，`Metadata.notifyAll()`唤醒消息发送线程
* key/value序列化
    * `key.serializer`: org.apache.kafka.common.serialization.StringSerializer
    * `value.serializer`: org.apache.kafka.common.serialization.StringSerializer
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
* 消息发送线程(`Sender`)

#### Consumer


[<< 上一篇: ElasticSearch权威指南](11-中间件/ElasticSearch权威指南.md)

[>> 下一篇: LVS](11-中间件/LVS.md)
