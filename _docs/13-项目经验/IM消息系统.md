## IM消息系统

#### TCP长连接鉴权

* http请求获取token
* 建立tcp长连接(待鉴权连接)
* 发送token -> 已鉴权连接

#### 用户在线/离线/隐身状态

#### 在线消息/离线消息

* bitmap

#### 消息可靠投递

#### 消息时序性

#### 群组消息

#### 消息撤回

* 删除存储消息
* 发送消息撤回指令

#### 消息类型

* 表情
* 文本
* 图片
* 视频

#### 消息id

#### 消息协议

#### 消息存储/检索/清除

#### 会话

#### TCP长连接

* 心跳保活，断线重连
* 固定频率发送心跳，心跳超时判断(接收到的最后一个数据包)
* 心跳超时次数阀值

#### im-server消息转发

* im-server注册到zookeeper
* im-server内网端口两两互连

#### 文献

* [IM (一)：基本介绍](https://www.jianshu.com/p/38e127cb03ec)
* [一套简洁的即时通信(IM)系统](https://kb.cnblogs.com/page/541190/)
* [Netty 入门与实战：仿写微信 IM 即时通讯系统](https://juejin.im/book/5b4bc28bf265da0f60130116)
* [即时通讯网](http://www.52im.net/)
