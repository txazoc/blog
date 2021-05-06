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
> show [full] processlist;
+----+------+-----------------+------+---------+------+----------+------------------+
| Id | User | Host            | db   | Command | Time | State    | Info             |
+----+------+-----------------+------+---------+------+----------+------------------+
|  6 | root | localhost:62714 | NULL | Query   |    0 | starting | show processlist |
+----+------+-----------------+------+---------+------+----------+------------------+
```

* Id: 线程id，可以通过`kill ${id}`来杀死该线程
* User: 用户名
* Host: 客户端ip和端口号
* db: 数据库
* Command: 命令
* Time: 线程处于当前状态的时间
* State: 线程的状态
* Info: sql语句

**Command:**

* Binlog Dump: 主从同步
* Query: 查询
* Sleep: 空闲

筛选出正在执行的线程，按time倒排序:

```sql
> select * from information_schema.processlist
  where command != 'Sleep' order by time desc;
```

连接按客户端ip分组:

```sql
> select client_ip, count(client_ip) as client_num
  from (select substring_index(host, ':', 1) as client_ip from information_schema.processlist) as connect_info
  group by client_ip order by client_num desc;
```

##### 查看连接数

**查看最大连接数**

```sql
> show variables like 'max_connections';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 1024  |
+-----------------+-------+
```

**查看当前连接数**

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

* Threads_connected: 当前打开的连接数，和`show full processlist`返回的连接数一致
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

#### 数据目录

查看MySQL的数据目录位置:

```sql
> show variables like 'datadir';
+---------------+--------------------------------------------------+
| Variable_name | Value                                            |
+---------------+--------------------------------------------------+
| datadir       | C:\Program Files\MySQL\mysql-5.7.26-winx64\data\ |
+---------------+--------------------------------------------------+
```

```sql
> create database test charset=utf8 collate=utf8_bin;
```

创建好数据库后，MySQL会在`datadir`目录下创建和数据库同名的子目录，同时在该子目录下创建名为`db.opt`的文件，存储该数据库的各种属性

`db.opt`

```console
default-character-set=utf8
default-collation=utf8_bin
```

数据库目录下的文件:

```console
table_innodb.frm        // Innodb表结构元数据
table_innodb.ibd        // Innodb数据和索引文件
table_myisam.frm        // MyISAM表结构元数据
table_myisam.MYD        // MyISAM数据文件
table_myisam.MYI        // MyISAM索引文件
```

#### 表空间

> 表空间被划分为许多连续的区，每个区(1M)默认由64个页(16k)组成，每256个区划分为一组(256M)，每个组的最开始的几个页面类型是固定的

为方便范围查询，InnoDB作了如下设计:

* 一个区就是在物理位置上连续的64个页，在表中数据量大的时候，为某个索引分配空间的时候就不再按照页为单位分配了，而是按照区为单位分配
* 叶子节点和非叶子节点都有自己独立的区

#### 执行计划explain

```sql
> explain select * from app_bac_activity where id = 12;
+----+-------------+------------------+------------+-------+---------------+---------+---------+-------+------+----------+-------+
| id | select_type | table            | partitions | type  | possible_keys | key     | key_len | ref   | rows | filtered | Extra |
+----+-------------+------------------+------------+-------+---------------+---------+---------+-------+------+----------+-------+
|  1 | SIMPLE      | app_bac_activity | NULL       | const | PRIMARY       | PRIMARY | 4       | const |    1 |   100.00 | NULL  |
+----+-------------+------------------+------------+-------+---------------+---------+---------+-------+------+----------+-------+
```

##### explain

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

##### const

> 通过主键`primary_key`或唯一键`unique_key`来定位一条记录，如果是联合索引，需要每个列都是等值查询

* 主键: 聚簇索引 -&gt; 完整的用户记录
* 唯一键: 二级索引 -&gt; 唯一主键id -&gt; 聚簇索引 -&gt; 完整的用户记录

<p style="text-align: center;"><img src="_media/db/const.png" alt="const" style="width: 80%"></p>

##### ref

> 非唯一二级索引与常数的等值查询

* 非唯一二级索引: 二级索引 -&gt; 多个主键id -&gt; 聚簇索引 -&gt; 完整的用户记录

<p style="text-align: center;"><img src="_media/db/ref.png" alt="const" style="width: 80%"></p>

##### ref_or_null

> 在`ref`的基础上对NULL值做额外查询

<p style="text-align: center;"><img src="_media/db/ref_or_null.png" alt="const" style="width: 80%"></p>

##### index_merge

> 多个索引查询结果合并，操作符`OR`、`AND`

##### range

> 索引的范围查询，操作符`>`、`>=`、`<`、`<=`、`IN()`、`BETWEEN()`

##### index

> 全表扫描索引树

##### ALL

> 全表扫描，`最坏的情况`

总结下，查询分为四大类:

* 针对主键或唯一二级索引的等值查询
* 针对普通二级索引的等值查询
* 针对索引列的范围查询
* 直接扫描整个索引

#### 分页

##### 避免大的offset

查询时，数据库不知道`offset`的位置在哪，只能从头开始遍历计数，直到`offset`的位置，`offset`太大时，会导致跨越多个分页和无效的遍历


[<< 上一篇: 读写分离](9-数据库/读写分离.md)

[>> 下一篇: Spring-Cloud-Hystrix](10-分布式/Spring-Cloud-Hystrix.md)
