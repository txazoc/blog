## IO

IO主要处理三个问题:

* `字节数组传输`: 包括读写文件、内存、网络
* `中间处理`: 包括缓冲、压缩/解压缩、加密解密
* `编码解码`: 包括字符编码/解码、基本数据类型、对象序列化/反序列化、自定义协议

编码 -> 中间处理 -> 字节数组传输 -> 中间处理 -> 解码

#### 节点流

* 文件流
    * FileInputStream/FileOutputStream
* 内存流
    * ByteArrayInputStream/ByteArrayOutputStream
    * CharArrayReader/CharArrayWriter
    * StringReader/StringWriter
* 网络流
    * SocketInputStream/SocketOutputStream

#### 适配器模式

* 字节字符转换流: 字节流转换为字符流
    * InputStreamReader/OutputStreamWriter
        * FileReader/FileWriter

#### 装饰器模式

* 缓冲流: 减少系统调用次数
    * BufferedInputStream/BufferedOutputStream
    * BufferedReader/BufferedWriter
* 数据流: 读写基本数据类型
    * DataInputStream/DataOutputStream
* 对象流: 对象的序列化和反序列化
    * ObjectInputStream/ObjectOutputStream
* 打印流: 换行、格式化输出
    * PrintStream
    * PrintWriter
* 压缩流: 压缩/解压缩
    * ZipInputStream/ZipOutputStream
    * GZIPInputStream/GZIPOutputStream

#### 序列化/反序列化

* Serializable
* Externalizable
    * readExternal()/writeExternal()
* readObject()/writeObject()
* 默认: 遍历非transient的field

#### 字符集&字符编码

#### Linux IO模型

先给出I/O模型涉及到的几个概念:

* **同步(sync)**: 操作执行完成后才返回
* **异步(async)**: 调用立即返回，操作执行完成后发送通知或回调
* **阻塞(blocking)**: 线程阻塞等待
* **非阻塞(non-blocking)**: 线程不用阻塞等待

阻塞/非阻塞、同步/异步的区别:

* 阻塞I/O和非阻塞I/O: 内核数据准备就绪阶段
* 同步I/O和异步I/O: 数据从内核空间copy到用户空间阶段

**I/O分类:**

* `BIO`: 同步阻塞I/O
* `NIO`: 同步非阻塞I/O
* `AIO`: 异步非阻塞I/O

**5种I/O模型:**

* 阻塞IO

以Socket的recv()为例:

* recv()调用
* `阻塞`: 等待接收缓冲区中的数据准备就绪
* `同步`: 数据从内核空间copy到用户空间

<p style="text-align: center;"><img src="_media/java/blocking-io.jpg" alt="Hash" style="width: 50%"></p>

* 非阻塞IO

以Socket(设置为非阻塞)的recv()为例:

* recv()调用
* `非阻塞`: 接收缓冲区中的数据未准备就绪，调用立即返回
* `同步`: 接收缓冲区中的数据准备就绪，数据从内核空间copy到用户空间

非阻塞式I/O需要不断轮询，消耗CPU，很少使用

<p style="text-align: center;"><img src="_media/java/nonblocking-io.jpg" alt="Hash" style="width: 50%"></p>

* IO多路复用

以Socket的recv()为例:

* select()调用等待有可读的套接字(接收缓冲区中的数据准备就绪)
* recv()调用
* `非阻塞`: 接收缓冲区中的数据已准备就绪
* `同步`: 数据从内核空间copy到用户空间

I/O多路复用的优点是一个线程可以处理多个连接

<p style="text-align: center;"><img src="_media/java/multi-io.jpg" alt="Hash" style="width: 50%"></p>

> I/O多路复用的原理是一个线程管理多个Socket，有三种实现: select、poll、epoll
>
> select和poll需要自己不断轮询所有fd集合，epoll基于事件回调
>
> select和poll的IO效率会随着fd数量增加而线性下降，epoll则不会

* 信号驱动IO

用的很少，略过

<p style="text-align: center;"><img src="_media/java/signal-driven-io.jpg" alt="Hash" style="width: 50%"></p>

* 异步IO

以Linux的aio_read()为例:

* aio_read()调用
* `非阻塞`: 提交异步io请求，调用返回
* `异步`: 内核等待接收缓冲区中的数据准备就绪，将数据从内核空间copy到用户空间，然后回调

<p style="text-align: center;"><img src="_media/java/async-io.jpg" alt="Hash" style="width: 50%"></p>


[<< 上一篇: Java注解](2-Java基础/Java注解.md)

[>> 下一篇: 动态代理](2-Java基础/动态代理.md)
