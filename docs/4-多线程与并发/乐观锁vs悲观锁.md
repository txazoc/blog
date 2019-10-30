## 乐观锁vs悲观锁

### 乐观锁

>  总是假设最好的情况，每次去拿数据的时候都认为别人不会修改，不会上锁

适用于`读多写少`的场景

#### CAS

> Compare and Swap

#### 版本号机制

```sql
update table set ..., version = version + 1 where version = ?
```

### 悲观锁

> 总是假设最坏的情况，每次去拿数据的时候都认为别人会修改，都会上锁，其它线程会阻塞

适用于`写多`的场景

#### 共享锁

`select ... lock in share mode`

#### 排它锁

* `select ... for update`
* insert、update、delete

#### synchronized & ReentrantLock


[<< 上一篇: volatile](4-多线程与并发/volatile.md)

[>> 下一篇: 同步队列&等待队列](4-多线程与并发/同步队列&等待队列.md)
