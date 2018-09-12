---

title: Prometheus
date: 2018-09-11 11:01:12
categories: DevOps
tags:
  - Prometheus
  - Monitoring

---


参考：

- Prometheus文档： <https://prometheus.io/docs>
- GitHub: <https://github.com/prometheus/>

环境：

- CentOS7x86_64
- Prometheus v2.3

<br>

<!--more-->

![Prometheus](/images/Prometheus/prometheus.jpg)


<br/>
<br/>

---

<br/>
<br/>




# 介绍

Introduction


<br/>


## 概述


<br/>


### Prometheus是什么

What is Prometheus?


Prometheus是一个最初在SoundCloud上构建的**开源监控系统和报警工具包**。现在是一个独立的开源项目，由社区进行维护。

<br>

**功能(Features)**
Prometheus的主要特点：

- 具有由度量名称(metric name)和键值对(key-value)标识的时间序列(time series)数据的多维(multi-dimensional)数据模型
- 灵活的查询语言，以利用此维度
- 不依赖分布式存储(distributed storage)，单个服务器节点是自治的(autonomous)
- 时间序列集合通过HTPP的`pull model`发生
- `push`时间序列通过中间网关(intermediary gateway)的支持
- 通过服务发现或静态配置来发现目标
- 图形和仪表盘支持多种模式

<br>

**组件(Components)**
Prometheus系统由多个组件构成，其中某些组件是可选的：

- 主要的**Prometheus Server**，用于存储时间序列数据
- **client libraries**，用于检测应用程序代码
- **push gateway**，用于支持短暂的(short-lived)工作
- **exporters**，用于服务的特殊目的
- **alertmanager**，用于处理报警
- 各种支持工具

<br>

**架构(Architecture)**
Prometheus的体系结构和系统组件图：

![Prometheus架构图](/images/Prometheus/architecture.png)


<br/>
<br/>


### 什么时候适合

When does it fit?


Prometheus适用于记录任何纯数字时间序列。它既适用于以机器为中心的监控，也适用于高度动态的面向服务架构的监控。在微服务的世界中，它对多维数据收集和查询的支持是一种特殊的优势。
Prometheus专为提高可靠性而设计，是你在断电期间可以快速诊断问题的系统。每个Prometheus Server都是独立的，不依赖于网络存储或其它远程服务。当基础架构其它部分损坏时，你仍可以依赖它，并且你不需要设置大量的基础架构来使用它。


<br/>
<br/>


### 什么时候不适合

When does it not fit?


Prometheus重视可靠性。即使在系统故障情况下，你也可以随时查看有关系统的可用统计信息。如果你需要100%的准确度，Prometheus不是一个好的选择，你可能需要使用其它系统。



<br/>
<br/>
<br/>



## 术语

GLOSSARY





<br/>
<br/>

---

<br/>
<br/>



# PROMETHEUS


<br/>


## 入门

GETTING STARTED


本节介绍如何安装，配置，使用Prometheus的简单例子。你将在本地安装和运行Prometheus，将其配置为自我填充和示例应用程序，然后使用查询，规则和图表来使用收集的序列数据。

<br>

**下载**

下载地址: <https://prometheus.io/download/>

```
tar xvfz prometheus-*.tar.gz

cd prometheus-*
```

<br>

**配置和监控**
Prometheus通过在目标上通过HTTP endPoints来抓取指标，来收集受监控目标的指标。由于Prometheus也以相同的方式公开自身数据，它也可以获取和监测自身的健康状况。
虽然Prometheus Server只收集有关自身的数据在实践中不是很有用，但它是一个很好的示例。如`prometheus.yml`示例配置文件：

```yaml
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']
```

<br>

**启动**
启动后，可访问9090端口查看状态。可访问`localhost:9090/metrics`查看有关自身的相关指标。

```
cd prometheus-2.3.2.linux-amd64
./prometheus --config.file="prometheus.yml"
```

![9090](/images/Promethues/9090.png)

<br>

**使用表达式浏览器**
让我们看一下Prometheus收集的一些数据。要使用Prometheus的内建表达式浏览器(expression browser)，请跳转到`http://localhost:9090/graph`并选择`Graph -> Console`，在其中输入表达式。
绘制表达式图形同样在此操作。

```
#表达式
prometheus_target_interval_length_seconds


#表达式
prometheus_target_interval_length_seconds{quantile="0.99"}


#计算返回的时间序列数
count(prometheus_target_interval_length_seconds)
```

![表达式结果](/images/Prometheus/expression01.png)

![表达式图形](/images/Prometheus/expression02.png)

<br>

**启动简单的目标**
启动一些示例目标让Prometheus获取。
确保已安装Go表一起并设置了正常的GO PATH。

```
mkdir ./sample && cd sample

git clone https://github.com/prometheus/client_golang.git
cd client_golang/examples/random
go get -d
go build


# Start 3 example targets in separate terminals:
./random -listen-address=:9091
./random -listen-address=:9092
./random -listen-address=:9093


#访问
http://localhost:9091/metrices
http://localhost:9092/metrices
http://localhost:9093/metrices
```

<br>

**监控示例目标**
现在需要配置Prometheus来抓取目标。

```yaml
scrape_configs:
  - job_name:       'example-random'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:8080', 'localhost:8081']
        labels:
          group: 'production'

      - targets: ['localhost:8082']
        labels:
          group: 'canary'
```

重启Prometheus，检测`rpc_durations_seconds` metric来验证。

<br>

**配置规则**
Configure rules for aggregating scraped data into new time series

聚合超过数千个时间序列的查询在计算`ad-hoc`时会变慢。为了提高效率，Prometheus允许你通过配置的规则将预录表达式预先记录到全新的持久时间序列中。

创建规则文件`prometheus.rules.yml`：
```
#job_service:rpc_durations_seconds_count:avg_rate5m
groups:
- name: example
  rules:
  - record: job_service:rpc_durations_seconds_count:avg_rate5m
    expr: avg(rate(rpc_durations_seconds_count[5m])) by (job, service)
```

要是Prometheus选择此新规则，需要修改Prometheus配置：

```
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # Evaluate rules every 15 seconds.

  # Attach these extra labels to all timeseries collected by this Prometheus instance.
  external_labels:
    monitor: 'codelab-monitor'

rule_files:
  - 'prometheus.rules.yml'

scrape_configs:
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:9090']

  - job_name:       'example-random'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['localhost:8091', 'localhost:8092']
        labels:
          group: 'production'

      - targets: ['localhost:9093']
        labels:
          group: 'canary'
```

重启Prometheus，使用`job_service:rpc_durations_seconds_count:avg_rate5m` metric验证。


<br/>
<br/>


## 安装




































