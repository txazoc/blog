## MySQL技术内幕-InnoDB存储引擎

### 主键

主键索引 &gt; 第一个非空唯一索引 &gt; DB_ROW_ID

插入性能: 自增索引、离散索引

### 行记录格式-Compact

* 非NULL定长/变长字段长度列表(逆序)
* NULL标志位: NULL字段
* 记录头信息: 5字节
* DB_ROW_ID: 6字节
* DB_TRX_ID: 6字节
* DB_ROLL_PTR: 7字节
* 非NULL列数据: 列1数据、列2数据、...

create table mytest (
t1 varchar(10),
t2 varchar(10),
t3 char(10),
t4 varchar(10)
) engine=innodb charset=utf8 row_format=compact;

insert into mytest values('a', 'bb', 'bb', 'ccc');
insert into mytest values('d', 'ee', 'ee', 'fff');
insert into mytest values('d', NULL, NULL, 'fff');

create table mytest2 (
t1 varchar(10) not null,
t2 varchar(10),
t3 varchar(10) not null,
t4 varchar(10) not null,
t5 varchar(10) not null,
t6 varchar(10) not null,
t7 varchar(10) not null,
t8 varchar(10) not null,
t9 varchar(10),
t10 varchar(10),
t11 varchar(10),
t12 varchar(10)
) engine=innodb charset=utf8 row_format=compact;

insert into mytest1 values('aaaa', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'fff');
insert into mytest1 values('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12');
insert into mytest2 values('1', NULL, '3', '4', '5', '6', '7', '8', '9', '10', NULL, NULL);

create table mytest3 (
id int(11) not null auto_increment primary key,
t1 varchar(10),
t2 varchar(10),
t3 varchar(10),
t4 varchar(10)
) engine=innodb charset=utf8 row_format=compact;

insert into mytest3 values('a', 'bb', 'ccc', 'dddd');

create table mytest4 (
t1 varchar(10) unique,
t2 varchar(10),
t3 varchar(10),
t4 varchar(10)
) engine=innodb charset=utf8 row_format=compact;

insert into mytest4 values('a', 'b', 'c', 'd');
insert into mytest4 values('bbb', 'c', 'd', 'e');
insert into mytest4 values('ccccc', 'd', 'e', 'f');
insert into mytest4 values('ddddddd', 'e', 'f', 'g');
