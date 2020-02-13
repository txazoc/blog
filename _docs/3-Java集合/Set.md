### Set

#### HashSet

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
