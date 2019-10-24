### Map

#### HashMap

* 数组 + 链表 + 红黑树(jdk8)
* 原理
    * key -> hash() -> hashcode
    * table[hashcode & (table.length - 1)]
    * hash冲突
        * 链表遍历
        * 红黑树查找
    * key `==`或者`equals()`
* 链表长度超过8，并且table的长度不小于64(否则resize())，将链表转换为红黑树
* Node: key、value、hash、next
* resize()
    * 扩容一倍
    * oldTab[i] -> `newTab[i]` or `newTab[oldTab.length + i]`

```java
public class HashMap {

    transient Node<K, V>[] table;
    transient int size;             // 元素大小
    int threshold;                  // 阈值(capacity * loadFactor)
    final float loadFactor;         // 负载因子

}
```

#### Hashtable

#### LinkedHashMap

* HashMap + 双向链表
* 插入节点时，节点移动到双向链表尾部，如果removeEldestEntry()返回true，则删除头结点
* 删除节点时，节点从双向链表中移除
* accessOrder为true时，`get()`和`非插入put()`都会调用afterNodeAccess将节点移到尾部

```java
public class LinkedHashMap extends HashMap {

    final boolean accessOrder;  // 控制双向链表顺序，true按访问顺序排序，false按插入顺序排序
    transient LinkedHashMap.Entry<K, V> head;   // 头节点
    transient LinkedHashMap.Entry<K, V> tail;   // 尾节点

    static class Entry<K, V> extends HashMap.Node<K, V> {

        Entry<K, V> before, after;  // 前后节点

    }

}
```

#### 基于LinkedHashMap实现简单的LRU

```java
public class LinkedHashMapLRU extends LinkedHashMap {

    private static final int MAX_SIZE = 1000;

    public LinkedHashMapLRU(int size) {
        super(size, 0.75F, true);
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry eldest) {
        return size() > MAX_SIZE;
    }

}
```

#### ConcurrentHashMap

jdk1.7实现:

* 采用分段锁实现，ConcurrentHashMap包含一个Segment数组
* Segment继承自ReentrantLock，同时又是一个HashMap
* get，不加锁，通过volatile保证内存可见性
* put，ReentrantLock加锁

jdk1.8实现:

* 数组 + 链表 + 红黑树
* CAS + synchronized + volatile
