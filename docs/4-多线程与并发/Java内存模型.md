## Java内存模型

### 共享内存

> 可以在线程之间共享的内存称为共享内存(主内存)

### happens-before规则

> 规定两个操作之间的执行顺序，提供内存可见性的保证

* 程序顺序规则: 一个线程中的每个操作，happens-before于该线程中的任意后续操作
* 监视器锁规则: 对一个监视器锁的解锁，happens-before随后对这个监视器锁的加锁
* volatile变量规则: 对一个volatile变量的写操作，happens-before随后对这个volatile变量的读操作
* 线程启动规则: 对一个线程的start()操作，happens-before这个线程中的任意操作
* 线程终止规则: 一个线程中的所有操作，happens-before从这个线程的join()返回
* 线程中断规则: 对一个线程的interrupt()操作，happens-before被中断线程检测到中断事件的发生
* 对象finalize规则: 一个对象的初始化完成，happens-before这个对象的finalize()开始
* 传递性: 如果A happens-before B，且B happens-before C，那么A happens-before C

### MESI-缓存一致性协议

> 支持回写高速缓存的协议

#### CPU多级缓存

* L1 Cache
* L2 Cache
* L3 Cache

#### 缓存一致性协议四种状态

缓存一致性协议给缓存行定义了四种状态:

* `M`: 修改态，Modified，此Cache Line已被修改(`脏行`)，和主存不一致，只存在于本cache中
    * 写回主存: 此Cache Line的状态变为`E`独享态
* `E`: 独享态，Exclusive，此Cache Line有效，和主存一致，只存在于本cache中
    * 写: 此Cache Line的状态变为`M`修改态
* `S`: 共享态，Shared，此Cache Line有效，和主存一致，也出现在其它cache中
    * 写
        * 此Cache Line的状态变为`M`修改态
        * 其它CPU中此Cache Line的状态变为`I`无效态
* `I`: 无效态，Invalid，此Cache Line无效
    * 读
        * 其它CPU无该Cache Line: 此Cache Line的状态变为`E`独享态
        * 其它CPU有该Cache Line: 所有CPU中此Cache Line的状态变为`S`共享态

***多核CPU下缓存行的状态变更***

| cache(CPU A) | cache(CPU B) | 操作 |
| --- | --- | --- |
| `E` | `-` | CPU A读x |
| `E -> S` | `S` | CPU B读x |
| `S -> M` | `S -> I` | CPU A写x |
| `M -> E -> S` | `I -> S` | CPU B读x |

### 内存屏障

> 解决指令重排导致的内存可见性问题

* 读内存屏障: 在读指令前插入Load Barrier，让缓存行失效，强制从主内存加载数据
* 写内存屏障: 在写指令后插入Store Barrier，将写缓冲区数据刷新到主内存

#### volatile内存语义的实现

* 在每个 volatile 写操作的前面插入一个 StoreStore 屏障: 禁止前面的写与volatile写重排序
* 在每个 volatile 写操作的后面插入一个 `StoreLoad` 屏障: 禁止volatile写与后面可能有的读和写重排序
* 在每个 volatile 读操作的后面插入一个 LoadLoad 屏障: 禁止volatile读与后面的读操作重排序
* 在每个 volatile 读操作的后面插入一个 LoadStore 屏障: 禁止volatile读与后面的写操作重排序

volatile重排序规则:

| 是否能重排序 | 普通读/写 | volatile读 | volatile写 |
| --- | --- | --- | --- |
| 普通读/写 | - | - | NO |
| volatile读 | NO | NO | NO |
| volatile写 | - | NO | NO |

* 任何形式的volatile读和volatile写都不能重排序
* 普通读/写和volatile写不能重排序
* volatile读和普通读/写不能重排序


[上一篇 final](4-多线程与并发/final.md)

[下一篇 synchronized](4-多线程与并发/synchronized.md)
