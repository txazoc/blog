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

* 自定义`_id`: `PUT /{index}/{type}/{id}`
* 自动生成`_id`: `POST /{index}/{type}`，自动生成的`_id`为`20位`的GUID字符串

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

##### 分页

`from`默认为0，`size`默认为10

```js
GET /app/_search
{
  "from": 1,
  "size": 2
}
```

> `注`: 避免深度分页

##### match_all查询

> 匹配所有文档的查询

```js
GET /test/test
{
    "match_all": {}
}
```

##### match查询

* 全文字段: 分词 -&gt; 查询
* 精确值字段: 精确匹配，可以使用`filter查询`取代

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

##### range查询

> 适用于数值型字段的范围查询

**range查询操作符:**

* gt: 大于
* gte: 大于等于
* lt: 小于
* lte: 小于等于

```js
{
    "query": {
        "filter": {
            "range": {
                "age": {
                    "gte": 20,
                    "lt": 30
                }
            }
        }
    }
}
```

##### term查询

> 精确值匹配

```js
{
    "term": {
        "name": "admin"
    }
}
```

##### terms查询

> 多值精确匹配

```js
{
    "terms": {
        "name": [ "root", "admin" ]
    }
}
```

##### exists查询/missing查询

* exists查询: is not null
* missing查询: is null

##### bool查询

> 组合查询

* must: 符合查询条件，计算_score
* filter: 符合查询条件，不计算_score，`filter查询`
* must_not: 不符合查询条件
* should: 至少符合一个查询条件

##### filter查询和query查询

* filter查询: 不计算_score，结果被缓存
* query查询: 计算_score，结果不被缓存

> 全文搜索和相关性得分搜索使用`query查询`，其它情况使用`filter查询`

#### 排序

##### 相关性排序

> 默认情况下，返回的文档按照相关性得分_score进行排序

##### 字段排序

> 自定义字段排序

```js
{
    "query": {
        // ...
    },
    "sort": {
        "date": {
            "order": "desc"
        }
    }
}
```

##### 多级排序

```js
{
    "sort": {
        "date": { "order": "desc" },
        "time": { "order": "desc" }
    }
}
```

##### 数组字段的排序

#### 相关性

##### 相似度算法

#### Doc Values

> ElasticSearch中，Doc Values是一种`列式存储`结构

#### 分布式搜索

```js
{
    "from": 90,
    "size": 10
}
```

##### query-查询阶段

* 协调节点: 创建一个大小为`from + size`的优先队列
* 协调节点: 广播查询请求到所有分片(主分片或副本分片)
* 分片节点: 每个分片处理请求，返回`from + size`的排序队列，结果集仅包含文档ID和排序值
* 协调节点: 将所有分片返回的结果合并到`from + size`的优先队列，选取`[from, from + size)`的文档ID列表

##### fetch-取数据阶段

* 协调节点: `[from, from + size)`的文档ID列表分片路由后进行分组发送请求
* 分片节点: 根据文档ID加载文档的_source字段返回
* 协调节点: 组装分组分片返回的结果，返回给客户端

#### scroll查询

```js
GET /test/test/_search?scroll=10m
{
    "query": {
        "match_all": {}
    },
    "sort": "_doc",
    "size": 100
}
```

```js
GET /_search/scroll
{
    "scroll": "1m",
    "scroll_id": "DnF1ZXJ5VGhlbkZldGNoBQAAAAAAAAl9FkhyRjV5RVMwUjlHbjZmeVZJS1pmaUEAAAAAAAAJfhZIckY1eUVTMFI5R242ZnlWSUtaZmlBAAAAAAAACXwWSHJGNXlFUzBSOUduNmZ5VklLWmZpQQAAAAAAAAl_FkhyRjV5RVMwUjlHbjZmeVZJS1pmaUEAAAAAAAAJgBZIckY1eUVTMFI5R242ZnlWSUtaZmlB"
}
```

#### 索引

##### 索引配置

* number_of_shards: 索引配置
* number_of_replicas: 备份配置

```js
PUT /app
{
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2
    }
}
```

##### 自定义分析器

```js
PUT /app
{
    "settings": {
        "analysis": {
            "char_filter": {
                "my_mapping": {
                    "type": "mapping",
                    "mappings": [ "dog => cat" ]
                }
            },
            "tokenizer": {
                "my_tokenizer": {
                    "type": "standard",
                    "max_token_length": 10
                }
            },
            "filter": {
                "my_stop": {
                    "type": "stop",
                    "stopwords": [ "this", "is", "a" ]
                }
            },
            "analyzer": {
                "my_analyzer": {
                    "type": "custom",
                    "char_filter": [ "html_strip", "my_mapping" ],
                    "tokenizer": "my_tokenizer",
                    "filter": [ "lowercase", "my_stop" ]
                }
            }
        }
    }
}
```

**使用自定义分析器进行分词:**

```js
GET /app/_analyze
{
    "analyzer": "my_analyzer",
    "text": "<p>This is a dog</p>"
}
```

```js
{
    "tokens": [
        {
            "token": "cat",
            "start_offset": 13,
            "end_offset": 16,
            "type": "<ALPHANUM>",
            "position": 3
        }
    ]
}
```

**应用自定义分词器:**

```js
PUT /app/_mappings/app
{
    "properties": {
        "description": {
            "type": "text",
            "analyzer": "my_analyzer"
        }
    }
}
```

#### _source字段

> source字段代表文档的JSON字符串

**禁用_source字段:**

```js
PUT /app
{
    "mappings": {
        "app": {
            "_source": {
                "enabled": false
            }
        }
    }
}
```

**获取指定字段:**

```js
GET /app/_search
{
    "query": {
        "match_all": {}
    },
    "_source": [ "name", "type", "price" ]
}
```

#### 分片内部原理

##### 索引不变性

> 倒排索引被写入磁盘后是`不可改变`的，永远不会被修改

##### 索引更新

* 一个`ElasticSearch索引`包含多个`分片`
* 一个`分片`就是一个`Lucene索引`
* 一个`Lucene索引`包含一个`提交点(Commit Point)`多个`段(Segment)`
* 一个`提交点`记录所有已提交的段，包含一个`.del文件`
* 一个`段`包含多个字段的`倒排索引`，可以被搜索
* `.del文件`记录被删除文档的段信息

##### refresh

> 写入和打开一个新段的过程叫做`refresh`，默认情况下每个分片每秒自动`refresh`一次，`refresh`后文档就变为可见，所以Elasticsearch是`近实时搜索`

**refresh流程:**

* `in-memory buffer`中的文档写入一个新的`Segment(os buffer)`
* 新的`Segment(os buffer)`被打开，可以被搜索
* 清空`in-memory buffer`

通过`refresh_interval`来控制`refresh`的频率

**关闭`refresh`:**

```js
PUT /app/_settings
{
    "refresh_interval": "-1"
}
```

**每10s`refresh`一次:**

```js
PUT /app/_settings
{
    "refresh_interval": "10s"
}
```

##### flush
