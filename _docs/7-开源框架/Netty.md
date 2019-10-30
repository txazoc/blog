## Netty

### 源码解析

#### 1. Netty Server启动

* NioServerSocketChannel注册`OP_ACCEPT`到boss线程池NioEventLoop的Selector上
* `boss`线程池NioEventLoop监听`OP_ACCEPT`事件，accept新的NioSocketChannel，并注册`OP_READ`到`worker`线程池NioEventLoop的Selector上
* `worker`线程池NioEventLoop监听`OP_READ`事件

#### 2. Netty Client启动

* NioSocketChannel注册`OP_READ`到`reactor`线程池NioEventLoop的Selector上
`reactor`线程池NioEventLoop监听`OP_READ`事件

#### 3. Netty Write

* channel.writeAndFlush()
* pipeline.write()
* unsafe.write: ByteBuf添加到ChannelOutboundBuffer(写缓冲区)中
* unsafe.flush: NioSocketChannel.doWrite()，ChannelOutboundBuffer中数据写入socket
* 没写完，注册`OP_WRITE`事件，NioSocketChannel绑定的NioEventLoop监听`OP_WRITE`事件，继续flush

#### 4. Netty Read

* NioSocketChannel绑定的NioEventLoop监听`OP_READ`事件
* NioByteUnsafe.read()
* 申请ByteBuf
* 读数据到ByteBuf
* pipeline.fireChannelRead()
* ByteBuf释放，重复使用
* pipeline.fireChannelReadComplete(): 一次Channel Read完成

### I/O模型

* IO多路复用: NioEventLoop -&gt; Selector

### 线程模型

#### NioEventLoopGroup

> 线程池，内部维护一组NioEventLoop线程

* parentGroup: `mainReactor线程池`
* childGroup: `subReactor线程池`

```java
public class ServerBootstrap {

    public ServerBootstrap group(EventLoopGroup parentGroup, EventLoopGroup childGroup) {
    }

}
```

* group: `业务线程池`，处理ChannelHandler，未指定则ChannelHandler由`childGroup`中和Channel绑定的NioEventLoop执行

```java
public interface ChannelPipeline {

    ChannelPipeline addLast(ChannelHandler... handlers);

    ChannelPipeline addLast(EventExecutorGroup group, ChannelHandler... handlers);

}
```

#### NioEventLoop

> 线程

* run()轮询
    * select()
    * processSelectedKeys(): 处理已就绪的I/O事件
    * runAllTasks(): 处理任务队列中的任务
    * ioRatio: 控制processSelectedKeys()和runAllTasks()的执行时间比例，默认为50

```java
public class NioEventLoop {

    // 选择器
    Selector selector;
    // 任务队列
    Queue<Runnable> taskQueue;
    // 调度任务队列
    Queue<ScheduledFutureTask<?>> scheduledTaskQueue;

}
```

### ByteBuf

* HeapByteBuf: 堆内存缓冲区
* DirectByteBuf: 直接内存缓冲区，Zero Copy
* PooledByteBuf: 池化缓冲区

```java
+-------------------+------------------+------------------+
| discardable bytes |  readable bytes  |  writable bytes  |
|                   |     (CONTENT)    |                  |
+-------------------+------------------+------------------+
|                   |                  |                  |
0      <=      readerIndex   <=   writerIndex    <=    capacity
```

### 事件驱动模型

#### ChannelPipeline

> 维护一个ChannelHandler链表

```java
                                             I/O Request
                                        via {@link Channel} or
                                    {@link ChannelHandlerContext}
                                                    |
+---------------------------------------------------+---------------+
|                           ChannelPipeline         |               |
|                                                  \|/              |
|    +---------------------+            +-----------+----------+    |
|    | Inbound Handler  N  |            | Outbound Handler  1  |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  |               |
|               |                                  \|/              |
|    +----------+----------+            +-----------+----------+    |
|    | Inbound Handler N-1 |            | Outbound Handler  2  |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  .               |
|               .                                   .               |
| ChannelHandlerContext.fireIN_EVT() ChannelHandlerContext.OUT_EVT()|
|        [ method call]                       [method call]         |
|               .                                   .               |
|               .                                  \|/              |
|    +----------+----------+            +-----------+----------+    |
|    | Inbound Handler  2  |            | Outbound Handler M-1 |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  |               |
|               |                                  \|/              |
|    +----------+----------+            +-----------+----------+    |
|    | Inbound Handler  1  |            | Outbound Handler  M  |    |
|    +----------+----------+            +-----------+----------+    |
|              /|\                                  |               |
+---------------+-----------------------------------+---------------+
                |                                  \|/
+---------------+-----------------------------------+---------------+
|               |                                   |               |
|       [ Socket.read() ]                    [ Socket.write() ]     |
|                                                                   |
|  Netty Internal I/O Threads (Transport Implementation)            |
+-------------------------------------------------------------------+
```

* Inbound Handler: `Socket.read()` -&gt; `ByteBuf` -&gt; `Inbound Handlers`
* Outbound Handler: `Channel.write()` -&gt; `Outbound Handlers` -&gt; `ByteBuf` -&gt; `Socket.write()`

#### ChannelHandler

> 处理I/O事件、拦截I/O操作，然后传递给ChannelPipeline中的下一个handler

### Codec编解码器

### 粘包/拆包

#### 粘包

> 多条数据在同一个ByteBuf中

#### 拆包

> 一条数据分散在多个ByteBuf中

#### 粘包/拆包解决方案

* 定长消息
    * `FixedLengthFrameDecoder`: 固定长度拆包器
* 特殊分隔符
    * `LineBasedFrameDecoder`: 行拆包器，以换行符作为分隔符
    * `DelimiterBasedFrameDecoder`: 分隔符拆包器
* 消息头/消息体
    * `LengthFieldBasedFrameDecoder`: 数据包长度拆包器，消息头指定消息长度
* 自定义协议

### Netty断线重连

### Netty架构图

<p style="text-align: center;"><img src="_media/openframework/netty-architecture.jpeg" alt="Netty Architecture" style="width: 72%"></p>

### 基于Netty实现RPC

简单的代码实现参见 [https://github.com/txazo/netty/tree/master/src/test/java/test/netty/core](https://github.com/txazo/netty/tree/master/src/test/java/test/netty/core)

* client: 动态代理、Future模式
* Netty Handler链: 协议、编码解码、序列化/反序列化
* server: 反射
