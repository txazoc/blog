### ElasticSearch权威指南

#### 概念

* ElasticSearch集群 <> 关系数据库
* `索引`(Index) <> 数据库
* `类型`(Type) <> 表
    * `映射`(Mapping) <> 表结构
* `文档`(Document) <> 行
* `字段`(Field) <> 列

#### ElasticSearch集群

#### API

##### _id查询

```js
GET /index/type/1
{
    "_index": "index",
    "_type": "type",
    "_id": "1",
    "_version": 1,
    "found": true,
    "_source": {}
}
```

#### DSL

##### match查询

```json
{
    "query": {
        "match": {
            "name": "游戏"
        }
    }
}
```

##### match_phrase查询

> 精确匹配短语

```json
{
    "query": {
        "match_phrase": {
            "name": "大话西游手游"
        }
    }
}
```

##### 批量API

* mget
* bulk

#### 分片路由

`shard = hash(routing) % number_of_primary_shards`

#### 文档

> 文档即json对象

##### 文档元数据

* _index
* _type
* _id

##### _id

* 自定义_id: `PUT /{index}/{type}/{id}`
* 自动生成_id: `POST /{index}/{type}`，自动生成的_id为`20位`的GUID字符串

##### 版本号_version

##### 更新文档

> `注`: ElasticSearch中文档是`不可改变`的

* 查询旧文档
* 旧文档标记为删除
* 索引新文档，_version++

##### 删除文档

* 查询文档
* 标记为删除，_version++

##### 乐观锁解决并发更新冲突

* _version: `PUT /{index}/{type}/{id}?version={version}`
* 外部版本号: `PUT /{index}/{type}/{id}?version={version}&version_type=external`，_version小于外部版本号

##### 部分更新

* 更新部分字段

```json
POST /{index}/{type}/{id}?_update
{
    "doc": {
        "status": 1
    }
}
```

* 脚本更新部分字段

```json
{
   "script" : "ctx._source.views+=1"
}
```

```json
{
    "script": "ctx._source.status=status",
    "params": {
        "status": 1
    }
}
```

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
