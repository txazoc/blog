## concurrent并发包

### 1. 原子类

> 原子操作，支持boolean、int、long、对象引用、对象字段、数组

* CAS: 保证原子性
* volatile: 保证可见性

### 2. 集合

#### CopyOnWriteArrayList

```java
volatile Object[] array;
```

* 读: volatile读
* 写: lock()，arraycopy，volatile写
* [参见 CopyOnWriteArrayList](/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/List?id=copyonwritearraylist)

#### ConcurrentHashMap

* 原理: key -&gt; hash() -&gt; hashcode `& (table.length - 1)` -&gt; table[index] -&gt; 链表/红黑树查找(hash==并且key==或equals)
* get(): volatile读table[index] -&gt; volatile读value
* put(): volatile读table[index] -&gt; synchronized(table[index]) -&gt; volatile写table[index]、volatile写value
* [参见 ConcurrentHashMap](/%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84/Map?id=concurrenthashmap)

#### ConcurrentSkipListMap

### 3. 队列

#### ArrayBlockingQueue(阻塞队列)

> 数组 + ReentrantLock + Condition

```java
public void put(E e) throws InterruptedException {
    final ReentrantLock lock = this.lock;
    lock.lockInterruptibly();
    try {
        while (count == items.length)
            notFull.await();
        enqueue(e);
    } finally {
        lock.unlock();
    }
}

public E take() throws InterruptedException {
    final ReentrantLock lock = this.lock;
    lock.lockInterruptibly();
    try {
        while (count == 0)
            notEmpty.await();
        return dequeue();
    } finally {
        lock.unlock();
    }
}
```

#### LinkedBlockingQueue(阻塞队列)

> 单向链表 + ReentrantLock(两把锁put、take) + Condition

#### ConcurrentLinkedQueue(非阻塞队列)

#### DelayQueue(延迟队列)

#### PriorityBlockingQueue(优先级阻塞队列)

#### SynchronousQueue(同步队列)

### 4. 线程池

#### ThreadPoolExecutor

#### ScheduledThreadPoolExecutor


[<< 上一篇: CompletableFuture](4-多线程与并发/CompletableFuture.md)

[>> 下一篇: final](4-多线程与并发/final.md)
