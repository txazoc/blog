### MySQL

#### MySQL命令行

##### 系统变量

> 影响MySQL服务器程序运行行为的变量

```sql
> show variables [like '匹配模式'];
```

##### 状态变量

> 用来显示服务器程序运行状况的变量

```sql
> show status [like '匹配模式'];
```

#### MySQL连接

##### 查看当前连接

```sql
> show processlist;
+----+------+-----------------+------+---------+------+----------+------------------+
| Id | User | Host            | db   | Command | Time | State    | Info             |
+----+------+-----------------+------+---------+------+----------+------------------+
|  6 | root | localhost:62714 | NULL | Query   |    0 | starting | show processlist |
+----+------+-----------------+------+---------+------+----------+------------------+
```

```sql
> show full processlist;
> select id, user, host, db, command, time, state, info
  from information_schema.processlist
  where command != 'Sleep' order by time desc;
```

**Command:** Sleep、Query、Binlog Dump

##### 查看最大连接数

```sql
> show variables like 'max_connections';
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

##### MySQL处理客户端请求

* 连接管理: 一个连接对应一个线程(限制客户端连接数量)
* 解析与优化
    * 查询缓存
    * 语法解析
    * 查询优化: 生成执行计划
* 存储引擎: 读写

#### MySQL字符集

##### 字符集

> 字符的编码规则

MySQL支持的字符集:

```sql
> show charset;
+----------+---------------------------------+---------------------+--------+
| Charset  | Description                     | Default collation   | Maxlen |
+----------+---------------------------------+---------------------+--------+
| ascii    | US ASCII                        | ascii_general_ci    |      1 |
| gb2312   | GB2312 Simplified Chinese       | gb2312_chinese_ci   |      2 |
| gbk      | GBK Simplified Chinese          | gbk_chinese_ci      |      2 |
| utf8     | UTF-8 Unicode                   | utf8_general_ci     |      3 |
| utf8mb4  | UTF-8 Unicode                   | utf8mb4_general_ci  |      4 |
| binary   | Binary pseudo charset           | binary              |      1 |
+----------+---------------------------------+---------------------+--------+
```

* Charset: 字符集名称
* Default 字符集默认比较规则
* Maxlen: 字符集的最大字节数

##### 比较规则

> 针对某种字符集中的字符比较大小的一种规则

查看字符集对应的比较规则:

```sql
> show collation like 'utf8\_%';
+--------------------------+---------+-----+---------+----------+---------+
| Collation                | Charset | Id  | Default | Compiled | Sortlen |
+--------------------------+---------+-----+---------+----------+---------+
| utf8_general_ci          | utf8    |  33 | Yes     | Yes      |       1 |
| utf8_bin                 | utf8    |  83 |         | Yes      |       1 |
+--------------------------+---------+-----+---------+----------+---------+
```

* utf8_general_ci: 不区分大小写
* utf8_general_cs: 区分大小写
* utf8_bin: 以二进制比较

##### 4个级别的字符集和比较规则

* 服务器级别

```sql
> show variables like '%_server';
+----------------------+--------------------+
| Variable_name        | Value              |
+----------------------+--------------------+
| character_set_server | utf8mb4            |
| collation_server     | utf8mb4_general_ci |
+----------------------+--------------------+
```

* 数据库级别

```sql
> create database test_utf8 charset=utf8 collate=utf8_bin;
> use test_utf8;
> show variables like '%_database';
+------------------------+----------+
| Variable_name          | Value    |
+------------------------+----------+
| character_set_database | utf8     |
| collation_database     | utf8_bin |
+------------------------+----------+
```

* 表级别

```sql
> create table test_utf8 (
  id int(11)
) charset=utf8 collate=utf8_bin;
```

* 列级别

```sql
> create table test_gbk (
  name varchar(10) character set gbk collate gbk_chinese_ci
) charset=utf8 collate=utf8_bin;
```

> `注:`
>
> 列未指定字符集和比较规则，则使用所在表的字符集和比较规则
>
> 表未指定字符集和比较规则，则使用所在库的字符集和比较规则
>
> 库未指定字符集和比较规则，则使用服务器的字符集和比较规则

##### 客户端和MySQL服务器通信中的字符集

```sql
> show variables like 'character_set\_%';
+--------------------------+---------+
| Variable_name            | Value   |
+--------------------------+---------+
| character_set_client     | gbk     |
| character_set_connection | gbk     |
| character_set_results    | gbk     |
+--------------------------+---------+
```

* character_set_client: 客户端请求的字符集
* character_set_connection: MySQL处理连接的字符集
* character_set_results: 返回数据给客户端的字符集

MySQL中字符集的转换过程:

* `character_set_client`解码  -&gt;  `character_set_connection`编码
* `character_set_connection`解码  -&gt;  `列字符集`编码
* `列字符集`解码  -&gt;  `character_set_results`编码

> 通常都把character_set_client、character_set_connection、character_set_results设置成和客户端使用的字符集一致，减少无谓的字符集转换

> jdbc中characterEncoding必须和character_set_client、character_set_results保持一致，否则会发生乱码

#### 存储引擎

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
