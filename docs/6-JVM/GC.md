## GC

### GC调优

#### GC调优目标

* 响应速度: GC停顿时间
* 吞吐量: GC线程的CPU使用率

### GC分代收集

* 新生代(Young Generation)
    * Eden
    * Survivor
        * S0、S1
        * From Survivor、To Survivor
* 老年代(Old Generation)
    * Old

#### Young GC(Minor GC)

> 新生代的垃圾回收，Young GC每次都会`Stop The World`

* Eden区空间不足，触发Young GC

#### Old GC

> 老年代的垃圾回收

* CMS

#### Full GC

> 整个堆的垃圾回收，包括新生代、老年代和元空间

#### Mixed GC

> 整个新生代以及部分老年代的垃圾回收

* G1

### GC日志分析

* -verbose:gc
* -XX:+PrintGCDetails
* -XX:+PrintGCTimeStamps
* -XX:+PrintGCDateStamps

### 内存分配策略

* 新对象优先在eden区分配
* 大对象直接进入老年代，`-XX:PretenureSizeThreshold=0`，默认为0
* 长期存活的对象从新生代晋升到老年代，对象晋升的最大阀值`-XX:MaxTenuringThreshold=15`，默认为15
* 空间分配担保
    * Young GC前
    * 老年代剩余空间大于新生代已使用空间 -> Young GC，否则下一步
    * 老年代剩余空间小于历史晋升到老年代对象的平均大小 -> Full GC，否则下一步
    * Young GC
    * 老年代剩余空间小于晋升到老年代对象的大小(担保失败`promotion failed`) -> Full GC，否则下一步
    * 担保成功，结束
* 动态对象年龄判定
    * compute_tenuring_threshold
    * 所有对象的年龄从0开始累加，加到年龄为n后，累加对象空间大于s0或s1大小 * `TargetSurvivorRatio` / 100时
    * 此次Young GC，对象晋升的年龄阀值为min(n, `MaxTenuringThreshold`)
    * Young GC后，Survivor空间不足，未达到晋升条件的新生代存活对象直接进入老年代

### 专有名次解释

* GC Roots
* Stop The World
* Safepoint

### 参考

* https://www.jianshu.com/p/945881f5d439
* https://www.jianshu.com/p/b4bb2d751810
* https://www.jianshu.com/p/0c7cd3811f7b
* https://www.jianshu.com/p/18931fbdac05
* https://www.jianshu.com/p/0d36c6d0ddf0
* https://www.jianshu.com/search?q=gc%20%E6%8B%85%E4%BF%9D&page=1&type=note
* https://blog.csdn.net/ustcyy91/article/details/76731659
* https://mp.weixin.qq.com/s/uvYmmrfDuUfc4Z5SOblG3w
* https://my.oschina.net/u/2663968/blog/3109540


[<< 上一篇: JVM案例分析](6-JVM/JVM案例分析.md)

[>> 下一篇: 类加载&对象初始化](6-JVM/类加载&对象初始化.md)
