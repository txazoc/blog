### Redis

#### 字符串-sds

#### 列表-list

```c
// 列表
typedef struct list {
    listNode *head;         // 表头节点指针
    listNode *tail;         // 表尾节点指针
    unsigned long len;      // 节点数
} list;

// 列表节点
typedef struct listNode {
    struct listNode *prev;  // 前置节点指针
    struct listNode *next;  // 后置节点指针
    void *value;            // 节点的值指针
} listNode;
```

#### 字典-dict

```c
// 字典
typedef struct dict {
    dictht ht[2];           // hash表数组, 大小为2, ht[0]用来读写, ht[1]用来rehash
    long rehashidx;         // rehash索引, 即table下标, 记录rehash的进度, 为-1时表示没有在rehash
} dict;

// hash表
typedef struct dictht {
    dictEntry **table;      // hash表数组
    unsigned long size;     // hash表大小, 2的n次方
    unsigned long sizemask; // hash表大小掩码, 等于size - 1
    unsigned long used;     // hash表中已有的节点数
} dictht;

// hash表节点
typedef struct dictEntry {
    void *key;              // 键
    union {
        void *val;
        uint64_t u64;
        int64_t s64;
        double d;
    } v;                    // 值
    struct dictEntry *next; // 下一个节点指针, 构成链表, 解决hash键冲突
} dictEntry;
```

##### hash

* index = `hash(key) & sizemask`
* hash键冲突: 链地址法
* 负载因子: `used / size`

##### 渐进式rehash

* 遍历ht[0]，转移到ht[1]
* rehash过程中有读写操作时，同步操作ht[0]和ht[1]

#### Redis内存淘汰

* volatile-lru: 从设置了过期时间的key中挑选最近最少使用的key淘汰
* volatile-ttl: 从设置了过期时间的key中挑选最快过期的key淘汰
* volatile-random: 从设置了过期时间的key中随机挑选key淘汰
* allkeys-lru: 从所有key中挑选最近最少使用的key淘汰
* allkeys-random: 从所有key中随机挑选key淘汰
* no-eviction: 内存淘汰关闭，写请求直接返回错误，`默认策略`

##### Redis LRU

#### Redis集群

##### 槽

* 槽解决的是粒度问题，把粒度变小，便于数据移动
* 哈希解决的是映射问题，使用key的哈希值映射到槽，便于数据分配

##### get

* key -&gt; hash -&gt; slot -&gt; node
* 客户端缓存槽和节点的映射
* node重定向
* 不支持mget不同的node，解决方案{prefix}.suffix
