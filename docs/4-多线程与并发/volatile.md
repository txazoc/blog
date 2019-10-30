## volatile

volatile用来解决可见性问题

JMM中规定的happens-before规则:

> 对一个volatile变量的写操作，happens-before随后对这个volatile变量的读操作

要满足这些条件，所以volatile关键字就有这些功能:

* 禁止缓存
* 禁止指令重排序

ACC_VOLATILE

[https://segmentfault.com/a/1190000016074254](https://segmentfault.com/a/1190000016074254)


[<< 上一篇: synchronized](4-多线程与并发/synchronized.md)

[>> 下一篇: 乐观锁vs悲观锁](4-多线程与并发/乐观锁vs悲观锁.md)
