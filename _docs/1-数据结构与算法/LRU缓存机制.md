## LRU缓存机制

> 运用你所掌握的数据结构，设计和实现一个  `LRU (最近最少使用)` 缓存机制。它应该支持以下操作： 获取数据 `get` 和 写入数据 `put` 。

> 获取数据 `get(key)` - 如果密钥 (key) 存在于缓存中，则获取密钥的值（总是正数），否则返回 -1。
> 写入数据 `put(key, value)` - 如果密钥不存在，则写入其数据值。当缓存容量达到上限时，它应该在写入新数据之前删除最近最少使用的数据值，从而为新的数据值留出空间。

> 进阶:

> 你是否可以在 `O(1)` 时间复杂度内完成这两种操作？

```java
public class LRUCache {

    private final LinkedHashMap<Integer, Integer> cache;


    public LRUCache(int capacity) {
        cache = new LRULinkedHashMap<>(capacity);
    }

    public int get(int key) {
        Integer value = cache.get(key);
        return value != null ? value : -1;
    }

    public void put(int key, int value) {
        cache.put(key, value);
    }

    private static class LRULinkedHashMap<K, V> extends LinkedHashMap<K, V> {

        private static final long serialVersionUID = 8202653567905852980L;

        private int capacity;

        public LRULinkedHashMap(int initialCapacity) {
            super(initialCapacity, 0.75F, true);
        }

        @Override
        protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
            return size() >= capacity;
        }

    }

}
```
