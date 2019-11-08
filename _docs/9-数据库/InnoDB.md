### InnoDB

#### InnoDB行格式

InnoDB有四种行格式:

* Compact
* Redundant
* Dynamic
* Compressed

##### Compact行格式

![Compact行格式](../_media/db/innodb_compact.png)(80%)

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
