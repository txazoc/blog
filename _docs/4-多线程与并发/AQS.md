## AQS

AQS核心组件:

* state
* CLH同步队列
* acquire()、release()、acquireshared()、releaseshared()
* LockSupport.park()、LockSupport.unpark()

### AbstractQueuedSynchronizer

> 提供一个框架用来实现锁和相关的同步器，依赖于FIFO等待队列

```java
public abstract class AbstractQueuedSynchronizer {

    // 独占模式下拥有独占锁的线程
    private transient Thread exclusiveOwnerThread;
    // 同步队列头部
    private transient volatile Node head;
    // 同步队列尾部
    private transient volatile Node tail;
    // 同步状态
    private volatile int state;

}
```

#### CLH同步队列

```text
     +------+  prev +-----+  prev +-----+
head |      | <---- |     | <---- |     |  tail
     +------+       +-----+       +-----+
```

CLH同步队列的节点结构:

```java
static final class Node {

    // 等待状态
    volatile int waitStatus;
    // 前驱节点
    volatile Node prev;
    // 后继节点
    volatile Node next;
    // 节点关联的线程
    volatile Thread thread;
    Node nextWaiter;

}
```

* `CANCELLED`(1): 线程已被取消(超时或中断)
* `SIGNAL`(-1): 后继节点要被unpark唤醒
* `CONDITION`(-2): 线程在condition队列上等待
* `PROPAGATE`(-3): releaseShared无条件地传播下去

#### acquire()

```java
public final void acquire(int arg) {
    if (!tryAcquire(arg) &&
            acquireQueued(addWaiter(AbstractQueuedSynchronizer.Node.EXCLUSIVE), arg))
        selfInterrupt();
}
```

* tryAcquire(): 尝试获取资源
* addWaiter(): 资源获取失败，创建独占节点添加到同步队列尾部
* acquireQueued()

#### release()

#### acquireShared()

#### releaseShared()

### ReentrantLock

ReentrantLock有公平锁和非公平锁两种实现，默认为非公平锁

#### 公平锁

> 严格按照FIFO的顺序获取锁，不允许抢占

```java
protected final boolean tryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    if (c == 0) {
        // 公平锁实现逻辑，在同步队列中是否有比当前线程更早的节点
        if (!hasQueuedPredecessors() &&
                compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    } else if (current == getExclusiveOwnerThread()) {
        // 重入锁实现逻辑
        int nextc = c + acquires;
        setState(nextc);
        return true;
    }
    return false;
}
```

#### 非公平锁

> 允许抢占，抢占失败后进入同步队列

```java
final void lock() {
    // 非公平锁第一次抢占
    if (compareAndSetState(0, 1))
        setExclusiveOwnerThread(Thread.currentThread());
    else
        acquire(1);
}

protected final boolean tryAcquire(int acquires) {
    return nonfairTryAcquire(acquires);
}

final boolean nonfairTryAcquire(int acquires) {
    final Thread current = Thread.currentThread();
    int c = getState();
    if (c == 0) {
        // 非公平锁第二次抢占
        if (compareAndSetState(0, acquires)) {
            setExclusiveOwnerThread(current);
            return true;
        }
    } else if (current == getExclusiveOwnerThread()) {
        // 重入锁实现逻辑
        int nextc = c + acquires;
        setState(nextc);
        return true;
    }
    return false;
}
```

#### unlock()

```java
protected final boolean tryRelease(int releases) {
    int c = getState() - releases;
    if (Thread.currentThread() != getExclusiveOwnerThread())
        throw new IllegalMonitorStateException();
    boolean free = false;
    if (c == 0) {
        // state为0时，解锁，返回true，唤醒后继节点
        free = true;
        setExclusiveOwnerThread(null);
    }
    setState(c);
    return free;
}
```

### Semaphore

#### acquire()

```java
// state -= n
final int nonfairTryAcquireShared(int acquires) {
    for (; ; ) {
        int available = getState();
        int remaining = available - acquires;
        if (remaining < 0 ||
                compareAndSetState(available, remaining))
            return remaining;
    }
}
```

* remaining >= 0，CAS成功，许可获取成功
* remaining >= 0，CAS失败，continue
* remaining < 0，许可不足，进入同步队列

#### release()

```java
// state += n
protected final boolean tryReleaseShared(int releases) {
    for (; ; ) {
        int current = getState();
        int next = current + releases;
        if (compareAndSetState(current, next))
            return true;
    }
}
```

### CountDownLatch

#### countDown()

* releaseShared(1)，释放资源1，state--

```java
protected boolean tryReleaseShared(int releases) {
    for (; ; ) {
        int c = getState();
        if (c == 0)
            return false;
        int nextc = c - 1;
        if (compareAndSetState(c, nextc))
            return nextc == 0;
    }
}
```

#### await()

* acquireSharedInterruptibly(1)，获取资源1，state为0时获取成功，从等待状态唤醒

```java
protected int tryAcquireShared(int acquires) {
    return (getState() == 0) ? 1 : -1;
}
```

### CyclicBarrier

```java
public class CyclicBarrier {

    // 用来保护屏障入口的锁
    private final ReentrantLock lock = new ReentrantLock();
    // 条件等待
    private final Condition trip = lock.newCondition();
    // 屏障数量
    private final int parties;
    // 等待中的屏障数量
    private int count;
}
```

#### await()

* lock加锁
* count减1后
    * count不为0，调用`trip.await()`进入等待，等待被唤醒
    * count为0，调用`trip.signalAll()`唤醒所有等待线程
* lock解锁

### Condition

* waitStatus = Node.CONDITION

```java
public class ConditionObject implements Condition {

    // Condition队列的头节点
    private transient Node firstWaiter;
    // Condition队列的尾节点
    private transient Node lastWaiter;

}
```

### ReentrantReadWriteLock
