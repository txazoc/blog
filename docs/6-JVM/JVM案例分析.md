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
