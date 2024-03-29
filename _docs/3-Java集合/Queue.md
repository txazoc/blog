### Queue

#### 线程安全队列的实现方案

* 阻塞算法
    * 一个锁: 入队和出队共用一把锁
    * 两个锁: 入队一把锁，出队一把锁
* 非阻塞算法
    * 循环CAS

#### ArrayBlockingQueue

* 队列: 数组
* 线程安全: ReentrantLock
* 阻塞: Condition

阻塞队列原理:

* 加锁: lock()
* 检查是否阻塞: await()
    * put(): 队列满了
    * take(): 队列为空
* 入队或出队
* 唤醒: signal()
* 解锁: unlock()

#### LinkedBlockingQueue

* 队列: 单向链表
* 线程安全: ReentrantLock
* 阻塞: Condition

#### PriorityQueue

* 最小堆

#### PriorityBlockingQueue

* 优先级队列: 最小堆
* 线程安全: ReentrantLock
* 阻塞: Condition

#### DelayQueue

* PriorityQueue + ReentrantLock + Condition

#### ConcurrentLinkedQueue

* 并发非阻塞队列
* volatile + CAS

```java
public class ConcurrentLinkedQueue<E> {

    volatile Node<E> head;
    volatile Node<E> tail;

    private static class Node<E> {

        volatile E item;
        volatile Node<E> next;

    }

}
```
