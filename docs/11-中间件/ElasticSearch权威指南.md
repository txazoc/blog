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

```js
POST /{index}/{type}/{id}?_update
{
    "doc": {
        "status": 1
    }
}
```

* 脚本更新部分字段

```js
{
   "script" : "ctx._source.views+=1"
}
```

```js
{
    "script": "ctx._source.status=status",
    "params": {
        "status": 1
    }
}
```

#### 文本分析(Text analysis)

文本分析过程: `字符过滤器` -&gt; `分词器` -&gt; `Token过滤器`

##### 字符过滤器(Character Filters)

> 过滤掉一些无效的字符

##### 分词器(Tokenizers)

> 字符串分割为单个的Token

##### Token过滤器(Token Filters)

> 对Token进行过滤处理，包括新增Token、修改Token、删除Token

##### 分析器(Analyzers)

> 字符过滤器 + 分词器 + Token过滤器的组合，ElasticSearch中内置了一些分析器

##### Analyze API

**指定分析器:**

```js
GET /_analyze
{
  "analyzer": "standard",
  "text": "中国"
}
```

**自定义字符过滤器、分词器、Token过滤器:**

```js
GET /_analyze
{
  "char_filter": [ "html_strip" ],
  "tokenizer": "standard",
  "filter": [ "lowercase" ],
  "text": "<p>Hi, tom</p>"
}
```

#### 映射(Mapping)

> 定义一个文档中包含的字段、字段类型、字段如何存储、字段如何索引

> ElasticSearch中索引的数据分为`精确值`和`全文`两类

##### 简单字段类型

**ElasticSearch支持以下几种简单字段类型:**

* 字符串: `text`(全文)、`keyword`(精确值)
* 日期: `date`
* 整数: `byte`、`short`、`integer`、`long`
* 浮点数: `float`、`double`
* 布尔: `boolean`

```js
PUT /app
{
  "mappings": {
    "app": {
      "properties": {
        "name": {
          "type": "keyword"
        },
        "type": {
          "type": "byte"
        },
        "price": {
          "type": "float"
        },
        "published": {
          "type": "boolean"
        },
        "date": {
          "type": "date"
        },
        "avatar": {
          "type": "text",
          "index": false
        },
        "description": {
          "type": "text",
          "analyzer": "standard"
        }
      }
    }
  }
}
```

```js
PUT /app/app/1
{
  "name": "QQ飞车",
  "type": 1,
  "price": 100.00,
  "published": true,
  "date": "2019-12-18",
  "avatar": "http://www.test.com/qqcar.png",
  "description": "《QQ飞车》腾讯游戏发行的一款网络游戏"
}
```

##### Multi-Field

> 以不同的方式同时索引同一个字段，ElasticSearch对字符串默认开启`text`和`keyword`

```js
PUT /test/test/1
{
  "name": "root"
}
```

```js
GET /test/test/_mapping
{
  "test": {
    "mappings": {
      "test": {
        "properties": {
          "name": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    }
  }
}
```

**keyword字段精确匹配:**

```js
GET /test/test/_search
{
  "query": {
    "match": {
      "name": "西游"
    }
  }
}
```

**text字段精确匹配:**

```js
GET /test/test/_search
{
  "query": {
    "match": {
      "name.keyword": "大话西游"
    }
  }
}
```

##### 数组类型

```js
PUT /{index}/{type}/{id}
{
  "tags": [ "red", "green" ]
}
```

##### JSON对象类型

```js
PUT /user/user/1
{
  "id": 1,
  "user": {
    "name": "吴亦凡",
    "age": 24
  }
}
```

```js
GET /user/user/_search
{
  "query": {
    "match": {
      "user.name.keyword": "吴亦凡"
    }
  }
}
```

#### 分布式

##### 分片路由

`shard = hash(routing) % number_of_primary_shards`

##### 写操作(插入、更新、删除文档)

* 协调节点: 分片路由，请求转发到主分片节点
* 主分片节点: 写文档，同步到副本分片节点
* 副本分片节点: 写文档

##### 读操作(查询文档)

* 协调节点: 分片路由，负载均衡选择副本分片节点
* 副本分片节点: 读文档

##### 批量操作mget/bulk

* 协调节点: 分片路由，分片分组，并行转发分组请求

#### 搜索

##### 搜索结果格式

```js
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 1,
    "max_score": 1,
    "hits": [
      {
        "_score": 1
        // ...
      }
    ]
  }
}
```

* took: 搜索消耗的时间
* timed_out: 是否超时
* _shards: 参与的分片数
* hits: 命中的文档
* total: 命中的文档总数
* max_score: _score的最大值
* _score: 文档的分值

##### 空搜索

```js
GET /app/_search
```

#### 分页

`from`默认为0，`size`默认为10

```js
GET /app/_search
{
  "from": 1,
  "size": 2
}
```

> `注`: 避免深度分页

##### match查询

```js
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

```js
{
  "query": {
    "match_phrase": {
      "name": "大话西游手游"
    }
  }
}
```

##### bool查询


[<< 上一篇: ElasticSearch](11-中间件/ElasticSearch.md)

[>> 下一篇: LVS](11-中间件/LVS.md)
