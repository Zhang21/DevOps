---

title: "MySQL"
date: "2018-01-16 10:47:12"
categories: "Database"
tags: "MySQL"

---


参考：

- MySQL5.7参考文档： <https://dev.mysql.com/doc/refman/5.7/en/>

<br/>

环境：

- CentOS7.x86_64
- MySQL5.7



<!--more-->

<br/>
<br/>

---

<br>



# 序言



MySQL官网： <https://www.mysql.com/>

由于MySQL5.7和以前版本之间的许多功能和其他差异，因此此手册不太适用于之前的老版本。之前的版本请参考MySQL相关版本的手册。

<br>

![MySQL](/images/MySQL/MySQL.png)




<br/>
<br/>

---

<br>


# 综述

General information


MySQL™ software提供了一个快速、多线程、多任务和健壮的SQL(结构化查询语言)的数据库服务器。MySQL server是为关键服务(mission-critical)、重负荷(heavy-load)生产系统以及嵌入式(embedding)大规模部署的软件而设计。
MySQL是Oracle Corporation的商标(trademark)。

MySQL software是双重许可的(dual license)：

1. Open Source product of the GNU General Public License
2. A Standard commercial License from Oracle




<br>
<br/>

## 关于此手册


- 该手册作为一个参考，它不提供关于SQL或关系型数据库概念的一般指令；
- MySQL Database Software正在不断发展，所以参考手册也经常更新。可在此 < http://dev.mysql.com/doc/> 获取最新版的手册；
- 参考手册(Reference Manual)的源文件使用DocBook XML格式书写的，其他版本(如HTML)等是自动生成的；
- 如果在使用过程中有任何问题或建议，请发邮件给我们；
- 手册由MySQL Documentation Team维护。



<br/>
<br>



## MySQL数据库管理系统

MySQL Database Management System


<br>


### MySQL介绍

MySQL是最流行的开源的SQL数据库管理系统，由Oracle Corporation开发、分发和支持。

<br>

- MySQL is a database management system
数据库是一个结构化的数据集合。它可能是从简单的购物清单到图片库，或是公司网络中的大量信息。若要添加、访问和处理存储在计算机数据库中的数据，你需要一个像MySQL Server这样的数据库管理系统。由于计算机非常擅长处理大量的数据，数据库管理系统在计算机中扮演这一个重要的角色。

- MySQL databases are relational
关系型数据库将数据存储在单独的表(table)中，而不是将所有数据放入一个大的库房中。数据库结构被组织成针对速度优化的物理文件。具有数据库(database)，表(table)，视图(view)，行(row)，列(column)等物理对象的逻辑模型提供了灵活的编程环境。你设置了管理不同数据字段之间关系的规则，如一对一，一对多，唯一，必须和可选关系，以及不同表之间的指针(pointer)。数据库强制执行这些规则，这样在设计良好的数据库中，应用程序就不会看到不一致、重复、孤立、过时或丢失的数据。

MySQL也是代表SQL(Structure Query Language)的一部分。SQL是访问数据库最常用的标准化语言。你可以直接使用SQL语句，或者将SQL语法隐藏到语言特定的API中。

-MySQL software is Open Source
MySQL software使用GPL(GNU General Public License)，开源意味着任何人都可以下载、转发、使用和修改软件，而不需要支付任何费用。

- MySQL database server is very fast,reliable,scalabe and easy to use

- MySQL server works in Client/Server or embedded system
MySQL Database Server是一个由多线程(multi-threaded)SQL Server组成的客户/服务器系统。它支持不同的后端，多个不同的客户程序和库、管理工具和广泛的APIs。
还提供MySQL Server作为一个嵌入式多线程库以便链接到你的产品，以获得一个更小，更快，更容易管理的独立产品。

- A large amount of contributed MySQL software is available


<br>
<br/>


### MySQL主要特点


#### Internals and Portability

- 由C和C++写成
- 适用于许多不同的平台
- 为了可移植性，使用`CMake`
- 采用独立(independent)模块的多层(layer)服务器设计
- 设计为使用内核线程的完全多线程，如果有多核CPU，能够轻松使用它们
- 提供了事务性(transactional)和非事务性(notransactional)存储引擎
- 使用非常快速的带有索引压缩的B-tree磁盘表
- 添加其他存储引擎相对容易
- 使用非常快速的基于线程的内存分配系统
- 使用优化的嵌套循环(nested-loop)连接执行非常快的联结
- 实现内存中的hash table，这些表用作临时表
- 使用高度优化的类库实现SQL函数

<br>

#### 数据类型

- 1,2,3,4和8byte的有无符号(signed/unsigned)的整数(integers)
- FLOAT
- DOUBLE
- CHAR, VARCHAR
- BINARY, VARBINARY
- TEXT
- BLOB
- DATE, TIME, DATETIME
- TIMESTAMP
- YEAR
- SET
- ENUM
- OpenGIS

<br>

#### 状态和功能

statement and function

- `SELECT`和`WHERT`中包含了所有支持的操作符和函数
- SQL中的`GROUP BY`和`ORDER BY`也全部支持
- GROUP functions(`COUNT()`, `AVG()`, `STD()`, `SUM()`, `MAX()`, `MIN()`, `GROUP_CONCAT()`)
- 支持`LEFT OUTER JOIN`和`ROGHT OUTER JOIN`
- 按照SQL标准支持table和columns的别名
- 支持`DELETE`,`INSERT`,`REPLACE`,`UPDATE`，以返回受影响的行数
- 支持MySQL特定的`SHOW`显示语句
- 一个`EXPLAIN`语句显示优化器如何解析查询

<br>

#### 安全

security

- 权限(privilege)和密码系统，非常灵活和安全，并且支持基于主机的验证
- 当连接到Server时，通过加密(encryption)所有密码通信量来确保密码安全

<br/>

#### 扩展性和限制

Scalability and Limits

- 支持大型数据库。包含五千万条记录，二十万个表，五十亿行
- 每个表最多支持64个索引，每个索引可以由1到16个列组成

<br/>

####　连通性

Conectivity

- 客户端使用如下几种协议连接到MySQL Server
	+ TCP/IP sockets
	+ --enable-named-pipe on Windows
	+ Unix domain socket files on UNIX
- MySQL客户端可用多种语言编写
- APIs对于多数语言是可用的

<br/>

#### 本地化

Localization

- Server可以向多种语言的客户端提供错误信息
- 完全支持几个不同的字符集(character sets)
- 所有数据都被保存在选取的字符集(chracter set)
- 排序和比较是根据默认的字符集和排序规则完成
- 服务器时区(time zone)可动态更改，个客户端也可修改自己的时区

<br/>

#### 客户端和工具

Clients and Tools

- MySQL包含几个客户机和使用程序
	+ command-line： `mysqldump`, `mysqladmin`
	+ graphical: MySQL Workbench
- MySQL Server内置了对SQL语句的支持来检查、优化和修复表
- MySQL程序可使用`--help`或`-?`来获取帮助


<br>
<br/>


### MySQL历史

History of MySQL

- MySQL is named after co-founder Monty Widenius's daughter, My.
- The name of the MySQL Dolphin (our logo) is “Sakila,” which was chosen from a huge list of names suggested by users in our “Name the Dolphin” contest.



<br/>
<br/>



## MySQL5.7新特色

What Is New in MySQL 5.7

<br>

### MySQL5.7新功能

Features Added in MySQL 5.7


<br>
<br/>


### MySQL5.7中过期的功能

Features Deprecated in MySQL 5.7


<br/>
<br>


### MySQL5.7中移除的功能

Features Removed in MySQL 5.7



<br>
<br/>



##  Server and Status Variables and Options Added, Deprecated, or Removed in MySQL 5.7



<br>
<br/>



## MySQL信息源

MySQL Information Sources

本章节将列出有关MySQL的帮助信息。


<br>


### MySQL站点

MySQL Websites

MySQL Documentation is <https://dev.mysql.com/doc>






















<br/>
<br/>

---

<br>



# 安装和升级

- mysql-repo: <http://repo.mysql.com/>
- yum-repo: <http://repo.mysql.com/yum/>


<br>


安装MySQL一般遵循以下步骤：

- 确定MySQL是否支持你的平台(platform)
	+ Unix、Linux、FreeBSD
	+ Windows
	+ OS X
- 选择要安装的发行版(distribution)
- 下载你想要安装的发行版
- 安装发行版
- 执行任何必要的安装后设置


<br>
<br>


## 通用安装指南

General Installation Guidance

<br>
<br/>


### 安装哪个发行版和MySQL版本

Which MySQL Version and Distribution to Install

<br>

在准备安装MySQL时，请决定使用哪种版本(version)和发行(distribution)格式(binary or source)


首先，决定安装开发版还是稳定版。

- Development release
	+ 具有新功能，但不推荐用于生产环境
- General Availability(GA) release
	+ 也称为稳定版(stable release)，推荐为生产环境使用

MySQL命名方案(naming scheme)， 例如MySQL5.7.1：

- 5为主版本号(major)
- 7为次版本号(minor)
- 1为发行(release)系列版本号
	+ 系列号描述了稳定的功能集。对于每个新的修补程序，这都会增加。

在选择要安装的MySQL版本之后，决定要为操作系统安装哪个发行版格式。

- 二进制(binary)
	+ RPM, DMG
- 源码(source)
	+ tar, zip

在某些情况下，最好使用源码安装MySQL：

- 想在某个明确的位置安装MySQL
- 希望使用二进制发行版中未包含的特性配置mysqld
- 希望配置mysqld，而不需要二进制发行版中包含的一些功能
- 你希望读取或修改组成MySQL的C、C++源代码
- 源码发行版比二进制发行版包含更多的测试和示例


<br/>
<br/>


### 如何获取MySQL

How to Get MySQL

<br>

- MySQL当前版本下载页： <https://dev.mysql.com/downloads/>
- 完整的MySQL镜像： <https://dev.mysql.com/downloads/mirrors/>
- 基于RPM的Linux平台，MySQL Yum Repository： <https://dev.mysql.com/downloads/repo/yum/>
- 基于Debian的Linux平台，MySQL APT Repository： <https://dev.mysql.com/downloads/repo/apt/>
- SUSE Linux平台，MySQL SUSE Repository： <https://dev.mysql.com/downloads/repo/suse/>


<br/>
<br/>


### 使用MD5校验和或GnuPG验证程序完整性

Verifying Package Integrity Using MD5 Checksums or GnuPG

<br>

下载好MySQL包并在安装它之前，请确保它是完整的并未被篡改。有如下三种方法：

- MD5 checksums
- Cryptographic signatures using GnuPG, the GNU Privacy Guard
- For RPM packages, the built-in RPM integrity verification mechanism


<br/>
<br/>

#### 验证MD5校验和

Verifying the MD5 Checksum

<br>

应确保下载的MySQL包的MD5校验和与MySQL官方提供的校验和相匹配。

```sh
md5sum mysql-standard-5.7.22-linux-i686.tar.gz
#aaab65abbec64d5e907dcd41b8699945  mysql-standard-5.7.22-linux-i686.tar.gz
```


<br>

#### 使用GnuPG进行签名检查

Signature Checking Using GnuPG

<br>

要验证软件包的签名，首先需要我们的公共GPG密钥的副本。可从<http://pgp.mit.edu/>下载。
你想要获得的密钥名为**mysql-build@oss.oracle.com**，如下:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1.4.5 (GNU/Linux)

mQGiBD4+owwRBAC14GIfUfCyEDSIePvEW3SAFUdJBtoQHH/nJKZyQT7h9bPlUWC3
RODjQReyCITRrdwyrKUGku2FmeVGwn2u2WmDMNABLnpprWPkBdCk96+OmSLN9brZ
fw2vOUgCmYv2hW0hyDHuvYlQA/BThQoADgj8AW6/0Lo7V1W9/8VuHP0gQwCgvzV3
BqOx后面还有很多，省略
-----END PGP PUBLIC KEY BLOCK-----
```

使用`gpg --import`将密钥导入到个人公共GPG密钥环中。如公共密钥为`mysql_pubkey.asc`：

```
gpg --import ./mysql_pubkey.asc


#或使用public key id下载公共密钥
gpg --recv-keys $pub-key-id
```

在rpm包中验证:

```
rpm --import ./mysql_pubkey.asc
```

确保两个文件都放置于同一目录下，然后运行命令验证签名：

```
gpg --verify package_name.asc

gpg --verify mysql-standard-5.7.22-linux-i686.tar.gz.asc
gpg: Signature made Tue 01 Feb 2011 02:38:30 AM CST using DSA key ID 5072E1F5
gpg: Good signature from "MySQL Release Engineering <mysql-build@oss.oracle.com>"
```

<br>

#### 使用RPM进行签名检查

Signature Checking Using RPM

<br/>

```
rpm --checksig package_name.rpm

[zhang@zabbix ~]$ rpm --checksig mysql-community-server-5.7.20-1.el7.x86_64.rpm
mysql-community-server-5.7.20-1.el7.x86_64.rpm: (sha1) dsa sha1 md5 gpg OK
```

rpm还支持从URL加载密钥:

```
rpm --import http://dev.mysql.com/doc/refman/5.7/en/checking-gpg-signature.html
```


<br/>
<br/>


### 安装布局

Installation Layouts

<br/>

不同的安装类型(native packages, binary tarballs, and source tarballs)有不同的安装布局，这样可能会导致混淆。


<br/>
<br/>



## 在Unix/Linux上使用通用二进制文件安装MySQL

Installing MySQL on Unix/Linux Using Generic Binaries

<br>

包括以压缩的tar文件形式的通用二进制发行版，以及针对特定平台封装格式的二进制文件。

MySQL压缩tar文件二进制发行版具有** mysql-VERSION-OS.tar.gz**的文件格式。

MySQL依赖于`libaio` Library：

```sh
yum install -y libaio
```

<br>

默认地，tar文件二进制发行版，解压后安装于`/usr/local/mysql`目录。会在目录下生产 通用Unix/Linux二进制包的MySQL安装布局目录

目录 | 内容
- | -
bin | mysqld server, client and utility programs
docs | MySQL manual in Info format
man | Unix manual pages
include | Include (header) files
lib | Libraries
share | Error messages, dictionary, and SQL for database installation
support-files | Miscellaneous support files


大致命令如下：

```
shell> groupadd mysql
shell> useradd -r -g mysql -s /bin/false mysql
shell> cd /usr/local
shell> tar zxvf /path/to/mysql-VERSION-OS.tar.gz
shell> ln -s full-path-to-mysql-VERSION-OS mysql
shell> cd mysql
shell> mkdir mysql-files
shell> chown mysql:mysql mysql-files
shell> chmod 750 mysql-files
shell> bin/mysqld --initialize --user=mysql
shell> bin/mysql_ssl_rsa_setup
shell> bin/mysqld_safe --user=mysql &
# Next command is optional
shell> cp support-files/mysql.server /etc/init.d/mysql.server



#添加环境变量
export PATH=$PATH:/usr/local/mysql/bin
```


<br/>
<br/>


## 在Linux上安装MySQL

Installing MySQL on Linux

<br>

Linux支持多种方法来安装MySQL。建议使用Oracle提供的一个发行版：

- Apt
- Yum
- Zypper
- RPM
- DEB
- Generic
- Source
- Docker
- Oracle Unbreakable Linux Network

作为一个选择，你可以使用系统中的包管理工具自动下载和安装MySQL。


<br>
<br>


### 在Linux上使用Yum Repository安装MySQL

Installing MySQL on Linux Using the MySQL Yum Repository

<br>


**安装一个全新的MySQL的步骤：**

- 添加MySQL Yum Repository
	- 首先，添加MySQL Yum repository到你的系统仓库列表
	- 选择和下载对应平台的release 或者 手动添加repository文件
	- 安装release package

```sh
#yum localinstall platform-and-version-specific-package-name.rpm
yun install http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql57-community-release-el7-10.noarch.rpm


yum repolist enabled | grep "mysql.*-community.*"
```

- 选择一个release series

默认是最新的GA series，当前最新是MySQL5.7。

查看所有的MySQL Yum repository: `yum repolist all | grep mysql`

安装最新MySQL不需要配置，而安装先前的版本则需要指定GA series。disable最新的GA series并且enable需要的GA series。

```
yum-config-manager --disable mysql57-community

yum-config-manager --enable mysql56-community
```

**或者手动创建repo，可直接定义版本**

```
[mysql57-community]
name=MySQL 5.7 Community Server
baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql
```

- 安装MySQL

在安装MySQL过程中出现错误，请务必查看日志文件。

```
yum install -y mysql-community-server mysql-community-client

#也可不安装客户端

```

- 开启MySQL Server

```
service mysqld start
#Starting mysqld:[ OK ]

service mysqld status
```

**在服务器初始启动时，如果服务器的数据目录为空，则会发生一下情况：**

- 服务器已初始化
- SSL certificate and key files 在数据目录中生成
- validate_password已安装并启用
- 超级用户账户'root'@'localhost'被创建，超级用户密码被设置并被存储在error log files
	+ 这一点和以前版本有很大区别，我被坑惨了

**注意：**
> ValidPassword的默认密码策略要求包含大写字母、小写字母、数字和特殊字符，并且密码长度至少为8个字符

```
#查看初始密码
grep 'temporary password' /var/log/mysqld.log


#无法使用mysqladmin修改密码，需要登录mysql后修改

mysql -uroot -p


#重置密码
ALTER USER 'root'@'localhost' IDENTIFIED BY 'NewPass4!;


#如果找不到初始密码
vim /etc/my.cnf

#在[mysqld]最后行加上skip-grant-tables实现无认证登录
#重启MySQL
UPDATE  mysql.user  SET  authentication_string =PASSWORD('新密码')  WHERE  USER='xxx';


#修改默认密码策略
#更改密码强度
set global validate_password_policy=0;

#设置密码最小长度
set global validate_password_length=4;
```


<br>

**使用Yum安装额外的MySQL产品和组件**

你可使用Yum安装和管理MySQL的个别组件。

```sh
yum --disablerepo=\* --enablerepo='mysql*-community*' list available

yum install package-name

#栗子
yum install mysql-community-libs
```


<br/>
<br/>


### 在Linux上使用Oracle提供的RPM包安装MySQL

Installing MySQL on Linux Using RPM Packages from Oracle

<br>

MySQL Community Edition的rpm包如下：

包名 | 描述
- | -
mysql-community-server | Database server and related tools
mysql-community-client | MySQL client applications and tools
mysql-community-common | Common files for server and client libraries
mysql-community-server-minimal | Minimal installation of the database server and related tools
mysql-community-devel | Development header files and libraries for MySQL database client applications
mysql-community-libs | Shared libraries for MySQL database client applications
mysql-community-libs-compat | Shared compatibility libraries for previous MySQL installations
mysql-community-embedded | MySQL embedded library
mysql-community-embedded-devel | Development header files and libraries for MySQL as an embeddable library
mysql-community-test | Test suite for the MySQL server

<br>

```
#rpm -qpl mysql-community-server-version-distribution-arch.rpm

#yum install mysql-community-{server,client,common,libs}-*


wget http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql-community-server-5.7.20-1.el7.x86_64.rpm
wget http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql-community-client-5.7.20-1.el7.x86_64.rpm

yum install -y mysql-community-server-5.7.20-1.el7.x86_64.rpm mysql-community-client-5.7.20-1.el7.x86_64.rpm
```

<br>

**Linux RPM包MySQL开发区的安装布局：**

文件或资源 | 位置
- | -
Client programs and scripts | /usr/bin
mysqld server | /usr/sbin
configuration file | /etc/my.cnf
data directory | /var/lib/mysql
error log file | /var/log/mysqld.log
Value of secure_file_priv | /var/lib/mysql-files
System V init script | /etc/init.d/mysqld
Systemd service | mysqld
pid file | /var/run/mysql/mysqld.pid
socket | /var/lib/mysql/mysql.sock
Keyring directory | /var/lib/mysql-keyring
Unix manual pages | /usr/share/man
include (header) files | /usr/include/mysql
Libraries | /usr/lib/mysql
Miscellaneous support files (for example, error messages, and character set files)	| /usr/share/mysql

<br>

The installation also creates a user named mysql and a group named mysql on the system.

> **注意**
> 安装MySQL会在系统上生成一个名为mysql的用户和群组
> 安装以前的MySQL版本可能会创建`my.cnf`配置文件。强烈建议先将`my.cnf`进行迁移，然后删除它。之后才安装MySQL


<br/>
<br/>


### 用systemd管理MySQL Server

Managing MySQL Server with systemd

<br>

#### systemd综述

Overview of systemd

<br>

`systemd`提供了MySQL Server的自动开启和关闭，使用`systemctl`命令进行管理。

或者，使用`system V`系统兼容的`service`命令。

```
systemctl {start|stop|restart|status} mysqld

service mysqld {start|stop|restart|status}
```

对systemd的支持包括这些文佳：

- mysqld.service
	+ systemd服务单元配置文件，以及有关MySQL服务的详细信息
- mysqld@.service
	+ 用于管理多个MySQL实例
- mysqld.tmpfiles.d
	+ 包含支持临时文件功能的信息
- mysqld_pre_systemd
	+ 支持单元文件的脚本

<br>

#### 为MySQL配置systemd

Configuring systemd for MySQL

<br>

为MySQL添加或修改systemd选项，参考如下方法：

- 使用一个本地化的systemd配置文件
- 安排systemd为MySQL Server进程设置环境变量
- 设置MYSQLD_OPTS systemd变量

创建`/etc/systemd/system/mysqld.service`本地化systemd配置文件，这里讨论的是将此文件名作为`override.conf`：

```sh
[Service]
LimitNOFILE=max_open_files
PIDFile=/path/to/pid/file
Nice=nice_level
LimitCore=core_file_limit
Environment="LD_PRELOAD=/path/to/malloc/library"
Environment="TZ=time_zone_setting"


#LimitNOFILE: 文件描述符数量
#LimitCore: 最大核心文件大小
#Nice: 优先级
#LD_PRELOAD: 特定内存分配库
#TZ: 指定时区
```

修改mysqld:

```
systemctl edit mysqld
```

重新加载systemd配置，然后重启MySQL service：

```
systemctl daemon-reload

systemctl restart mysqld
```

可在`override.conf`中设置如下参数：

```sh
[Service]
PIDFile=/var/run/mysqld/mysqld-custom.pid
ExecStart=
ExecStart=/usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld-custom.pid $MYSQLD_OPTS
```

在`/etc/sysconfig/mysql`下指定值：

```sh
LD_PRELOAD=/path/to/malloc/library
TZ=time_zone_setting


systemctl restart mysqld
```

<br>

#### 使用systemd配置多个MySQL实例

Configuring Multiple MySQL Instances Using systemd

<br>

由于systemd具有在平台上管理多个MySQL实例的能力，而不必须需要`mysqld_multi`和`mysqld_multi.server`。

若要使用多实例(multiple-instance)功能，请修改`/etc/my.cnf`文件以包含每个实例的关键选项配置。
例如，管理replication01和replication02两个实例：

```
vim /etc/my.cnf


[mysqld@replica01]
datadir=/var/lib/mysql-replica01
socket=/var/lib/mysql-replica01/mysql.sock
port=3307
log-error=/var/log/mysqld-replica01.log


[mysqld@replica02]
datadir=/var/lib/mysql-replica02
socket=/var/lib/mysql-replica02/mysql.sock
port=3308
log-error=/var/log/mysqld-replica02.log
```

**这里的名称使用`@`作为分隔符(delimiter)，因为这个是`systemd`支持的唯一分隔符。**

管理两个实例:

```
systemctl start mysqld@replica01
systemctl start mysqld@replica02


systemctl enable mysqld@replica01
systemctl enable mysqld@replica02


#使用通配符
systemctl status 'mysqld@replica*'


systemctl stop mysqld@replica0{1,2}
```

对于同一个机器上的不同MySQL实例，systemd自动使用不同的单元文件。
在unit file中，`%I`和`%i`用于`@`标记后传入参数，用于管理特定实例。

```sh
#像这样
mysqld --defaults-group-suffix=@%I ...


systemctl status mysqld@replica01

# mysqld@replica01.service - MySQL Server
#  Loaded: loaded (/usr/lib/systemd/system/mysqld@.service; disabled; vendor preset: disabled)
#  Active: active (running) since Tue 2018-02-27 12:18:34 CST; 1min 6s ago
#    Docs: man:mysqld(8)
#          http://dev.mysql.com/doc/refman/en/using-systemd.html
# Process: 3927 ExecStart=/usr/sbin/mysqld --defaults-group-suffix=@%I --daemonize --pid-file=/var/run/mysqld/mysqld-%i.pid $MYSQLD_OPTS (code=exited, status=0/SUCCESS)
# Process: 3845 ExecStartPre=/usr/bin/mysqld_pre_systemd %I (code=exited, status=0/SUCCESS)
#Main PID: 3930 (mysqld)
#  CGroup: /system.slice/system-mysqld.slice/mysqld@replica01.service
#          `-3930 /usr/sbin/mysqld --defaults-group-suffix=@replica01 --daemonize --pid-file=/var/run/mysqld/mysqld-replica01.pid
#
#eb 27 12:18:27 zabbix.me systemd[1]: Starting MySQL Server...
#eb 27 12:18:34 zabbix.me systemd[1]: Started MySQL Server.
```

<br/>

#### 从mysqld_safe迁移到systemd

Migrating from mysqld_safe to systemd

<br>

因为`mysqld_safe`没有安装在使用`systemd`管理MySQL的平台上，所以以前需要为该程序指定选项：`[mysqld_safe]`

- 一些`[mysqld_safe]`的选项也能被`[mysqld]`支持
- 一些`[mysqld_safe]`的选项类似于`[mysqld]`选项



<br/>
<br/>


## 从源码安装MySQL

Installing MySQL from Source

<br>

从源代码构建MySQL使我们能够自定义构建参数(parameter)、编译器优化(compiler optimization)和安装位置(installation location)。

在使用源码安装前，请检查Oracle是否为你的平台生成预编译的二进制发行版，以及是否适合你。Oracle付出了很多努力确保提供的二进制文件具有最佳的性能选择。

**源码安装系统需求：**
使用源码安装MySQL需要多种开发工具。

使用源码安装MySQL，必须满足一下系统需求：

- CMake, which is used as the build framework on all platforms
- A good make program
- A working ANSI C++ compiler
- The Boost C++ libraries are required to build MySQL
- The ncurses library
- Sufficient free memory
- Perl is needed if you intend to run test scripts

使用standard source distribution安装MySQL，需要以下工具来unpack分发文件：

- For a .tar.gz compressed tar file: `tar`
- For a .zip Zip archive: `zip`
- For an .rpm RPM package: `rpmbuild`


<br/>
<br/>


### 用于源码安装的MySQL布局

MySQL Layout for Source Installation

<br>

默认地，再从源码编译后安装MySQL时，安装步骤会将文件安装在`/usr/local/mysql`下。


<br/>
<br/>


### 使用标准源码发行版安装MySQL

Installing MySQL Using a Standard Source Distribution

<br>

从一个标准源码发行版安装MySQL：

1. 确保系统满足工具需求
2. 获取发行文件
3. 配置、构建和安装
4. 执行安装后程序

<br>

如果是source RPM:

```sh
rpmbuild --rebuild --clean MySQL-VERSION.src.rpm
```

<br>

如果是compressed tar file 或 zip archive source:

```sh
# Preconfiguration setup
shell> groupadd mysql
shell> useradd -r -g mysql -s /bin/false mysql


# Beginning of source-build specific instructions
shell> tar zxvf mysql-VERSION.tar.gz
shell> cd mysql-VERSION
shell> mkdir bld
shell> cd bld
shell> cmake ..
shell> make
shell> make install


# End of source-build specific instructions
# Postinstallation setup
shell> cd /usr/local/mysql
shell> mkdir mysql-files
shell> chown mysql:mysql mysql-files
shell> chmod 750 mysql-files
shell> bin/mysqld --initialize --user=mysql
shell> bin/mysql_ssl_rsa_setup
shell> bin/mysqld_safe --user=mysql &


# Next command is optional
shell> cp support-files/mysql.server /etc/init.d/mysql.server
```

**/sbin/nologin和/bin/false的区别**

- /bin/false是最严格的禁止login选项，一切服务都不能用
	+ `mongod:x:996:994:mongod:/var/lib/mongo:/bin/false`
- /sbin/nologin只是不允许系统login，可以使用其他服务
	+ `ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin`

<br>

**执行预配置(preconfiguration)设置**

在Unix上，设置MySQL用户和组，用于运行和执行MySQL服务器和数据库目录。

<br>

**获得和解包distribution**

选择要解压分发的目录，并将位置更改到其中。

```sh
tar zxvf mysql-VERSION.tar.gz

#gunzip < mysql-VERSION.tar.gz | tar xvf -
#cmake -E tar zxvf mysql-VERSION.tar.gz
```

<br/>
<br/>


### 使用开发源码树安装MySQL

Installing MySQL Using a Development Source Tree

<br>

install MySQL from the latest development source codew hich is hosted on GitHub: <https://github.com/mysql/mysql-server>

**设置一个MySQL git repository**

1. 克隆MySQL git repository到本机

```sh
git clone https://github.com/mysql/mysql-server.git
```

2. 查看

```sh
cd mysql-server
```

3. 使用`git branch -r`查看远程MySQL分支

```sh
cd mysql-server

git branch -r
```

4. 查看分支

```sh
cd mysql-server

git branch
```

5. 切换分支

```sh
cd mysql-server

git checkout 5.7
```

6. 获取远程MySQL git repository更新

```sh
cd mysql-server

git pull
```

7. 检查提交历史

```sh
cd mysql-server

git log

#也可在MySQL GitHub上查看commit history
```

9. 在克隆MySQL git repository并切换到需要的分支后，便可以从源代码构建MySQL Server。

在生产机器上从分发源码树安装构件时要小心，安装命令可能会覆盖您的实时发行版安装。


<br/>
<br/>


### MySQL源码配置选项

MySQL Source-Configuration Options

<br/>

CMake程序提供了一个强大的如何配置MySQL源码发行版的控制。

具体链接参考: <https://dev.mysql.com/doc/refman/5.7/en/source-configuration-options.html>


<br/>
<br/>

### 处理MySQL编译问题

Dealing with Problems Compiling MySQL

<br>

- 如果CMake先前已经运行过，那么现在运行的CMake可能使用先前的调用过程中收集到的信息。这些信息存储在 CMakeCache.txt。在CMake启动时，它会寻找和读取此文件。
- 每次运行`CMake`，必须再次运行`make`才能重新编译。

防止使用old object file或配置文件:

```sh
make clean
rm CMakeCache.txt
```


<br/>
<br/>


## 安装之后的设置和测试

Postinstallation Setup and Testing

<br>

在安装MySQL后你应该做的事：

- 如有必要，初始化数据目录并创建MySQL授权表
- 开启Server并确保它可以正常访问
- 将密码分配给授权表中的root用户
- 可选地，设置Server自启动
- 可选地，填写时区表，以便识别时区


<br>


### 初始化数据目录

Initializing the Data Directory

<br>


安装MySQL之后，必须初始化数据目录，包括mysql系统数据库中的表。有些安装方法会自动初始化，有些则需要手动初始化。
当然，如果修改了默认数据目录位置，那么也是需要手动初始化的。

初始化数据库目录，主要是包含了初始MySQL授权表(grant table)的MySQL服务器，这些表确定了如何允许用户连接到服务器。
但是，初始化数据目录是不会覆盖(overwrite)任何现有权限表，因此在任何情况下运行都是安全的。

数据目录初始化会在MySQL数据库汇总创建time zone，但不会填充它，所以它是空的。

```sh
cd /usr/local/mysql

mkdir mysql-files

chown mysql:mysql ./mysql-files
chmod 750 ./mysql-files


#--user
#使数据库目录文件属于mysql用户，以确保Server有读取权限
/usr/local/mysql/bin/mysqld --initialize --user=mysql


#开启安全连接
/usr/local/mysql/bin/mysql_ssl_rsa_setup
```

<br>

#### 使用mysqld手动初始化数据目录

Initializing the Data Directory Manually Using mysqld

<br>

```sh
cd /usr/local/mysql/bin


#使数据库目录文件属于mysql用户，以确保Server有读取权限
#默认是secure，会生成root初始密码
./mysqld --initialize --user=mysql


#不生成root初始密码
./bin/mysqld --initialize-insecure --user=mysql


#指定目录
--basedir=/usr/local/mysql
--datadir=/var/lib/mysql


#或者将其写入配置文件
vim /etc/my.cnf

[mysqld]
basedir=/usr/local/mysql
datadir=/var/lib/mysql

#指定配置文件初始化
./mysqld --defaults-file=/etc/mysql.cnf --initialize --user=mysql
```

<br>

#### 使用mysql_install_db初始化数据目录

Initializing the Data Directory Manually Using mysql_install_db

<br>

```sh
cd /usr/local/mysql/bin


#mysql_install_db命令会创建数据目录，并在数据目录下创建mysql数据库和授权表
./mysql_install_db --user=mysql


#指定目录是必须的
--basedir=/usr/local/mysql
--datadir=/var/lib/mysql

./mysqld_safe --user=mysql &
#systemctl start mysqld

mysql -u root -p xxx

mysql>SET PASSWORD FOR 'root'@'localhost' = PASSWORD('new_password');
```


<br/>
<br/>


### Starting the Server


- Start the MySQL server like this if your installation includes mysqld_safe
	+ `/usr/local/mysql/binmysqld_safe --user=mysql &`
- Start the server like this if your installation includes systemd support
	+ `systemctl start mysqld`
- 使用non-root用户运行MySQL服务很重要
- 如有错误请查看日志


<br>
<br/>


### Testing the Server

执行一些简单测试以保证Server正常工作。

```sh
#使用mysqladmin验证Server正在运行
mysqladmin --help

mysqladmin -uuser -ppasswd version

mysqladmin -uuser -ppasswd variables

mysqladmin -user -ppasswd shutdown


# 使用mysqlshow查看数据库
mysqlshow -uuser -ppasswd

#查看指定数据库信息
mysqlshow -uuser -ppasswd mysql


#读取信息
#-e,Execute command and quit
mysql -uuser -ppasswd -e "SELECT user, host from mysql.user"
```


<br/>
<br/>


### 保护初始化MySQL账户

Securing the Initial MySQL Accounts

<br>

在安装MySQL后，root账户密码可能已经被分配。

`mysql.user`授权表定义了初始化MySQL用户账户和它们的访问权限。
MySQL5.7只创建了一个`'root'@'localhost'`账户，但早期的版本可能有多个用户。

请务必为每一个MySQL账户创建密码。

查看用户：

```sh
#存储在authentication_string列中的密码可能包含无法正常显示的二进制数据
#所以将其转换为十六进制
mysql> SELECT user, host, hex(authentication_string) FROM mysql.user;
mysql> SELECT user, host, authentication_string FROM mysql.user;

#或
mysql -uuser -ppasswd -e "SELECT user, host, hex(authentication_string) FROM mysql.user;"


#5.7以前的版本
mysql> mysql> SELECT user, host, password FROM mysql.user;

#或
mysql -uuser -ppasswd -e "SELECT user, host, password FROM mysql.user;"
```

<br>

**为root账户分配密码**

```
#5.7.6
mysql> ALTER USER user IDENTIFIED BY 'new_passwd';

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_passwd';


#5.7.6前
mysql> SET PASSWORD FOR username = PASSWORD('new_passwd');

mysql> SET PASSWORD FOR 'root'@'localhost' = PASSWORD('new_passwd');
```

<br>

**给anonymous账户分配密码**

```
mysql> SET PASSWORD FOR ''@'localhost' = PASSWORD('new_passwd');
```

<br>

**移除匿名账户**

```
mysql> DROP USER ''@'localhost';
```


<br/>
<br/>


## 升级或降级MySQL

Upgrading or Downgrading MySQL

<br>

- 升级是一个常见的过程。请在测试系统上确保运行正常后再实施到生产环境
- 降级不太常见。一般是由于新版本在生产环境上发生某些兼容性或性能问题，并且是在测试环境中没有发现的情况下，从而需要降级。请现在测试系统上运行正常后再实施到生产环境。


<br/>
<br/>


### 升级MySQL

请使用有管理权限的MySQL账户执行升级相关命令。(如root账户)

<br>

#### MySQL升级策略

MySQL Upgrade Strategies

<br>

**升级方法**

- 直接升级(In-Place Upgrade)
	+ 包含关闭旧版MySQL，替换为新的MySQL版本，在现有数据目录上重启MySQL，运行`mysql_upgrade`
- 逻辑升级(Logical Upgrade)
	+ 包含使用`mysqldump`导出现有数据文件，安装新版MySQL，导入数据文件到新版MySQL，运行`mysql_upgrade`

<br>

**升级路径**

- 只支持GA release之间
- 这是一个发行系列的升级
	+ 如5.6.x到5.6.y
- 升级到下一个版本之前，建议先升级到最新版本
	+ 如先升级到5.6最新版，再升级到5.7
- 不支持跳版本升级
	+ 如5.5到5.7

<br>

**升级之前**

- 升级之前，请一定备份数据
- 查看新版本的Release Note
	+ 删除和增加了什么功能
- 新版本依赖什么
- 如果在InnoDB中使用XA事务，则在升级之前运行XA恢复以检查未提交的XA事务
- 如果MySQL数据量很大，就地升级以后可能需要很长的时间才能进行转换
	+ 你可能会发现创建一个"dummy"数据库实例是很有用的，以及评估可能需要哪些转换以及执行这些转换所涉及的工作
- 无论在你安装或升级到一个MySQL新版本，建议重建和重装MySQL language interface
	+ 如PHP MySQL扩展

<br/>

**直接升级**

- 配置MySQL执行slow shutdown

innoDB在关闭前执行一个完整的清除和更改缓冲区合并，这确保数据文件在不同的版本的文件格式做好充分准备。

```sh
mysql -u root -p --execute="SET GLOBAL innodb_fast_shutdown=0"
```

- 关闭MySQL Server

```sh
mysql -uroot -p shutdown
```

- 升级MySQL

- 开启新版MySQL

- 运行mysql_upgrade

`mysql_upgrade`检查所有数据库中的所有表与当前版本MySQL的不兼容性。

```sh
mysql_upgrade -uroot -p

#Upgrade process completed successfully.
#Checking if update is needed.
```

- 关闭和重启MySQL Server来确保改变生效

```sh
mysqladmin -uroot -p shutdown

systemctl start mysqld
```

<br>

**逻辑升级**

- 导出所有数据

```sh
mysqldump -uroot -p  --all-databases --force > mysqldb_backup.sql


#-f, --force         Continue even if we get an SQL error
#Use the --routines and --events options if your databases include stored programs
#--add-drop-database Add a DROP DATABASE before each create.
mysqldump -uroot -p --add-drop-table --routines --events --all-databases --force > mysqldb_backup.sql
```

- 关闭MySQL Server

```sh
mysqladmin -uroot -p shutdown
```

- 安装新版MySQL

-  初始化MySQL并启动

- 载入数据文件

```sh
mysql -uroot -p --force < ./mysqldb_backup.sql
```

- 运行mysql_upgrade

```sh
mysql_upgrade -uroot -p

#Upgrade process completed successfully.
#Checking if update is needed.
```

- 关闭并重启MySQL Server以确保更改生效


<br>

#### 通过MySQL Yum Repository进行升级

Upgrading MySQL with the MySQL Yum Repository

<br>

**选择一个target series**

默认情况下，MySQL Yum Repository会将MySQL升级到该release系列的最新版本。如5.7.1升级到5.7.10。

如果要升级到其他release(如5.6到5.7)，就必须要先禁用此subrepository，并选择和启用新的subrepository。

As a general rule, to upgrade from one release series to another, go to the next series rather than skipping a series.

<br>

**升级MySQL**

```sh
yum update mysql-server mysql-client
```

<br>

**重启MySQL**

MySQL Server总是在Yum更新之后重启，一旦重启，请运行`mysql_upgrade`来检查旧数据与升级软件之间的任何不兼容问题。

```sh
mysql_upgrade -uroot -p

#Upgrade process completed successfully.
#Checking if update is needed.
```

<br>

**升级Shared Client Libraries**


所以说，用yum repository安装软件是很方便的。不管是在管理还是升级等方面...


<br/>

#### 通过直接下载RPM包升级MySQL

直接下载mysql相应组件的rpm进行升级。
建议备份好配置文件。

```sh
wget http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql-community-server-5.7.20-1.el7.x86_64.rpm
wget http://repo.mysql.com/yum/mysql-5.7-community/el/7/x86_64/mysql-community-client-5.7.20-1.el7.x86_64.rpm


yum install mysql-community-server-5.7.20-1.el7.x86_64.rpm mysql-community-client-5.7.20-1.el7.x86_64.rpm
```


<br>
<br/>


### mysql降级

MySQL降级类似于MySQL升级。也包含有直接降级和逻辑降级。



<br/>
<br/>


### 重建或修复表或索引

Rebuilding or Repairing Tables or Indexes

<br>

- MySQL处理数据类型和字符集的方式的更改
- 表维修或升级(mysqlcheck, mysql_upgrade)

重建表的方法：

- Dump and Reload
- ALTER TABLE
- REPAIR TABLE

<br>

**Dump and Reload Method**

由于MySQL升级/降级之后，不同版本的MySQL无法处理这些表，则需要转储和重载的方法来重建表。

```sh
mysqldump -uroot -p --all-databases --force > mysql_backdb.sql
mysql -uroot -p --force < mysql_backdb.sql


#某个库或表
mysqldump -uroot -p --databases test --force > db_test.sql
mysql -uroot -p test < db_test.sql

mysqldump -uroot -p --databases test --tables table222 > table222.sql
mysql -uroot -p test  < table222.sql
```

<br>

**ALTER TABLE Method**

更改表以使用它已经拥有的存储引擎。

```
ALTER TABLE test ENGINE = InnoDB;
```

<br>

**REPAIR TABLE Method**

`REPAIR TABLE`仅适用于MyISAM， ARCHIVE和 csv 表。

`mysqlcheck --repair`提供了对`REPAIR TABLE`的命令行访问。

```
REPAIR TABLE t1;


mysqlcheck --repair --databases db_name ...
mysqlcheck --repair --all-databases
```


<br>
<br/>


### 复制MySQL数据库到其他机器

Copying MySQL Databases to Another Machine

<br>

在需要为不同体系架构之间传输MySQL数据库时，可使用`mysqldump`创建包含SQL语句的`.sql`文件，然后复制到另外的计算机上，将其作为输入提供给MySQL客户端。

不要忘记复制mysql数据库，因为这个存储授权表的地方。

```
mysqldump --host 'remote-host' -uxxx -p --compress --all-databases | mysql -uxxx -p

mysqldump --host 'remote-host' -uxxx -p --compress db_name | mysql -uxxx -p db_name


mysqladmin -uxxx -p flush-privileges
```




<br/>
<br/>

---

<br/>



# Tutorial


如何使用MySQL client程序来创建和使用数据库。


<br>


## 连接和断开服务器

Connecting to and Disconnecting from the Server

<br>

Like this:

- 不建议把密码直接写在命令行上
- host表示了MySQL Server运行在的机器
- 某些MySQL允许匿名用户连接
- `-ppassword, not as -p password`

```sh
mysql --host host --user username -p


#maybe not default port
mysql --host host --user username -p  --port port


#匿名用户连接
mysql


#退出
mysql> QUIT
#Unix
mysql> Ctrl+D
```


<br/>
<br/>


## 输入查询

Entering Queries

<br>

```sql
#简单查询
mysql> SELECT VERSION(), CURRENT_DATE;


#简单计算
SELECT SIN(PI()/2), (4+1)*5;


#一行中输入多个语句
SELECT VERSION(); SELECT NOW();


#多行输入一个命令
mysql> SELECT
    -> USER()
    -> ,
    -> CURRENT_DATE;
```

![MySQL简单查询](/images/MySQL/20180301101009.jpg)

<br>

这QUERY说明了有关MySQL的几件事：

- MySQL查询通常由一个`SQL statement`和`;`组成
- MySQL将查询发送给服务器并返回结果，然后打印下一个`mysql>`提示
- MySQL以表格形式(rows and columns)显示查询输出
- MySQL显示返回多少行，以及执行查询花费了多长时间
- MySQL查询不区分大小写，但建议使用大写
- MySQL支持在一行中输入多个语句
- MySQL支持一个命令多行输入

<br>

**MySQL提示符：**

Prompt | Meaning
- | -
`mysql>` | 准备新查询
`->` | 等待多行查询的下一行
`'>` | 等待下一行，等待单引号开头的字符串的完成
`">` | 等待下一行，等待双引号字开头的字符串的完成
`\`>` | 等待下一行，等待以反引号开始的标识符的完成
`/*>` | 等待下一行，等待以`/*`开头的注释的完成-->`/*comments*/`



<br>
<br/>


## 创建和使用数据库

Creating and Using a Database

<br>

大致操作：

- Create a database
- Create a table
- Load data into the table
- Retrieve data from the table in various ways
- Use multiple tables

<br>

```sql
#显示数据库
#不能显示你没有权限的数据库
mysql> SHOW DATABASES;

#mysql数据库描述用户访问权限
#test数据库通常作为用户尝试使用工作区


#访问数据库
mysql> USE test;

#USE和QUIT一样可以不使用分号，使用也无妨
#USE只能是一个单行


#授权
#GRANT ALL ON da_name.table TO 'username'@'host';
mysql> GRANT ALL ON test.* TO 'test'@'127.0.0.1';
```


<br/>
<br>


### 创建和选择数据库

Creating and Selecting a Database

<br>

**Unix是区分大小写的(case-sensitive)，这与SQL keyword不一致。请注意。**

```sql
mysql> CREATE DATABASE db01;

mysql> USE db01;

#也可在mysql连接时直接指定数据库
mysql -u username -p db01


#查看当前选择的数据库
mysql> SELECT DATABASE();
```


<br/>
<br/>


### 创建表

Creating a Table

<br>

**困难的部分是决定数据库的结构应该是什么： 你需要哪些表以及每个表中应该包含哪些列。**


`VARCHAR`对于name，owner，species来说是一个不错的选择，因为column值的长度有所不同。
`DATE`对于出生和死亡column来说很不错。
如果以后你发现你需要更长的字段，MySQL提供了一个`ALTER TABLE`语句来修改。

```sql
#创建一个宠物表
mysql> CREATE TABLE pet (name VARCHAR(20), owner VARCHAR(20),
    -> species VARCHAR(20), sex CHAR(1), birth DATE, death DATE);


mysql> SHOW TABLES;


#验证表格
#如果你忘记了表中列的名称或类型，使用DESCRIBE
mysql> DECRIBE pet;
+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| name    | varchar(20) | YES  |     | NULL    |       |
| owner   | varchar(20) | YES  |     | NULL    |       |
| species | varchar(20) | YES  |     | NULL    |       |
| sex     | char(1)     | YES  |     | NULL    |       |
| birth   | date        | YES  |     | NULL    |       |
| death   | date        | YES  |     | NULL    |       |
+---------+-------------+------+-----+---------+-------+
6 rows in set (0.00 sec)
```


<br/>
<br/>


### 将数据载入表格

Loading Data into a Table

<br>

假设pet表信息如下：

name | owner | species | sex | birth | death
- | - | - | - | -
PetA | Aa | cat | f | 1993-02-04 |
PetB | Bb | cat | m | 1994-03-17 |
PetC | Cc | dog | f | 1989-05-13 |
PetD | Aa | dog | m | 1979-08-25 | 1995-02-21
PetE | Cc | bird | | 1991-02-17 |

<br>

你可以创建一个`pet.txt`文本文件，每行包含一个记录，值由制表符分割，并按照`CREATE TABLE`语句中列出的顺序给出。

```sh
vim pet.txt


PetA    Aa     cat    f      1993-02-04    \N
PetB    Bb     cat    m      1994-03-17    \N
PetC    Cc     dog    f      1989-05-13    \N
PetD    Aa     dog    m      1979-08-25    1995-02-21
PetE    Cc     bird  \N      1991-02-17    \N
```

将`pet.txt`载入`pet`表中：

```sql
mysql> LOAD DATA LOCAL INFILE '/path/file.txt' INTO TABLE table_name;


mysql> LOAD DATA LOCAL INFILE '/home/zhang/pet.txt' INTO TABLE pet;
Query OK, 5 rows affected, 0 warnings (0.00 sec)
Records: 5  Deleted: 0  Skipped: 0  Warnings: 0


mysql> SELECT * FROM pet;
+-------+-------+---------+------+------------+------------+
| name  | owner | species | sex  | birth      | death      |
+-------+-------+---------+------+------------+------------+
| PetA  |  Aa   |  cat    | f    | 1993-02-04 | NULL       |
| PetB  |  Bb   |  cat    | m    | 1994-03-17 | NULL       |
| PetC  |  Cc   |  dog    | f    | 1989-05-13 | NULL       |
| PetD  |  Aa   |  dog    | m    | 1979-08-25 | 1995-02-21 |
| PetE  |  Cc   |  bird   | NULL | 1991-02-17 | NULL       |
+-------+-------+---------+------+------------+------------+
5 rows in set (0.00 sec)



#通过命令行载入
mysql> INSERT INTO pet
    -> VALUES ('PetF', 'Ff', 'hamster', 'f', '1999-03-21', NULL)
    -> ;
Query OK, 1 row affected (0.00 sec)
```


<br/>
<br/>


### 从表中检索信息

Retrieving Information from a Table

<br>

`SELECT`语句用于从表中提取信息：

```sql
SELECT what_to_select
FROM which_table
WHERE condition;
```


<br>

#### 查询所有数据

Selecting All Data

<br>

```sql
mysql> SELECT * FROM pet;


mysql> DELETE FROM pet;


mysql> UPDATE pet SET birth = '1989-06-17' WHERE name = 'PetC';
```


<br>

#### 查询特定行

Selecting Particular Rows

<br>

当一个表很大时，你通常不想看到整个表。

```sql
#条件查询

mysql> SELECT * FROM pet WHERE name = 'PetA';


mysql> SELECT * FROM pet WHERE owner = 'Cc';


mysql> SELECT * FROM pet WHERE birth >= '1990-01-01';


#AND
mysql> SELECT * FROM pet WHERE species = 'dog' AND sex = 'f';


#OR
mysql> SELECT * FROM pet WHERE species = 'dog' OR species = 'bird';


#AND和OR也可以混合使用
mysql> SELECT * FROM pet WHERE (species = 'cat' AND sex = 'm') OR (species = 'dog' AND sex='f');
```


<br>

#### 查询特定列

Selecting Particular Columns

<br>

```sql
mysql> SELECT name FROM pet;


mysql> SELECT name, species FROM pet;


#获取唯一结果
mysql> SELECT DISTINCT species FROM pet;
+---------+
| species |
+---------+
| cat     |
| dog     |
| bird    |
+---------+
3 rows in set (0.00 sec)


mysql> SELECT name, species, birth FROM pet WHERE species = 'dog' OR species = 'cat';
```


<br>

#### 行排序

Sorting Rows

<br>

使用`ORDER BY`语句对结果进行排序。默认排序顺序是升序。

```sql
mysql> SELECT name, birth FROM pet ORDER BY birth;
+------+------------+
| name | birth      |
+------+------------+
| PetD | 1979-08-25 |
| PetC | 1989-06-17 |
| PetE | 1991-02-17 |
| PetA | 1993-02-04 |
| PetB | 1994-03-17 |
+------+------------+
5 rows in set (0.00 sec)


#倒序
mysql> SELECT name, birth FROM pet ORDER BY birth DESC;
```

可对多列进行排序，也可按不同的方向对不同的列进行排序。

```sql
mysql> SELECT name, species, birth FROM pet
    -> ORDER BY species, birth DESC;
+------+---------+------------+
| name | species | birth      |
+------+---------+------------+
| PetE | bird    | 1991-02-17 |
| PetB | cat     | 1994-03-17 |
| PetA | cat     | 1993-02-04 |
| PetC | dog     | 1989-06-17 |
| PetD | dog     | 1979-08-25 |
+------+---------+------------+
5 rows in set (0.00 sec)


mysql> SELECT name, species, birth FROM pet
    -> ORDER BY species DESC, birth DESC
```


<br>

#### 日期计算

Date Calculations

<br>

MySQL提供了几个函数用于日期计算。如计算年龄或提取日期一部分等。

<br>

- `TIMESTAMPDIFF()`
	+ 使用`TIMESTAMPDIFF()`函数计算pet的年龄。它的两个参数为两个相隔的日期

```sql
mysql> SELECT name, species, birth, CURDATE(),
    -> TIMESTAMPDIFF(YEAR, birth, CURDATE()) AS age
    -> FROM pet
    -> ORDER BY age DESC;
+------+---------+------------+------------+------+
| name | species | birth      | CURDATE()  | age  |
+------+---------+------------+------------+------+
| PetD | dog     | 1979-08-25 | 2018-03-01 |   38 |
| PetC | dog     | 1989-06-17 | 2018-03-01 |   28 |
| PetE | bird    | 1991-02-17 | 2018-03-01 |   27 |
| PetA | cat     | 1993-02-04 | 2018-03-01 |   25 |
| PetB | cat     | 1994-03-17 | 2018-03-01 |   23 |
+------+---------+------------+------------+------+
5 rows in set (0.00 sec)


#死去的pet的age
mysql> SELECT name, species, birth, death,
    -> TIMESTAMPDIFF(YEAR, birth, death) AS age
    -> FROM pet
    -> WHERE death IS NOT NULL
    -> ORDER BY age;
+------+---------+------------+------------+------+
| name | species | birth      | death      | age  |
+------+---------+------------+------------+------+
| PetD | dog     | 1979-08-25 | 1995-02-21 |   15 |
+------+---------+------------+------------+------+
1 row in set (0.00 sec)
```

<br>

- `YEAR()`
	+ 年
- `MONTH()`
	+ 月
- `DAYOFMONTH()`
	+ 日


```sql
mysql> SELECT name, birth,
    -> YEAR(birth) AS bir_year,
    -> MONTH(birth) AS bir_month,
    -> DAYOFMONTH(birth) AS bir_day
    -> FROM pet;
+------+------------+----------+-----------+---------+
| name | birth      | bir_year | bir_month | bir_day |
+------+------------+----------+-----------+---------+
| PetA | 1993-02-04 |     1993 |         2 |       4 |
| PetB | 1994-03-17 |     1994 |         3 |      17 |
| PetC | 1989-06-17 |     1989 |         6 |      17 |
| PetD | 1979-08-25 |     1979 |         8 |      25 |
| PetE | 1991-02-17 |     1991 |         2 |      17 |
+------+------------+----------+-----------+---------+
5 rows in set (0.00 sec)



#查找生日是2月的pet
mysql> SELECT name, birth FROM pet WHERE MONTH(birth) =2;
+------+------------+
| name | birth      |
+------+------------+
| PetA | 1993-02-04 |
| PetE | 1991-02-17 |
+------+------------+
```

<br>

- `DATE_ADD()`
	+ 将日期间隔添加到给定日期

```sql
mysql> SELECT name, birth FROM pet
    -> WHERE MONTH(birth) = MONTH(DATE_ADD(CURDATE(), INTERVAL 1 MONTH));
```

<br>

#### 使用NULL值

Working with NULL Values

<br>

从概念上讲，NULL value意味着**一个缺失的未知值**，它与其它值在某种程度上是不同的。

- 使用`IS NULL`和`IS NOT NULL`操作符
- 不能对NULL value使用算术运算符(arithmetic cpmparison operators)
	+ 如：`=`, `<`, `>`, `<>`
	+ 任何对NULL value的算术运算符的结果也是NULL value，所以无法得到有意义的结果
- 在MySQL中，0或NULL表示false，其他任何值都意味着true
- 两个NULL在`GROUP BY`中被认为是相等的
- NULL在`ORDER BY`正向排序中首先显示。反之，最后显示


```sql
mysql> SELECT 1 IS NULL, 1 IS NOT NULL;
+-----------+---------------+
| 1 IS NULL | 1 IS NOT NULL |
+-----------+---------------+
|         0 |             1 |
+-----------+---------------+
```

因此，完全可以将一个**zero**或**empty string**插入到一个**NOT NULL**的column中，因为这些值NOT NULL。


<br>

#### 模式匹配

Pattern Matching

<br>

MySQL提供标准的SQL模式匹配以及基于扩展正则表达式的模式匹配形式。类似于Unix实用程序(vi, grep, sed...)

SQL模式匹配允许:

- 使用`_`来匹配可以使用的任意单字符(single character)
- 使用`%`来匹配可以使用的任意数目的字符(arbitrary number of characters)
- SQL模式不区分大小写
- 使用`LIKE`或`NOT LIKE`而不是`=`或`<>`

```sql
mysql> SELECT * FROM pet WHERE name LIKE '%b';
+------+-------+---------+------+------------+-------+
| name | owner | species | sex  | birth      | death |
+------+-------+---------+------+------------+-------+
| PetB | Bb    | cat     | m    | 1994-03-17 | NULL  |
+------+-------+---------+------+------------+-------+



mysql> SELECT * FROM pet WHERE name LIkE '___A' or name LIKE '___C';
+------+-------+---------+------+------------+-------+
| name | owner | species | sex  | birth      | death |
+------+-------+---------+------+------------+-------+
| PetA | Aa    | cat     | f    | 1993-02-04 | NULL  |
| PetC | Cc    | dog     | f    | 1989-06-17 | NULL  |
+------+-------+---------+------+------------+-------+
```

<br>

MySQL提供的其它类型的模式匹配使用扩展的正则表达式：

- `REGEXP` 或 `RLIKE`
- `NOT REGEXP` 或 `NOT RLIKE`
- 了解正则表达式知识

```sql
mysql> SELECT * FROM pet WHERE name RLIKE '^pet[AB]';
+------+-------+---------+------+------------+-------+
| name | owner | species | sex  | birth      | death |
+------+-------+---------+------+------------+-------+
| PetA | Aa    | cat     | f    | 1993-02-04 | NULL  |
| PetB | Bb    | cat     | m    | 1994-03-17 | NULL  |
+------+-------+---------+------+------------+-------+



mysql> SELECT * FROM pet WHERE owner RLIKE 'c$';
+------+-------+---------+------+------------+-------+
| name | owner | species | sex  | birth      | death |
+------+-------+---------+------+------------+-------+
| PetC | Cc    | dog     | f    | 1989-06-17 | NULL  |
| PetE | Cc    | bird    | NULL | 1991-02-17 | NULL  |
+------+-------+---------+------+------------+-------+



#包含某个字符
mysql> SELECT * FROM pet WHERE name RLIKE 'ete';
+------+-------+---------+------+------------+-------+
| name | owner | species | sex  | birth      | death |
+------+-------+---------+------+------------+-------+
| PetE | Cc    | bird    | NULL | 1991-02-17 | NULL  |
+------+-------+---------+------+------------+-------+



#匹配字符个数
mysql> SELECT * FROM pet WHERE name RLIKE '^....$';

mysql> SELECT * FROM pet WHERE name RLIKE '^.{4}$';



#强制区分大小写
mysql> SELECT * FROM pet WHERE name RLIKE BINARY '^Pet[AB]';
```

<br/>

#### 行数计算

Counting Rows

<br>

- 使用`COUNT()`计算行数

```sql
#总行数
mysql> SELECT COUNT(*) AS count FROM pet;
+-------+
| count |
+-------+
|     5 |
+-------+




#针对某个统计行数
mysql> SELECT owner, COUNT(*) FROM pet GROUP BY owner;
+-------+----------+
| owner | COUNT(*) |
+-------+----------+
| Aa    |        2 |
| Bb    |        1 |
| Cc    |        2 |
+-------+----------+



#多个条件
mysql> SELECT species, sex, COUNT(*) FROM pet GROUP BY species, sex;
+---------+------+----------+
| species | sex  | COUNT(*) |
+---------+------+----------+
| bird    | NULL |        1 |
| cat     | f    |        1 |
| cat     | m    |        1 |
| dog     | f    |        1 |
| dog     | m    |        1 |
+---------+------+----------+
```


<br/>

#### 使用多个表

Using More Than one Table

<br/>

创建一个额外的宠物信息表：

name | date | type | remark
- | - | - | -
Fluffy | 1995-05-15 | litter | 4 kittens, 3 female, 1 male
Buffy | 1993-06-23 | litter | 5 puppies, 2 female, 3 male
Buffy | 1994-06-19 | litter | 3 puppies, 3 female
Chirpy | 1999-03-21 | vet | needed beak straightened
Slim | 1997-08-03 | vet | broken rib
Bowser | 1991-10-12 | kennel |
Fang | 1991-10-12 | kennel |
Fang | 1998-08-28 | birthday | Gave him a new chew toy
Claws | 1998-03-17 | birthday | Gave him a new flea collar
Whistler | 1998-12-09 | birthday | First birthday



```sql
mysql> CREATE TABLE event ( name VARCHAR(20), date DATE,
    -> type VARCHAR(15), remark VARCHAR(255) );


mysql> LOAD DATA INFILE '/path/event.txt' INTO TABLE event;
```


<br/>
<br/>


## 获取数据库和表的信息

Getting Information About Databases and Tables

<br>

- 查看当前数据库
	+ `mysql> SELECT DATABASE();`
- 查看当前数据库下的表
	+ `mysql> SHOW TABLES;`
- 查看表的结构
	+ `mysql> DESCRIBE pet;`
- 创建数据库
	+ `mysql> CREATE DATABASE db_01;`
- 创建表
	+ `mysql> CREATE TABLE table_01 {c1 VARCHAR(10), c2 INT, ...};`
- 查看索引(如果存在)
	+ `SHOW INDEX FROM table_01;`



<br/>
<br/>


## 在批处理下使用mysql

Using mysql in Batch Mode

<br>

在前面，我们都是使用MySQL交互式(interactively)输入命令并查看结果。但还可在批处理模式下运行MySQL。
我们可以创建一个脚本文件，然后以这种方式执行脚本文件。

```sh
mysql < batch-file

msyql -h host -u user -p < /path/batch-file


#出现错误也继续运行
msyql -h host -u user -p --force < /path/batch-file
```

<br>

为什么要使用脚本：

- 如果需要反复(repeat)执行查询，将其写入脚本以避免每次执行时重新输入查询
- 通过复制和修改脚本文件从现有查询中生成新的查询
- 批处理模型在开发查询时也很有用，特别是对于多行语句。写错了直接修改脚本就好，而不必重新输入
- 如果查询产生大量输出，可通过传呼机而不是翻滚到屏幕的最上方
	+ `mysql < batch-file | more`
- 可以把输出捕获到一个文件中
	+ `mysql < batch-file > mysql.out`
- 可将脚本文件分发给其他人
- 批处理模式下的MySQL输出更简洁
	+ 可使用`mysql -t`获得交互式数据格式
	+ 使用`mysql -v`将执行语句回显
- 在mysql命令行中载入脚本
	+ `mysql> source filename;`
	+ 或'mysql> \. filename;


<br>
<br/>


## 常见查询

Examples of Common Queries

<br/>

- 在命令行使用mysql并选择数据库

```sh
mysql db_name -u user -p
```

- 创建和填充表

```sql
CREATE TABLE shop (
    article INT(4) UNSIGNED ZEROFILL DEFAULT '0000' NOT NULL,
    dealer  CHAR(20)                 DEFAULT ''     NOT NULL,
    price   DOUBLE(16,2)             DEFAULT '0.00' NOT NULL,
    PRIMARY KEY(article, dealer));
INSERT INTO shop VALUES
    (1,'A',3.45),(1,'B',3.99),(2,'A',10.99),(3,'B',1.45),
    (3,'C',1.69),(3,'D',1.25),(4,'D',19.95);
```

- 查看表内容

```sql
SELECT * FROM shop;
```

- 列的最大值(maximum)

```sql
SELECT MAX(article) AS article FROM shop;



SELECT article, MAX(price) AS price
FROM   shop
GROUP BY article;
```

- 使用用户定义的变量(user-defined variables)

```sql
mysql> SELECT @min_price:=MIN(price),@max_price:=MAX(price) FROM shop;

mysql> SELECT * FROM shop WHERE price=@min_price OR price=@max_price;
```

- 使用外键(Foreign Keys)

在MySQL中，InnoDB表支持检查外键约束。
外键约束不仅仅需要连接两个表。

```sql
CREATE TABLE person (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name CHAR(60) NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE shirt (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    style ENUM('t-shirt', 'polo', 'dress') NOT NULL,
    color ENUM('red', 'blue', 'orange', 'white', 'black') NOT NULL,
    owner SMALLINT UNSIGNED NOT NULL REFERENCES person(id),
    PRIMARY KEY (id)
);


INSERT INTO person VALUES (NULL, 'Antonio Paz');


SELECT @last := LAST_INSERT_ID();


INSERT INTO shirt VALUES
(NULL, 'polo', 'blue', @last),
(NULL, 'dress', 'white', @last),
(NULL, 't-shirt', 'blue', @last);


INSERT INTO person VALUES (NULL, 'Lilliana Angelovska');


SELECT @last := LAST_INSERT_ID();


INSERT INTO shirt VALUES
(NULL, 'dress', 'orange', @last),
(NULL, 'polo', 'red', @last),
(NULL, 'dress', 'blue', @last),
(NULL, 't-shirt', 'white', @last);
```

- 在两个键上查找(Searching on Two Keys)

```sql
SELECT field1_index, field2_index FROM test_table
WHERE field1_index = '1' OR  field2_index = '1'
```

- 使用自动增量

`AUTO_INCREMENT`属性能够为新行生成一个唯一的标识符。

```sql
CREATE TABLE animals (
     id MEDIUMINT NOT NULL AUTO_INCREMENT,
     name CHAR(30) NOT NULL,
     PRIMARY KEY (id)
);


INSERT INTO animals (name) VALUES
    ('dog'),('cat'),('penguin'),
    ('lax'),('whale'),('ostrich');



#设置指定增量开始值
mysql> ALTER TABLE tbl AUTO_INCREMENT = 100;
```



<br>
<br/>

---

<br/>


# MySQL程序


<br>


## MySQL程序概述

Overview of MySQL Programs

<br>

**MySQL安装中有多个不同的程序：**

- **mysqld**
SQL daemon, MySQL Server, **mysqld**是执行大部分工作的主要程序

- **mysqld_safe**
服务器启动脚本
`mysqld_safe`尝试去启动`mysqld`

- **mysql.server**
服务器启动脚本
此脚本用于`System V`系统，包含启动特定运行级别的系统服务脚本
它调用`mysqld_safe`来启动MySQL Server

- **mysql_multi**
可启动和关闭安装在系统上的多个服务器的启动脚本

- **comp_err**
在MySQL build/installation过程中使用
从错误源文件中编译错误消息文件

- **mysql_install_db**
初始化MySQL(数据目录，授权表，并设置InnoDB系统表空间)
通常用于首次安装MySQL时

- **mysql_plugin**
配置MySQL Server插件

- **mysql_secure_installation**
能够提高MySQL安装的安全性

- **mysql_ssl_rsa_setup**
如果这些文件丢失，该程序会创建支持安全连接所需的SSL证书和密钥文件以及RSA密钥对文件

- **mysql_tzinfo_to_sql**
从mysql数据库中加载时区表

- **mysql_upgrade**
在MySQL升级操作后使用
它检查表的不兼容性并在必要时修复它们，并用更新版的MySQL的任何更改来更新授权表

- **mysql**
交互式输入SQL语句的命令行工具
或执行一个批处理模式的文件

- **mysqladmin**
执行管理操作的客户端
如创建或删除数据库，重新加载授权表，刷新表的磁盘...
也可用获取服务器版本、状态、进程信息

- **mysqlcheck**
表格客户端
用于检查、修复、分析和优化表格

- **mysqldump**
将MySQL数据库转储为SQL、文本或XML文件的客户端

- **mysqlimport**
使用`LOAD DATA INFILE`将文本文件导入各自表格的客户端

- **mysqlpump**
将MySQL数据库转转储为SQL文件的客户端

- **mysqlsh**
用于MySQL Server的高级命令行客户端和代码编辑器
除了SQL外，MySQL Shell还为JS和Python提供了脚本功能

- **mysqlshow**
显示有关数据库、表、列和索引的信息的客户端

- **mysqlslap**
用于模拟MySQL Server的客户端负载并报告每个阶段的时间

<br>

**MySQL管理和实用程序：**

- **innochecksum**
InnoDB脱机文件校验和程序

- **myisam_ftdump**
在MyISAM表中显示有关全文索信息

- **myisamchk**
描述，检查，优化和修复MyISAM表

- **myisamlog**
处理MyISAM日志文件

- **myisampack**
压缩MyISAM表以生成更小的只读表

- **mysql_config_editor**
能够将认证凭证存储在名为安全的加密登录路径文件中

- **mysqlbinlog**
从二进制日志中读取语句

- **mysqldumpslow**
读取和总结慢查询日志内容

<br>

**MySQL程序开发实用程序：**

- **mysql_config**
一个shell脚本，用于在编译MySQL程序是生产所需的选项值

- **my_print_defaults：**
显示选项文件的选项组中存在哪些选项

- **resolve_stack_dump**
将数值堆栈跟踪转储解析为符号

<br>

**杂项(Miscellaneous)工具：**

- **lz4_decompress**
解压缩使用LZ4压缩格式的mysqldump输出

- **perror**
显示系统或MySQL错误代码含义

- **replace**
再输入文本中执行字符串替换

- **resolveip**
将主机名解析为IP地址，反之亦然

- **zlib_decompress**
解压缩使用ZLIB压缩格式的mysqldump输出

<br>

Oracle公司还提供了MySQL Workbench GUI工具，用于管理、创建、知悉和评估查询，以及从其它关系数据库管理系统迁移到MySQL系统。

MySQL Client和Server间的通信使用如下环境变量：

| Environment Variable | Meaning |
| - | - |
| MYSQL_UNIX_PORT | The default Unix socket file; used for connections to localhost |
| MYSQL_TCP_PORT | The default port number; used for TCP/IP connections |
| MYSQL_PWD | The default password, insecure |
| MYSQL_DEBUG | Debug trace options when debugging |
| TMPDIR | The directory where temporary tables and files are created |



<br/>
<br/>



## 使用MySQL程序


### 调用MySQL程序

从命令行调用一个MySQL程序，输入程序名称和选项及参数。

```sh
$ mysql --user=root test
$ mysqladmin extended-status variables
$ mysqlshow --help
$ mysqldump -u root personnel

```


<br/>
<br/>


### 连接到MySQL Server


介绍如何连接到MySQL Server。

MySQL程序环境变量的优先级最低，命令行选项最高。你可在配置文件中指定程序的默认值，同时你又可以使用命令行选项覆盖它。
MySQL选项按顺序处理，所以如果多次指定选型，则最后一个选项优先。

```sh
mysql --hostname xx --port xx --user xx --password ${dbname} --protocol=TCP

mysql -h -P -u -p ${dbname}

```

`--protocol`值：

- TCP(all)
- SOCKET(Unix)
- PIPE(windows)
- MEMORY(windows)

<br>

你可以在选项文件的`[client]`部分指定连接参数:

```
[client]
host=xxx
port=xxx
user=xxx
password=xxx
```

<br>

```
mysqladmin -u user -p --count=1k --sleep=10 ping

mysql -u user -pxxx --execute="DESCRIBE db.table"


#执行多个语句
mysql -u root -p -e 'SELECT VERSION(); SELECT NOW()'


```


<br/>
<br/>


### 配置文件


大多数MySQL程序都可从选项文件中读取启动选项。

MySQL不保证配置文件的读取顺序。

Unix和Unix-Like平台的MySQL配置文件：

| 文件 | 描述
| - | -
| `/etc/my.cnf` | 全局选项
| `/etc/mysql/my.cnf` | 全局选项
| `$SYSCONFDIR/my.cnf` | 全局选项
| `$MYSQL_HOME/my.cnf` | MySQL Server Only
| `~/.my.cnf` | 特定用户选项
| `~/.mylogin.cnf` | 特定用户登录选项，Client Only
| `default-extra-file` | 使用`--defaults-extra-file`指定的文件

<br>

配置文件解释：

- 空行被忽略
- `#`号表示注释
- 前后空格将自动从选项名称和值中删除
- `[group]`
为其设置配置项的程序名或组名。在此之后，任何选项设置都会应用到指定组，知道给出结尾。选项组名称不区分大小写。

- 你可在选项值中使用转义序列
`\b, \t, \n, \r, \\, \s`

- `!include`来包含其它配置文件




```
DATADIR
mysqld --datadir


[mysqld]
port=3306
socket=/tmp/mysql.sock
key_buffer_size=16M
max_allowed_packet=8M

[mysql]
port=3306
socket=/tmp/mysql.sock
no-auto-rehash


[mysqldump]
quick


!include /home/mysql/myopt.cnf
```

<br>

**影响配置文件的命令行选项**

- `--print-defaults`
- `--defaults-extra-file`
- `--defaults-file`
- `--defaults-group-suffix`
- `--login-path`
- `--no-defaults`

<br>

**使用选项指定环境变量**

```
[mysql]
max_allowed_packet=16M

[mysqld]
key_buffer_size=512M


mysql --max_allowed_packet=16M

shell> mysql --max_allowed_packet=16*1024*1024
mysql> SET GLOBAL max_allowed_packet=16*1024*1024;
```



<br/>
<br/>


## MySQL Server


- `mysqld`
The MySQL Server

- `mysql_safe`
MySQL Server Startup Script

- `mysql.server`
MySQL Server Startup Script

- `mysqld_multi`
Manage Multiple MySQL Servers


<br/>


### mysqld

mysqld，也被称为MySQL服务器，是执行MySQL大部分工作的主要程序。MySQL服务器管理对包含数据库和表的MySQL数据目录的访问。

查看帮助： `mysqld --verbose --help`


<br/>


### mysql_safe


**对于某些Linux平台，从RPM或DBP包安装的MySQL包括了用于管理MySQL服务启动和管理的systemd支持。在这些平台上，`mysqld_safe`不会被安装，因为它不是必须的。**

`mysql_safe`是Unix上启动mysqld服务器的推荐方式。它添加了一些安全特性，如发生错误是重启服务器并将运行时的错误记录到日志。

`mysqld_safe`尝试启动一个名为mysqld的可执行程序。它会读取配置文件中`[mysqld], [server], [mysqld_safe]`部分的所有选项。


`mysqld_safe`选项：

```
--basedir

--core-file-size

--datadir

--defaults-extra-file

--defaults-file

--ledir

--log-error

--mallocl-lib

--mysqld

--mysqld-safe-login-timestamps

--mysql-version

--nice

--no-defaults

--open-files-limit

--pid-file

--plugin-dir

--plugin-dir

--port

--skip-kill-mysqld

--skip-syslog

--socket

--syslog-tag

--timezone

--user
```


<br/>
<br/>


### mysql.server


**对于某些Linux平台，从RPM和DPG包安装的MySQL包括了用于管理MySQL Server启动和关闭的systemd支持。在这些平台上，没有安装`mysql.server`和`mysqld_safe`，因为它们不是必须的。**

Unix和Unix-Like平台上的MySQL发行版包含一个名为`mysql.server`的脚本，该脚本使用`mysqld_safe`启动MySQL Server。


<br/>
<br/>


### mysqld_multi


**对于某些Linux平台，从RPM和DPG包安装的MySQL包括了用于管理MySQL Server启动和关闭的systemd支持。在这些平台上，没有安装`mysqld_multi`，因为它们不是必须的。**

`mysqld_multi`设计用于管理多个监听不同Unix socket文件和TCP/IP port上连接的mysqld进程。



<br/>
<br/>


## MySQL安装相关程序


这些程序用于安装或升级MySQL！

- `com_err`
Compile MySQL Error Message File

- `mysql_install_db`
Initialize MySQL Data Directory

- `mysql_plugin`
Configure MySQL Server Plugins

- `mysql_secure_installation`
Improve MySQL Installation Security

- `mysql_ssl_rsa_setup`
Create SSL/RSA Files

- `mysql_tzinfo_to_sql`
Load the Time Zone Tables

- `mysql_upgrade`
Check and Upgrade MySQL Tables


<br/>


### com_err

`comp_err`创建errmsg.sys文件，`mysqld`使用此文件来确定为不同错误代码(error code)显示错误消息。通常，在构建MySQL时，`comp_err`会自动运行。它从位于MySQL源发行版`sq;/share/errmsg-utf8.txt`文本文件汇编`errmsg.sys`文件。

`comp_err`同样会生成`mysqld_error.h, mysqld_ername.h, sql_state.h`头文件。


<br/>
<br/>


### mysql_install_db

在MySQL5.7中，由于`mysql_install_db`的功能已经被集成到mysqld中，因此不推荐使用它。
在MySQL5.7.5之前，`mysql_install_db`是一个Perl脚本并依赖于Perl。在此之后，它是由C++写的可执行二进制文件。还有一些选项的更迭。

```
mysqld --initailize

#or
mysqld --initialize-insecure
```

<br>

`mysql_install_db`处理在MySQL Server(mysqld)准备好使用之前，必须执行的初始化任务：

- 初始化MySQL数据目录，创建它包含的系统表
- 初始化管理InnoDB表所需的`system tablespace`和相关数据结构
- 加载服务器端help表
- 安装`sys schema`
- 创建一个管理员账户
老版本的`mysql_install_db`可能会创建匿名账户。

<br>

如果`mysql_install_db`生成了一个随机管理员密码，它将把此密码写入文件并显示此文件名。密码包含一个时间戳以指示它的写入时间。
默认情况下，该文件是用户主目录中的`.mysql_secret`文件。


<br/>
<br/>


### mysql_plugin

从MySQL5.7.11开始，不推荐使用`mysql_plugin`，并会在MySQL8.0中移除此功能。
使用如下命令替代：

```
--plugin-load
--plugin-load-add

#或
mysql> INSTALL PLUGIN
mysql> UNINSTALL PLUGIN
```

<br>

`mysql_plugin`功能允许MySQL管理员管理由MySQL Server载入的插件。


<br/>
<br/>


### mysql_secure_installation

`mysql_secure_installation`通过以下方式来提高MySQL安装的安全性：

- 为root用户设置密码
- 删除可从本机外部访问的root账户
- 删除匿名账户
- 删除test数据库(默认情况下可由任何用户访问，包括匿名用户)
- 删除允许任何人访问以`test_`开头的数据库的权限


<br/>
<br/>


### mysql_ssl_rsa_setup

`mysql_ssl_rsa_setup`创建SSL证书和key文件和RSA key-pair文件，用于支持使用SSL进行安全连接。它生成的整数是自签名的，不太安全。请考虑从注册机构申请CA证书。
`mysql_ssl_rsa_setup`使用`opensll`命令，所以请安装OpenSSL。


<br/>
<br/>


### mysql_tzinfo_to_sql

`mysql_tzinfo_to_sql`加载MySQL数据库中的zone table。它使用系统上的`zoneinfo`信息。


<br/>
<br/>


### msyql_upgrade

`mysql_upgrade`检查数据库中的所有表与当前版本的MySQL Server的不兼容，它还升级系统表，以便你可以利用新权限和功能。
如果`mysql_upgrade`发现表有可能的不兼容性，它会执行检查表，如果发现问题，则会尝试修复表。

每次升级MySQL时都应该执行`mysql_upgrade`。
在执行upgrade之前，你应该始终备份你的MySQL。



<br/>
<br/>


## MySQL客户端程序


- mysql
The MySQL Command-Line Tool

- mysqladmin
Client for Administering a MySQL Server

- mysqlcheck
A Table Maintenance Program

- mysqldump
A Database Backup Program

- mysqlimport
A Data Import Program

- mysqlpump
A Database Backup Program

- mysqlsh
The MySQL Shell

- mysqlshow
Display Database, Table, and Column Information

- mysqlslap
Load Emulation Client


<br/>


## mysql

mysql是一个具有输入编辑功能的SQL shell。

```sql
mysql --host= --port= --user= --password db_name


#SQL文件
#SQL语句以 ;或\g或\G结束
mysql db_name < script.sql > output.tab
```


<br/>


### mysql选项

MySQL支持很多选项。这些选项可以写入配置文件的`[mysql]`和`[client]`组中。

```
mysql --help
```


<br/>
<br/>


### mysql命令

mysql将你发出的每个SQL语句发送到要执行的Server。如下为mysql自己解释的命令：

```
mysql> help;

List of all MySQL commands:
Note that all text commands must be first on line and end with ';'
?         (\?) Synonym for `help'.
charset
clear     (\c) Clear the current input statement.
connect   (\r) Reconnect to the server. Optional arguments are db and host.
delimiter (\d) Set statement delimiter.
edit      (\e) Edit command with $EDITOR.
ego       (\G) Send command to mysql server, display result vertically.
exit      (\q) Exit mysql. Same as quit.
go        (\g) Send command to mysql server.
help      (\h) Display this help.
nopager   (\n) Disable pager, print to stdout.
notee     (\t) Don't write into outfile.
pager     (\P) Set PAGER [to_pager]. Print the query results via PAGER.
print     (\p) Print current command.
prompt    (\R) Change your mysql prompt.
quit      (\q) Quit mysql.
rehash    (\#) Rebuild completion hash.
source    (\.) Execute an SQL script file. Takes a file name as an argument.
status    (\s) Get status information from the server.
system    (\!) Execute a system shell command.
tee       (\T) Set outfile [to_outfile]. Append everything into given outfile.
use       (\u) Use another database. Takes database name as argument.
charset   (\C) Switch to another charset. Might be needed for processing binlog with multi-byte charsets.
warnings  (\W) Show warnings after every statement.
nowarning (\w) Don't show warnings after every statement.
resetconnection(\x) Clean session context.
```

<br>

**修改MySQL提示符**

```
#shell
export MYSQL_PS1="(\u@\h) [\d]> "


#mysql
mysql --prompt="(\u@\h) [\d]> "


#配置文件
[mysql]
prompt=(\\u@\\h) [\\d]>\\_


#mysql prompt
mysql> prompt (\u@\h) [\d]>\_
```


<br/>
<br/>


### mysql服务端帮助

mysql Server-Side Help

如果给`help`命令提供一个参数，mysql将其用作搜索字符串，以从MySQL参考手册的内容访问服务端帮助。

```
mysql> help me


mysql> help contents


mysql> help logs


mysql> help rep%
```


<br/>
<br/>


### 从文本文件执行SQL语句

mysql忽略文件开头的Unicode字节顺序标记(BOM)字符。BOM的存在不会导致MySQL更改其默认字符集(charset)。因此，请使用`--default-char-set`选项。

```
#shell
mysql db_name < test_file


mysql> source file_name
mysql> \. file_name


#显示进度信息
SELECT '<info_to_display>' AS ' ';
```


<br/>
<br/>


## MySQL管理和实用程序

- inochecksum
Offline InnoDB File Checksum Utility

- myisam_ftdump
Display Full-Text Index information

- myisamchk
MyISAM Table-Maintenance Utility

- myisamlog
Display MyISAM Log File Contents

- myisampack
Generate Compressed, Read-Only MyISAM Tables

- mysql_config_editor
MySQL Configuration Utility

- mysqlbinlog
Utility for Processing Binary Log Files

- mysqldumpslow
Summarize Slow Query Log Files



<br/>
<br/>


## mysql开发实用程序


- `mysql_config`
Display Options for Compiling Clients

- `my_print_defaults`
Display Options from Option Files

- `resolve_stack_dump`
Resolve Numeric Stack Trace Dump to Symbols



<br/>
<br/>



## 杂项程序

Miscellaneous Programs

- `lz4_decompress`
Decompress mysqlpump LZ4-Compressed Output

- `perror`
 Explain Error Codes

- `replace`
A String-Replacement Utility

- `resolveip`
Resolve Host name to IP Address or Vice Versa

- `zlib_decompress`
Decompress mysqlpump ZLIB-Compressed Output



<br/>
<br/>



## MySQL环境变量


这些环境变量直接或间接的被MySQL使用。

| Variable |  Description
| - | -
| AUTHENTICATION_LDAP_CLIENT_LOG |  Client-side LDAP authentication logging level.
| AUTHENTICATION_PAM_LOG |  PAM authentication plugin debug logging settings.
| CC |  The name of your C compiler (for running CMake).
| CXX |  The name of your C++ compiler (for running CMake).
| CC |  The name of your C compiler (for running CMake).
| DBI_USER |  The default user name for Perl DBI.
| DBI_TRACE |  Trace options for Perl DBI.
| HOME |  The default path for the mysql history file is $HOME/.mysql_history.
| LD_RUN_PATH |  Used to specify the location of libmysqlclient.so.
| LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN |  Enable mysql_clear_password authentication plugin; see Section 6.5.1.6, “Client-Side Cleartext Pluggable Authentication”.
| LIBMYSQL_PLUGIN_DIR |  Directory in which to look for client plugins.
| LIBMYSQL_PLUGINS |  Client plugins to preload.
| MYSQL_DEBUG |  Debug trace options when debugging.
| MYSQL_GROUP_SUFFIX |  Option group suffix value (like specifying --defaults-group-suffix).
| MYSQL_HISTFILE |  The path to the mysql history file. If this variable is set, its value overrides the default for $HOME/.mysql_history.
| MYSQL_HISTIGNORE |  Patterns specifying statements that mysql should not log to $HOME/.mysql_history, or syslog if --syslog is given.
| MYSQL_HOME |  The path to the directory in which the server-specific my.cnf file resides.
| MYSQL_HOST |  The default host name used by the mysql command-line client.
| MYSQL_OPENSSL_UDF_DH_BITS_THRESHOLD |  Maximum key length for CREATE_DH_PARAMETERS(). See Section 12.18.2, “Enterprise Encryption Usage and Examples”.
| MYSQL_OPENSSL_UDF_DSA_BITS_THRESHOLD |  Maximum DSA key length for CREATE_ASYMMETRIC_PRIV_KEY(). See Section 12.18.2, “Enterprise Encryption Usage and Examples”.
| MYSQL_OPENSSL_UDF_RSA_BITS_THRESHOLD |  Maximum RSA key length for CREATE_ASYMMETRIC_PRIV_KEY(). See Section 12.18.2, “Enterprise Encryption Usage and Examples”.
| MYSQL_PS1 |  The command prompt to use in the mysql command-line client.
| MYSQL_PWD |  The default password when connecting to mysqld. Using this is insecure. See Section 6.1.2.1, “End-User Guidelines for Password Security”.
| MYSQL_TCP_PORT |  The default TCP/IP port number.
| MYSQL_TEST_LOGIN_FILE |  The name of the .mylogin.cnf login path file.
| MYSQL_TEST_TRACE_CRASH |  Whether the test protocol trace plugin crashes clients. See note following table.
| MYSQL_TEST_TRACE_DEBUG |  Whether the test protocol trace plugin produces output. See note following table.
| MYSQL_UNIX_PORT |  The default Unix socket file name; used for connections to localhost.
| MYSQLX_TCP_PORT |  The X Plugin default TCP/IP port number.
| MYSQLX_UNIX_PORT |  The X Plugin default Unix socket file name; used for connections to localhost.
| PATH |  Used by the shell to find MySQL programs.
| PKG_CONFIG_PATH |  Location of mysqlclient.pc pkg-config file. See note following table.
| TMPDIR |  The directory in which temporary files are created.
| TZ |  This should be set to your local time zone. See Section B.5.3.7, “Time Zone Problems”.
| UMASK |  The user-file creation mode when creating files. See note following table.
| UMASK_DIR |  The user-directory creation mode when creating directories. See note following table.
| USER |  The default user name on Windows when connecting to mysqld.




<br/>
<br/>

---

<br/>



# MySQL Server管理


## MySQL Server

mysqld is the MySQL Server.
并非所有的MySQL Server二进制文件和配置都支持所有的存储引擎。

```
#查看帮助
mysqld --verbose --help


#运行Server的环境变量
mysql> SHOW VARIABLES;


#运行Server的状态
mysql> SHOW STATUS;

```


<br/>
<br/>


## MySQL数据目录


由MySQL管理的信息存储在称为数据目录的目录下。

- 数据目录子目录：每个子目录都是数据库目录对应于Server管理的数据库
	+ mysql
	+ performance_schema
	+ sys
	+ 数据库
- 日志文件由Server写入
- innoDB表空间和日志文件
- 自动生成的SSL/RSA证书和密钥文件
- Server PID



<br/>
<br/>



## mysql数据库

The mysql System Database

The mysql database is the system database.它的表中存储了MySQL Server运行时需要的信息。

<br>

**授权系统表**
如下这些系统表包含了用户账户和权限的授权信息。

- user
User accounts, global privileges, and other non-privilege columns.

- db
 Database-level privileges.

- tables_priv
Table-level privileges.

- columns_priv
Column-level privileges.

- procs_priv
Stored procedure and function privileges.

- proxies_priv
Proxy-user privileges.

<br>

**对象信息系统表**
如下这些系统表包含了存储程序，用户定义函数和服务器端插件的信息。

- event
关于Event Scheduler事件的信息

- func
用户定义函数的信息

- plugin
服务器端的插件的信息

- proc
有关存储过程和函数的信息

<br>

**日志系统表**
Server使用如下系统表记录日志。日志表使用CSV存储引擎。

- general_log
一般查询日志表

- slow_log
慢查询日志表

<br>

**服务器端帮助系统表**
如下系统表包含了服务器端帮助信息。

- help_category
Information about help categories.

- help_keyword
Keywords associated with help topics.

- help_relation
Mappings between help keywords and topics.

- help_topic
Help topic contents.

<br>

**时区系统表**
如下系统表包含了时区信息。

- time_zone
Time zone IDs and whether they use leap seconds.

- time_zone_leap_second
When leap seconds occur.

- time_zone_name
Mappings between time zone IDs and names.

- time_zone_transition, time_zone_tansition_type
Time zone descriptions.

<br>

**副本系统表**
Server使用如下这些系统表来提供副本服务。这些表使用InnoDB存储引擎。

- gtid_executed
Table for storing GTID values.

- ndb_binlog_index
Binary log information for NDB Cluster replication.

- slave_master_info, slave_relay_log_info, slave_worker_info
Used to store replication information on slave servers.

<br>

**优化器系统表**
如下系统表用于优化。

- innodb_index_stats, innodb_table_stats
Used for InnoDB persistent optimizer statistics

- server_cost, engine_cost
The optimizer cost model uses tables that contain cost estimate information about operations that occur during query execution.

<br>

**杂项系统表**

- audit_log_filter, audit_log_user
- firewall_users, firewall_whitelist
- servers



<br/>
<br/>



## MySQL Server Logs


MySQL Server提供如下几种日志：

- Error log
启动、运行或停止mysqld遇到的问题

- General query log
建立Client连接和从Client收到的语句

- Binary log
更改数据的语句

- Relay log
从replication master server收到的数据更改

- Slow query log
执行时间超过`long_query_time`秒的查询

- DDL(Metadata) log
由DDL语句执行的元数据操作

<br>

默认情况下，不启用任何日志。

如果启用了这些日志，MySQL Server可以灵活地控制一般查询日志和慢查询日志的输出目的地——它可为日志文件或`mysql`数据库中的`general_log`和`slow_log`表。

```
#--log-output
#它的值可为TABLE/FILE/NONE
#--general-log, --slow-query-log


#TABLE和FILE
mysqld --log-output=TABLE,FILE --general-log=msyql.general_log --slow-query-log=mysql.slow_log



#or
[mysqld]
log_output=
general_log=
slow_query_log=
```

查看两个日志表的标准格式：

```
SHOW CREATE TABLE mysql.general_log;
SHOW CREATE TABLE mysql.slow_log;
```


<br/>
<br/>


### 错误日志

The Error Log

错误日志包含mysqld启动和关闭时间的记录。它还包含诊断信息。

<br>

**Unix/Unix-Like OS**
使用`mysqld --log-error`选项来将错误日志写入控制台(stderr)或文件。

如果未指定文件名，则默认为数据目录下的`host_name.err`文件。
YUM或APT包安装，则配置的错误日志文件为`--log-error=/var/log/mysqld.log`。

<br>

**将错误日志记录到系统日志**
Error Logging to the System Log

使用如下系统变量：

- `log_syslog`
启用此变量将错误日志发送到系统日志

- `log_syslog_facility`
syslog消息的默认设置时daemon。设置此变量以指定其它工具。

- `log_syslog_include_pid`
是否在syslog输出中包含Server的PID。

- `log_syslog_tag`
在syslog消息中添加一个tag。

```
msyqld --log_syslog=

```

<br>

**错误日志过滤**
Error Log Filtering

`log_error_verbosity`变量控制错误日志的详细程度。值如下：

- 1
error only

- 2
errors, warning

- 3(默认)
errors, warnings, notes

<br>

**错误日志消息格式**
Error Log Message Format

错误日志中包含的ID是mysqld中负责编写消息的线程的ID。这表示Server的哪部分生成了消息。
`log_timestamps`变量控制写入错误日志的时区和时间格式。

```
mysqld --log-timestamps=
```

<br>

**错误日志文件刷新**
Error Log File Flushing and Renaming

如果你使用`FLUSH_ERROR_LOGS`, `FLUSH_LOGS`或`mysqladmin flush-logs`刷新日志，Server将关闭并重新打开它正在写的任何错误日志文件。

```
mv host_name.err host_name.err-old
mysqladmin flush-logs
```


<br/>
<br/>



### 一般查询日志

The General Query Log

一般查询日志是mysqld执行操作的记录。当Client连接或断开时，Server将此信息写入日志，并记录从Client收到的每个SQL语句。
mysqld按照接收的顺序而不是执行顺序将语句写入日志。

默认情况下，一般查询日志是禁用的。
指定初始化查询日志状态`--general_log={0|1}`。`1`启用，`0`禁用。
指定日志文件名`--general-log-file=file-name`.如果未指定，默认为数据目录下`host_name.log`，除非指定了其它路径。
指定日志文件位置`--log-output=`.

```
mysqld --log-output='/var/log/mysql' --general-log=1 --general-log-file='general.log'


shell> mv host_name.log host_name-old.log
shell> mysqladmin flush-logs
```



<br/>
<br/>



### 二进制日志

The Binary Log




















































































<br/>
<br/>

---

<br/>




# 安全

Security


当考虑MySQL安装中的安全性时，你应该考虑各种可能的主题以及他们如何影响MySQL Server和相关应用程序的安全性:

- 影响安全性的一般因素。包括选择好的密码，不向用户授予不必要的权限，防止SQL注入和数据损坏来确保应用程序的安全性...
- 安装本身的安全性。应保护数据文件，日志文件和安装的所有应用程序文件，以确保未经授权方无法读写这些文件...
- 数据库系统本身的访问控制和安全性。包括允许访问数据库中使用的数据库，视图和存储应用程序的用户和数据库...
- 安全相关插件提供的功能...
- MySQL和你的系统的网络安全性。安全性还与用户的授权有关，但你可能希望限制MySQL，使其仅在本地主机上可用，或者在一组有限的其它主机上可用...
- 确保你备份了足够和适当的数据库文件，配置和日志文件。还要确保你已准备好恢复解决方案，并测试是否能够从备份种恢复信息...


<br/>



## 一般安全问题

General Security Issues


本节介绍了要注意的一般安全问题，以及如何使MySQL安装更安全，防止攻击或滥用。


<br/>


### 安全指南

Security Guidelines


在连接了Internet的计算机上使用MySQL的任何人都应阅读本节，以避免最常见的安全错误。
在讨论安全性时，有必要考虑完全保护整个服务器主机免受所有类型的攻击：窃听，更改，拒绝服务...

MySQL使用基于访问控制列表(ACL)的安全性，来处理用户可以尝试执行的所有连接、查询和其它操作。MySQL Client和Server之间SSL加密连接。

当运行MySQL时，遵循以下准则：

- 不要让任何人(root除外)访问`mysql.user`数据表，这很关键。

- 了解MySQL访问权限系统的工作原理。使用`GRANT`和`REVOKE`语句来控制对MySQL的访问。不要授予超出必要的权限，永远不要授予所有主机权限。
如果你能够在不被要求输入密码的情况下成功连接到MySQL Server，则任何人都可以以具有完全权限的root用户身份连接到MySQL Server。请重新查看MySQL安装说明，特别注意有关设置root密码的信息。
检查哪些账户拥有访问权限，并移除不必要的权限。

```
#测试
mysql -u root


#访问权限
SHOW GRANTS;


#移除权限
#help REVOKE
REVOKE
```

- 不要在数据库中存储明文密码。如果计算机被攻击，入侵者可以获得完整的密码列表并使用他们。相反，使用一些HASH函数并存储散列值。

- 不要从字典中选择密码，即不要使用简单和常规密码。存在某些破解密码的程序能计算你的密码。

- 启用防火墙。这可以保护你免受大部分漏洞攻击。将MySQL放在防火墙后面或DMZ。
使用端口扫描软件(如nmap)扫描主机端口。MySQL默认使用3306端口。不应从不受信任的主机访问此端口。测试你的端口安全性：

```
[zhang@zhang21 ~]$ telnet zhang21 3306
Trying 192.168.31.119...
Connected to zhang21.
Escape character is '^]'.
@Host 'zhang21' is not allowed to connect to this MySQL serverConnection closed by foreign host.



[zhang@zhang21 ~]$ telnet localhost 3306
Trying ::1...
Connected to localhost.
Escape character is '^]'.
J
5.7.22
[cqo3I  @kX@n#I\mysql_native_password
```

- 访问MySQL的应用程序不应该信任用户输入的任何数据，应该使用适当的防御性编程技术编写。

- 不要通过Internet传输普通数据(未加密)。请使用SSL或SSH加密协议。MySQL支持内部SSL连接；或是使用SSH端口转发为通信创建加密隧道。

- 学习使用`tcpdump`和`strings`使用程序。
可使用如下命令来检查MySQL数据流是否加密:

```
tcpdump -l -i eth0 -w - src or dst port 3306 | strings

```


<br/>
<br/>


### 密码安全

Keeping Passwords Secure


密码出现在MySQL的多个上下文中。此解提供了一些准则，使用户和管理员能够保护这些密码的安全性，并避免暴露这些密码。还讨论了MySQL如何在内部使用密码散列以及可用来强制执行更严格密码的插件。


<br/>


#### 密码安全用户指南

End-User Guidelines for Password Security

MySQL用户应使用以下准则来保证密码安全。当运行Client连接到MySQL server时，不建议以公开的方式来指定你的密码。

- 使用`mysql_config_editor`实用程序，它可将身份认证凭据存储在名为`.mylogin.cnf`的加密登录路径文件中。
- 使用`-pPASSWD`或`--password=PASSWD`选项
- 使用`-p`或`--password`选项不指定值
- 将密码存储到配置文件
- 将密码存储到`MYSQL_PWD`环境变量

```sh
#强烈不推荐
#这虽然方便却不安全
mysql -u user -pPASSWD db_name



#推荐
#但这适用于交互式
mysql -u user -p db_name
Enter password: xxx



#写入配置文件
chmod 600 ~/.my.cnf
vim ~/.my.cnf

[client]
password=xxx

mysql --defaults-file=~/.my.cnf



#指定MySQL密码环境变量的方法非常不安全，不应该使用
```

<br>

在Unix上，MySQL Client将执行语句的记录写入历史文件。默认情况下，此文件为`~/.mysql_history`。密码可以在SQL语句中以纯文本形式写入(如`CREATE USER`, `ALTER USER`)，如果使用了这些语句，它们将被记录到历史文件中。要保证此文件的安全，请使用限制访问模式。

如果命令解释器程序配置为维护历史记录，则保存命令的任何文件都将包含在命令行中输入的MySQL密码。如bash下的`~/.bash_history`。


<br/>
<br/>


#### 密码安全管理员指南

Administrator Guidelines for Password Security

MySQL数据库管理员应使用以下准则来保证密码安全：

- MySQL在`mysql.user`表中存储用户账户密码。永远不要向任何非管理账户授予此表的访问权限
- 账户密码可以过期，以便用户必须重置密码
- `validate_password`插件可用于对可接受的密码强制实施策略
- 应该保护可能写入密码的日志文件等文件


<br/>
<br/>


#### 密码和日志

Passwords and Logging

密码可在SQL语句中以纯文本形式写入，如`CREATE USET`, `GRANT`, `SET PASSWORD`和调用`PASSWORD()`函数的语句。如果MySQL Server记录了这些语句，那么访问日志的任何人都可以看到密码。

语句记录避免以明文形式为以下语句编写密码：

```sql
CREATE USER ... IDENTIFIED BY ...
ALTER USER ... IDENTIFIED BY ...
GRANT ... IDENTIFIED BY ...
SET PASSWORD ...
SLAVE START ... PASSWORD = ...
CREATE SERVER ... OPTIONS(... PASSWORD ...)
ALTER SERVER ... OPTIONS(... PASSWORD ...)
```

<br>

对于常规查询日志，可通过使用`--log-raw`选项启动Server来抑制密码重写。出于安全原因，此选项不建议用于生产环境。处于诊断目的，查看Server收到的语句的确切文本可能很有用。
审计日志插件生成的审计日志文件的内容未加密。出于安全原因，应将此文件写入只有MySQL Server和用户才能访问的目录，并且有正当理由查看目录。
只有在需要纯文本密码时才会进行密码重写，对于具有期望密码散列语法的语句，不会发生重写。
要保护日志文件免受不必要的暴露，请将他们放在限制访问Server和管理员的目录中。
副本集slave将复制副本集master的密码存储在主信息存储库中，它可以是文件或表。确保只能由管理员访问此库。

使用受限的访问模式来保护包含日志表或密码的日志文件的数据库备份。


<br/>
<br/>


#### 密码散列

Password Hashing in MySQL


MySQL在`mysql.user`数据表中列出用户账户。可以为每个MySQL账户分配一个密码，尽管用户表不存储明文密码，而是存储密码的散列值。

MySQL在Client/Server通信的两个阶段中使用密码：

- 当客户端尝试连接到Server时，有一个初始身份认证步骤，其中客户端必须提供密码，该密码的散列值与`mysql.user`用户表中存储的散列值相匹配
- 客户端连接之后，它可以(如果有足够权限)设置或更改`mysql.user`用户表中账户的密码的散列值。客户端可通过使用`PASSWORD()`函数来生成密码散列，或使用密码生成语句(`CREATE USER`, `GRANT`, `SET PASSWORD`)来完成此操作。

换句话说，Server在客户端首次尝试连接时在身份认证期间检查散列值。如果连接的客户端调用`PASSWORD()`函数，或使用密码生成语句来设置/更改密码，则Server会生成散列值。

```
help PASSWORD;
#This function is deprecated as of MySQL 5.7.6 and will be removed in a future MySQL release



#The Original (Pre-4.1) Hashing Method
#原始散列方法产生一个16Byte的字符串
mysql> SELECT PASSWORD('mypass');
+--------------------+
| PASSWORD('mypass') |
+--------------------+
| 6f8c114b58f2ce9e   |
+--------------------+



#The 4.1 Hashing Method
#MySQL4.1引入了密码散列，提供了更好的安全性并降低了密码被截获的风险
#生成更长的41Byte的散列值
mysql> SELECT PASSWORD('mypass');
+-------------------------------------------+
| PASSWORD('mypass')                        |
+-------------------------------------------+
| *6C8989366EAF75BB670AD8EA7A7FC1176A95CEF4 |
+-------------------------------------------+
```

<br>

**散列方法的兼容性问题**
Compatibility Issues Related to Hashing Methods



<br/>
<br/>


### 使MySQL安全抵御攻击者

Making MySQL Secure Against Attackers


连接到MySQL server时，应使用密码。密码在连接时不会以明文形式传输。所有其它信息都以文本形式传输，对任何能够看到连接的人都可读。如果连接通过不信任的网络，则可以使用压缩协议使流量更难以解密。你还可以使用MySQL的内部SSL支持来使连接更安全。或者，使用SSH在MySQL server和client之间获得加密的TCP/IP连接。

要使得MySQL系统安全，你应该强烈考虑以下建议：

- 要求所有MySQL账户都有密码
- 确保只有Unix用户账户对数据库目录具有读写权限，它是用于运行mysqld的账户
- 永远不要以root用户运行MySQL server，应该使用普通的非特权用户运行
- MySQL用户账户和Unix系统账户没有关联
- 不要对非管理员用户授予`FILE`权限，具有此权限的用户都可使用mysqld daemon的权限在文件系统的任何位置编写文件，同样也可读取文件，并将文件载入数据库
- 不要对非管理员用户授予`PROCESS`或`SUPER`权限(可用于终止连接，修改系统变量...)
- 不允许对表使用符号链接
- 安全地存储程序和视图
- 如果不信任DNS，则应在授权表中使用IP地址而非主机名
- 如果想要限制单个账户的连接数，可在mysqld中配置`max_user_connection`变量
- 如果插件目录对server可写，这可修改它为只读


```
#服务
cat /usr/lib/systemd/system/mysqld.service
[Service]
User=mysql
Group=mysql



#或配置文件
/etc/my.cnf
[mysqld]
user=mysql



#查看当前正在执行的语句
msyql> SHOW PROCESSLIST;
+----+------+-----------+-------+---------+------+----------+------------------+
| Id | User | Host      | db    | Command | Time | State    | Info             |
+----+------+-----------+-------+---------+------+----------+------------------+
| 18 | root | localhost | mysql | Query   |    0 | starting | SHOW PROCESSLIST |
+----+------+-----------+-------+---------+------+----------+------------------+



# Disabling symbolic-links is recommended to prevent assorted security risks
cat /etc/my.cnf
symbolic-links=0
```


<br/>
<br/>


### 安全相关的mysqld选项和变量

Security-Related mysqld Options and Variables


下表显示了影响安全性的mysqld的选项和系统变量:

| Name | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
| - | - | - | - | - | - | - |
| allow-suspicious-udfs | Yes | Yes |  |  |  |  |
| automatic_sp_privileges |  |  | Yes |  | Global | Yes |
| chroot | Yes | Yes |  |  |  |  |
| des-key-file | Yes | Yes |  |  |  |  |
| local_infile |  |  | Yes |  | Global | Yes |
| old_passwords |  |  | Yes |  | Both | Yes |
| safe-user-create | Yes | Yes |  |  |  |  |
| secure-auth | Yes | Yes |  |  | Global | Yes |
| - Variable: secure_auth |  |  | Yes |  | Global | Yes |
| secure-file-priv | Yes | Yes |  |  | Global | No |
| - Variable: secure_file_priv |  |  | Yes |  | Global | No |
| skip-grant-tables | Yes | Yes |  |  |  |  |
| skip-name-resolve | Yes | Yes |  |  | Global | No |
| - Variable: skip_name_resolve |  |  | Yes |  | Global | No |
| skip-networking | Yes | Yes |  |  | Global | No |
| - Variable: skip_networking |  |  | Yes |  | Global | No |
| skip-show-database | Yes | Yes |  |  | Global | No |
| - Variable: skip_show_database |  |  | Yes |  | Global | No |


<br/>
<br/>


### 以普通用户运行MySQL

How to Run MySQL as a Normal User


在Linux上，使用MySQL-repo、RPM包、Debian包来安装MySQL。MySQL server mysqld默认是由操作系统的mysql用户来启动。

对于使用`.tar.gz`包进行的安装，你需要修改为non-root用户。

```
chown -R user_name /path/to/mysql/datadir



vim /etc/my.cnf
[mysqld]
user=user_name
```


<br/>
<br/>


### `LOAD DATA LOCAL`的安全问题

`LOAD DATA`语句可以载入主机上的文件。

这有两个潜在的安全问题：

- 从Client到Server的文件传输是由MySQL server启动。理论上，server可告诉client传输server选择的文件而不是`LOAD DATA`语句中client指定的文件。这样，server可以访问client端用户可访问的任何文件。
- 在client从web server连接的Web环境中，用户可使用`LOAD DATA LOCAL`来读取Web server进程具有访问权限的任何文件。

为了避免`LOAD DATA`问题，客户端应该避免使用`LOCAL`。为避免连接到不受信任的Server，Client可通过`--ssl-mode=xxx`选项和相应的CA证书建立安全的连接。

<br>

要是管理员和应用程序能够管理本地数据加载功能，`LOCAL`配置的工作方式如下：

- On the server side
`local_infile`系统变量控制服务器端的`LOCAL`功能。默认启用`local_infile`。

- On the client side
`ENABLED_LOCAL_INFILE` CMake选项控制MySQL Client Library的已编译的默认`LOCAL`功能。
使用C API的客户端程序可通过调用`mysql_options()`来启用/禁用`MYSQL_OPT_LOCAL_INFILE`。
对于mysql Client，默认禁止本地数据载入。使用`--local-infile=1/0`
对于mysqlimport client，默认禁用本地数据载入。使用`--local=1/0`


<br/>
<br/>


### 客户端程序安全指南

Client Programming Security Guidelines


访问MySQL的应用程序不应该信任用户输入的任何数据，用户可以尝试通过在Web表单，URL或构建的任何应用程序中输入特殊字符序列来欺骗你。如果用户输入`DROP DATABASE mysql;`类似语句，请确保你的应用程序保持安全，这是一个极端栗子。
有时人们会认为，如果数据库只包含公开可用的数据，则无需受到保护。这是不正确的。即使允许在数据库中显示任何行，你仍应该防止拒绝服务攻击。

检查清单：

- 启用更严格的SQL模式以告知server对其接收的数据做更多限制
- 注意单/双引号
- 通过添加`%22("), %23("), %27(')`来修改动态URLs
- 动态修改URL中的数据类型
- 尝试输入字符、空格和特殊符号，而不是 数字
- 将数据传递给MySQL前检查数据大小
- 使用不同于管理员的用户将应用程序连接到数据库



<br/>
<br/>
<br/>



## 访问权限系统

The MySQL Access Privilege System


MySQL权限系统的主要功能就是对从给定主机连接的用户进行身份认证，并将用户与数据库的权限(`SELECT, INSERT, UPDATE, DELETE`)相关联。其它功能包含匿名用户(anonymous user)和MySQL特定功能的授权。

有些事情你无法使用MySQL权限系统：

- 你无法明确指定拒绝给定用户访问
- 你无法指定用户创建/删除表的权限，但不能指定创建/删除数据库自身
- 适用于账户全局性的密码

<br>

MySQL权限系统的用户接口(user interface)由： `CREATE USER, GRANT, REVOKE`语句组成。

在内部，Server将权限信息存储在`mysql`数据库的授权表中。MySQL server在启动时将这些表内容读入内存，并根据授权表的内存中的副本建立访问控制决策。
MySQL权限系统确保所有用户只能执行允许的操作。作为用户，当你连接到MySQL server时，你的身份由你连接的主机和你指定的用户名决定。在连接后，系统会根据你的身份和要执行的操作授予权限。
MySQL会识别你的主机名和用户名，因为没有理由认为给定的用户名属于所有主机上的同一个人。

```
SHOW GRANTS;

SHOW GRANTS FOR 'joe'@'office.example.com';
SHOW GRANTS FOR 'joe'@'home.example.com';
```

<br>

当运行客户端程序连接到server时，MySQL访问控制包含两个阶段：

1. server根据你的身份来接受/拒绝连接，以及你是否可通过提供正确的密码来验证你的身份
2. 假设你可以连接，server会检查你发出的每个语句，以确定是否有足够的权限来执行它



<br/>
<br/>


### MySQL提供的权限

Privileges Provided by MySQL


授予MySQL账户的权限决定了账户可以指定的操作。MySQL权限在它们适用的上下文和不同操作级别上有所不同：

- 管理员权限(Administrative privileges)允许用户管理MySQL Server的操作。这些权限是全局的，因为它们不是特定于特定数据库
- 数据库权限(privileges for database)适用于数据库及其中的所有对象。可以为特定数据库或全局赋予这些权限，以便它们适用于所有数据库
- 数据库对象权限(privileges for database object)，如表，索引，视图...


<br/>
<br/>


#### 可用权限

Summary of Available Privileges

下表显示了`GRANT`和`REVOKE`语句中使用的权限名称，以及每个权限关联的列名和权限适用的上下文:

| Privilege | Grant Table Column | Context |
| - | - | - |
| ALL [PRIVILEGES] | Synonym for “all privileges” | Server administration |
| ALTER | Alter_priv | Tables |
| ALTER ROUTINE | Alter_routine_priv | Stored routines |
| CREATE | Create_priv | Databases, tables, or indexes |
| CREATE ROUTINE | Create_routine_priv | Stored routines |
| CREATE TABLESPACE | Create_tablespace_priv | Server administration |
| CREATE TEMPORARY TABLES | Create_tmp_table_priv | Tables |
| CREATE USER | Create_user_priv | Server administration |
| CREATE VIEW | Create_view_priv | Views |
| DELETE | Delete_priv | Tables |
| DROP | Drop_priv | Databases, tables, or views |
| EVENT | Event_priv | Databases |
| EXECUTE | Execute_priv | Stored routines |
| FILE | File_priv | File access on server host |
| GRANT OPTION | Grant_priv | Databases, tables, or stored routines |
| INDEX | Index_priv | Tables |
| INSERT | Insert_priv | Tables or columns |
| LOCK TABLES | Lock_tables_priv | Databases |
| PROCESS | Process_priv | Server administration |
| PROXY | See proxies_priv | table  Server administration |
| REFERENCES | References_priv | Databases or tables |
| RELOAD | Reload_priv | Server administration |
| REPLICATION CLIENT | Repl_client_priv | Server administration |
| REPLICATION SLAVE | Repl_slave_priv | Server administration |
| SELECT | Select_priv | Tables or columns |
| SHOW DATABASES | Show_db_priv | Server administration |
| SHOW VIEW | Show_view_priv | Views |
| SHUTDOWN | Shutdown_priv | Server administration |
| SUPER | Super_priv | Server administration |
| TRIGGER | Trigger_priv | Tables |
| UPDATE | Update_priv | Tables or columns |
| USAGE | Synonym for “no privileges” | Server administration |


<br/>
<br/>


#### 授权指南

Privilege-Granting Guidelines

最好只向账户授权它所需要的权限，在授予`FILE`和管理权限时应特别小心:

- `FILE`： 可在MySQL Server主机上读取的任何文件读入数据库表
- `GRANT OPTION`： 使用户能够将其权限授权其他用户。具有不同权限且具有`GRANT OPTION`权限的两个用户可以组合权限
- `ALTER`: 可通过重命名表来破坏权限系统
- `SHUTDOWN`： 通过终止Server完全拒绝向其它用户提供服务
- `PROCESS`： 用于查看当前正在执行的语句的纯文本，包括设置和更改密码的语句
- `SUPER`： 用于终止其它会话或更改服务器的运行方式
- 为mysql系统数据本自身授予的权限可用于更改密码和其它访问权限信息：
	+ 密码以加密方式存储，因此恶意用户无法简单地读取明文密码。然而，具有对`mysql.user`表`authentication_string`列具有写权限的用户可以更改账户密码，然后进行登录
	+ 为mysql系统数据库授予`INSERT`或`UPDATE`权限允许用户添加或修改现有权限
	+ mysql系统数据库的`DROP`权限使用户能够访问远程权限表，甚至是数据库本身



<br/>
<br/>



### 授权表

Grant Tables


mysql系统数据库包含多个授权表，其中包含有关用户账户及其拥有的权限信息。
mysql数据库表包含的授权信息：

- `user`: 用户账户，全局权限，其它非权限列
- `db`: 数据库级别权限
- `tables_priv`：表级别权限
- `columns_priv`： 列级别权限
- `procs_priv`： 存储过程和功能权限
- `proxies_priv`： 代理用户权限

每个授权表包含的列范围和列权限：

- 列范围确定表中每行的范围
- 列权限指示表中行授予的权限

Server以下列方式使用授权表：

- `user`表范围列确定是拒绝还是允许传入连接
- `db`表范围列确定哪些用户可以从哪些主机上访问数据库
- `tables_priv`和`columns_priv`表更精细，它们适用于表级别和列级别
- `procs_priv`表用于存储的例程
- `proxies_priv`表指示哪些用户可以充当其它用户的代理，以及用户是否可以将`PROXY`权限授予其它用户



<br/>
<br/>



### 指定账户名

Specifying Account Names


MySQL账户名由用户名和主机名组成。这样可以为具有相同名称且可以从不同主机连接的用户创建账户。

在SQL语句中，账户名称遵循以下规则：

- 账户名语法为: `username@hostname`
- 仅包含用户名的账户相当于`username@%`
- 注意反引号、单引号、双引号
- 引号的正确用法: `'username'@'hostname'`

MySQL使用单独的用户名和主机名部分将账户名称存储到mysql系统数据库的授权表中：

- `user`表包含每个账户的一行，`user.User`，`user.Host`列存储用户名和主机名，此表还指示了账户具有哪些全局权限
- 其它授权表指示账户对数据库和库中对象的权限，这些表也有`User, Host`列来存储用户名和主机名
- 处于访问检查的目的，User value区分大小写，Host value不区分大小写

<br>

用户名和主机名还具有某些特殊值或通配符约定，如下:
账户名的用户名部分是非空白值，或者是与任何用户名匹配的空值。具有空白用户名的账户是匿名用户(anonymous user)。在SQL语句中指定一个匿名用户，使用带引号的空用户名，如`''@'localhost'`。

账户名的主机名部分可以采用多种形式，并允许使用通配符：

- host value可以是主机名或IP地址(ipv4, ipv6)

- 主机名或IP地址值中允许使用`%`和`_`通配符。
例如，主机值`%`匹配任何主机名，如`%.mysql.com`匹配`mysql.com`域中的任何主机。

- 对于IPv4地址，可以给出网络掩码以指示用于网络号的地址位数

```
CREATE USER 'test'@'198.51.100.0/255.255.255.0；
```

Server使用系统DNS解析程序为客户端主机名或IP地址返回的值，意味着你应该使用DNS使用的相同格式指定的账户主机值。



<br/>
<br/>



### 连接验证

Access Control, Stage 1: Connection Verification



































<br/>
<br/>

---

<br/>








# 备份和恢复

Backup and Recovery





















<br/>
<br/>

---

<br/>


















# 优化

Optimization


























<br/>
<br/>

---

<br/>













# 语言结构

Language Structure



























<br/>
<br/>

---

<br/>











# 字符集和编码

Character Sets, Collations, Unicode




















<br/>
<br/>

---

<br/>





# 数据类型

Data Type


MySQL支持多种类型的SQL数据类型：

- numeric
- date/time
- string
	+ character
	+ byte
- JSON

<br>

数据类型描述使用如下约定：

- `M`表示整数类型的最大显示宽度
- `D`适用于浮点和定点类型，并指示小数点后面的位数
- `fsp`适用于TIME, DATATIME, TIMESTAMP类型，表示小数点的秒精度
- 方括号`[]`表示类型定义的可选部分



<br/>
<br/>



## 数字

Numberic type


如果为数字列指定`ZEROFILL`，MySQL会自动将`UNSIGNED`属性添加到列中。

数字数据类型允许`UNSIGNED`(无符号)属性，也允许`SIGNED`(符号)。默认情况下，这些数据类型是`SIGNED`，因此`SINGED`属性不起作用。


<br>

- BIT
A bit-value type.(1-64)

- TINYINT
A very small integer.
有符号范围: `-128 to 127`, 无符号范围: `0-255`

- BOOL

- SMALLINT
A small integer.
有符号范围: `-32768 to 32767`, 无符号范围: `0-65535`

- MEDIUMINT
A medium-sized integer.
有符号范围: `-8388608 to 8388607`, 无符号范围: `0-16777215`

- INT
A normal-size integer.
有符号范围: `-2147483648 to 2147483647`, 无符号范围: `0- 4294967295`

- INTERGER
此类型是INT的同义词。

- BIGINT
A large integer.
符号范围: `-9223372036854775808 to 9223372036854775807`, 无符号范围: `0 to 18446744073709551615`
`SERIAL`是`BIGINT UNSIGNED NOT NULL AUTO_INCREMENT UNIQUE`的别名。

- DECIMAL/DEC

- FLOAT
A small(单精度) floating-point number.
允许的值为: -3.402823466E+38 to -1.175494351E-38, 0, and 1.175494351E-38 to 3.402823466E+38

- DOUBLE
A normal-size(双精度) floating-point number.
允许值为: -1.7976931348623157E+308 to -2.2250738585072014E-308, 0, and 2.2250738585072014E-308 to 1.7976931348623157E+308

- FLOAT
A floating-point number.









<br/>
<br/>


## 日期和时间

Date and Time Type


MySQL允许的TIME, DATETIME, TIMESTAMP值的小数，精度高达微秒(小数点后6位)。

- DATE
A date.
支持范围: `1000-01-01`到`9999-12-31`。
MySQL以`YYYY-MM-DD`格式显示DATE值，但允许使用字符串或数字将值分配给DATE列。

- DATETIME
A date and time combination.
支持范围: `1001-01-01 00:00:00.000000`到`9999-12-31 23:59:59.999999`。
MySQL以`YYYY-MM-DD HH:MM:SS.[fraction]`的格式显示DATETIME值，同样允许字符串或数字将值分配给DATETIME列。

- TIMESTAMP
A timestamp.
支持范围: `1970-01-01 00:00:01.000000`UTC到`2038-01-19 03:14:07.999999`UTC
TIMESTAMP值存储为自纪元`1970-01-01 00:00:01.000000 UTC`以来的秒数，这也叫原子时间。

- TIME
A time.
支持范围: `-838:59:59.000000` to `838:59:59.000000`
MySQL以`HH:MM:SS[.fraction]`的格式显示TIME值，但允许使用字符串或数字将值分配给TIME列。

- YEAR
A year in four-digit format.
MySQL以`YYYY`格式显示YEAR值，但允许使用字符串或数字将值分配给YEAR列。






<br/>
<br/>

---

<br/>


## 字符串

String Type


在某些情况下，MySQL可能会使用`CREATE TABLE`或`ALTER TABLE`语句更改字符串的类型。

**CHARACTER SET/CHARSET**
指定字符集

```sql
CREATE TABLE t
(
    c1 VARCHAR(20) CHARACTER SET utf8,
    c2 TEXT CHARACTER SET latin1 COLLATE latin1_general_cs
);
```

<br>

- CHAR
一个固定长度的字符串，在存储时使用用空格填充指定长度。
VARCHAR的有效最大长度取决于最大行大小(65535字节)和使用的字符集。

- VARCHAR
一个可变长度的字符串。

- BINARY
BINARY类似于CHAR，但存储二进制字节字符串而不是非二进制字符串。

- VARBINARY

- TINYBLOB
A BLOB column with a maximum length of 255 (2^8 − 1) bytes.

- TINYTEXT
A TEXT column with a maximum length of 255 (2^8 − 1) characters.

- BLOB
A BLOB column with a maximum length of 65,535 (2^16 − 1) bytes.

- TEXT
A TEXT column with a maximum length of 65,535 (2^16 − 1) characters.

- MEDIUMBLOB
A BLOB column with a maximum length of 16,777,215 (2^24 − 1) bytes.

- MEDIUMTEXT
A TEXT column with a maximum length of 16,777,215 (2^24 − 1) characters.

- LONGBLOB
A BLOB column with a maximum length of 4,294,967,295 or 4GB (2^32 − 1) bytes.

- LONGTEXT
A TEXT column with a maximum length of 4,294,967,295 or 4GB (2^32 − 1) characters.

- ENUM
An enumeration.

- SET
A set.















































