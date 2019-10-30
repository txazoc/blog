## MySQL锁

### 表锁

> Table Lock，锁定整个表

* 表共享读锁

```sql
lock table tableName read
```

* 表独占写锁

```sql
lock table tableName write
```

### 意向锁

> Intention Lock，表级锁，用来支持表锁和行锁的共存，表明接下来会申请什么类型的行锁

* 意向共享锁(IS锁): 事务准备给表中的行加共享锁
* 意向排他锁(IX锁): 事务准备给表中的行加排他锁

意向锁的作用: `快速检测表锁和行锁之间的冲突`，实现表锁和行锁的共存

表锁和意向锁兼容矩阵:

|    | X | IX | S | IS |
| --- | --- | --- | --- | --- |
| X  | - | - | - | - |
| IX | - | + | - | + |
| S  | - | - | + | + |
| IS | - | + | + | + |

### 行锁(记录锁)

> Record Lock，锁定索引项

* 共享锁(S锁)

> Shared Lock

```sql
select ... lock in share mode
```

* 排他锁(X锁)

> Exclusive Lock

```sql
select ... for update
```

### 间隙锁

> Gap Lock，锁定索引项之间的间隙，`(-oo, m)`、`(m, n)`、`(n, +oo)`

间隙锁的作用:

* 防止幻读
* 防止间隙内有新数据插入
* 防止已存在的数据更新为间隙内的数据

### Next-Key锁

> Next-Key Lock，记录锁和间隙锁的结合，`(-oo, m]`、`(m, n]`、`(n, +oo)`，InnoDB默认的加锁方案

### 插入意向锁

> Insert Intention Lock，是一种特殊的间隙锁，插入前，如果该间隙已有其它Gap锁/Next-Key锁时，会申请插入意向锁

插入意向锁的作用:

* 防止幻读，阻塞等待Gap锁/Next-Key锁释放
* 提高并发插入性能，插入意向锁不互斥，同一区间插入多条不同数据，不会出现冲突等待

### sql语句读写分析

* `update/delete`: X锁
* `select ... lock in share mode`: S锁
* `select ... for update`: X锁
* `select ...`: 各种事务隔离级别下的处理方式不一样
    * READ UNCOMMITTED
        * `select`不加锁，可能读到脏数据
    * READ COMMITTED
        * 一致性非锁定读
    * REPEATABLE READ
        * 一致性非锁定读，加Gap锁/Next-Key锁
    * SERIALIZABLE
        * autocommit = on: 一致性非锁定读
        * autocommit = off: `select`转换为`select ... lock in share mode`

InnoDB的两种一致性读:

* 一致性非锁定读: MVCC
    * READ COMMITTED: 当前读，读最新的快照数据，每次读取都生成一个`ReadView`
    * REPEATABLE READ: 快照读，读事务开始时的快照数据，第一次读取时生成一个`ReadView`
* 一致性锁定读
    * `select ... lock in share mode`
    * `select ... for update`


[<< 上一篇: MySQL](9-数据库/MySQL.md)

[>> 下一篇: 分库分表](9-数据库/分库分表.md)
