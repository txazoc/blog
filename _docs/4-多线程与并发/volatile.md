### volatile

> volatile用来保证可见性，不保证原子性

JMM中规定的happens-before规则:

> 对一个volatile变量的写操作，happens-before随后对这个volatile变量的读操作

要满足这些条件，所以volatile关键字就有这些功能:

* 禁止缓存，保证变量的可见性，在一个线程中修改了变量的值，在另一个线程中是立即可见的
* 禁止指令重排序

ACC_VOLATILE

* https://segmentfault.com/a/1190000016074254
* https://my.oschina.net/tantexian/blog/808032
