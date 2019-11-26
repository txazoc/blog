### InnoDB

#### InnoDB行格式

InnoDB有四种行格式:

* Compact
* Redundant
* Dynamic
* Compressed

##### Compact行格式

<p style="text-align: center;"><img src="_media/db/innodb_compact.png" alt="Compact行格式" style="width: 80%"></p>

```sql
> create table record_compact(
    id int(11) not null auto_increment primary key,
    c1 char(10),
    c2 varchar(10),
    c3 varchar(10) not null,
    c4 varchar(10)
) ENGINE=InnoDB CHARSET=ascii ROW_FORMAT=COMPACT;
> insert into record_compact(c1, c2, c3, c4) values
    ('a', 'bb', 'ccc', 'ddd'),
    (null, 'e', 'ff', null);
> select * from record_compact;
+----+------+------+-----+------+
| id | c1   | c2   | c3  | c4   |
+----+------+------+-----+------+
|  1 | a    | bb   | ccc | ddd  |
|  2 | NULL | e    | ff  | NULL |
+----+------+------+-----+------+
```

* 变长字段长度列表

> 存放变长字段的长度，变长字段包括varchar、text、blob，逆序存放，只存放`非NULL`的列的长度

```console
04 03 02    // id=1(c4、c3、c2)
02 01       // id=2(c3、c2)
```

> `注:`
>
> char列的字符集为变长字符集时，对应char列的长度也会被加到变长字段长度列表中

* NULL值列表

> 存放允许为NULL的列的NULL标识，每个允许为NULL的列对应一个二进制位，二进制位为1代表该列为NULL，二进制位逆序排列

record_compact表有三个允许为NULL的列，c1、c2、c4

```console
00          // id=1(0000 0000)
05          // id=2(0000 0101)
```

* 记录头信息

5字节

* 列数据

> 列数据包括隐藏列和表中定义的列

**隐藏列:**

* DB_ROW_ID: 行id，主键id
* DB_TRX_ID: 事务id
* DB_ROLL_PTR: 回滚指针

**表中定义的列:**

```console
// id=1
61 20 20 20 20 20 20 20 20 20   // char长度不够用空格填充
62 62
63 63 63
64 64 64 64

// id=2
65
66 66
```

**VARCHAR(M)最多能存储的数据**

```sql
> create table varchar_size_test_1(
    c varchar(65533) not null
) engine=InnoDB charset=ascii row_format=compact;
ERROR 1118 (42000): Row size too large. The maximum row size for the used table type, not counting BLOBs, is 65535.
This includes storage overhead, check the manual. You have to change some columns to TEXT or BLOBs
```

> `注:`
>
> 一个行中所有列(不包括隐藏列和记录头信息)占用的字节数的和不能超过65535个字节，包括`变长字段长度列表`、`NULL值列表`和`真实数据`占用的字节数

```sql
# 变长字段长度列表2字节 + NULL值列表1字节 + 真实数据65532字节 = 65535
> create table varchar_size_test_2(
    c varchar(65532)
) engine=InnoDB charset=ascii row_format=compact;

# 变长字段长度列表2字节 + 真实数据65533字节 = 65535
> create table varchar_size_test_3(
    c varchar(65533) not null
) engine=InnoDB charset=ascii row_format=compact;

# 变长字段长度列表2字节 + 真实数据65532字节(21844 * 2) = 65534
> create table varchar_size_test_4(
      c varchar(21844) not null
  ) engine=InnoDB charset=utf8 row_format=compact;
```

**行溢出**

> MySQL中规定一个页中至少存放两行记录，如果某一列中的数据非常多，在本记录的真实数据处只会存储该列的前768个字节的数据和一个指向其他页的地址

##### Dynamic行格式和Compressed行格式

> Dynamic行格式是MySQL默认的行格式，同Compact行格式，在处理行溢出数据时，把所有的字节都存储到其他页中，只在记录的真实数据处存储其他页的地址
>
> Compressed行格式同Dynamic行格式，不过会采用压缩算法对页进行压缩

#### InnoDB数据页

InnoDB中页的大小为`16k`

**数据页组成:**

* File Header: 文件头
* Page Header: 页头
* Infimum + Supremum: 最小记录和最大记录
* User Records: 用户记录
* Free Space: 空闲空间
* Page Directory: 页目录
* File Trailer: 文件尾

##### 用户记录(User Records)

* 最小记录: Infimum记录
* 最大记录: Supremum记录
* 真实数据记录: 记录之间通过`next_record`按照主键从小到大组成一个单向链表

<p style="text-align: center;"><img src="_media/db/user_record.png" alt="用户记录" style="width: 80%"></p>

* insert
* 删除记录: 记录的`delete_mask`设为1，上一条记录的`next_record`指向下一条记录

##### 页目录(Page Directory)

* 槽(Slot)，分组
    * `n_owned`: 分组内的记录数
* 主键查找
    * 二分法查找定位槽
    * 通过`next_record`遍历槽对应分组中的记录

> `注`: InnoDB规定，对于最小记录所在的分组只能有`1`条记录，最大记录所在的分组拥有的记录条数只能在`1~8`条之间，剩下的分组中记录的条数范围只能在是`4~8`条之间

<p style="text-align: center;"><img src="_media/db/page_directory.png" alt="页目录" style="width: 80%"></p>

##### 文件头部(File Header)

页之间通过上一页`FIL_PAGE_PREV`和下一页`FIL_PAGE_NEXT`组成一个双向链表

<p style="text-align: center;"><img src="_media/db/file_header.png" alt="文件头部" style="width: 80%"></p>

<p style="text-align: center;"><img src="_media/db/file_header_2.png" alt="文件头部" style="width: 80%"></p>

#### 索引

<p style="text-align: center;"><img src="_media/db/user_record_2.png" alt="用户记录" style="width: 80%"></p>

<p style="text-align: center;"><img src="_media/db/user_record_3.png" alt="用户记录" style="width: 80%"></p>

##### 目录项记录

> 目录项记录只存储主键值和对应的页号

**B+树:**

* 根节点
* 非叶子节点
* 叶子节点

<p style="text-align: center;"><img src="_media/db/index_record.png" alt="目录项记录" style="width: 80%"></p>

> 一般情况下，我们用到的B+树都不会超过4层

##### 聚簇索引

##### 二级索引

> 二级索引的目录项记录存储的是`二级索引列 + 主键 + 页号`的值
>
> 二级索引的叶子节点存储的是`二级索引列 + 主键`的值

> `注:` MyISAM的索引全部是二级索引，包括主键索引

**二级索引查找:**

* 二级索引查找主键值
* 主键索引查找完整的用户记录(回表)

##### 联合索引

> 以多个列的大小作为排序规则建立索引
>
> 联合索引的目录项记录存储的是`多个列 + 主键 + 页号`的值
>
> 联合索引的叶子节点存储的是`多个列 + 主键`的值

##### 前缀索引

> 使用列的前缀代替整个列作为前缀

```sql
alter table table_name add index `name` (name(8));
```

##### 索引查找

* **全列匹配:** where子句中的列和索引列一致，例如，联合索引(index_field_1, index_field_2, index_field_3)

```sql
select * from table_name where index_field_1 = 'value1' and index_field_2 = 'value2' and index_field_3 = 'value3'
```

* **最左匹配:** where子句中的列只包含联合索引左边的列，例如，联合索引(index_field_1, index_field_2, index_field_3)

```sql
select * from table_name where index_field_1 = 'value1' and index_field_2 = 'value2'
```

* **列前缀匹配:** 字符串前缀模糊匹配

```sql
select * from table_name where name like 'as%';
```

* **范围匹配:** 索引列的值在某个范围内

```sql
select * from table_name where id > 1000 and id < 10000;
```

> `注:` 对联合索引中的多个列进行范围查找时，只有联合索引最左边范围查找的列可以用到索引

```sql
select * from table_name where index_field_1 = 'range1' > and index_field_1 < 'range2';
select * from table_name where index_field_1 = 'value1' and index_field_2 = 'range1' > and index_field_2 < 'range2';
```

##### 索引排序

> 利用索引列的有序性进行排序，避免内存或磁盘上的文件排序`filesort`

```sql
select * from table_name order by index_field_1 limit 10;
select * from table_name order by index_field_1, index_field_2 limit 10;
select * from table_name where index_field_1 = 'value1' order by index_field_2, index_field_3 limit 10;
```

不能使用索引进行排序的情况:

* `ASC`、`DESC`混用时

```sql
select * from table_name order by index_field_1 asc, index_field_2 desc limit 10;
```

* where子句中出现非排序使用到的索引列

```sql
select * from table_name where field_other = 'value' order by index_field_1 limit 10;
```

* 排序列包含非同一个索引的列

```sql
select * from table_name order by index_field_1, field_other limit 10;
```

* 排序列使用了复杂的表达式

```sql
select * from table_name order by upper(index_field_1) limit 10;
```

##### 索引分组

> 同`索引排序`，索引也可以用来分组

```sql
select index_field_1, index_field_2, count(1) from table_name group by index_field_1, index_field_2;
```

##### 回表

> 二级索引列中不包含完整的查询列，需要用二级索引中的主键id到聚簇索引中查找完整的用户记录(`回表`)

* 二级索引: `顺序IO`
* 回表: 离散主键id -&gt; `随机IO` -&gt; 主键索引

> `注:` `离散主键id`越多，需要回表的记录就越多，使用二级索引的性能就越低

##### 覆盖索引

> 索引列中包含全部的查询列，不需要回表操作

```sql
select index_field_1, index_field_2 where index_field_1 = 'value';
```

##### 主键插入顺序

* 自增主键或递增主键
    * 数据页未满，`User Records连续插入
    * 数据页已满，申请新的数据页继续插入
    : 插入时一个数据页一个数据页的插入，单数据页内连续插入
* 离散主键(`包括所有的非聚集索引`)
    * 索引所在的数据页分散，查找索引所在的数据页
    * 索引页未满，记录移位
    * 索引页已满，页面分裂

##### 索引注意事项

* 只为用于搜索、排序或分组的列创建索引: where、join、order by、group by子句中出现的列
* 考虑列的基数: 建立索引列的基数必须足够大，否则会导致大量的回表操作
* 索引列的类型尽量小: 可以加快索引的比较操作，同时索引占用的存储空间越少，一个数据页中就可以存放更多的索引项记录，可以更好的利用数据页缓存和减少磁盘I/O
* 索引字符串值的前缀: 只对字符串的前几个字符进行索引，但此时不支持索引排序
* 索引列在比较表达式中不是以单独列的形式出现，而是以表达式、函数调用的形式出现的话，是用不到索引的
* 不要创建冗余和重复索引
* 不要创建太多的索引，索引会占用一定的存储空间，同时会导致插入和更新变慢

##### 适合建索引的情况

* 全值匹配
* 最左匹配
* 范围匹配
* 精确匹配某一列并范围匹配另外一列
* 用于排序
* 用于分组

#### ACID

> ACID是数据库事务的四个特性

#### 事务隔离级别

* A: 原子性，Atomicity，一个事务中的所有操作，要么全部执行，要么全部不执行，不会停留在某个中间状态，允许回滚
    * commit: redo log
    * rollback: undo log
* C: 一致性，Consistency，事务从一个一致性状态切换到另一个一致性状态，事务的中间状态不会被其它事务看到
    * 锁、MVCC、doublewrite buffer
* I: 隔离性，Isolation，事务之间互相影响的程度，适当的破坏`一致性`来提升并发度
    * 锁、MVCC
* D: 持久性，Durability，事务提交后，数据会被持久化到数据库，不会丢失
    * redo log、doublewrite buffer
    * `innodb_flush_log_at_trx_commit`
    * `sync_binlog`

事务并发会带来不一致的问题:

* 脏读
* 不可重复读
* 幻读

为此，定义四种事务隔离级别:

* `Read Uncommitted`: 读未提交，可能读到脏数据
* `Read Committed`: 读已提交
    * MVCC: 解决`脏读`
* `Repeatable Read`: 可重复读，InnoDB默认隔离级别
    * MVCC: 解决`脏读`、`不可重复读`
    * Gap锁/Next-Key锁: 解决部分`幻读`
* `Serializable`: 串行化
    * `select`加共享锁: 解决所有并发问题

#### InnoDB事务实现

* redo log: 重做日志，顺序记录数据变更的操作
* undo log: 撤销日志，记录数据变更的反向操作
* MVCC

```console
mysql> select * from Account;
+----+--------+--------+
| id | userId | amount |
+----+--------+--------+
|  1 |   1000 |  100   |
|  2 |   2000 |  200   |
+----+--------+--------+
```

```sql
start transaction;
update Account set amount += 50 where userId = 1000;
update Account set amount -= 50 where userId = 2000;
commit;
```

```console
1. 开始事务

2. 记录undo log: update Account set amount -= 50 where userId = 1000
3. 修改buffer pool: update Account set amount += 50 where userId = 1000
4. 记录redo log: update Account set amount += 50 where userId = 1000

5. 记录undo log: update Account set amount += 50 where userId = 2000
6. 修改buffer pool: update Account set amount -= 50 where userId = 2000
7. 记录redo log: update Account set amount -= 50 where userId = 2000

8. redo log写入磁盘
9. 提交事务
```

#### redo log重做日志

##### redo日志格式

##### redo日志缓冲区

> redo log buffer

`ib_logfile0`、`ib_logfile1`

redo日志刷盘时机:

* redo log buffer空间不足时
* 事务提交时
* 后台线程刷，1s刷一次

`innodb_flush_log_at_trx_commit`

#### 二级索引下主键是否有序

> 相同的二级索引下，叶子节点的记录项是否按主键排序

创建表:

```sql
create table test(
    id int(11) not null auto_increment primary key,
    name varchar(3) not null,
	index `name` (`name`)
) ENGINE=InnoDB CHARSET=utf8;
```

插入10000条测试数据:

```sql
insert into test(name) values('cac');
insert into test(name) values('ccb');
insert into test(name) values('cca');
insert into test(name) values('cac');
insert into test(name) values('bac');
insert into test(name) values('bac');
insert into test(name) values('bcc');
insert into test(name) values('bcc');
insert into test(name) values('ccb');
insert into test(name) values('bba');
...
```

二级索引下主键排序的sql:

```sql
> explain select * from test where name = 'aaa' order by id limit 100,10;
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+--------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref   | rows | filtered | Extra                    |
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+--------------------------+
|  1 | SIMPLE      | test  | NULL       | ref  | name          | name | 11      | const |  411 |   100.00 | Using where; Using index |
+----+-------------+-------+------------+------+---------------+------+---------+-------+------+----------+--------------------------+
```

通过explain可以看出，并没有`Using filesort`，因此可以得出结论，`相同的二级索引下，叶子节点的记录项是按主键排序的`


[<< 上一篇: TCP](8-网络通信/TCP.md)

[>> 下一篇: MySQL](9-数据库/MySQL.md)
