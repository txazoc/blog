## SPI机制

SPI，Service Provider Interface，服务提供者接口，是一种服务动态发现的机制

#### SPI开发步骤

* 定义服务接口

```java
public interface Invoker {

    public void invoke();

}
```

* 服务接口实现类

```java
public class MockInvoker implements Invoker {

    @Override
    public void invoke() {
        System.out.println("MockInvoker invoke");
    }

}
```

```java
public class RpcInvoker implements Invoker {

    @Override
    public void invoke() {
        System.out.println("RpcInvoker invoke");
    }

}
```

* META-INF/services目录下新建以服务接口命名的文件

`resources/META-INF/services/org.txazo.java.spi.Invoker`

```txt
org.txazo.java.spi.RpcInvoker
org.txazo.java.spi.MockInvoker
```

* ServiceLoader加载服务接口的实现类

```java
public static void main(String[] args) {
    ServiceLoader serviceLoader = ServiceLoader.load(Invoker.class);
    for (Iterator<Invoker> iterator = serviceLoader.iterator(); iterator.hasNext(); ) {
        Invoker invoker = iterator.next();
        invoker.invoke();
    }
}
```

#### SPI原理

* ServiceLoader.load()，延迟加载
* 获取服务接口配置文件列表
* 遍历服务接口配置文件列表
    * 逐行读取
    * 实例化服务接口实现类并尝试转型为服务接口
