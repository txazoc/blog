## Tomcat

### Tomcat请求流程

* `acceptCount`(backlog): 100
* Acceptor
    * `maxConnections`: 10000
    * accept()
    * offer Poller.events
* Poller[2]
    * Selector selector
    * SynchronizedQueue<PollerEvent> events
    * events -> poll() -> register OP_READ
    * selector -> select() -> isReadable -> SocketProcessor
* Executor
    * `minSpareThreads`: 10
    * `maxThreads`: 200
    * execute(SocketProcessor)
* SocketProcessor
    * parse HTTP
    * request
        * mapping
        * ApplicationFilterChain.doFilter()
        * servlet.service(request, response)
    * response
        * write()
        * register OP_WRITE

<p style="text-align: center;"><img src="_media/middleware/tomcat-request-process.png" alt="Tomcat Request Process" style="width: 60%"></p>
