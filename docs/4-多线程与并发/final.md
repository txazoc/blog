## final

### final修饰类

> final修饰的类不可被继承

### final修饰方法

> final修饰的方法不可被重写

### final修饰变量

> final修饰的变量在初始化后不可被修改

#### static final静态变量

* static final静态变量存储在方法区
* 在类加载时，给static final静态变量分配内存空间，赋初值，并执行static代码块

#### final实例变量

* final实例变量存储在堆中
* 对象创建时，final实例变量必须被初始化

#### final局部变量

* final局部变量存储在栈中的局部变量表中

#### final方法参数

* final方法参数存储在栈中的局部变量表中

#### 匿名内部类 & final

> 匿名内部类中访问的局部变量或方法参数必须被声明为final

```java
public Runnable getTask(final String name) {
    return new Runnable() {

        @Override
        public void run() {
            System.out.println(name);
        }

    };
}
```

上面的例子中，返回的匿名内部类对象内部会访问到方法参数name，但此时getTask方法已退出，该方法的栈帧已被虚拟机栈弹出，方法参数name就没有了。

为此，在创建匿名内部类对象时，通过构造函数将方法参数name拷贝到匿名内部类对象的实例变量中。

final就是为了保证拷贝时，方法参数name没有被修改。

### final内存屏障

> 新建对象时，对final变量的初始化写入和把这个对象赋值给其它引用变量，这两者之间不可重排序


[上一篇 concurrent并发包](4-多线程与并发/concurrent并发包.md)

[下一篇 Java内存模型](4-多线程与并发/Java内存模型.md)
