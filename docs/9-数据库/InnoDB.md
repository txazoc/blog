## InnoDB

### ACID

> ACID是数据库事务的四个特性

### 事务隔离级别

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

### InnoDB事务实现

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

### redo log重做日志

#### redo日志格式

#### redo日志缓冲区

> redo log buffer

`ib_logfile0`、`ib_logfile1`

redo日志刷盘时机:

* redo log buffer空间不足时
* 事务提交时
* 后台线程刷，1s刷一次

`innodb_flush_log_at_trx_commit`


[上一篇 TCP](8-网络通信/TCP.md)

[下一篇 MySQL](9-数据库/MySQL.md)
