## Redis

### Redis集群

#### 槽

* 槽解决的是粒度问题，把粒度变小，便于数据移动
* 哈希解决的是映射问题，使用key的哈希值映射到槽，便于数据分配

#### get

* key -&gt; hash -&gt; slot -&gt; node
* 客户端缓存槽和节点的映射
* node重定向
* 不支持mget不同的node，解决方案{prefix}.suffix


[<< 上一篇: ElasticSearch](11-中间件/ElasticSearch.md)

[>> 下一篇: Tomcat](11-中间件/Tomcat.md)
