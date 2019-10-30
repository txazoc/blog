## Set

### HashSet

* 基于HashMap实现

```java
public class HashSet {

    private static final Object PRESENT = new Object();

    private transient HashMap<E, Object> map;

    public HashSet() {
        map = new HashMap<>();
    }

    public boolean add(E e) {
        return map.put(e, PRESENT) == null;
    }

}
```


[上一篇 Queue](3-Java集合/Queue.md)

[下一篇 优先级队列](3-Java集合/优先级队列.md)
