### MySQL

#### MySQL连接

##### 查看当前连接

```sql
> show processlist;
> show full processlist;
> select id, user, host, db, command, time, state, info from information_schema.processlist where command != 'Sleep' order by time desc;
```

**Command:** Sleep、Query、Binlog Dump

##### 查看最大连接数

```sql
> show variables like '%max_connections%';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 1024  |
+-----------------+-------+
```

```sql
> show status like 'Threads%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Threads_cached    | 76    |
| Threads_connected | 143   |
| Threads_created   | 219   |
| Threads_running   | 3     |
+-------------------+-------+
```

* Threads_connected: 当前打开的连接数
* Threads_running: 当前未挂起的连接数

#### 服务器处理客户端请求

* 连接管理: 一个连接对应一个线程(限制客户端连接数量)
* 解析与优化
    * 查询缓存
    * 语法解析
    * 查询优化: 生成执行计划
* 存储引擎: 读写

#### 执行计划explain

#### explain

* `id`：select查询的序列号
* `select_type`：select查询的类型
* `table`：表名
* `type`：类型
* `possible_keys`：可能用到的索引
* `key`：实际用到的索引
* `key_len`：实际用到的索引长度
* `ref`
* `rows`：扫描的行数
* `Extra`：额外信息

关心字段: `type`、`key`、`key_len`、`rows`、`Extra`

##### type

* `system`: 表仅有一行，`const`的特例
* `const`: 单表`primary_key`或`unique_key`查询，最多匹配一行，操作符`=`
* `eq_ref`: 多表`primary_key`或`unique_key`关联查询，最多匹配一行，操作符`=`，`最好的关联类型`
* `ref`: 单表索引查询或多表索引关联查询，操作符`=`
* `ref_null`: 在`ref`的基础上对NULL值做额外搜索
* `index_merge`: 多个索引查询合并，操作符`OR`、`AND`
* `range`: 单表索引范围查询，操作符`>`、`>=`、`<`、`<=`、`IN()`、`BETWEEN()`
* `index`: 全表扫描索引树
* `ALL`: 全表扫描，`最坏的情况`


[<< 上一篇: InnoDB](9-数据库/InnoDB.md)

[>> 下一篇: MySQL锁](9-数据库/MySQL锁.md)
