## JVM

> JVM，Java Virtual Machine，Java虚拟机

### 类文件结构

> Java源代码编译后的二进制的字节码

### 类加载链接初始化

### 字节码执行

#### 字节码指令集

字节码指令集格式:

```java
<opcode> [<operand1> [<operand2> ...]]
```

javap后的格式：

```java
<index> <opcode> [<operand1> [<operand2> ...]] [<comment>]
```

* index: 字节码的偏移位置
* opcode: 指令
* operand&lt;n&gt;: 指令的操作数
* comment: 注释

### 运行时数据区

#### 程序计数器

```c
while (true) {
    opcode = *pc;
    execute(opcode);    // 执行当前指令
    update(pc);         // pc指向下一条指令地址
}
```

#### Java虚拟机栈

#### 本地方法栈

#### 堆

#### 方法区

#### 运行时常量池

### 内存分配

Java对象内存分配流程:

* 栈上分配
* 尝试在TLAB分配
* 大对象直接在老年代分配
* 尝试在Eden区分配
* Eden区空间不足，触发yong gc

#### TLAB

> Thread Local Allocation Buffer，线程本地分配缓冲区

```c
// TLAB结构
class ThreadLocalAllocBuffer : public CHeapObj<mtThread> {

  private:

    HeapWord *_start;                       // 开始地址
    HeapWord *_top;                         // 上次分配后的地址
    HeapWord *_end;                         // 结束地址(不包括对齐保留的内存空间)

};

// TLAB分配，指针碰撞
inline HeapWord *ThreadLocalAllocBuffer::allocate(size_t size) {
    // top地址
    HeapWord *obj = top();
    // 检查剩余空间是否满足分配
    if (pointer_delta(end(), obj) >= size) {
        // 分配成功, 更新top地址
        set_top(obj + size);
        return obj;
    }
    return NULL;
}
```

#### Eden

```c
// 堆区连续内存空间内存分配，指针碰撞
inline HeapWord *ContiguousSpace::par_allocate_impl(
        size_t size,                    // 分配内存大小
        HeapWord *const end_value       // end()
) {
    do {
        // top地址
        HeapWord *obj = top();
        // 检查剩余空间是否满足分配
        if (pointer_delta(end_value, obj) >= size) {
            // 剩余空间满足分配
            HeapWord *new_top = obj + size;
            // CAS尝试更新top地址
            HeapWord *result = (HeapWord *) Atomic::cmpxchg_ptr(new_top, top_addr(), obj);
            if (result == obj) {
                // 分配成功, 返回分配到的基地址
                return obj;
            }
            // 分配失败, 重试
        } else {
            // 剩余空间不满足分配, 返回NULL
            return NULL;
        }
    } while (true);
}
```

#### oop-kclass

***对象***

```c
instanceOop {
    markOop     _mark       // 对象头
    _metadata   _metadata   // 元数据指针
    ...                     // 字段值
}
```

***数组***

```console
arrayOop {
    markOop     _mark       // 对象头
    _metadata   _metadata   // 元数据指针
    jint        length      // 数组长度
    ...                     // 数组元素
}
```

#### 内存碎片

### 垃圾回收

> 自动回收不可用的内存

#### 标记算法

* 引用计数法: 循环引用问题
* 可达性分析法

***GC Roots***:

* 线程栈帧: 方法参数、局部变量
* 本地方法栈
* 方法区中static变量
* 常量池

***Minor GC标记***:

* Young Gen: GC Roots级联
* Old Gen: 卡片标记

> 卡片标记，老年代的内存分片，一个片默认512字节，上次老年代GC后，如果分片中的对象发生修改或者指向新生代对象，将此分片标记为dirty，Minor GC时，只扫描dirty卡片中的对象，而无需扫描整个老年代

#### 垃圾回收算法

* 复制算法
* 标记-清除算法
* 标记-整理算法
* 分代算法

#### 安全点

> Safepoint，在代码执行过程中的一些特殊位置，虚拟机的状态是安全的，可以在这个位置暂停

#### GC触发条件

***Minor GC触发条件***

* 新生代eden内存空间不足
* -XX:+CMSScavengeBeforeRemark: 在执行CMS Remark前执行一次Young GC，减少老年代对新生代的引用，降低Remark的开销
* Full GC时会先触发Minor GC

***Full GC触发条件***

* System.gc()
* 老年代空间不足
* 永久代空间不足
* CMS GS时promotion failed: Minor GC时
* CMS GS时concurrent mode failure: CMS GS时大对象进入老年代，而老年代空间不足

#### GC调优

***GC调优目标***

* 减少gc次数
* 减小gc停顿时间
* 提高吞吐量

***GC调优策略***

* 垃圾收集器组合选择
* 参数调整
* 分析gc日志

### 垃圾收集器



#### 参数
