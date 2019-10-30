## synchronized

### 锁的分类

* 自旋锁
* 悲观锁、乐观锁
* 共享锁、排它锁
* 可重入锁、不可重入锁
* 公平锁、非公平锁
* 类锁、对象锁

synchronized属于悲观锁、排它锁、可重入锁

### synchronized特性

* 同步
* 保证可见性

### synchronized使用

* synchronized同步实例方法
* synchronized同步静态方法
* synchronized同步代码块

> jdk1.6对synchronized进行了各种优化

`monitorenter`、`monitorexit`、`ACC_SYNCHRONIZED`

### synchronized优化

* 锁粗化
* 锁消除

### 偏向锁

CAS `Thread Id`，适用于只有一个线程访问同步块的场景

### 轻量级锁

CAS `Mark Word`，适用于线程交替执行同步块的场景，同步块执行速度非常快，不存在锁竞争

### 自旋锁

CAS自旋

### 重量级锁

参考: [Synchronized解析](https://juejin.im/post/5d5374076fb9a06ac76da894)


[<< 上一篇: Java内存模型](4-多线程与并发/Java内存模型.md)

[>> 下一篇: volatile](4-多线程与并发/volatile.md)
