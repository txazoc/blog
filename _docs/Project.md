### Project

#### 序列号

* 序列号 = 随机数(数字 + 26个字母) + 序列号类型id + 检验码
* 分库分表(序列号维度查询、序列号类型id查询)

#### 商品

* 商品基本信息表
* 商品扩展信息表
* 商品详情表
* appId生成: 商品类型分区间 + Redis incr

#### 白名单

* {ruleType_rule}_type_ObjectId

#### 站内信

#### PostOffice

#### 工具类

* LambdaUtils
