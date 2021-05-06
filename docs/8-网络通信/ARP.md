### ARP

> Address Resolution Protocol，`地址解析协议`，根据ip地址获取mac地址

#### ARP数据包

* 单播请求报文

```console
12	20.806089	Dell_87:d7:cc	Cisco_87:d6:db	ARP	42	Who has 192.168.80.254? Tell 192.168.80.34

Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: Dell_87:d7:cc (b0:83:fe:87:d7:cc)
    Sender IP address: 192.168.80.34
    Target MAC address: Cisco_87:d6:db (2c:33:11:87:d6:db)
    Target IP address: 192.168.80.254
```

* 广播请求报文

```console
68	148.631686	Cisco_87:d6:db	Broadcast	ARP	60	Who has 192.168.80.130? Tell 192.168.80.254

Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: Cisco_87:d6:db (2c:33:11:87:d6:db)
    Sender IP address: 192.168.80.254
    Target MAC address: 00:00:00_00:00:00 (00:00:00:00:00:00)
    Target IP address: 192.168.80.130
```

* 单播响应报文

```console
13	20.807258	Cisco_87:d6:db	Dell_87:d7:cc	ARP	60	192.168.80.254 is at 2c:33:11:87:d6:db

Address Resolution Protocol (reply)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: reply (2)
    Sender MAC address: Cisco_87:d6:db (2c:33:11:87:d6:db)
    Sender IP address: 192.168.80.254
    Target MAC address: Dell_87:d7:cc (b0:83:fe:87:d7:cc)
    Target IP address: 192.168.80.34
```

#### ARP缓存表

> 本机缓存ip地址和mac地址的映射关系

```console
> arp -a
(192.168.94.109) at 00:50:56:81:cb:fc [ether] on eth0
(192.168.95.153) at e4:54:e8:a1:ee:c8 [ether] on eth0
(192.168.94.29) at 00:50:56:ae:11:63 [ether] on eth0
(192.168.95.224) at 44:82:e5:a3:38:04 [ether] on eth0
(192.168.94.58) at 00:50:56:ae:73:9f [ether] on eth0
```


[<< 上一篇: Spring-MVC](7-开源框架/Spring-MVC.md)

[>> 下一篇: HTTP](8-网络通信/HTTP.md)
