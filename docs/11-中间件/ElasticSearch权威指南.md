### ElasticSearch权威指南

##### 分片路由

`shard = hash(routing) % number_of_primary_shards`

#### Mapping

* text
* keyword
* date
* long
* double
* boolean

```json
PUT /test
{
  "properties": {
    "employee-id": {
      "type": "keyword",
      "index": "no"
    }
  }
}
```


[<< 上一篇: ElasticSearch](11-中间件/ElasticSearch.md)

[>> 下一篇: LVS](11-中间件/LVS.md)
