### 虚拟IP

> `VIP`，虚拟IP，是一个不与特定计算机或计算机中的网络接口卡相连的IP地址

#### VRRP

> Virtual Router Redundancy Protocol，虚拟路由冗余协议，可以将几台路由器联合组成一台虚拟的路由器

* `虚拟路由器`: Virtual Router，多个物理路由器对外以一个IP地址(VIP)提供服务，仿佛一台路由器，一台物理路由器宕机后，通过VRRP机制选举出新的物理路由器作为网关路由器

##### VRRP状态机

* `Initialize`
* `Master`
    * 定时发送VRRP报文
    * 以虚拟MAC地址响应对虚拟IP地址的ARP请求
    * 转发目的MAC地址为虚拟MAC地址的IP报文
* `Backup`
    * 接收Master发送的VRRP报文，判断Master状态是否正常
    * 对虚拟IP地址的ARP请求，不做响应
    * 丢弃目的IP地址为虚拟IP地址的IP报文

#### Keepalived主从

* `Master`: 主机
    * IP: `192.168.100.1`
    * MAC: `2c:33:11:87:d6:db`
* `Backup`: 备机
    * IP: `192.168.100.2`
    * MAC: `b0:83:fe:87:d7:cc`
* `VIP`: `192.168.100.3`

**Master Keepalived配置:**

```js
global_defs {
    router_id router-1
}

vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 50
    priority 100
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        192.168.100.3
    }
}
```

**Backup Keepalived配置:**

```js
global_defs {
    router_id router-1
}

vrrp_instance VI_1 {
    state BACKUP
    interface eth0
    virtual_router_id 50
    priority 90
    advert_int 1
    authentication {
        auth_type PASS
        auth_pass 123456
    }
    virtual_ipaddress {
        192.168.100.3
    }
}
```

##### Master正常

> Master对外广播ARP报文，`VIP指向主机(192.168.100.1)`

**ARP缓存:**

```bash
> arp -a
(192.168.100.1) at 2c:33:11:87:d6:db [ether] on eth0
(192.168.100.2) at b0:83:fe:87:d7:cc [ether] on eth0
(192.168.100.3) at 2c:33:11:87:d6:db [ether] on eth0
```

##### Master宕机

> Backup发现Master宕机后，VRRP根据优先级选举出新的Master，对外广播ARP报文，`VIP指向备机(192.168.100.2)`，即发生了`IP地址漂移`

**ARP缓存:**

```bash
> arp -a
(192.168.100.1) at 2c:33:11:87:d6:db [ether] on eth0
(192.168.100.2) at b0:83:fe:87:d7:cc [ether] on eth0
(192.168.100.3) at b0:83:fe:87:d7:cc [ether] on eth0
```


[<< 上一篇: TCP](8-网络通信/TCP.md)

[>> 下一篇: InnoDB](9-数据库/InnoDB.md)
