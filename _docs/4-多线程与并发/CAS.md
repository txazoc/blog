## CAS

> Compare and Swap，比较并交换，属于硬件同步原语，提供基本内存操作的原子性保证

### CAS语法

```java
/**
 * expected 期望的旧值
 * new      新值
 */
boolean CAS(expected, new)
```

比较旧值和期望的旧值，若相等，则将旧值交换为新值，返回true，否则操作失败不交换，返回false

### CAS实现

#### Unsafe

* Unsafe.compareAndSwapInt(): 比较并交换`int变量`
* Unsafe.compareAndSwapLong(): 比较并交换`long变量`
* Unsafe.compareAndSwapObject(): 比较并交换`对象引用`

#### incr

```java
private volatile int value = 0;

private int incr() {
    int expected;
    int newValue;
    do {
        expected = value;
        // expected = unsafe.getIntVolatile(this, valueOffset);
        newValue = expected + 1;
        // CAS自旋
    } while (!unsafe.compareAndSwapInt(this, valueOffset, expected, newValue));
    return newValue;
}
```

### lock前缀

> CAS底层通过lock前缀来实现

lock前缀的语义:

* 内存的读-改-写操作原子执行
    * 总线锁定
    * 缓存锁定: 缓存一致性协议
* 禁止指令重排序
* 写缓冲区中的数据刷新到内存

### CAS存在的问题

* ABA问题
* 长时间自旋CAS会导致大的CPU开销
* 只能保证一个共享变量的原子操作，不能用于多个变量的原子操作

### 原子类

`java.util.concurrent.atomic`包下提供一系列的原子操作类

* AtomicBoolean: 原子操作布尔类型
* AtomicInteger: 原子操作int类型
* AtomicLong: 原子操作long类型

#### LongAdder
