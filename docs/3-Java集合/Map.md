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

* synchronized

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
* get()
    * volatile读table
    * 遍历链表或查找红黑树
* put()
    * volatile读table
    * synchronized链表头节点

```java
public class ConcurrentHashMap<K, V> {

    volatile Node<K, V>[] table;

    static class Node<K, V> {
        final int hash;
        final K key;
        volatile V val;
        volatile Node<K, V> next;
    }

}
```

#### TreeMap

* 红黑树

```java
public class TreeMap<K, V> {

    int size;
    Entry<K, V> root;

    static final class Entry<K, V> {
        K key;
        V value;
        Entry<K, V> left;
        Entry<K, V> right;
        Entry<K, V> parent;
        boolean color = BLACK;
    }

}
```

#### ConcurrentSkipListMap

* 跳表 + volatile + CAS
* head &gt; 向右 &gt; 向下

```console
Head nodes          Index nodes
+-+    right        +-+                      +-+
|2|---------------->| |--------------------->| |->null
+-+                 +-+                      +-+
 | down              |                        |
 v                   v                        v
+-+            +-+  +-+       +-+            +-+       +-+
|1|----------->| |->| |------>| |----------->| |------>| |->null
+-+            +-+  +-+       +-+            +-+       +-+
 v              |    |         |              |         |
Nodes  next     v    v         v              v         v
+-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+
| |->|A|->|B|->|C|->|D|->|E|->|F|->|G|->|H|->|I|->|J|->|K|->null
+-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+  +-+
```

```java
public class ConcurrentSkipListMap<K, V> {

    volatile HeadIndex<K, V> head;

    static final class HeadIndex<K, V> extends Index<K, V> {

        final int level;

    }

    static class Index<K, V> {

        final Node<K, V> node;
        final Index<K, V> down;
        volatile Index<K, V> right;

    }

    static final class Node<K, V> {

        final K key;
        volatile Object value;
        volatile Node<K, V> next;

    }

}
```

#### WeakHashMap

> WeakHashMap的`Entry`是一个弱引用

```java
/**
 * 继承自WeakReference
 */
private static class Entry<K, V> extends WeakReference<Object> implements Map.Entry<K, V> {

    // key为Reference的referent
    // value
    V value;
    // hash值
    final int hash;
    // next
    Entry<K, V> next;

    Entry(Object key, V value,
          ReferenceQueue<Object> queue,
          int hash, Entry<K, V> next) {
        super(key, queue);
        this.value = value;
        this.hash = hash;
        this.next = next;
    }

}
```

* key只被WeakReference.Entry弱引用，gc时key被回收，key = null
* 被回收key的entry入队列queue
* 操作WeakHashMap时，会执行expungeStaleEntries()清除queue中的entry
* expungeStaleEntries()
    * queue中的entry出队列
    * entry从entry链中删除
    * entry.value = null
* 下一次gc，value如果不被其它对象引用，就会被回收


[<< 上一篇: List](3-Java集合/List.md)

[>> 下一篇: Queue](3-Java集合/Queue.md)
