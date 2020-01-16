### Kafka

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

#### Consumer
