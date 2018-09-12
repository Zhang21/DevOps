---

title: "SaltStack"
date: "2017-12-25 09:47:39"
tags: "SaltStack"
categories: "Linux"

---

参考：
- SaltStack官网：<https://saltstack.com>
- SaltStack文档：<https://docs.saltstack.com/en/latest/topics>
- SaltStack-GitHub：<https://github.com/saltstack>
- Salt-repo：<https://repo.saltstack.com/>

环境：
- CentOS7_x64;
- Salt-2018.02

<!--more-->



<br>

---

<br>



# 说明

`SaltStack`是一种革命性的用速度(speed)取代复杂性(complexity)的基础设施(infrastucture)管理方法。

- 简单(Simple)，可以在几分钟内运行；
- 可伸缩性(Scalable)，足以管理数以万计的Server；
- 快速(Fast)，能在几秒内与各系统间进行通信。

<br/>

**You'll learn how to:**

- 安装和配置SaltStack；
- 在所有托管系统上远程执行命令(Remotely execute commands)；
- 设计、开发和部署系统配置；
- 使用Salt Reactor是基础设施自动化(automate)；
- 使用Salt Orchestration协调复杂管理操作。

![SaltStack](/images/Salt/SaltStack.png)

<br/>

Salt是建立在动态通信总线(dynamic communication bus)上的基础设施管理的一种新方法。Salt可以用于数据驱动(data-driven)业务，远程执行(remote execution)任何基础设施，配置管理(configuration management)任意应用堆栈...

- REMOTE EXECUTION;
- CONFIGURATION MANAGEMENT;
- EVENT-DRIVEN INFRASTRUCTURE;
- SALT ESSENTIALS.



<br>

---

<br>


# 安装

Installation


如果是第一次设置环境，你应该在专用的管理服务器上安装`Salt master`，然后在每个使用Salt管理的系统上安装`Salt minion`。现在不需要担心你的系统架构(architecture)，你可以在以后轻易添加组件(componet)和修改配置(configuration)而不需要重新安装任何东西。

The general installation process is as follows:

- 安装`Salt master`，通过各平台说明安装或通过Salt `bootstrap.sh `脚本来安装；
- 确保你的`Salt minion`能够找到`Salt master`；
- 在想要管理的每个系统上安装`Salt minion`；
- 在`Salt minion`连接后接受`Salt minion key`。

在此之后，就可以**运行一个简单命令**，并从所有的`Salt minion`**接收返回**。

```sh
#salt <minion-id> <cmd>

salt minion1 test.ping
salt * test.ping
```


<br>
<br>

## 快速安装

Quick install


在绝大多数发行版本上，可以使用**Salt Bootstrap**脚本进行快速安装。

参考：[Salt Bootstrap](https://docs.saltstack.com/en/latest/topics/tutorials/salt_bootstrap.html#salt-bootstrap)

```
#wget
wget https://bootstrap.saltstack.com -O bootstrap-salt.sh
sh bootstrap-salt.sh

#curl
curl -o bootstrap-salt.sh -L https://bootstrap.saltstack.com
sh bootstrap-salt.sh
```


<br>
<br>


## 指定平台

Platform-Specific Installation

[选择发行版本安装](https://docs.saltstack.com/en/latest/topics/installation/index.html#platform-specific-installation-instructions)


<br>


### CentOS7

repo: <https://repo.saltstack.com/#rhel>

**1. 下载SaltStack-Repository进行安装：**

`systemd`和`systemd-python`是Salt必须的，在安装Salt前需装好。

```sh
#安装salt-repo
yum install -y https://repo.saltstack.com/yum/redhat/salt-repo-latest-2.el7.noarch.rpm


yum clean expire-cache


#安装salt组件
yum install -y salt-master salt-minion salt-ssh salt-syndic salt-cloud salt-api


#开启
systemctl start salt-master
```

<br/>

**2. 自建salt-repo：**

```sh
vim /etc/yum.repos.d/saltstack.repo


[saltstack-repo]
name=SaltStack repo for Cent0S7
baseurl=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest
enalbed=1
gpgcheck=1
gpgkey=https://repo.saltstack.com/yum/redhat/$releasever/$basearch/latest/SALTSTACK-GPG-KEY.pub
```



<br>
<br/>


## 初始化

Initial Configuration


### 配置salt

Configuration Salt

`salt-master` 的默认配置会为安装而工作，唯一要求是在`salt-minion`的配置文件中设置`salt-master`的位置。


<br>


#### salt-master

默认的，`salt-master`配置文件位于`/etc/salt/master`，在all interfaces(0.0.0.0)上监听`4505`和`4506`端口。

```sh
vim /etc/salt/master

interface: 0.0.0.0
```


<br>


#### salt-minion
默认，一个`salt-minion`会尝试连接到DNS名称为`salt`。如果`salt-minion`能够正确解析(resolve)这个名称，则可以不需要配置文件。如果DNS名称`salt`未能解析为`salt-master`的正确位置，那么可在`/etc/salt/minion`配置文件下重新定义`salt`。

```sh
vim /etc/salt/minion


#master: salt
#如果是默认的salt,需要在本地hosts下解析salt
#此处我们修改为salt-master的IP地址
master: 192.168.1.9
```

**修改配置文件后，请重启服务。**


<br>


#### minion代理配置

PROXY MINION CONFIGURATION

A Proxy Minion模仿一个规律的行为和继承(inherit)他们的选项。
类似地，它的配置文件存放于`/etc/salt/proxy`，`proxy`也将尝试连接DNS名为`salt`的主机。

除了`salt-minion`有规律的选型，`proxy`还有一些特定的选项。参考:[Proxy minion](https://docs.saltstack.com/en/latest/ref/configuration/proxy.html#configuration-salt-proxy)


<br>


#### 运行Salt

以`salt`命令运行:

```sh
salt-master
#开启守护进程
salt-master -d

#systemd
systemctl start salt-master



salt-minion
salt-minion -d
systemctl start salt-minion



#日志信息
salt-master --log-level=debug
```

**以non-root运行salt**
- 确保此用户有相应的权限；
- 可能需要修改相应目录的权限：
	+ /etc/salt
	+ /var/cache/salt
	+ /var/log/salt
	+ /var/run/salt


<br/>


#### 密钥识别

Key Identity

在`initial key`交换之前，`Salt`会提供命令来验证(validate)`salt-master`和`salt-minion`的身份。
验证身份有助于避免疏忽地连接到错误的`salt-master`，并且在建立初始化连接的阻止MiTM攻击。

**Master Key Fingerprint**
复制`master.pub`的值，并将其作为`salt-minion`配置文件`/etc/salt/minion`中`master_finger`的值。

```sh
#salt-key is used to manage Salt authentication keys

#查看master的key
salt-key -F master

Local Keys:
master.pem:  60:87:25:6a:68:28:4a:bf:5e:87:ee:4f:3f:46:d4:8e:38:8b:58:d9:8a:f4:44:b6:64:67:d9:da:0f:5d:f3:b4
master.pub:  46:52:c1:36:f2:6f:33:c0:72:a1:18:5e:99:36:04:ea:1a:9b:ea:e7:61:3b:d9:30:34:c1:f1:3b:65:08:f8:42
#将公钥写入salt-minion配置文件


#查看minion的finger
#salt-key --finger <minion_id>
salt-key --finger '192.168.1.7'
```

**Minion Key Fingerprint**

```sh
#salt-call is used to execute module functions locally on a Salt Minion


#查看minion key fingerprint
#可在master上查看，比对两者是否相同
salt-call --local key.finger
```


<br>


#### 密钥管理

Key Management

Salt使用AES Encryption加密`salt-master`与`salt-minion`间的所有通信。这确保了发送到Minion的命令不会被篡改(tamper)，并保证了master与minion间是认证的和受信任的。

当命令发送到`salt-minion`之前，`salt-minion`的key必须要被`salt-master`所接受。

```sh
#列出salt-master上已知的keys
salt-key -L
```

其中包含四项:

- Accepted Keys:
- Denied Keys:
- Unaccepted keys:
- Rejected keys:

**让`salt-master`接收key，并允许`salt-minion`被`salt-master`控制**

```sh
#-a 192.168.1.7, --accept=192.168.1.7
#-A, --accept-all

salt-key -A
```


<br>


#### 发送命令

Sending Commands

`salt-master`和`salt-minion`之间通过运行`test.ping`命令来证实(verified)。

```sh
salt 192.168.1.7 test.ping

salt * test.ping
```



<br/>
<br/>



## 其它安装指南

Additional Installation Guides


<br/>


### Salt Bootstrap

Salt Bootstrap脚本允许用户在各种系统和版本上安装`salt-minion`和`salt-master`。shell脚本为`bootstrap-salt.sh`，运行一系列的检查来确定操作系统的类型和版本，然后通过适当的方法安装salt二进制文件。salt-bootstrap脚本安装运行`salt`的最小化安装包，如Git便不会安装。

Salt Bootstrap's GitHub: <https://github.com/saltstack/salt-bootstrap>


<br>


#### 栗子

Satl Bootstrap脚本有多种可以传递的选项，以及获取引导脚本本身的方法。

**1. 使用`curl`**

```
curl -o bootstrap-salt.sh -L https://bootstrap.saltstack.com
sh bootstrap-salt.sh git develop
```

**2. 使用`wget`**

```
wget -O bootstrap-salt.sh https://bootstrap.saltstack.com
sh bootstrap-salt.sh
```

**3. An Insecure one-liner**

```
curl -L https://bootstrap.saltstack.com | sh

wget -O - https://bootstrap.saltstack.com | sh

curl -L https://bootstrap.saltstack.com | sh -s -- git develop
```

**4. cmd line options**

```
#查看帮助
sh bootstrap-salt.sh -h
```


<br/>


### 防火墙

`salt-master`和`salt-minion`间的通信使用AES加密的`ZeroMQ`，它使用TCP的4505和4506端口，仅需要在`salt-master`上可访问就行。

下面概述了关于`salt-master`的防火墙规则：

**RHEL7/CENTOS7**

```
firewall-cmd --permanent --zone=<zone> --add-port=4505-4506/tcp
firewall-cmd --reload
```


<br/>

### Preseed minion with accepted key

某些情况下，在`salt-master`上接受`minion-key`之前等待`salt-minion`启动是不方便的。比如，你可能希望`minion`一上线(online)就引导。

有多种方式生成`minion-key`，下面是一般生成`minion-key`的四个步骤：

1. 在master上生成key：

```
#请给key取个名字
salt-key --gen-keys=[key_name]
```

2. 把公钥(publick key)添加到已接受的minion文件夹中:

公钥文件和 minion_id 有相同的名字是很有必要的，这就是Salt如何通过key与minions匹配。
还有，由于不同操作系统或特定的master配置文件，pki 文件夹可能位于不同的位置。

```
cp <key_name>.pub /etc/salt/pkimaster/minions/<minion_id>
```

3. 分配`minion-key`：

对于minion来说，没有单一方法去得到密钥对，难点是找到一种安全的分配方法。

由于`master`已经接受了`minion-key`，因此分发私钥(private key)会有潜在的安全风险。

4. 配置带key的minion：

你可能希望在启动`salt-miniont daemon`之前取得`minion-key`的位置。

```
/etc/salt/pki/minion/minion.pem
/etc/salt/pki/minion/minion.pub
```


<br/>


### 以普通用户运行root

Running salt as normal user tutorial

**以普通用户(non-root)运行salt function**

如果你不想使用`root`用户安装或运行salt，你可以在你的工作目录中创建一个虚拟根目录(virtual root dir)来配置它。
salt system使用`salt.syspath`module来查找变量。

如果你运行salt-build，它会生成在: `./build/lib.linux-x86_64-2.7/salt/_syspaths.py`；

运行`python setup.py build`命令来生成它；

复制生成的module到你的salt dir，`cp ./build/lib.linux-x86_64-2.7/salt/_syspaths.py ./salt/_syspaths.py`

修改它，并加入需要的变量和新路径：

```python
# you need to edit this
ROOT_DIR = *your current dir* + '/salt/root'

# you need to edit this
INSTALL_DIR = *location of source code*

CONFIG_DIR =  ROOT_DIR + '/etc/salt'
CACHE_DIR = ROOT_DIR + '/var/cache/salt'
SOCK_DIR = ROOT_DIR + '/var/run/salt'
SRV_ROOT_DIR= ROOT_DIR + '/srv'
BASE_FILE_ROOTS_DIR = ROOT_DIR + '/srv/salt'
BASE_PILLAR_ROOTS_DIR = ROOT_DIR + '/srv/pillar'
BASE_MASTER_ROOTS_DIR = ROOT_DIR + '/srv/salt-master'
LOGS_DIR = ROOT_DIR + '/var/log/salt'
PIDFILE_DIR = ROOT_DIR + '/var/run'
CLOUD_DIR = INSTALL_DIR + '/cloud'
BOOTSTRAP = CLOUD_DIR + '/deploy/bootstrap-salt.sh'
```

创建目录结构：

```
mkdir -p root/etc/salt root/var/cache/run root/run/salt root/srv
root/srv/salt root/srv/pillar root/srv/salt-master root/var/log/salt root/var/run
```

填充配置文件：

```
cp -r conf/* /etc/salt/


vi /etc/salt/master

user: *your user name*
```

运行：

```py
PYTHONPATH=`pwd` scripts/salt-cloud
```


<br>


### minion独立运行

Standalone minion

因为`salt-minion`包含了如此广泛的功能，它可以独立运行。
一个独立的minion可以用来做很多事情:

- 在没有连接到`master`的系统上使用`salt-call`命令；
- 无主状态(masterless states)。

当以无主模式运行salt时，不要运行`salt-minion daemon`。否则，它将尝试连接到master并失败。
`salt-call`命令是独立的，不需要`salt-minion daemon`。


<br/>


#### minion配置

有几个参考方法来设置不同的选项来配置`masterless minion`，`salt-minion`很容易通过配置文件(默认位于:`/etc/salt/minion`)进行配置。

<br/>

**告诉salt运行masterless**

`salt-call`命令用于在`salt-minion`本地运行模块功能，而不是在`salt-master`执行他们。通常，`salt-call`命令检查主机检索文件服务器和支柱数据，当时当运行`standalone salt-call`时，需要指示不要检查master的这些数据。
为了指示`minion`不要查找`master`，需要在运行`salt-call`时设置`file_client`配置选项。默认情况下，`file_client`被设置为`remote`让`minion`知道将从`master`中收集文件服务器和支柱数据。当设置`file_client`为`local`时，`minion`将不会从`master`收集这些数据。

```yaml
file_client: local

#这样，salt-call命令将不会查找master
#并认为本地系统拥有所有的文件文支柱资源
```

<br/>

**masterless运行状态**

the state system在所有需要的文件都在`minion`本地，轻易地在没有`salt-master`的情况下运行。为了达到此效果，需要配置`minion`配置文件，以了解如何像`master`一样返回file_roots信息。

```yaml
file_roots:
  base:
    - /srv/salt
```

现在设置salt state tree, top file和SLS modules，就像在`master`上设置它们一样。将`file_client`设置为`local`，并且一个可用的state tree会调用state module中的function，将使用`minion`上的file_roots中的信息而不是`master`。

当在一个`minion`上创建一个`state tree`时，不需要语法或路径的更改。`master`上的SLS modules不需要进行任何修改就可以与`minion`一起工作。这就使得salt scrit不需要设置一个`master`就能轻易部署，并允许这些SLS modules随着部署发展而容易转移到`master`。

```sh
#以声明的状态可以执行
salt-call state.apply


#无需修改配置文件
salt-call state.apply --local
```


<br>


### Salt无主模式

Salt masterless quickstart

运行一个无主模式的minion可以允许你在单一主机上使用salt配置管理，而不用在另一台主机上调用master。
在无主模式下运行salt时，请勿运行salt daemon。否则，它将尝试连接到master并失败。`salt-call`命令时独立的

<br>

**bootstrap salt minion**

```
curl -L https://bootstrap.saltstack.com -o bootstrap_salt.sh
sudo sh bootstrap_salt.sh
```

<br>

**告诉salt运行masterless模式**
在minion配置文件中配置此，表示不去寻找master，并假设本地系统拥有所有文件和资源。

```
vim /etc/salt/minion

file_client: local
```

<br>

**创建状态树(state tree)**

1. 创建`top.sls`文件

```
vim /srv/salt/top.sls

base:
  '*':
    - webserver
```

2. 创建webserver状态树

```
vim /srv/salt/webserver.sls
#这是基于Debian

apache:               # ID declaration
  pkg:                # state declaration
    - installed       # function declaration
```

3. `salt-call`
`salt-call`命令在minion本地运行远程执行功能，而不是在master执行。

```
#--local,在本地文件系统查找状态树
salt-call --local state.apply

#minion首先检查top.sls，然后应用webserver.sls
```



<br/>
<br/>

---

<br/>



# 配置salt


本节介绍如何配置用户访问，查看，存储作业结果，安全，疑难解答以及如何执行其它管理任务。


<br/>


## 配置master

salt系统的两个组件都有相应的配置文件: master，minion。


<br/>


### master配置项


**基础配置**

```
#INTERFACE，默认值0.0.0.0
interface: 0.0.0.0


#IPv6，默认值False
ipv6: False


#PUBLISH_PORT，默认值4505
publish_port: 4505


#MASTER_ID，默认值None
master_id: Master


#USER，默认值root
user: root


#ENALBE_SSH_MINIONS，默认值False
enable_ssh_minions: True


#RET_PORT，默认值4506
#接收命令执行返回的端口
ret_prot: 4506


#PIDFILE，默认值/var/run/salt-master.pid
pidfile: /var/run/salt-master.pid


#ROOT_DIR，默认值/
root_dir: /


#CONF_FILE，默认值/etc/salt/master
conf_file: /etc/salt/master


#PKI_DIR，默认值/etc/salt/pki/master
#存储pki认证密钥的目录
pki_dir: /etc/salt/pki/master


#EXTENSION_MODULES，默认值/var/cache/salt/master/extmods
extension_modules: /root/salt_extmods


#EXTMOD_WHITELIST/EXTMOD_BLACKLIST
#有效的选项: modules, states, grains, renderers, returners, output, proxy, runners,
#wheel, engines, queues, utils, pillar, sdb, cache, clouds, tops, roster, tokens
extmod_whitelist:
  modules:
    - custom_module
  engines:
    - custom_engine
  pillars: []

extmod_blacklist:
  modules:
    - specific_module


#MODULE_DIRS，默认值[]
module_dirs:
  - /var/cache/salt/minion/extmods


#CACHEDIR，默认值/var/cache/salt/master
cachedir: /var/cache/salt/master


#VERIFY_ENV，默认值True
#在启动时验证并设置目录权限
verify_env: True


#KEEP_JOBS，默认值24
#设置保留旧作业信息的小时数，0表示禁用缓存清理
keep_jobs: 24


#GATHER_JOB_TIMEOUT，默认10
#客户端请求正在运行的作业信息是等待的秒数
gather_job_timeout: 10


#TIMEOUT，默认值5
#salt命令和api默认超时值
timeout: 5


#LOOP_INTERVAL，默认值60
#维护过程检查周期的秒数
loop_interval: 60


#OUTPUT，默认值nested
#设置命令使用的默认输出器
output: nested


#OUTPUTTER_DIRS，默认值[]
#salt输出器附加目录列表
outputter_dirs: []


#OUTPUT_FILE，默认值None
#salt命令使用的默认输出文件
output_file: /path/output/file


#SHOW_TIMEOUT，默认值True
#告诉client已超时的minion
show_timeout: True


#SHOW_JID，默认值False
#告诉client在工作发布时显示jid
show_jid: False


#COLOR，默认值True
color: False


#COLOR_THEME，默认值""
color_theme: /etc/salt/color_theme


#CLI_SUMMARY，默认False
#显示目标minion数量的摘要
cli_summary: False


#SOCK_DIR
#Default: /var/run/salt/master
#创建Unix socket的位置
sock_dir: /var/run/salt/master


#ENABLE_GPU_GRAINS
#Default: True
#启用GPU硬件数据


#JOB_CACHE
#Default: True
#维护一个临时作业缓存
job_cache: True


#MINION_DATA_CACHE
#Default: True
#存储在master端的minion数据缓存
minion_data_cache: True


#CACHE
#Default: localfs
#缓存子系统模块用于minion数据缓存
cache: consul


#MEMCACHE_EXPIRE_SECONDS
#Default: 0，禁用
#内存缓存数据过期时间
memcache_expire_seconds: 30


#MEMCACHE_MAX_ITEMS
#Default: 1024
#缓存项限制
memcache_max_items: 1024


#MEMCACHE_FULL_CLEANUP
#Default: False
#如果缓存已满(超过max_literms)，则项目将清除其存储
memcache_full_cleanup: True


#MEMCACHE_DEBUG
#Default: False
#收集缓存统计信息并记入调试日志级别
memcache_debug: True


#EXT_JOB_CACHE
#Default: ''
#指定所有minion的默认returner
ext_job_cache: redis


#EVENT_RETURN
#Default: ''
#指定用于记录时间的returner
event_return:
  - syslog
  - splunk


#EVENT_RETURN_QUEUE
#Default: 0
#在繁忙的系统上，启用event_returns可能会给存储系统造成相当大的负载。事件可以在master使用队列排队，并以批处理方式使用单个事务存储多个事件
event_return_queue: 0


#EVENT_RETURN_WHITELIST
#Default: []
event_return_whitelist:
  - salt/master/a_tag
  - salt/run/*/ret


#EVENT_RETURN_BLACKLIST
#Default: []
event_return_blacklist:
  - salt/master/not_this_tag
  - salt/wheel/*/ret


#MAX_EVENT_SIZE
#Default: 1048576，单位为Byte
#传递非常大的事件可能导致minion消耗大量的内存
max_event_size: 1048576


#PING_ON_ROTATE
#Default: False
#告知master在AES密钥刷新后立即ping所有minion
ping_on_rotate: False


#MASTER_JOB_CACHE
#Default: local_cache
master_job_cache: redis


#ENFORCE_MINE_CACHE
#Default: False
enforce_mine_cache: False


#MAX_MINIONS
#Default: 0，表示不限制
#master允许连接的最大minion数
max_minions: 100


#CON_CACHE
#Default: False
#为所有连接提供缓存
con_cache: True


#PRESENCE_EVENTS
#Default: False
#master周期性地寻找主动连接的minion


#TRANSPORT
#Default: zeromq
#修改底层传输层
transport: zeromq


#TRANSPORT_OPTS
#Default: {}
#启用多个传输
transport_opts:
  tcp:
    publish_port: 4605
    ret_port: 4606
  zeromq: []


#MASTER_STATS
#Default: False


#MASTER_STATS_EVENT_ITER
#Default: 60


#SOCK_POOL_SIZE
#Default: 1
#为了避免将数据写入套接字是阻塞等待，启用salt应用程序的套接字池
sock_pool_size: 15


#IPC_MODE
#Default: ipc
ipc_mode: ipc


#TCP_MASTER_PUB_PORT
#Default: 4512
#ipc_mode的tcp端口
tcp_master_pub_port: 4512


#TCP_MASTER_PULL_PORT
#Default: 4513
#ipc_mode的tcp端口
tcp_master_pull_port: 4513


#TCP_MASTER_PUBLISH_PULL
#Default: 4514
tcp_master_publish_pull: 4514


#TCP_MASTER_WORKERS
#Default: 4515
# mworkers连接到master的端口
tcp_master_workers: 4515


#AUTH_EVENTS
#Default: True
auth_events: True


#MINION_DATA_CACHE_EVENTS
#Default: True
minion_data_cache_events: True

```

<br>

**salt-ssh配置**

```
#ROSTER
#Default: flat
#定义默认ROSTER模块
roster: cache


#ROSTER_FILE
#Default: /etc/salt/roster
roster_file: /root/roster


#ROSTERS
#Default: None
rosters:
 - /etc/salt/roster.d
 - /opt/salt/some/more/rosters


#SSH_PASSWD
#Default: ''
ssh_passwd: abc@123


#SSH_PORT
#Default: 22
ssh_port: 22


#SSH_SCAN_PORTS
#Default: 22
#多个值以逗号(,)分隔
ssh_scan_ports: 22


#SSH_SCAN_TIMEOUT
#Default: 0.01
ssh_scan_timeout: 0.01


#SSH_SUDO
#Default: False
ssh_sudo: False


#SSH_TIMEOUT
#Default: 60
ssh_timeout: 60


#SSH_USER
#Default: root
ssh_user: root


#SSH_LOG_FILE
#Default: /var/log/salt/ssh
ssh_log_file: /var/log/salt/ssh


#SSH_MINION_OPTS
#Default: None
ssh_minion_opts:
  gpg_keydir: /root/gpg


#SSH_USE_HOME_KEY
#Default: False
#使用~/.ssh/id_rsa对salt-ssh身份验证
ssh_use_home_key: False


#SSH_IDENTITIES_ONLY
#Default: False
ssh_identities_only: False


#SSH_LIST_NODEGROUPS
#Default: {}
ssh_list_nodegroups:
  groupA: minion1,minion2
  groupB: minion1,minion3


#THIN_EXTRA_MODS
#Default: None
#包含在salt thin中的附加模块


#MIN_EXTRA_MODS
#Default: None

```

<br>

**SECURITY 配置**

```
#OPEN_MODE
#Default: False
#open mode关闭认证并通知master接受所有身份认证
open_mode: False


#AUTO_ACCEPT
#Default: False
#自动接收所有来自minion的public key
auto_accept: False


#KEYSIZE
#Default: 2048
keysize: 2048


#AUTOSIGN_TIMEOUT
#Default: 120


#AUTOSIGN_FILE
#Default: not defined
#此文件中指定的传入key将自动被接受


#AUTOREJECT_FILE
#Default: not defined
#此文件中指定的传入key将自动被拒绝


#AUTOSIGN_GRAINS_DIR
#Default: not defined
autosign_grains_dir: /etc/salt/autosign_grains


#PERMISSIVE_PKI_ACCESS
#Default: False
permissive_pki_access: False


#PUBLISHER_ACL
#Default: {}
#允许master上用户执行特定模块
publisher_acl:
  fred:
    - test.ping
    - pkg.*


#PUBLISHER_ACL_BLACKLIST
#Default: {}
publisher_acl_blacklist:
  users:
    - root
    - '^(?!sudo_).*$'   #  all non sudo users
  modules:
    - cmd.*
    - test.echo


#SUDO_ACL
#Default: False
sudo_acl: False


#EXTERNAL_AUTH
#Default: {}
external_auth:
  pam:
    fred:
      - test.*


#TOKEN_EXPIRE
#Default: 43200(12h)
token_expire: 43200


#TOKEN_EXPIRE_USER_OVERRIDE
#Default: False
token_expire_user_override:
  pam:
    - fred
    - tom
  ldap:
    - gary


#KEEP_ACL_IN_TOKEN
#Default: False
keep_acl_in_token: False


#EAUTH_ACL_MODULE
#Default: ''
eauth_acl_module: django


#FILE_RECV
#Default: False
#允许minion将文件推送给master
file_recv: False


#FILE_RECV_MAX_SIZE
#Default: 100
file_recv_max_size: 100


#MASTER_SIGN_PUBKEY
#Default: False
#使用master公钥的加密签名来签署master认证回复
master_sign_pubkey: True


#MASTER_SIGN_KEY_NAME
#Default: master_sign
#自定义签名密钥的名称
master_sign_key_name: <filename_without_suffix>


#MASTER_PUBKEY_SIGNATURE
#Default: master_pubkey_signature
master_pubkey_signature: <filename>


#MASTER_USE_PUBKEY_SIGNATURE
#Default: False
master_use_pubkey_signature: True


#ROTATE_AES_KEY
#Default: True
#当salt-key删除一个minion-public时，轮询salt-master的AES-key
rotate_aes_key: True


#PUBLISH_SESSION
#Default: 86400
#master上AES key轮询之间的秒数
publish_session: Default: 86400


#SSL
#Default: None
#TLS/SSL连接项
ssl:
    keyfile: <path_to_keyfile>
    certfile: <path_to_certfile>
    ssl_version: PROTOCOL_TLSv1_2


#ALLOW_MINION_KEY_REVOKE
#Default: False
#默认情况下，当minion key被移除时，master会删除它的缓存数据
```

<br>

**大规模调整设置**

MASTER LARGE SCALE TUNING SETTINGS

```
#MAX_OPEN_FILES
#Default: 100000
#请注意ulimit
max_open_files: 100000


#WORKER_THREADS
#Default: 5
worker_threads: 5


#PUB_HWM
#Default: 1000
pub_hwm: 1000


#ZMQ_BACKLOG
#Default: 1000
#zeromq backlog的监听队列大小
zmq_backlog: 1000


#SALT_EVENT_PUB_HWM AND EVENT_PUBLISHER_PUB_HWM
salt_event_pub_hwm: 20000
event_publisher_pub_hwm: 10000

```

<br>


**模块管理**

```
#RUNNER_DIRS
#Default: []
runner_dirs:
  - /var/lib/salt/runners


#UTILS_DIRS
#Default: []
utils_dirs:
  - /var/lib/salt/utils


#CYTHON_ENABLE
#Default: False
cython_enable: False
```

<br>

**状态系统设置**
STATE SYSTEM


```
#STATE_TOP
#Default: top.sls
state_top: top.sls


#STATE_TOP_SALTENV
#无默认值
state_top_saltenv: dev


#TOP_FILE_MERGING_STRATEGY
#Default: merge
top_file_merging_strategy: same


#ENV_ORDER
#Default: []
env_order:
  - base
  - dev
  - qa

```

<br>

**文件服务器设置**
FILE SERVER

```


```

<br>

**PILLAR**

```


```

<br>

**REACTOR**

```



```

<br>

**SYNDIC SERVER**

```


```

<br>

**PEER PUBLISH**

```


```

<br>

**LOGGING**

```
#LOG_FILE
#Default: /var/log/salt/master
log_file: /var/log/salt/master


#LOG_LEVEL
#Default: warning
log_level: notice


#LOG_LEVEL_LOGFILE
#Default: warning
log_level_logfile: warning


#LOG_DATEFMT
#Default: %H:%M:%S
log_datefmt: '%H:%M:%S'


#LOG_DATEFMT_LOGFILE
#Default: %Y-%m-%d %H:%M:%S
log_datefmt_logfile: '%Y-%m-%d %H:%M:%S'


#LOG_FMT_CONSOLE
#Default: [%(levelname)-8s] %(message)s
log_fmt_console: '%(colorlevel)s %(colormsg)s'
log_fmt_console: '[%(levelname)-8s] %(message)s'


#LOG_FMT_LOGFILE
#Default: %(asctime)s,%(msecs)03d [%(name)-17s][%(levelname)-8s] %(message)s
log_fmt_logfile: '%(asctime)s,%(msecs)03d [%(name)-17s][%(levelname)-8s] %(message)s'


#LOG_GRANULAR_LEVELS
#Default: {}

```

<br>

**NODE GROUPS**
雨荨minion进行逻辑分组

```
#NODE GROUPS
#Default: {}
nodegroups:
  group1: 'L@foo.domain.com,bar.domain.com,baz.domain.com or bl*.domain.com'
  group2: 'G@os:Debian and foo.domain.com'
  group3: 'G@os:Debian and N@group1'
  group4:
    - 'G@foo:bar'
    - 'or'
    - 'G@foo:baz'
```

<br>

**RANGE CLUSTER**

```
#RANGE_SERVER
#Default: 'range:80'
range_server: range:80
```

<br>

**INCLUDE CONFIGURATION**

```
#DEFAULT_INCLUDE
#Default: master.d/*.conf


#INCLUDE
#Default: not defined
# Include files from a master.d directory in the same
# directory as the master config file
include: master.d/*

# Include a single extra file into the configuration
include: /etc/roles/webserver

# Include several files and the master.d directory
include:
  - extra_config
  - master.d/*
  - /etc/roles/webserver

```

<br>

**KEEPALIVE**

```
#TCP_KEEPALIVE
#Default: True
tcp_keepalive: True


#TCP_KEEPALIVE_CNT
#Default: -1
#Sets the ZeroMQ TCP keepalive count
tcp_keepalive_cnt: -1


#TCP_KEEPALIVE_IDLE
#Default: 300


#TCP_KEEPALIVE_INTVL
#Default: -1

```



<br/>
<br/>



## minion配置


**基础配置**

```
#MASTER
#Default: salt
master: salt

#MASTER:PORT SYNTAX
#master: localhost:1234
#master: '[2001:db8:85a3:8d3:1319:8a2e:370:7348]:1234'


#LIST OF MASTERS SYNTAX
#需启用multi-master模式
master:
  - address1
  - address2
master_type: failover



```

<br>

** EXECUTION MODULE**

```


```

<br>

**TOP FILE**

```



```

<br>

**STATE**

```



```

<br>

**FILE DIRECTORY**

```


```

<br>

**PILLAR**

```



```

<br>

**SECURITY**

```


```

<br>

**REACTOR**

```


```

<br>

**THREAD**

```


```

<br>

**LOGGING**

```


```

<br>

**INCLUDE**

```
#DEFAULT_INCLUDE
#Default: minion.d/*.conf


#INCLUDE
#Default: not defined
```

<br>

**KEEPALIVE**

```


```

<br>

**FROZEN BUILD UPDATE**

```


```



<br/>
<br/>



## proxy minion配置

`/etc/salt/minion`

```
#ADD_PROXYMODULE_TO_OPTS
#Default: False
add_proxymodule_to_opts: True


#PROXY_MERGE_GRAINS_IN_MODULE
#Default: True


#PROXY_KEEP_ALIVE
#Default: True
#死亡时是否重启与远程设备的连接
proxy_keep_alive: False


#PROXY_KEEP_ALIVE_INTERVA
#Default: 1(min)
#keepalive检查频率
proxy_keep_alive_interval: 5


#PROXY_ALWAYS_ALIVE
#Default: True
proxy_always_alive: False


#PROXY_MERGE_PILLAR_IN_OPTS
#Default: False


#PROXY_DEEP_MERGE_PILLAR_IN_OPTS
#Default: False


#PROXY_MERGE_PILLAR_IN_OPTS_STRATEGY
#Default: smart


#PROXY_MINES_PILLAR
#Default: True
```



<br/>
<br/>



## minion blackout配置

当一个minion处于blackout mode时，所有远程执行命令都被禁用。

minion blackout mode通过pillar key——`minion_blackout`进行配置。如果此为True，则minion将拒绝除`saltutil.refresh_pillar`命令外的所有传入命令。
它也支持whitelist:

```
minion_blackout_whitelist:
  - test.ping
  - pillar.get
```



<br/>
<br/>


## 访问控制系统

ACCESS CONTROL SYSTEM


































