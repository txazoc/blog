## Java 8新特性

### Lambda表达式

* `(params) -> expression`
* `(params) -> statement`
* `(params) -> { statement }`

### 函数式接口

> 只有一个抽象方法的接口

`@FunctionalInterface`注解用来标识一个接口是函数式接口

```java
@FunctionalInterface
public interface Runnable {

    public abstract void run();

}
```

### 方法引用

### 接口默认方法

```java
public interface List<E> {

    default void sort(Comparator<? super E> c) {
    }

}
```

### Stream API

> 流式API

`stream pipeline`，流管道

* `source`(源): 创建Stream
    * array、collection
* `intermediate operations`(中间操作): `stream` -&gt; `stream`，转换Stream
    * map、filter、distinct
* `terminal operation`(终止操作): 聚合，`lazy`
    * count、forEach、collect

### Date Time API

> 新的日期时间API

### Optional类

> 用来解决空指针异常


[<< 上一篇: Java引用](2-Java基础/Java引用.md)

[>> 下一篇: Timer定时任务](2-Java基础/Timer定时任务.md)
