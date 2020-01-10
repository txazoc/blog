## JVM案例分析

### Tomcat session内存泄漏

* 高并发压测
* session未过期，StandardSession数量过多导致内存泄漏
* HttpServletRequest
    * sessionid
        * DEFAULT_SESSION_COOKIE_NAME: JSESSIONID
        * DEFAULT_SESSION_PARAMETER_NAME: jsessionid
    * getSession(boolean create): sessionid
* 排查思路
* 解决方案
    * 关闭session
    * 调小session过期时间(默认30分钟)

### CPU飙高

* `top` -&gt; 进程id
* `top -Hp 进程id` -&gt; 线程id(十进制) -&gt; `printf "%x"` -&gt; 线程id(十六进制)
* jstack 进程id -&gt; 线程堆栈(十六进制)
* 线程堆栈中查找线程id -&gt; 目标线程


[<< 上一篇: JVM排错](6-JVM/JVM排错.md)

[>> 下一篇: JVM监控工具](6-JVM/JVM监控工具.md)
