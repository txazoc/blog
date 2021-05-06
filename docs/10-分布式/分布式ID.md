## 分布式ID

* 必需: 全局唯一
* 可选: 趋势递增、单调递增、时间相关

### UUID

128位二进制，`32位十六进制`

`550e8400-e29b-41d4-a716-446655440000`

**UUID编码规则:**

* 1~8位采用系统时间，在系统时间上精确到毫秒级保证时间上的惟一性
* 9~16位采用底层的IP地址，在服务器集群中的惟一性
* 17~24位采用当前对象的HashCode值，在一个内部对象上的惟一性
* 25~32位采用调用方法的一个随机数，在一个对象内的毫秒级的惟一性

### 数据库分表

* 不同的`auto_increment_offset`
* 相同的`auto_increment_increment`
* `table_000`: 初始值=n 步长=n
* `table_001`: 初始值=n+1 步长=n
* ...

### Redis

* incr

### 数据库发号器

> 按号段进行分配，`[n, n + 1000)`

表结构设计:

* biz_tag: 业务标识
* max_id: 已被分配号段的最大值，`bigint(20)`
* step: 每次分配号段的长度

```sql
begin;
update table set max_id = max_id + step where biz_tag = ?;
select biz_tag, max_id, step from table where biz_tag = ?;
commit;
```

优化:

* 预分配加载: 当前号段下发50%，拉取下一个号段，双号段缓存
* MySQL主从: 半同步复制、全同步复制

### 雪花算法(Snowflake)

> Snowflake是Twitter提出来的一个算法

* 最高位是符号位，始终为0，不可用
* `41位的时间序列`，精确到毫秒级，41位的长度可以使用69年，时间位还有一个很重要的作用是可以根据时间进行排序
* workerid: `10位的机器标识`，10位的长度最多支持部署1024个节点，可以拆分为机房id + 机器id
    * zookeeper持久顺序节点
* sequence: `12位的计数序列号`，序列号即一系列的自增id，可以支持同一节点同一毫秒生成多个ID序号，12位的计数序列号支持每个节点每毫秒产生4096个ID序号

#### 时钟回拨

* 失败
* 使用新的workerid
* 记录并使用回拨时钟的sequence自增

### 雪花算法变种

> `时间戳`、`机房id`、`机器id`、`自增id`、`业务id`组合


[<< 上一篇: Spring-Cloud](10-分布式/Spring-Cloud.md)

[>> 下一篇: Spring-Cloud-Zuul](10-分布式/Spring-Cloud-Zuul.md)
