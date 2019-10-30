## ElasticSearch

> 分布式全文搜索引擎

### ElasticSearch层次结构

#### Cluster(集群)

#### Node(节点)

* Master Node: 主节点，负责管理集群相关操作
* Data Node: 数据节点，负责索引和搜索文档
* Ingest Node: 预处理节点
* Coordinating Node: 协调节点，负责接收客户端请求，将请求转发给数据节点，收集数据节点的返回结果，合并后返回给客户端

#### Index(索引)

* 周期性索引: 以时间为单位来创建索引，例如`index_20190426`、`index_20190427`
* 索引别名: 关联并聚合多个索引

#### Shard(分片)

> 一个分片是一个Lucene索引

* Primary Shard: 主分片
* Replica Shard: 副本分片
* `index.number_of_shards`: 分片数
* 分片路由: `shard = hash(routing) % number_of_shards`，`routing`默认为文档的`_id`

#### Replica(副本)

#### Lucene Index(Lucene索引)

> Lucene索引是一个完整的搜索引擎

#### Segment(段)

> 一个Segment是一个倒排索引，每次`refresh`都会生成一个新的Segment，Segment具有不变性

* Commit point: 记录所有Segment的元数据
* Segment: `in-memory buffer` -&gt; `os buffer` -&gt; `Segment File`
    * in-memory buffer: 每次都写in-memory buffer
    * os buffer: refresh，in-memory buffer写入os buffer，清空in-memory buffer
    * Segment File: flush，os buffer写入Segment File
* Translog: `os buffer` -&gt; `Translog File`
    * os buffer: 每次都写os buffer
    * Translog File: 每隔5s，os buffer写入Translog File
* Segment合并: 较小的段合并为大的段，合并后标记为删除的文档不会写入新分段

#### Document(文档)

> 文档由(_index, _type, _id)唯一标识，存储一个json对象

* _id: 文档标识
* _version: 文档版本号，文档被修改时版本号递增，可实现乐观锁
* _source: 文档数据

#### Field(域)

> 每个Field被单独建立索引

#### Term(词)

> 分词

### ElasticSearch动作

#### refresh

* `index.refresh_interval`: refresh时间间隔，默认为1s，为-1则关闭refresh
* 强制刷新: `http://127.0.0.1:9200/index/_refresh`
* refresh流程
    * in-memory buffer中的文档写入一个新的Segment(os buffer)
    * Segment(os buffer)被打开，可以被搜索
    * 清空in-memory buffer

#### flush

* `index.translog.flush_threshold_period`: flush时间间隔，默认为30分钟
* `index.translog.flush_threshold_size`: translog的最大大小，超过后flush
* `index.translog.disable_flush`: 禁用事务日志flush
* 强制刷新: `http://127.0.0.1:9200/index/_flush`
* flush流程
    * in-memory buffer中的文档写入一个新的Segment(os buffer)
    * 清空in-memory buffer
    * 写Commit point
    * Segment(os buffer) fsync到磁盘
    * translog被删除，新建一个translog

### ElasticSearch读写

#### 写入

* 客户端: 请求发送给协调节点
* 协调节点: 分片路由，转发到主分片，执行成功后，返回客户端
* 主分片: 索引写入，并行转发给副本分片，所有的副本分片执行成功后，返回协调节点
* 副本分片: 索引写入，返回主分片

`索引写入`，先写Lucene，后写translog

##### Create

> 文档写入新的Segment

* 指定`_id`时，会先查询index中是否存在相同`_id`的doc
* 不指定`_id`时，ES自动生成唯一`_id`，跳过查询`_id`的步骤

##### Update

> 文档写入新的Segment，老的文档标记为删除

##### Delete

> 文档标记为删除

`标记删除`，以`_id`为单位的删除操作不会删除文档，只是将文档标记为删除

#### Get

> 分片路由，负载均衡，返回客户端

#### Search

> 循环遍历所有分片，负载均衡，合并排序，fetch，返回客户端


[<< 上一篇: 限流](10-分布式/限流.md)

[>> 下一篇: Redis](11-中间件/Redis.md)
