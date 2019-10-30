### List

#### ArrayList

```java
public class ArrayList {

    // 大小
    private int size;
    // 修改次数
    protected transient int modCount = 0;
    // 元素数组
    transient Object[] elementData;

}
```

* 数组实现
* 实现`RandomAccess`接口，支持基于下标的快速随机访问
* 遍历，for循环遍历时可利用CPU缓存行
* 下标插入或删除时会导致arraycopy
* 扩容，add时容量不够会导致扩容，每次扩容1/2，初始化时可指定大小避免频繁扩容
* 由于elementData尾部部分空间是浪费的，ArrayList自定义了序列化和反序列化
* modCount，add或remove时，modCount++，iterator遍历时modCount改变会抛出ConcurrentModificationException，remove时会同步modCount

#### LinkedList

* 双向链表实现
* 头尾插入删除效率高，查询和下标插入删除效率低

#### Vector

* 类似ArrayList
* 线程安全，通过synchronized实现
* 每次扩容一倍

#### Stack

* `extends Vector`
* LIFO(后进先出)

#### CopyOnWriteArrayList

* ReentrantLock + volatile + arraycopy
* 适用于读多写少的场景
* 每次修改操作都会导致arraycopy, 大数组频繁修改容易引发GC问题

```java
public class CopyOnWriteArrayList<E> implements List<E>, RandomAccess {

    final transient ReentrantLock lock = new ReentrantLock();
    // 元素数组
    private transient volatile Object[] array;

    final Object[] getArray() {
        return array;
    }

    final void setArray(Object[] a) {
        array = a;
    }

    public E get(int index) {
        return (E) getArray()[index];
    }

    // 同remove set
    public boolean add(E e) {
        final ReentrantLock lock = this.lock;
        // 加锁
        lock.lock();
        try {
            // 获取原数组
            Object[] elements = getArray();
            int len = elements.length;
            // 原数组copy到新数组
            Object[] newElements = Arrays.copyOf(elements, len + 1);
            // 修改新数组
            newElements[len] = e;
            // 原数组替换为新数组
            setArray(newElements);
            return true;
        } finally {
            // 解锁
            lock.unlock();
        }
    }

}
```


[上一篇 Java数据结构](3-Java集合/Java数据结构.md)

[下一篇 Map](3-Java集合/Map.md)
