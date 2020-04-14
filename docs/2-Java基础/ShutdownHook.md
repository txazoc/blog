### ShutdownHook

```java
Runtime.getRuntime().addShutdownHook(new Thread() {

    @Override
    public void run() {
        System.out.println("Shutdown hook execute");
    }

});
```

```java
class ApplicationShutdownHooks {

    private static IdentityHashMap<Thread, Thread> hooks;

    static void runHooks() {
        Collection<Thread> threads;
        synchronized (ApplicationShutdownHooks.class) {
            threads = hooks.keySet();
            hooks = null;
        }

        for (Thread hook : threads) {
            hook.start();
        }
        for (Thread hook : threads) {
            try {
                hook.join();
            } catch (InterruptedException x) {
            }
        }
    }

}
```


[<< 上一篇: NIO](2-Java基础/NIO.md)

[>> 下一篇: SPI机制](2-Java基础/SPI机制.md)
