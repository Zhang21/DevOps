---
title: Kubernetes
date: 2018-06-26 11:38:33
tags:
  - Kubernetes
  - k8s
categories: DevOps
---

参考：

- Kubernetes: <https://zh.wikipedia.org/wiki/Kubernetes>
- 官方文档: <https://kubernetes.io/docs/>
- 中文文档: <http://docs.kubernetes.org.cn/>
- GitHub: <https://github.com/kubernetes/kubernetes>
- etcd: <https://coreos.com/etcd/docs/latest/>
- flannel: <https://coreos.com/flannel/docs/latest/>

环境：

- CentOS7x86_64
- Kubernetes v1.11


<br/>
<br/>

<!--more-->

---

<br/>


![Kubernetes](/images/K8s/Kubernetes_logo.png)

<br/>



# 配置

此章节提供了有关安装k8s和配置k8s集群的相关说明。


<br/>


## 安装

有几种方式创建k8s集群：

- minikube(自动部署)
- kubeadm(自动部署)
- 软件包(建议初学者使用此方式)


<br/>


### 使用minikube创建集群

Using Minikube to Create a Cluster


目标：

- 了解k8s集群是什么
- 了解Minikube是什么
- 启动一个k8s集群

<br>

**k8s 集群**
k8s协调一个高度可用的计算机集群，它们连接起来作为一个单元工作 。
k8s以更有效的方式自动化跨集群分发和调整应用程序容器。

k8s集群包含两种类型的资源：

- Master
- Nodes

Master负责管理集群。它协调集群中的所有活动。
Node是工作主机。每个节点有一个Kubelet的Agent，负责管理节点并与Master(API)通信。此外，节点上还应有处理容器操作的工具(如Docker)。生成环境的k8s集群至少有三个节点。
用户可通过k8s API直接与集群进行交互。

<br>

使用Minikube部署集群: <https://github.com/kubernetes/minikube>
Minikube是一个工具，它运行一个单节点的k8s集群供开发用户使用。

**Linux平台**

```sh
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 && \
chmod +x minikube && \
sudo mv minikube /usr/local/bin/

##安装kubectl
curl -Lo kubectl https://storage.googleapis.com/kubernetes-release/release/v1.10.0/bin/linux/amd64/kubectl && \
chmod +x kubectl && \
sudo mv kubectl /usr/local/bin/


minikube version
minikube start

kubectl version
kubectl cluster-info
kubectl get nodes
```


<br/>
<br/>


### kubeadm创建集群


#### 安装kubeadm

本节介绍了如何安装**kubeadm**工具。

**安装前**

- 2GB RAM+
- 2 cpus+
- 集群主机网络互通
- node上唯一的主机名，MAC，UUID
- 开放特定端口(防火墙)
- Swap disabled。必须关闭swap才能使kubelet正常工作。

<br>

**验证MAC或UUID对每个node都是唯一的**

- `ifconfig -a`获取MAC
- `cat /sys/class/dmi/id/product_uuid`查看UUID

<br>

**检查网络适配器**

如果k8s组件不可达，请手动添加路由。

<br>

**检查需要的端口**

```
#master
Protocol    Direction	Port Range	Purpose					Used By
TCP    Inbound		6443*		Kubernetes API server	All
TCP    Inbound		2379-2380	etcd server client API	kube-apiserver, etcd
TCP    Inbound		10250		Kubelet API				Self, Control plane
TCP    Inbound		10251		kube-scheduler			Self
TCP	   Inbound		10252		kube-controller-manager	Self


#worker
Protocol	Direction	Port Range	Purpose			Used By
TCP		Inbound		10250		Kubelet API		Self, Control plane
TCP		Inbound		30000-32767	NodePort Services**	All

```

<br>

**安装docker**
使用阿里云镜像。
`kubeadm v1.11.1`最高支持`Docker 17.03`，请注意。

```sh
wget https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
mv docker-ce.repo /etc/yum.repos.d

yum install -y docker-ce.x84_64

#由于kubeadm不支持最新版的docker，所以需要安装指定版本
yum list docker-ce --showduplicates

yum install -y docker-ce-17.03.2.ce
```

<br>

**安装kubeadm, kubelet, kubectl**

- kubeadm: 引导集群
- kubelet: k8s agent
- kubectl: command line

```sh
#创建repo
cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

#国外镜像凉凉，所以换用阿里云

cat <<EOF > /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF



#禁用防火墙
systemctl stop firewalld
systemctl disable firewalld



#关闭selinux
setenforce 0
sed -i "s/^SELINUX=permissive/SELINUX=disabled/g" /etc/selinux/config



#关闭swap，否则kubelet无法正常使用
swapoff -a
#将/etc/fstab中swap注释掉
sed -i 's/.*swap.*/#&/' /etc/fstab



#安装
yum install -y epel-release ebtables ethtool



yum install -y kubelet kubeadm kubectl
systemctl enable kubelet && systemctl start kubelet


#系统配置，开启网络桥接
cat <<EOF >  /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF

#生效
sysctl -p /etc/sysctl.d/k8s.conf
sysctl --system
systemctl daemon-reload



#各主机时区，时间同步
timedatectl set-timezone Asia/Shanghai

#crontab -e
#ntp
*/30 * * * * /sbin/ntpdate 1.cn.pool.ntp.org > /dev/null 2>&1



#hosts
<master-ip> master
<node-ip> node
```

<br>

**配置cgroup driver**
使用docker时，kubelet会将其驱动设置与Docker相同。kubeadm会自动检查kubelet的cgroup驱动，并在运行时将其设置到`/var/lib/kubelet/kubeadm-flags.env`文件。

```sh
docker info | grep -i 'cgroup driver'
Cgroup Driver: systemd


#此文件是kubeadm init生成的
cat /var/lib/kubelet/kubeadm-flags.env
KUBELET_KUBEADM_ARGS=--cgroup-driver=systemd --cni-bin-dir=/opt/cni/bin --cni-conf-dir=/etc/cni/net.d --network-plugin=cni


#如果此文件未配置此信息，我们手动添加
cd /etc/systemd/system/kubelet.service.d
vim 10-kubeadm.conf
KUBELET_KUBEADM_ARGS=--cgroup-driver=systemd --cni-bin-dir=/opt/cni/bin --cni-conf-dir=/etc/cni/net.d --network-plugin=cni
```


<br/>
<br/>


#### 拉取k8s.gcr.io镜像

链接: <https://console.cloud.google.com/gcr/images/google-containers/GLOBAL?location=GLOBAL&project=google-containers>

利用某台能上网的主机，拉取Google上kubeadm需要的`k8s.gcr.io/image`镜像。

<br>

```
#查看kubeadm需要使用的image
kubeadm config images list

k8s.gcr.io/kube-apiserver-amd64:v1.11.1
k8s.gcr.io/kube-controller-manager-amd64:v1.11.1
k8s.gcr.io/kube-scheduler-amd64:v1.11.1
k8s.gcr.io/kube-proxy-amd64:v1.11.1
k8s.gcr.io/pause-amd64:3.1
k8s.gcr.io/etcd-amd64:3.2.18
k8s.gcr.io/coredns:1.1.3


#最好把所有镜像都拉下来，否则后面初始化的时候容易报错
#在gcr.io上查找镜像
#浏览器访问: <https://console.cloud.google.com/gcr/images/google-containers/GLOBAL?location=GLOBAL&project=google-containers>


#找一台能用的服务器，将这些image拉下来，推到自己的repo上再在kubeadm机器上拉取镜像，之后tag成kubeadm需要的格式
#写一个脚本自动拉取镜像，更名镜像，推送镜像
#我基本上把全部镜像都拉了
vim k8sImages.sh

images=(
coredns:1.1.3
etcd-amd64:3.1.15
etcd-amd64:3.1.16
etcd-amd64:3.1.17
etcd-amd64:3.2.17
etcd-amd64:3.2.18
flannel-amd64:0.5.5
heapster-amd64:v1.4.0
heapster-amd64:v1.4.1
heapster-amd64:v1.4.2
heapster-amd64:v1.4.3
heapster-amd64:v1.5.0
heapster-amd64:v1.5.1
heapster-amd64:v1.5.2
heapster-amd64:v1.5.3
heapster-amd64:v1.5.4
heapster-grafana-amd64:v4.4.3
heapster-grafana-amd64:v5.0.4
heapster-influxdb-amd64:v1.3.3
heapster-influxdb-amd64:v1.5.2
k8s-dns-dnsmasq-nanny-amd64:1.14.10
k8s-dns-dnsmasq-nanny-amd64:1.14.6
k8s-dns-dnsmasq-nanny-amd64:1.14.7
k8s-dns-dnsmasq-nanny-amd64:1.14.8
k8s-dns-dnsmasq-nanny-amd64:1.14.9
k8s-dns-kube-dns-amd64:1.14.10
k8s-dns-kube-dns-amd64:1.14.5
k8s-dns-kube-dns-amd64:1.14.6
k8s-dns-kube-dns-amd64:1.14.7
k8s-dns-kube-dns-amd64:1.14.8
k8s-dns-kube-dns-amd64:1.14.9
k8s-dns-sidecar-amd64:1.14.10
k8s-dns-sidecar-amd64:1.14.5
k8s-dns-sidecar-amd64:1.14.6
k8s-dns-sidecar-amd64:1.14.7
k8s-dns-sidecar-amd64:1.14.8
k8s-dns-sidecar-amd64:1.14.9
kube-apiserver-amd64:v1.10.5
kube-apiserver-amd64:v1.10.6
kube-apiserver-amd64:v1.11.0
kube-apiserver-amd64:v1.11.1
kube-apiserver-amd64:v1.9.10
kube-controller-manager-amd64:v1.10.5
kube-controller-manager-amd64:v1.10.6
kube-controller-manager-amd64:v1.11.0
kube-controller-manager-amd64:v1.11.1
kube-controller-manager-amd64:v1.9.10
kube-proxy-amd64:v1.10.6
kube-proxy-amd64:v1.11.0
kube-proxy-amd64:v1.11.1
kube-proxy-amd64:v1.9.10
kubernetes-dashboard-amd64:v1.6.2
kubernetes-dashboard-amd64:v1.6.3
kubernetes-dashboard-amd64:v1.7.0
kubernetes-dashboard-amd64:v1.7.1
kubernetes-dashboard-amd64:v1.8.0
kubernetes-dashboard-amd64:v1.8.1
kubernetes-dashboard-amd64:v1.8.2
kubernetes-dashboard-amd64:v1.8.3
kube-scheduler-amd64:v1.10.6
kube-scheduler-amd64:v1.11.0
kube-scheduler-amd64:v1.11.1
kube-scheduler-amd64:v1.9.10
pause-amd64:3.0
pause-amd64:3.1
pause:3.1
)

#可能pause与pause-amd64是一个，到时只需拉一个，然后tag

for image in ${images[@]}
do
    docker pull k8s.gcr.io/${image}
    docker tag k8s.gcr.io/${image} zhang21/${image}
    docker image rm k8s.gcr.io/${image}
    docker push zhang21/${image}
done



#查看
docker image ls

#到我的docker-hub中查看
#https://hub.docker.com/u/zhang21/


#现在在kubeadm集群机器上操作
#还是写一个脚本来拉取镜像，更名镜像，删除镜像
vim k8sImage.sh

images=(
coredns:1.1.3
etcd-amd64:3.1.15
etcd-amd64:3.1.16
etcd-amd64:3.1.17
etcd-amd64:3.2.17
etcd-amd64:3.2.18
flannel-amd64:0.5.5
heapster-amd64:v1.4.0
heapster-amd64:v1.4.1
heapster-amd64:v1.4.2
heapster-amd64:v1.4.3
heapster-amd64:v1.5.0
heapster-amd64:v1.5.1
heapster-amd64:v1.5.2
heapster-amd64:v1.5.3
heapster-amd64:v1.5.4
heapster-grafana-amd64:v4.4.3
heapster-grafana-amd64:v5.0.4
heapster-influxdb-amd64:v1.3.3
heapster-influxdb-amd64:v1.5.2
k8s-dns-dnsmasq-nanny-amd64:1.14.10
k8s-dns-dnsmasq-nanny-amd64:1.14.6
k8s-dns-dnsmasq-nanny-amd64:1.14.7
k8s-dns-dnsmasq-nanny-amd64:1.14.8
k8s-dns-dnsmasq-nanny-amd64:1.14.9
k8s-dns-kube-dns-amd64:1.14.10
k8s-dns-kube-dns-amd64:1.14.5
k8s-dns-kube-dns-amd64:1.14.6
k8s-dns-kube-dns-amd64:1.14.7
k8s-dns-kube-dns-amd64:1.14.8
k8s-dns-kube-dns-amd64:1.14.9
k8s-dns-sidecar-amd64:1.14.10
k8s-dns-sidecar-amd64:1.14.5
k8s-dns-sidecar-amd64:1.14.6
k8s-dns-sidecar-amd64:1.14.7
k8s-dns-sidecar-amd64:1.14.8
k8s-dns-sidecar-amd64:1.14.9
kube-apiserver-amd64:v1.10.5
kube-apiserver-amd64:v1.10.6
kube-apiserver-amd64:v1.11.0
kube-apiserver-amd64:v1.11.1
kube-apiserver-amd64:v1.9.10
kube-controller-manager-amd64:v1.10.5
kube-controller-manager-amd64:v1.10.6
kube-controller-manager-amd64:v1.11.0
kube-controller-manager-amd64:v1.11.1
kube-controller-manager-amd64:v1.9.10
kube-proxy-amd64:v1.10.6
kube-proxy-amd64:v1.11.0
kube-proxy-amd64:v1.11.1
kube-proxy-amd64:v1.9.10
kubernetes-dashboard-amd64:v1.6.2
kubernetes-dashboard-amd64:v1.6.3
kubernetes-dashboard-amd64:v1.7.0
kubernetes-dashboard-amd64:v1.7.1
kubernetes-dashboard-amd64:v1.8.0
kubernetes-dashboard-amd64:v1.8.1
kubernetes-dashboard-amd64:v1.8.2
kubernetes-dashboard-amd64:v1.8.3
kube-scheduler-amd64:v1.10.6
kube-scheduler-amd64:v1.11.0
kube-scheduler-amd64:v1.11.1
kube-scheduler-amd64:v1.9.10
pause-amd64:3.0
pause-amd64:3.1
pause:3.1
)

for image in ${images[@]}
do
    docker pull zhang21/${image}
    docker tag zhang21/${image} k8s.gcr.io/${image}
    docker image rm zhang21/${image}
done


#查看
docker image ls
```



<br/>
<br/>


#### 创建单master集群

`kubeadm`可帮助你引导符合最佳实践的最小化可行的k8s集群。使用`kubeadm`，你的集群应通过k8s一致性测试。`kubeadm`还支持其它集群生命周期功能，如升级、降级和管理引导令牌(bootstrap token)。
`kubeadm`旨在成为新用户开始尝试k8s的一种简单方法。可使用deb/rpm软件包在系统上轻松安装`kubeadm`。
因为你可在各种类型的机器上安装`kubeadm`，所以它非常适合于Ansible/Salt等配置系统集成。

`kubeadm`的简单性意味着它可以服务于各种用例：

- 新用户可以从`kubeadm`开始，第一次尝试k8s
- 熟悉k8s的用户可以使用`kubeadm`启动集群，并测试他们的应用程序
- 较大的项目可以包括`kubeadm`作为更复杂系统中的构件，也可以包括其它安装程序工具

kubeadm Maturity(成熟度)

| Area | Maturity Level |
| - | - | - |
| Command line UX | beta |
| Implementation | beta |
| Config file API | alpha |
| Self-hosting | alpha |
| kubeadm alpha subcommands | alpha |
| CoreDNS | GA |
| DynamicKubeletConfig | alpha |

kubeadm的整体功能状态为Beta，并将很快添加到GA(General Availability)。一些子功能，如自托管(self-hosting)和配置文件API仍在积极开发中。

k8s版本通常支持九个月，这也适用于kubeadm。

| Kubernetes version | Release month | End-of-life-month |
| - | - | - |
| v1.6.x | March 2017 | December 2017 |
| v1.7.x | June 2017 | March 2018 |
| v1.8.x | September 2017 | June 2018 |
| v1.9.x | December 2017 | September 2018   |
| v1.10.x | March 2018 | December 2018   |
| v1.11.x | June 2018 | March 2019   |

<br>

**开始前**

- 一台或多台主机
- 2GB+ RAM(每台机器)
- 2CPUs+(master)
- 网络互通

<br>

**目标**

- 安装 **单master/高可用性** 的k8s集群
- 在集群上安装pod-network，以便pod间可互相通信

<br>

**组件**

```
#Master
etcd
kube-apisever
kube-controller-manager
kube-scheduler
kube-flannel
kube-proxy
kube-dns
kubectl


#Node
kube-flannel
kube-proxy
kubectl
```

<br>

**说明**

- 安装kubeadm
如已安装，可升级到最新版。

<br>

- 初始化集群
master主机是控制组件运行的地方，包括`etcd`, `API server`...

```
#1
#选择一个 pod network add-on，并验证是够需要将任何参数传递给kubeadm初始化。你可以使用--pod-network-cidr来指定特定值
#这里使用flannel


#2，可选
#除非另有说明，否则kubeadm使用与默认网关关联的网络接口来通告master
#使用kubeadm init --apiserver-advertise-address=<ip-addr>来使用不同网络接口


#3，可选
#在kubeadm init之前运行kubeadm config images pull以验证与gcr.io的连接
#或kubeadm config images list查看需要的镜像


#运行
kubeadm init <args>
```

<br>

- 更多信息
`kubeadm init`首先运行一系列检查，以确保机器 已准备好运行k8s。这些预检查会显示警告并退出错误。然后`kubeadm init`下载并安装集群控制组件。这可能需要一些时间。

```
kubeadm --help
kubeadm init --help



#k8s底层环境依赖于Docker
#on master
systemctl enable docker kubelet && systemctl start docker
kubeadm init

I0806 14:04:54.415853    2191 feature_gate.go:230] feature gates: &{map[]}
[init] using Kubernetes version: v1.11.1
[preflight] running pre-flight checks
        [WARNING Service-Docker]: docker service is not enabled, please run 'systemctl enable docker.service'
I0806 14:04:54.433879    2191 kernel_validator.go:81] Validating kernel version
I0806 14:04:54.433934    2191 kernel_validator.go:96] Validating kernel config
[preflight/images] Pulling images required for setting up a Kubernetes cluster
[preflight/images] This might take a minute or two, depending on the speed of your internet connection
[preflight/images] You can also perform this action in beforehand using 'kubeadm config images pull'


[preflight] Some fatal errors occurred:
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/kube-apiserver-amd64:v1.11.1]: exit status 1
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/kube-controller-manager-amd64:v1.11.1]: exit status 1
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/kube-scheduler-amd64:v1.11.1]: exit status 1
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/kube-proxy-amd64:v1.11.1]: exit status 1
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/pause-amd64:3.1]: exit status 1
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/etcd-amd64:3.2.18]: exit status 1
        [ERROR ImagePull]: failed to pull image [k8s.gcr.io/coredns:1.1.3]: exit status 1
[preflight] If you know what you are doing, you can make a check non-fatal with `--ignore-preflight-errors=...`


#此处错误，由于镜像在Google，国内访问会超时。因此需要额外准备镜像。
#需要做上面一步操作来拉取镜像



#初始化
#请确保资源满足条件，我就是由于VM内存为1GB而导致初始化失败，找了很久才找到这个错误

kubeadm init --kubernetes-version=v1.11.1 --pod-network-cidr=10.244.0.0/16

[init] using Kubernetes version: v1.11.1
[preflight] running pre-flight checks
I0807 14:47:10.658405   10612 kernel_validator.go:81] Validating kernel version
I0807 14:47:10.658484   10612 kernel_validator.go:96] Validating kernel config
[preflight/images] Pulling images required for setting up a Kubernetes cluster
[preflight/images] This might take a minute or two, depending on the speed of your internet connection
[preflight/images] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[preflight] Activating the kubelet service
[certificates] Generated ca certificate and key.
[certificates] Generated apiserver certificate and key.
[certificates] apiserver serving cert is signed for DNS names [master kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 192.168.31.49]
[certificates] Generated apiserver-kubelet-client certificate and key.
[certificates] Generated sa key and public key.
[certificates] Generated front-proxy-ca certificate and key.
[certificates] Generated front-proxy-client certificate and key.
[certificates] Generated etcd/ca certificate and key.
[certificates] Generated etcd/server certificate and key.
[certificates] etcd/server serving cert is signed for DNS names [master localhost] and IPs [127.0.0.1 ::1]
[certificates] Generated etcd/peer certificate and key.
[certificates] etcd/peer serving cert is signed for DNS names [master localhost] and IPs [192.168.31.49 127.0.0.1 ::1]
[certificates] Generated etcd/healthcheck-client certificate and key.
[certificates] Generated apiserver-etcd-client certificate and key.
[certificates] valid certificates and keys now exist in "/etc/kubernetes/pki"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/admin.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/kubelet.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/controller-manager.conf"
[kubeconfig] Wrote KubeConfig file to disk: "/etc/kubernetes/scheduler.conf"
[controlplane] wrote Static Pod manifest for component kube-apiserver to "/etc/kubernetes/manifests/kube-apiserver.yaml"
[controlplane] wrote Static Pod manifest for component kube-controller-manager to "/etc/kubernetes/manifests/kube-controller-manager.yaml"
[controlplane] wrote Static Pod manifest for component kube-scheduler to "/etc/kubernetes/manifests/kube-scheduler.yaml"
[etcd] Wrote Static Pod manifest for a local etcd instance to "/etc/kubernetes/manifests/etcd.yaml"
[init] waiting for the kubelet to boot up the control plane as Static Pods from directory "/etc/kubernetes/manifests" 
[init] this might take a minute or longer if the control plane images have to be pulled
[apiclient] All control plane components are healthy after 42.001662 seconds
[uploadconfig] storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.11" in namespace kube-system with the configuration for the kubelets in the cluster
[markmaster] Marking the node master as master by adding the label "node-role.kubernetes.io/master=''"
[markmaster] Marking the node master as master by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[patchnode] Uploading the CRI Socket information "/var/run/dockershim.sock" to the Node API object "master" as an annotation
[bootstraptoken] using token: uzdl9x.91uu2p155jczkgb3
[bootstraptoken] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstraptoken] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstraptoken] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstraptoken] creating the "cluster-info" ConfigMap in the "kube-public" namespace
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes master has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

You can now join any number of machines by running the following on each node
as root:

  kubeadm join 192.168.31.49:6443 --token uzdl9x.91uu2p155jczkgb3 --discovery-token-ca-cert-hash sha256:bc5af0f4fbee0d0500c9d6782a279ee172ed45547a006136bfbad93d61ad39c7





#root用户
#一定要记得做此步骤，由于kubeadm设置的apiserver的监听端口为6443，而不是8080，所以执行会报错。
export KUBECONFIG=/etc/kubernetes/admin.conf
#之后，可将其写入/etc/profile



#安装pod-network
#你必须先安装pod network add-on，才能和pod相互通信。
#必须在应用程序之前部署网络。
#配置flannel
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/v0.10.0/Documentation/kube-flannel.yml
#如果无法访问，可将此文件下载到本地
#kubectl apply -f /etc/kubernetes/kube-flannel.yml

clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.extensions/kube-flannel-ds created



#token用于master与node之间相互认证，它是加密的。
#使用kubeadm token列出、创建和删除token
#kubeadm token create
#kubeadm token list



#on node
#kubeadm join
#kubeadm join --token xxxxxxxxxxx host:port
systemctl enable kubelet docker && systemctl start docker
kubeadm join 192.168.31.49:6443 --token uzdl9x.91uu2p155jczkgb3 --discovery-token-ca-cert-hash sha256:bc5af0f4fbee0d0500c9d6782a279ee172ed45547a006136bfbad93d61ad39c7




#测试
kubectl get node

NAME      STATUS    ROLES     AGE       VERSION
master    Ready     master    48m       v1.11.1
node      Ready     <none>    15m       v1.11.1

#查看
kubectl get pods --all-namespaces -o wide
NAMESPACE     NAME                             READY     STATUS    RESTARTS   AGE       IP               NODE
kube-system   coredns-78fcdf6894-hn46d         1/1       Running   0          52m       10.244.0.3       master
kube-system   coredns-78fcdf6894-wqxbx         1/1       Running   0          52m       10.244.0.2       master
kube-system   etcd-master                      1/1       Running   0          41m       192.168.31.49    master
kube-system   kube-apiserver-master            1/1       Running   0          41m       192.168.31.49    master
kube-system   kube-controller-manager-master   1/1       Running   0          41m       192.168.31.49    master
kube-system   kube-flannel-ds-7gbvd            1/1       Running   0          41m       192.168.31.49    master
kube-system   kube-flannel-ds-ktkxp            1/1       Running   0          19m       192.168.31.174   node
kube-system   kube-proxy-pw7gz                 1/1       Running   0          19m       192.168.31.174   node
kube-system   kube-proxy-rhrks                 1/1       Running   0          52m       192.168.31.49    master
kube-system   kube-scheduler-master            1/1       Running   0          41m       192.168.31.49    master

```

<br>

- master isolation
默认情况下，出于安全原因，你的集群不会在master上调度pod。如果你想在master上调度pod，对于单master的k8s集群，执行如下命令：

```
#从拥有它的节点删除node-role.kubernetes.io/master污染
kubectl taint nodes --all node-role.kubernetes.io/master-

```

<br>

- 加入节点
要向集群添加新节点，请为每台计算机执行以下操作：

```
#node

#root/sudo

#kubeadm init后执行下命令
#kubeadm token list
kubeadm join --token <token> <master-ip>:<master-port> --discovery-token-ca-cert-hash sha256:<hash>
```

<br>

- 从master之外控制集群(可选)

```
scp root@<master-ip>:/etc/kubernetes/admin.conf .
kubeclt --kubeconfig ./admin.conf get nodes
```

<br>

**局限性**
此处创建的集群只有一个master，其上运行一个etcd数据库。这意味着如果master出现故障，你的集群可能会丢失数据。可考虑向k8s添加高可用支持。


<br/>
<br/>



#### 使用kubeadm配置kubelet

Configuring each kubelet in your cluster using kubeadm


`kubeadm CLI`工具的生命周期与`Kubernetes Node  Agent(kubelet)`相分离，kubelet是运行在k8s集群master/node上的守护进程，它始终在后台运行。而`kubeadm CLI`工具由用户执行。
由于`kubelet`是一个守护进程，它需要由`init system`或服务管理器来维护。Redhat7上使用`systemd`来进行管理。
在集群设计的kubelet中，一些kubelet配置细节需相同；而其它方面则需要在每台机器的kubelet上单独配置。你可以手动管理kubelet配置，但kubeadm现在提供了一个`MaterConfig API`来集中管理kubelet配置。

注意，本节是利用`kubeadm`来配置`kubelet`，而不是手动配置`kubelet`。

<br>

**kubelet配置模式**

- 将集群级别配置传播到每个kubelet
kubelet提供了一个版本化、结构化的API对象，可配置kubelet中大多数参数，并将此配置推送到集群中所有正在运行的kubelet。它被称为  the kubelet’s ComponentConfig(组件配置)

```
#为kubelet提供默认值。
kubeadm init
kubeadm join


#修改服务默认子网
kubeadm init --service-cidr 10.96.0.0/12
#现在服务的VIP由此子网分配


#还需要设置kubelet使用的DNS地址，每个kubelet必须相同
--cluster-dns


#componentConfig
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
clusterDNS:
  - 10.96.0.10

```

<br>

- 提供特定实例的配置细节
由于不同硬件、操作系统、网络...，一些主机需要特定的kubelet配置。
由于我是使用`systemd`管理kubelet，所以可相应的修改对应的值。

```
#DNS解析文件路径，如果路径错误，则在kubelet配置错误的节点上DNS将解析失败
--resolve-conf


#节点API对象，默认被设置为主机名
.metadata.name
#使用如下标志指定节点名来服务默认值
--hostname-overide


#目前，kubelet无法自动检查CRI runtime的cgroup driver
#指定的驱动请与docker保持一致
--cgroup-driver


#根据集群使用的CRI runtime，可能需要为kubelet指定不同的标志
#如，当使用Docker时，你需要指定如 --network-plugin=cni
#但，当使用额外runtime，你需要指定 --container-runtime=remote, --container-runtime-path-endpoint=<path>



#systemd
cd /etc/systemd/system/kubelet.service.d/
vim 10-kubeadm.conf
#修改具体配置项


#EnvFile
vim /var/lib/kubelet/kubeadm-flags.env


systemctl daemon-reload && systemctl restart kubelet
```

<br>

**使用kubeadm配置kubelet**
`kubeadm config API`的`MasterConfiguration`类型，嵌入了`kubelet's ComponentConfig`到`.kubeletConfiguration.baseConfig`键下面。任何用户都可编写`MasterConfiguration`文件使用此配置键为集群中的所有kubelet设置基本配置。

- 使用`kubeadm init`的工作流程(workflow)
当调用`kubeadm init`时，`.kubeletConfiguration.baseConfig`结构被整理到磁盘`/var/lib/kubelet/config.yaml`，并且上传到集群中的`ConfigMap`。ConfigMap名为`kubelet-config-1.x`，`.x`表示k8s的次要版本。kubelet配置文件同样被写入`/etc/kubernetes/kubelet.conf`。此配置文件指向允许kubelet与API server通信的客户端证书。

为了解决特定实例的配置细节的模式，`kubeadm`将环境文件写入`/var/lib/kubelet/kubeadm-flags.env`，它包含了在启动时传递给kubelet的许多标志。它还包含许多动态参数(如cgroup driver)。

```
#标志栗子
KUBELET_KUBEADM_ARGS="--flag1=value1, --flag2=value2 ..."


#在将这两个文件整理到磁盘后，kubeadm会尝试运行如下两个命令
systemctl daemon-reload && systemctl restart kubelet

#在上面两个命令执行成功后，初始化会继续
```

<br>

- 使用`kubeadm join`的工作流程
当运行`kubeadm join`命令时，kubeadm使用Bootstrap Token凭据执行TLS bootstrap，它下载`kubelet-config-1.x` ConfigMap并将其写入`/var/lib/kubelet/config.yaml`。动态环境文件`/vat/lib/kubelet/kubeadm-flags.env`的生成方式与`kubeadm init`完成相同。

```
#同样，执行这两条命令
systemctl daemon-reload && systemctl restart kubelet
```

在kubelet载入新的配置文件后，kubeadm会写入`/etc/kubernetes/bootstrap-kubelet.conf` KubeConfig文件，该文件包含CA证书和Bootstrap Token。这些由kubelet用于执行TLS Bootstrap并获得唯一的凭证，该凭证存储在`/etc/kubernetes/kubelet.conf`中。
写入文件后，kubelet完成执行TLS Bootstrap.

<br>

**systemd的kubelet管理文件**
此配置文件在RPM包安装的时候写入`/etc/systemd/system/kubelet.service.d/10-kubeadm.conf`，它由`systemd`使用。

```
cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf


# Note: This dropin only works with kubeadm and kubelet v1.11+
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"
# This is a file that "kubeadm init" and "kubeadm join" generates at runtime, populating the KUBELET_KUBEADM_ARGS variable dynamically
EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env
# This is a file that the user can use for overrides of the kubelet args as a last resort. Preferably, the user should use
# the .NodeRegistration.KubeletExtraArgs object in the configuration files instead. KUBELET_EXTRA_ARGS should be sourced from this file.
EnvironmentFile=-/etc/sysconfig/kubelet
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS


#此文件指定kubeadm为kubelet管理的所有文件的默认位置


#TLS Bootstrap
/etc/kubernetes/bootstrap-kubelet.conf

#unique kubelet identity
/etc/kubernetes/kubelet.conf

#kubelet's ComponentConfig
/var/lib/kubelet/config.yaml

#dynamic env file, KUBELET_KUBEADM_ARGS
/var/lib/kubelt/kubeadm-flags.env

#user-specified  flag overrides, KUBELET_EXTRA_ARGS, 它具有最高优先级
/etc/sysconfig/kubelet
```

<br>

**k8s 二进制文件和包内容**

k8s release附带的DEB和RPM包：

| Package name | Description |
| - | - |
| kubeadm | Installs the /usr/bin/kubeadm CLI tool and [The kubelet drop-in file(#the-kubelet-drop-in-file-for-systemd) for the kubelet. |
| kubelet | Installs the /usr/bin/kubelet binary. |
| kubectl | Installs the /usr/bin/kubectl binary. |
| kubernetes-cni | Installs the official CNI binaries into the /opt/cni/bin directory. |
| cri-tools | Installs the /usr/bin/crictl binary from https://github.com/kubernetes-incubator/cri-tools. |



<br/>
<br/>


#### 使用kubeadm自定义控制面板配置

Customizing control plane configuration with kubeadm

`kubeadm`配置公开以下字段，这些字段可覆盖传递给控制面板组件的默认标志：

- APIServerExtraArgs
- ControllerManagerExtraArgs
- SchedulerExtraArgs


```
#apiserver
#栗子
apiVersion: kubeadm.k8s.io/v1alpha2
kind: MasterConfiguration
kubernetesVersion: v1.11.0
metadata:
  name: 1.11-sample
apiServerExtraArgs:
  advertise-address: 192.168.0.103
  anonymous-auth: false
  enable-admission-plugins: AlwaysPullImages,DefaultStorageClass
  audit-log-path: /home/johndoe/audit.log


#controllermanager
#栗子
apiVersion: kubeadm.k8s.io/v1alpha2
kind: MasterConfiguration
kubernetesVersion: v1.11.0
metadata:
  name: 1.11-sample
controllerManagerExtraArgs:
  cluster-signing-key-file: /home/johndoe/keys/ca.key
  bind-address: 0.0.0.0
  deployment-controller-sync-period: 50


#scheduler
#栗子
apiVersion: kubeadm.k8s.io/v1alpha2
kind: MasterConfiguration
kubernetesVersion: v1.11.0
metadata:
  name: 1.11-sample
schedulerExtraArgs:
  address: 0.0.0.0
  config: /home/johndoe/schedconfig.yaml
  kubeconfig: /home/johndoe/kubeconfig.yaml
```


<br/>
<br/>


#### 使用kubeadm创建高可用集群

Creating Highly Available Clusters with kubeadm



<br/>
<br/>


#### 使用kubeadm配置etcd高可用集群

Set up a Highly Availabile etcd Cluster With kubeadm


<br/>
<br/>


#### Troubleshooting kubeadm

官方Troubleshooting: <https://kubernetes.io/docs/setup/independent/troubleshooting-kubeadm/>

<br>

此外，在我启动`kubelet`之后，`kubelet`频繁出现一个错误信息：

```
#错误信息
#journal -u kubelet
kubelet[10720]: E0810 14:32:14.748713   10720 summary.go:102] Failed to get system container stats for "/system.slice/kubelet.service": failed to get cgroup stats for "/system.slice/kubelet.service": failed to get container info for "/system.slice/kubelet.service": unknown container "/system.slice/kubelet.service"



#解决方法
vim /etc/sysconfig/kubelet

#添加额外参数
KUBELET_EXTRA_ARGS="--runtime-cgroups=/systemd/system.slice --kubelet-cgroups=/systemd/system.slice"



#重启服务
systemctl restart kubelet

```




<br/>
<br/>


### 使用软件包创建集群

请定义相应的防火墙规则！

我是CentOS7x86_64，所以只包含了RPM包。

自带的源安装的k8s可能版本比较老，如需较新版本，可以在网上搜索kubernetes rpm包进行手动安装。
Rpmfind: <https://rpmfind.net/>

<br>

**k8s集群组件**

- etcd
- flannel
- kube-apiserver
- kube-controller-manager
- kube-scheduler
- kubelet
- kube-proxy
- kube-dns
- kubectl

<br>

**Master**

- etcd
- flannel
- kube-apiserver
- kube-controller-manager
- kube-scheduler
- kubectl


```sh
#默认镜像源安装
yum install -y etcd flannel kubernetes-master kubernetes-client


#配置kubernetes-master
#cd /etc/kubernetes
#apiserver  config  controller-manager  scheduler

#修改监听地址
vim apiserver
KUBE_API_ADDRESS="--insecure-bind-address=0.0.0.0"
#生成环境一定要加上认证，我由于是测试，并未做认证
#未添加认证，去掉 KUBE_ADMISSION_CONTROL中的SecurityContextDeny,ServiceAccount
#Flag --admission-control has been deprecated, Use --enable-admission-plugins or --disable-admission-plugins instead.
#KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,ResourceQuota"
KUBE_ADMISSION_CONTROL="--enable-admission-plugins=NamespaceLifecycle,NamespaceExists,LimitRanger,ResourceQuota"

#此处我修改了cidr
KUBE_SERVICE_ADDRESSES="--service-cluster-ip-range=172.16.0.0/16"



#配置etcd，可先使用默认值
#后面可创建etcd-cluster
vim /etc/etcd/etcd.conf
#修改监听地址
ETCD_LISTEN_CLIENT_URLS="http://0.0.0.0:2379"


#创建pod-network，cidr为kube-apiserver中的配置项
#/atomic.io/network为flannel_etcd前缀,之后再启动flannel
etcdctl mk /atomic.io/network/config '{"Network":"172.16.0.0/16"}'
etcdctl ls
etcdctl get '/atomic.io/network/config'



#配置flannel
vim /etc/sysconfig/flanneld



#配置后启动
systemctl start etcd flannel kube-apiserver kube-controller-manager kube-scheduler


#查看
[root@master kubernetes]# kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   172.16.0.1   <none>        443/TCP   4m



#具体参数请根据实际情况来配置
```

<br>

**Node**

- flannel
- kubelet
- kube-porxy
- kubectl

```sh
#epel
yum install -y flannel kubernetes-node kubernetes-client


#ls /etc/kubertes
#config  kubelet  proxy


#配置etcd的地址
vim /etc/sysconfig/flanneld
FLANNEL_ETCD_ENDPOINTS="http://master:2379

vim /etc/kubernertes/config
KUBE_MASTER="--master=http://master:8080"


#修改kubelet地址
KUBELET_ADDRESS="--address=node_addr"
KUBELET_HOSTNAME="--hostname-override=node_addr"
KUBELET_API_SERVER="--api-servers=http://master:8080"


#配置后启动
systemctl start flanneld kube-proxy kubelet


#具体参数请根据实际情况来配置
```

<br/>

**验证集群**

```
#Master
#kubectl安装如前
kubectl get nodes

```

<br/>

**安装较新的k8s**
由于自带的源k8s版本比较低，可能我们需要较新的k8s版本。


```
#安装较新的Kubernetes

浏览器访问 https://rpmfind.net/

搜索：
kubernetes-master(x86-64)
kubernetes-node(x86-64)
kubernetes-client(x86-64)

选择合适的版本进行下载，三者版本请一致
安装步骤和下面类似

请注意，k8s组件安装好后，还需要安装额外组件。
如docker, flannel, etcd...



#master
yum install -y k8s-master k8s-client

#node
yum install -y k8s-node k8s-client
```



<br/>
<br/>



### k8s-release生成rpm包

kubernetes-release: <https://github.com/kubernetes/release>

使用k8s-release手动生成rpm/dep包。
由于yum源更不上k8s的更新速度，所以才需要我们手动制作。

需要安装并运行Docker，它要运行一个`rpm-builder`容器。

它生成一下rpm包：

- kubeadm
- kubelet
- kubectl


<br>

官方说明：

![官方](/images/K8s/buildingLinuxPackages.png)

<br/>

```
git clone https://github.com/kubernetes/release.git

cd ./release/rpm
./docker-build.sh

#此处如果连接google下载超时的话，可以在其它主机上下载，然后复制到此目录下

#成功

----------------------------------------

RPMs written to:
cri-tools-1.11.0-0.x86_64.rpm  kubectl-1.11.0-0.x86_64.rpm  kubernetes-cni-0.6.0-0.x86_64.rpm
kubeadm-1.11.0-0.x86_64.rpm    kubelet-1.11.0-0.x86_64.rpm  repodata

Yum repodata written to:
5e470d3c1c28cdd798237a48172b46f753655edee30988f4fde7000fde859d5a-primary.xml.gz
9497c84e5650b15bf6edcffb68900b4f59f7271fa6318d3c0336386c99afd2d8-other.xml.gz
94da9da6abd2dc8364ef51b4ca135b804deef0a37f1f13e4abeee455a8b0e897-primary.sqlite.bz2
971e5af9d861f5ba85b12bad481749aa26546051090fa4e21c2393c21590dd5a-filelists.xml.gz
b752df67070ff5552bd3137f00fb217578f1d810084a3e42579a53eee2a26085-other.sqlite.bz2
f0ec7692c0654c1ec5ad9c8576ebe5b8f135c45b5d5242066df6e2d631a3ef6f-filelists.sqlite.bz2
repomd.xml


#会在./release/rpm/output/x86_64下生成特定版本的rpm包
pwd
#/root/release/rpm/output/x86_64

ls -l
total 47056
-rw-r--r-- 1 root root  4383318 Aug  3 10:25 cri-tools-1.11.0-0.x86_64.rpm
-rw-r--r-- 1 root root  7906382 Aug  3 10:25 kubeadm-1.11.0-0.x86_64.rpm
-rw-r--r-- 1 root root  7859238 Aug  3 10:25 kubectl-1.11.0-0.x86_64.rpm
-rw-r--r-- 1 root root 19012182 Aug  3 10:25 kubelet-1.11.0-0.x86_64.rpm
-rw-r--r-- 1 root root  9008530 Aug  3 10:25 kubernetes-cni-0.6.0-0.x86_64.rpm
drwxr-xr-x 2 root root     4096 Aug  3 10:25 repodata

```

请注意，默认会自动编译所有平台。如果只需要`x84_64`，可以更改`entry.sh`文件，将其它平台去掉，以加快编译速度。

```
vim ./release/rpm/entry.sh

  ARCHS=(
    amd64/x86_64
    #arm/armhfp
    #arm64/aarch64
    #ppc64le/ppc64le
    #s390x/s390x
  )
```

后面还是需要使用`kubeadm`来进行引导！


<br/>
<br/>



### 编译源码生成rpm包

参考：
- How to build Kubernetes RPM: <https://mritd.me/2017/07/12/how-to-build-kubernetes-rpm/>

由于墙的原因，使用kubeadm进行引导还是会timeout。使用自带的yum源或网上下载的k8s rpm可能也不是最新的版本。因此需要手动编译源码以生成rpm包。

生成如下rpm包：

- kubernetes-master
- kubernetes-client
- kubernetes-node



<br/>
<br/>


### k8s Dashboard

说明:

- GitHub: <https://github.com/kubernetes/dashboard>
- image: kubernetes-dashboard-amd64:v1.8.3
- FAQ: <https://github.com/kubernetes/dashboard/wiki/FAQ>
- Let's Encrypt: <https://letsencrypt.org/>

Let's Encrypt是一个免费，自动化和开放的证书颁发机构。


<br>


#### 快速配置

Quick setup

快速部署`kubernetes-dashboard`的方法请参考README。它适用于k8s新手并希望快速开始使用Dashboard的人。其它配置适用于有一定经验的用户，详情在以下章节。

k8s Dashboard是k8s集群的基于Web的通用UI。它允许用户管理运行在集群中的应用程序，并对应用程序进行故障排除，以及管理集群本身。

请注意，Dashboard使用了安全设置。这意味着，默认情况下它具有最小的权限集，并且只能通过https访问。
建议在安装和执行Dashboard之前，先阅读**[Access Control](https://github.com/kubernetes/dashboard/wiki/Access-control)**指南。

<br>

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml

#或
#wget https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml
#kubectl apply -f /path/kubernetes-dashboard.yaml

secret/kubernetes-dashboard-certs created
serviceaccount/kubernetes-dashboard created
role.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
rolebinding.rbac.authorization.k8s.io/kubernetes-dashboard-minimal created
deployment.apps/kubernetes-dashboard created
service/kubernetes-dashboard created


#查看
kubectl get pods -n kube-system -o wide |grep dashboard
kubernetes-dashboard-6948bdb78-rnnjp   1/1       Running   1          1d        10.244.1.2       node

 kubectl get service -n kube-system -o wide |grep dashboard
kubernetes-dashboard   ClusterIP   10.110.83.129   <none>        443/TCP         13m       k8s-app=kubernetes-dashboard



#要从本地访问Dashboard，必须为k8s集群创建安全通道
kubectl apply
Starting to serve on 127.0.0.1:8001



#访问Dashboard
http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/

#http://localhost:8001/ui已弃用
#<h3>Unauthorized</h3>
#会直接报403，还需要做前面所说的操作。

#Heapster必须在集群中运行才能使metric, graphs可用
#Heapster已被弃用，请考虑使用metrics-server和第三方metrics pipeline收集Prometheus格式的指标
```


<br/>
<br/>


#### 安装

Installation


**官方版**
当从旧版Dashboard升级到 `v1.7+`，请确保删除`kubernetes-dashboard`服务账户的集群角色绑定，否则Dashboard将具有对集群的完全管理权限。

<br>

**快速配置**
快速部署`kubernetes-dashboard`的方法请参考README。它适用于k8s新手并希望快速开始使用Dashboard的人。

<br>

**推荐配置**
直接访问Dashboard(不是`kubectl proxy`)，应该使用有效的证书来建立安全的HTTPS连接。它们可由公共可信证书颁发机构(如[Let's Encrypt](https://letsencrypt.org/))生成，使用它们替代Dashboard自动生成的证书。

此配置要求证书存储在`kube-system`命名空间中名为`kubernetes-dashboard-certs`的证书中。
假设你有存储在`$HOME/certs`目录下的`dashboard.crt`和`dashboard.key`文件。你应该使用这些文件创建`secret`。之后，便可以开始配置Dashboard。

```sh
#查看
kubectl get secret -n kube-system | grep dashboard

#查看
kubectl describe secret/kubernetes-dashboard-certs -n kube-system
Name:         kubernetes-dashboard-certs
Namespace:    kube-system
Labels:       k8s-app=kubernetes-dashboard
Annotations:
Type:         Opaque

Data
====


#创建
kubectl create secret generic kubernetes-dashboard-certs --from-file=$HOME/certs -n kube-system


#部署Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml

```

<br>

**替代配置**
此配置并不安全。不使用证书，仅通过HTTP公开Dashboard。在此配置中，只能通过使用`Authorization Header`功能来确保访问控制。

```sh
#配置
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/alternative/kubernetes-dashboard.yaml

```

<br>

**开发版**
不建议在线上环境使用开发版，请使用稳定的正式版。

```sh
#部署
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard-head.yaml

```

<br>

**升级**
安装后，Deployment不会自动更新。为了更新它，你需要删除部署的pod并等待它重新创建。重新创建之后，它会使用最新的镜像`image:latest`.

```sh
#删除pod
kubectl -n kube-system delete $(kubectl -n kube-system get pod -o name | grep dashboard)
```


<br/>
<br/>


#### 证书管理

Certificate management


本节简短介绍了如何获取可在Dashboard中启用HTTPS的证书。有两个步骤要做：

- 生成证书
	+ 证书认证机构(Certificate Authority)
	+ 自签名证书(Self-signed certificate)
- 将证书传递给Dashboard
	+ 按照前面的推荐配置方法
	+ 其它情况，你需要修改Dashboard的YAML部署文件，并将`--tls-key-file`, `--tls-cert-file`传递给Dashboard

<br>

**公众信任的证书认证机构**
Public trusted Certificate Authority

有许多公共和免费的证书提供商可供选择。如前面提到的[Let's encrypt](https://letsencrypt.org/)，具体操作查看此网站说明。

<br>

**自签名证书**
Self-signed certificate

如果你打算自己生成证书，你需要像[OpenSSL](https://www.openssl.org/)这样的库来帮助你。

- 生成私钥(private key)和证书签名请求(certificate signing request)
- 生成SSL证书



```
#Generate private key and certificate signing request
#创建SSL证书需要私钥和证书签名请求

openssl genrsa -des3 -passout pass:x -out dashboard.pass.key 2048

openssl rsa -passin pass:x -in dashboard.pass.key -out dashboard.key

rm dashboard.pass.key

#需要填写一些信息
#A challenge password []请直接按回车，不要填写内容
openssl req -new -key dashboard.key -out dashboard.csr

Country Name (2 letter code) [XX]:CN
State or Province Name (full name) []:SC
Locality Name (eg, city) [Default City]:CD
Organization Name (eg, company) [Default Company Ltd]:Student
Organizational Unit Name (eg, section) []:HT
Common Name (eg, your name or your server's hostname) []:Zhang21
Email Address []:reds@zhang21.cn

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:



#Generate SSL certificate
#自签名SSL证书由 .key私钥 和 .csr生成
openssl x509 -req -sha256 -days 1000 -in dashboard.csr -signkey dashboard.key -out dashboard.crt

Signature ok
subject=/C=CN/ST=SC/L=CD/O=Student/OU=HT/CN=Zhang21/emailAddress=reds@zhang21.cn
Getting Private key



#查看
ls
dashboard.crt  dashboard.csr  dashboard.key


#将密钥和证书移动到需要的目录下
mv ./dashboard.* /etc/kubernetes/pki/dashboard


#接下来便可以创建secret了
```


<br/>
<br/>


#### 访问Dashboard

Accessing Dashboard


在集群上安装Dashboard后，可通过几种不同的方式访问它。遇到什么问题，可查看FAQ。

- 1.6.x and below
- 1.7.x and above


<br/>


##### 1.7.x and above

Accessing Dashboard 1.7.X and above


我的Dashboard v1.8.5.

前面的HTTP/HTTPs都不说了。
但请注意，不要把Dashboard使用HTTP公开展示。


<br>

**kubectl proxy**
`kubectl proxy`在你的计算机和k8s APIserver之间创建代理服务器。默认情况下它只能在本地访问。

注意，不应该使用`kubectl proxy`命令公开Dashboard，因为它只允许HTTP连接。对于`localhost`和`127.0.0.1`以外的域，将无法登录。

首先让我们检查kubectl是否已正确配置并是否可访问集群:

```sh
kubectl cluster-info

#Kubernetes master is running at https://192.168.31.49:6443
#KubeDNS is running at https://192.168.31.49:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy



#启动代理服务器
kubectl proxy

#Starting to serve on 127.0.0.1:8001

#之后你便可以从浏览器访问Dashboard
#http://localhost:8001/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/
#但我访问还是403，应该还需要创建Service Token之类。

```

<br>

**NodePort**
这种访问Dashboard的方式，建议用于单节点设置的开发环境中。
请注意，此HTTPS方式需要安装前面生成的证书。

```sh
#编辑 kubernetes-dashboard服务
kubectl -n kube-system edit service/kubernetes-dashboard


# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file will be
# reopened with the relevant failures.
#
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"k8s-app":"kubernetes-dashboard"},"name":"kubernetes-dashboard","namespace":"kube-system"},"spec":{"ports":[{"port":443,"targetPort":8443}],"selector":{"k8s-app":"kubernetes-dashboard"}}}
  creationTimestamp: 2018-08-09T01:14:01Z
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kube-system
  resourceVersion: "200618"
  selfLink: /api/v1/namespaces/kube-system/services/kubernetes-dashboard
  uid: 80091845-9b71-11e8-a08a-000c298ee39f
spec:
  clusterIP: 10.110.83.129
  ports:
  - port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}



#将 type: ClusterIP 修改为 type: NodePort
type: NodePort

#直接保存退出(:wq)
#service/kubernetes-dashboard edited


#查看
kubectl -n kube-system get service/kubernetes-dashboard
NAME                   TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
kubernetes-dashboard   NodePort   10.110.83.129   <none>        443:31965/TCP   6h

#查看端口
netstat -nltup | grep 31965
tcp6       0      0 :::31965                :::*                    LISTEN      11280/kube-proxy


#Dashboard展示在 31965(HTTPS) 端口上。
#现在可在浏览器访问 <master-ip>:31965

#可使用Nginx做前端代理

#此处注意，需要将dashboard.crt证书安装到你的电脑上
#不然浏览器会拒绝



#如果你尝试在多节点集群上使用`NodePort`公开Dashboard，则必须找到运行Dashboard的节点的IP才能访问它。
https://<node-ip>:<nodeport>
```

![Dashboard NodePort](/images/K8s/k8s_dashboard_nodeport.png)

![没有权限](/images/K8s/k8s_dashboard_forbidden.png)

由图可看出，还需要配置权限才能够正常访问Dashboard！

<br>

**API Server**
如果公开k8s API server并可以从外部访问，则你可直接访问url。
Dashboard: <https://master-ip:apiserver-port/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/>

注意，只有在浏览器中安装证书时，才能使用这用访问方式。

<br>

**Ingress**
Dashboard可以使用 `ingress` 进行公开。详情: <https://kubernetes.io/docs/concepts/services-networking/ingress/>


<br/>
<br/>


#### Nginx反向代理

直接使用`NodePort`方式访问比较麻烦，所以配置使用Nginx反向代理来访问。

Nginx配置文件:

```
vim /etc/nginx/conf.d/k8sUI.conf


server {
    listen 443 ssl;
    server_name k8s.ui;

    ssl_certificate /etc/kubernetes/pki/dashboard/dashboard.crt;
    ssl_certificate_key /etc/kubernetes/pki/dashboard/dashboard.key;


    location / {
      proxy_pass https://127.0.0.1:31965;
      proxy_read_timeout 60s;
      proxy_send_timeout 60s;
      proxy_connect_timeout 60s;
      proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_404;

      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection 'upgrade';
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto https;

      proxy_buffer_size 64k;
      proxy_buffers 4 64k;
      proxy_busy_buffers_size 128k;
      proxy_temp_file_write_size 128k;
    }
}


nginx -t
nginx -s reload
```

之后解析DNS，就可直接通过域名访问了。



<br/>
<br/>


#### 访问控制

Access Control


安装Dashboard后，我们便可以专注于为用户配置对集群资源的访问控制。从 `v1.7` 开始，Dashboard默认不再具有完全管理权限(admin privilige)，所有权限都被撤销，并且只授予了Dashboard工作所需的最小权限。所以下面的介绍都只针对于 `v1.7+` 版本。
如果Dashboard只能由受信任的人员访问，你可能希望授予他们完全管理权限，则所有人都具有完全管理的权限。请注意，其它应用程序不应直接访问Dashboard，因为它可能导致权限升级。确保集群内的流量仅限于命名空间，或者只是撤销集群内应用程序对Dashboard的访问权限。

可查看`kubernetst-dashboard.yaml`配置文件，里面有`minimal`的权限。

<br>

**介绍**
k8s支持几种方法来认证(authenticating)和授权(authorizing)用户。授权由k8s API server处理。Dashboard仅充当代理并将所有认证信息传递给API server。在禁止访问的情况下，相应的警告信息会显示到Dashboard上。

<br>

**默认Dashboard权限**

- `v1.7`
	+ `create` and `watch` permissions for secrets in `kube-system` namespace required to create and watch for changes of `kubernetes-dashboard-key-holder` secret.
	+ `get`, `update` and `delete` permissions for secrets named `kubernetes-dashboard-key-holder` and `kubernetes-dashboard-certs` in `kube-system` namespace.
	+ `proxy` permission to `heapster` service in `kube-system` namespace required to allow getting metrics from heapster.

- `v1.8`
	+ `create` permission for secrets in `kube-system` namespace required to create `kubernetes-dashboard-key-holder` secret.
	+ `get`, `update` and `delete` permissions for secrets named `kubernetes-dashboard-key-holder` and `kubernetes-dashboard-certs` in `kube-system` namespace.
	+ `get` and `update` permissions for config map named `kubernetes-dashboard-settings` in `kube-system` namespace.
	+ `proxy` permission to `heapster` service in `kube-system` namespace required to allow getting metrics from heapster.

<br>

**Authentication**
从`v1.7`版本开始，Dashboard支持的用户认证基于：

- `Authorization: Bearer <token>`
- `Bearer Token`
- `Username/password `
- `Kubeconfig `

<br>

**Login view**
要使其显示在Dashboard中，你需要启用HTTPS访问Dashboard。

使用跳过选项将使Dashboard使用Service Account权限。

![Login view](/images/K8s/login_view.png)

<br>

**Authorization header**
在通过HTTP访问Dashboard时，使用 `authorization header` 是使Dashboard充当用户的唯一方法。

要使Dashboard使用`authorization header`，你只需将每个请求中的`Authorization: Bearer <token>`传递给Dashboard。这可以通过在Dashboard前端配置反向代理来实现。代理将负责身份提供者的身份验证，并将请求头部中生成的token传递给Dashboard。注意，需要正确配置k8s API server才能接受这些token。

注意： 如果通过API server proxy访问Dashboard，则`authorization header`将不起作用。这是因为一旦请求到达API server，所有其它header都将被删除。

<br>

**Bearer Token**
建议先熟悉[k8s authentication doc](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)，以了解如何获取可用于登录的token。例如，每个`Service Account`都有一个具有有效`Bearer token`，用于登录Dashboard。

推荐讲座，了解如何创建服务账户并对其进行授权：

- [Service Account Tokens](https://kubernetes.io/docs/reference/access-authn-authz/authentication/#service-account-tokens)
- [Role and  ClusterRole](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#role-and-clusterrole)
- [Service Account Permissions](https://kubernetes.io/docs/reference/access-authn-authz/rbac/#service-account-permissions)

![Bearer Token](/images/K8s/bearer_token.png)

<br>

```
#使用kubectl获取token
#默认情况下，k8s创建了许多服务账号。所有都具有不同的访问权限

kubectl -n kube-system get secret

NAME                                             TYPE                                  DATA      AGE
attachdetach-controller-token-bszq5              kubernetes.io/service-account-token   3         2d
bootstrap-signer-token-bqv44                     kubernetes.io/service-account-token   3         2d
bootstrap-token-uzdl9x                           bootstrap.kubernetes.io/token         7         2d
certificate-controller-token-rsftn               kubernetes.io/service-account-token   3         2d
clusterrole-aggregation-controller-token-x64f5   kubernetes.io/service-account-token   3         2d
coredns-token-dfmpb                              kubernetes.io/service-account-token   3         2d
cronjob-controller-token-xwtkc                   kubernetes.io/service-account-token   3         2d
daemon-set-controller-token-vxzp4                kubernetes.io/service-account-token   3         2d
default-token-5868t                              kubernetes.io/service-account-token   3         2d
deployment-controller-token-jc6bs                kubernetes.io/service-account-token   3         2d
disruption-controller-token-znghk                kubernetes.io/service-account-token   3         2d
endpoint-controller-token-mnxfh                  kubernetes.io/service-account-token   3         2d
expand-controller-token-6srzj                    kubernetes.io/service-account-token   3         2d
flannel-token-7548k                              kubernetes.io/service-account-token   3         2d
generic-garbage-collector-token-22qd2            kubernetes.io/service-account-token   3         2d
horizontal-pod-autoscaler-token-zs8pj            kubernetes.io/service-account-token   3         2d
job-controller-token-zbfhd                       kubernetes.io/service-account-token   3         2d
kube-proxy-token-xxp9h                           kubernetes.io/service-account-token   3         2d
kubernetes-dashboard-certs                       Opaque                                3         1h
kubernetes-dashboard-key-holder                  Opaque                                2         2d
kubernetes-dashboard-token-sgq5t                 kubernetes.io/service-account-token   3         2d
namespace-controller-token-25n2k                 kubernetes.io/service-account-token   3         2d
node-controller-token-289v8                      kubernetes.io/service-account-token   3         2d
persistent-volume-binder-token-x7t7x             kubernetes.io/service-account-token   3         2d
pod-garbage-collector-token-xxjqp                kubernetes.io/service-account-token   3         2d
pv-protection-controller-token-9s4x7             kubernetes.io/service-account-token   3         2d
pvc-protection-controller-token-l7m7j            kubernetes.io/service-account-token   3         2d
replicaset-controller-token-mszv9                kubernetes.io/service-account-token   3         2d
replication-controller-token-8gl9s               kubernetes.io/service-account-token   3         2d
resourcequota-controller-token-whljw             kubernetes.io/service-account-token   3         2d
service-account-controller-token-h87wp           kubernetes.io/service-account-token   3         2d
service-controller-token-qn5jz                   kubernetes.io/service-account-token   3         2d
statefulset-controller-token-zps2l               kubernetes.io/service-account-token   3         2d
token-cleaner-token-nccrw                        kubernetes.io/service-account-token   3         2d
ttl-controller-token-dmmb9                       kubernetes.io/service-account-token   3         2d



kubectl -n kube-system describe secret/replicaset-controller-token-mszv9
Name:         replicaset-controller-token-mszv9
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name=replicaset-controller
              kubernetes.io/service-account.uid=d18a5f8f-9a0d-11e8-a08a-000c298ee39f

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJyZXBsaWNhc2V0LWNvbnRyb2xsZXItdG9rZW4tbXN6djkiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoicmVwbGljYXNldC1jb250cm9sbGVyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDE4YTVmOGYtOWEwZC0xMWU4LWEwOGEtMDAwYzI5OGVlMzlmIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOnJlcGxpY2FzZXQtY29udHJvbGxlciJ9.O6hXQwsXdSXREsaao_V7pmeQkfWGEd4QLDxczxNZVcrT2yN9F1KFJ9IklYVlGSTo1cKA4OxkYqjKWzWPBEn6wVLhVbf6_WqTrFi4qEtj_nmhXwqcwkpioJzyXu7x7wljpH-H32bEaLW1l-y5kQBUztF9fAHZZyv0f9vaRK4u4zVzuq4JzauLB9aVBrgt6rSaOENdr8OGm1yjM_--gQtc1qoF8mLo3RK6qLpFjT70EZKgyys_GXpFrrnhG5maUmlFqCPZ6P0cl8d6SuDfkQIlFxNHxtJmOPSCIE6wjgkOncRtgWHRRVsRPnhDGOp0kbmdLTfpOx2zZEiCD5btXL0OkA


#我们可以使用显示的token登录Dashboard

```

<br>

**Basic**
默认情况下，禁用基本身份认证，也就是用户密码认证。原因是需要使用授权模式`RBAC`和`--basic-auth-file`标志配置k8s API server。没有的话，API server会自动回退到匿名用户(anonymous user)，并且无法检查提供的凭据是否有效。

修改`--authentication-mode=basic`标志在Dashboard中启用基本身份认证，默认值为`--authentication-mode=token`。

<br>

**kubeconfig**
这种登录方法是为了方便起见而提供的。`kubeconfig file`仅支持`--authentication-mode`标志指定认证选项。如果它配置为其它方式，Dashboard中将显示错误消息。

![kubeconfig](/images/K8s/kubeconfig.png)

<br>

**Admin privileges**
注意： 在操作之前，请确保你知道自己在做什么。向Dashboard的服务账号赋予管理权限可能会存在安全风险。

你可以通过创建`ClusterRoleBinding`来授权Dashboard的服务账号完全的管理权限。

```
#栗子
dashboard-admin.yaml

#官方文档版

apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard
  labels:
    k8s-app: kubernetes-dashboard
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kubernetes-dashboard
  namespace: kube-system


#开发版
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: kubernetes-dashboard-head
  labels:
    k8s-app: kubernetes-dashboard-head
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: kubernetes-dashboard-head
  namespace: kube-system

```


<br/>


#### 创建示例用户

Creating sample user


在本节中，我们将了解如何使用k8s Service Account机制创建新用户，授权用户管理权限并使用与此用户关联的`Bearer Token`进行登录。
关于`grant/deny`权限，请查看文档[authentication](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)和[authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/)以了解详情。

创建`xxx.yaml`文件，并使用`kubectl create -f xxx.yaml`命令创建它们。

<br>

**创建 Service Account**
在`kube-system`命名空间中创建名为`admin-user`的服务账户:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kube-system

```

```sh
#创建
kubectl create -f /etc/kubernetes/auth/admin-user_SA.yaml
#serviceaccount/admin-user created


#查看
kubectl -n kube-system get secret | grep admin-user
#admin-user-token-qj8hj                           kubernetes.io/service-account-token   3         56s
```

<br>

**创建 ClusterRoleBinding**
在大多数情况下，在使用`kops`, `kubeadm`等管理配置集群后，`Role`都已存在于集群中。我们可使用它为`ServiceAccount`仅创建`RoleBinding`。

注意: `ClusterRoleBinding`的`apiVersion`资源可能不同于k8s version。从`v1.8`开始，它被提升为`rbac.authorization.k8s.io/v1`。

```yaml
apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kube-system
```

```sh
#创建
kubectl create -f /etc/kubernetes/Auth/cluster-admin_CRB.yaml 
#clusterrolebinding.rbac.authorization.k8s.io/admin-user created

```

<br>

**Bearer Token**
现在我们需要去找到用于登录的Token。

```
kubectl -n kube-system describe secret $(kubectl -n kube-system get secret | grep admin-user | awk '{print $1}')

Name:         admin-user-token-qj8hj
Namespace:    kube-system
Labels:       <none>
Annotations:  kubernetes.io/service-account.name=admin-user
              kubernetes.io/service-account.uid=58d39b31-9c40-11e8-a08a-000c298ee39f

Type:  kubernetes.io/service-account-token

Data
====
ca.crt:     1025 bytes
namespace:  11 bytes
token:      eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXFqOGhqIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiI1OGQzOWIzMS05YzQwLTExZTgtYTA4YS0wMDBjMjk4ZWUzOWYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZS1zeXN0ZW06YWRtaW4tdXNlciJ9.4hCqFj7R7CwAewnFxsy5QC91v6288T7aOCZXae7AbqXECiFb2yB5x7VQs0GjnUj8jbSZamBpI_D6D7p8PoRUmPZg2NOF46TEztsR9wcsEywUr6EHdXMGy6HUtvedy45K1j9h8oFp9nAqvxa6M7hrfV_yy-XlJdqTo7J06VlT_czpWNScCkjejIOlZXFvYL5f5ha0V4L5XCdlFkf7DYbsNV6odquIKavg270g4nAr1ZAJ14SjeFdfRVvimS4N-W7pb9vmOeZBnAmGuotKoqU1OlzZrMfpsPGIXy5GW3zD8PvsbGU9Xn6lyPHH08X0kXCUACQHx4UiaMFzlnhaC2XIMQ

```

现在复制Token来登录.

![Login](/images/K8s/admin_user_token.png)

![Dashboash](/images/K8s/admin_user_dashboard.png)


<br/>
<br/>



### Heapster


GitHub: <https://github.com/kubernetes/heapster>

注意: Heapster已被启用，考虑使用`metric-server`和第三方`metric pipeline`来收集Prometheus格式的指标。

<br>

**Heapster 启用时间轴**

| Kubernetes Release | Action | Policy/Support |
| - | - | - |
| Kubernetes 1.11 | Initial Deprecation | No new features or sinks are added. Bugfixes may be made. |
| Kubernetes 1.12 | Setup Removal | The optional to install Heapster via the Kubernetes setup script is removed. |
| Kubernetes 1.13 | Removal | No new bugfixes will be made. Move to kubernetes-retired organization. |


<br/>
<br/>


### metric-server


GitHub: <https://github.com/kubernetes-incubator/metrics-server>

具体详情可参考README。

```
#下载到本地
git clone https://github.com/kubernetes-incubator/metrics-server.git


#移动到管理目录
mv metrics-server/ /etc/kubernetes/


#k8s v1.8+
ls /etc/kubernetes/metrics-server/deploy/v1.8+/
auth-delegator.yaml  auth-reader.yaml  metrics-apiservice.yaml  metrics-server-deployment.yaml  metrics-server-service.yaml  resource-reader.yaml


#注意metrics-server-deployment.yaml文件，需要一个镜像，请准备
#gcr.io/google_containers/metrics-server-amd64:v0.2.1

docker pull zhang21/metrics-server-amd64:v0.2.1
docker tag zhang21/metrics-server-amd64:v0.2.1 gcr.io/google_containers/metrics-server-amd64:v0.2.1



#创建
#注意，在顶层进行创建
cd /etc/kubernetes/metrics-server
kubectl create -f deploy/v1.8+/

clusterrolebinding.rbac.authorization.k8s.io/metrics-server:system:auth-delegator created
rolebinding.rbac.authorization.k8s.io/metrics-server-auth-reader created
apiservice.apiregistration.k8s.io/v1beta1.metrics.k8s.io created
serviceaccount/metrics-server created
deployment.extensions/metrics-server created
service/metrics-server created
clusterrole.rbac.authorization.k8s.io/system:metrics-server created
clusterrolebinding.rbac.authorization.k8s.io/system:metrics-server created


#查看
kubectl -n kube-system  get deployment

NAME                   DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
coredns                2         2         2            2           2d
kubernetes-dashboard   1         1         1            1           19h
metrics-server         1         1         1            0           39s

```





<br/>
<br/>



## pause容器


参考:

- 《Kubernetes之“暂停”容器》: <http://dockone.io/article/2785>
- 《Pause容器》: <https://jimmysong.io/kubernetes-handbook/concepts/pause-container.html>
- GitHub: <https://github.com/kubernetes/kubernetes/tree/master/build/pause>

<br>

Pause容器，又叫Infra容器。它不是pod，而是一个容器。

```
docker ps | grep pause
35c9aaa68a06        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_coredns-78fcdf6894-hn46d_kube-system_daab8e60-9a0d-11e8-a08a-000c298ee39f_0
d22a1baac736        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_coredns-78fcdf6894-wqxbx_kube-system_daac5838-9a0d-11e8-a08a-000c298ee39f_0
4d0cdc392629        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_kube-flannel-ds-7gbvd_kube-system_59129dff-9a0f-11e8-a08a-000c298ee39f_0
4f28747a2044        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_kube-proxy-rhrks_kube-system_da990e28-9a0d-11e8-a08a-000c298ee39f_0
f2bd7bd47eb4        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_kube-scheduler-master_kube-system_537879acc30dd5eff5497cb2720a6d64_0
d732ffba5530        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_kube-controller-manager-master_kube-system_01c36146e2c80849d7b6993e68aa5e67_0
cd7636bac6df        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_kube-apiserver-master_kube-system_1bd24cc043a06bf7e71b96167946c220_0
d4adb3504543        k8s.gcr.io/pause:3.1   "/pause"                 18 hours ago        Up 18 hours                             k8s_POD_etcd-master_kube-system_2cc1c8a24b68ab9b46bca47e153e74c6_0


#或者是这样
#registry.access.redhat.com/rhel7/pod-infrastructure:latest



#rpm包安装kubelet的默认配置
KUBELET_POD_INFRA_CONTAINER="--pod-infra-container-image=registry.access.redhat.com/rhel7/pod-infrastructure:latest"

#kubeadm安装kubelet的默认配置
KUBELET_POD_INFRA_CONTAINER=--pod-infra-container-image=k8s.gcr.io/pause:3.1

```

<br>

**pause容器的作用**
k8s中的pause容器主要为每个业务提供以下功能：

- 在`pod`中担任Linux命名空间共享的基础
- 启用`pid`命名空间，开启`init`进程

![pause容器](/images/K8s/pause-container.png)

<br>

使用`pause`容器和共享命名空间创建pod示例：

```
#启动pause，以便可以将容器添加到pod中
docker run -d --name pause k8s.gcr.io/pause-amd64:3.1


#nginx
cat <<EOF >> /tmp/nginx.conf
> error_log stderr;
> events { worker_connections  1024; }
> http {
>     access_log /dev/stdout combined;
>     server {
>         listen 80 default_server;
>         server_name example.com www.example.com;
>         location / {
>             proxy_pass http://127.0.0.1:2368;
>         }
>     }
> }
> EOF


#指定网络和命名空间

docker run -d --name nginx -v /tmp/nginx.conf:/etc/nginc/nginx.conf -p 8880:80 --net=container:pause --ipc=container:pause --pid=container:pause docker.io/nginx:lates

#ghost博客
docker run -d --name ghost --net=container:pause --ipc=container:pause --pid=container:pause docker.io/ghost:latest
```

在这两种情况下，我们将`pasue`容器指定为我们要加入的**命名空间**容器。这将有效地创建我们的pod。

访问<localhost:8880>可以看到`ghost`通过`nginx`代理运行。因为网络命名空间在`pause`, `nginx`, `ghost`容器之间共享。
而这两个容器的`init`进程都是`pause`这个容器。

```
docker logs -f nginx

192.168.31.28 - - [08/Aug/2018:02:00:49 +0000] "GET / HTTP/1.1" 200 3195 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
192.168.31.28 - - [08/Aug/2018:02:00:49 +0000] "GET /assets/built/screen.css?v=0bf822a279 HTTP/1.1" 200 7360 "http://node:8880/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
......


docker logs -f ghost

[2018-08-08 02:00:30] INFO Creating table: posts
[2018-08-08 02:00:30] INFO Creating table: users
[2018-08-08 02:00:30] INFO Creating table: posts_authors
......



#查看init
docker exec -it ghost /bin/bash

root@f12a374141a7:/var/lib/ghost# ps  -ef
UID        PID  PPID  C STIME TTY          TIME CMD
root         1     0  0 01:55 ?        00:00:00 /pause
root         5     0  0 01:58 ?        00:00:00 nginx: master process nginx -g daemon off;
systemd+     9     5  0 01:58 ?        00:00:00 nginx: worker process
node        10     0  0 02:00 ?        00:00:03 node current/index.js
root       127     0  0 02:37 ?        00:00:00 /bin/bash
root       131   127  0 02:37 ?        00:00:00 ps -ef

```




<br/>
<br/>



## 构建大型集群

Building Large Clusters


在k8s v1.11，k8s支持做多5 000个节点的集群。更具体地说，支持满足以下条件的配置：

- 不超过5 000个node
- 总量不超过150 000个pod
- 总量不超过300 000个container
- 每个节点不超过100个pod


<br/>
<br/>


## 使用salt配置k8s

Configuring Kubernetes with Salt


k8s集群能够使用salt进行配置。



<br/>
<br/>


## 验证节点配置

Validate Node Setup


<br/>


**节点一致性测试**
Node Conformance Test

节点一致性测试是一种容器化测试框架，为节点提供系统验证和功能测试。
该测试验证节点是够满足k8s的最低要求，通过测试的节点有资格加入k8s集群。


<br/>


**局限**
Limitations

在k8s v1.5中，节点一致性测试具有如下限制：

- 节点一致性测试仅支持Docker作为容器runtime


<br/>


**节点先决条件**
Node Prerequisite

要运行节点一致性测试，节点必须满足与标准k8s节点相同的先决条件。该节点至少要安装一下守护进程:

- Container Runtime(Docker)
- Kubelet


<br/>

**运行节点一致性测试**
Running Node Conformance Test

执行如下步骤：

```
1. 将kubelet执行localhost，测试框架启动一个master来测试kubelet
#可使用 --pod-cidr, --cloud-provide标志
--api-servers="http://localhost:8080"


2. 运行节点一致性测试
# $CONFIG_DIR is the pod manifest path of your Kubelet.
# $LOG_DIR is the test output path.
sudo docker run -it --rm --privileged --net=host \
  -v /:/rootfs -v $CONFIG_DIR:$CONFIG_DIR -v $LOG_DIR:/var/result \
  k8s.gcr.io/node-test:0.2


#一致性测试的架构支持
node-test-adm64
node-test-arm
node-test-arm64
```


<br>


**运行选定测试**
Running Selected Test

```
#运行指定测试，使用你想要运行的测试的正则表达式 覆盖环境变量FOCUS
sudo docker run -it --rm --privileged --net=host \
  -v /:/rootfs:ro -v $CONFIG_DIR:$CONFIG_DIR -v $LOG_DIR:/var/result \
  -e FOCUS=MirrorPod \ # Only run MirrorPod test
  k8s.gcr.io/node-test:0.2


#跳过指定测试，覆盖环境变量SKIP
sudo docker run -it --rm --privileged --net=host \
  -v /:/rootfs:ro -v $CONFIG_DIR:$CONFIG_DIR -v $LOG_DIR:/var/result \
  -e SKIP=MirrorPod \ # Run all conformance tests but skip MirrorPod test
  k8s.gcr.io/node-test:0.2

```

强烈建议仅运行一致性测试，因为它需要更复杂的配置来运行不一致性测试。





<br/>
<br/>

---

<br/>




# 概念

concepts


概念部分可帮助你了解k8s系统的各个部分以及k8s用于表示集群的抽象，并帮助你更深入地了解k8s的工作原理。


<br/>



## 标准词汇

Standardized Glossary


<br>

- **Annotation**
用于将任意非标识元数据(metadata)附加到随想的键值对。

- **Application Architect**
负责程序高级设计的人员。

- **Application Developer**
编写在Kubernetes集群中运行的应用程序的人。

- **Approver**
可以审批Kubernetes代码贡献的人。

- **CLA(Contributor License Agreement)**
贡献者向开源项目授予其贡献许可的条款。

- **Certificate**
一个加密安全文件，用于验证对Kubernetes集群的访问的加密。

- **Cloud Controller Manager**

- **Cloud Provider**

- **Cluster**
一组称为节点(node)的机器，运行着由Kubernetes管理的容器化的应用程序。

- **Cluster Architect**
设计一个或多个Kubernetes集群的基础架构的人。

- **Cluster Operator**
配置，控制和监控集群的人。

- **Code Contributor**
为Kubernetes开源代码库开发和共享代码的人。

- **ConfigMap**
一个API对象，用于在键值对中存储非机密的数据。可认为是环境变量，命令行参数...

- **Container**
一个轻量化和可移植的包含应用程序及其依赖项的可执行的镜像。

- **Container Environment Variables**
容器环境变量是`name/value`对，为Pod中运行的容器提供有用的信息。

- **Contributor**
捐赠代码，文档或时间来帮助Kubernetes项目或社区的人。

- **Controller**
一个控制循环，通过APIServer监视集群的共享状态，并进行修改，尝试将当前状态移至理想(desired)状态。

- **CronJob**
管理一个定期运行的工作。

- **CustomResourceDefinition**
自定义码，用于定义要添加到Kubernetes APIServer的资源，而无需构建完整的自定义服务器。

- **DaemonSet**
确保Pod的副本在集群的一组节点上运行。

- **Deployment**
一个管理副本应用程序的API对象

- **Dynamic Volume Provision**
允许用户请求自动创建存储卷。

- **etcd**
一致且高度可用的键值存储，用作Kubernetes所有集群数据的备份存储。

- **Helm Chart**
可以使用Helm工具管理的预配置Kubernetes资源包。

- **Horizontal Pod Autoscaler**
一个API资源，可根据目标CPU利用率或自定义的指标自动调整Pod副本数。

- **Image**
一个容器的存储实例，其中包含运行一个应用程序需要的一组软件。

- **Ingress**
一个管理集群中服务的外部访问的API对象，通常是HTTP。

- **Init Container**
一个或多个初始化容器，必须在任意应用程序容器运行之前完成运行。

- **Istio**
一个开放平台，提供统一的方式来继承微服务，管理流量，实施策略和聚合遥测数据。

- **Job**
运行完成的 有限/一批 任务。

- **Kops**
一个命令行工具，可帮助你创建，销毁，升级和维护生产级、高可用性的Kubernetes集群。(仅支持AWS)

- **Kubeadm**
一个快速安装Kubernetes和设置安全集群的工具。

- **Kubectl**
用于与Kubernetes APIServer通信的命令行工具。

- **Kubelet**
在集群的每个节点上运行的Agent。它确保容器运行在Pod中。

- **Kubernetes API**
通过RESTful接口提供Kubernetes功能的应用程序，用于存储集群的状态。

- **Label**
标记与用户有意义且相关的标识属性的对象。

- **Minikube**
一个在本地运行Kubernetes的工具。

- **Name**
客户端提供的字符串，用于引用资源URL中的对象。如`/api/vi/pods/some-name`.

- **Namespace**
一个抽象概念，用于Kubernetes支持同一物理集群上的多个虚拟集群。

- **Network Policy**
允许Pod组如何与其它网络端点进行通信的规范。

- **Node**
节点是Kubernetes中的一个工作机器。

- **Persistent Volume**
一个表示集群中一块存储的API对象。

- **Persistent Volume Claim**
声明定义在一个PersistentVolume中的存储资源，以便可以作为一个volume挂载到容器中。

- **Pod**
最小和最简单的Kubernetes对象。Pod表示集群上一组正在运行的容器。

- **Pod Security Policy**
启用Pod创建和更新的细粒度授权。

- **PodPreset**
一个API对象，在创建时将信息(secrets, volume, env var...)注入到Pod中。

- **RBAC（role-basesd access control)**
管理授权决策，允许管理员通过Kubernetes API动态配置访问策略。

- **ReplicaSet**
副本集是下一代副本控制器。

- **Resource Quotas**
提供限制每个命名空间的聚合资源消耗的约束。

- **Reviemer**
在项目的某些部分检查代码质量和正确性的人。

- **Secret**
存储敏感信息，如密码，token...

- **Security Context**
`securityContext`字段定义Pod或容器的权限和访问控制设置，包括运行时UID和GID。

- **Selector**
允许用户根据label过滤资源列表。

- **Service**
一个API对象，描述如何访问应用程序，并可以描述端口和负载均衡器。

- **Service Account**
为运行在Pod中的进程提供一个标识。

- **Service Catalog**
一个扩展API，允许Kubernetes集群中运行的应用程序能够轻松使用外部托管软件，如数据库存储服务。

- **StatefulSet**
管理一组Pods的部署和伸缩，并提供有关这些Pod的排序和唯一性的保证。

- **UID**
Kubernetes系统生成的一个字符串，用于唯一标识对象。

- **Volume**
一个包含数据的目录，可供Pod中的容器访问。

- **Volume Plugin**
卷插件可在Pod中集成存储。

- **kube-apiserver**
一个Master组件，用于暴露Kubernetes API。它是Kubernetes控制面的前端。

- **kube-controller-manager**
一个Master组件，用于运行控制器。

- **kube-proxy**
运行在集群中的每一个节点上的网络代理。

- **kube-scheduler**
Master上的组件，用于监测未创建节点新创建的Pod，并选择一个节点供其运行。



<br/>
<br/>



## 概述


### K8s是什么

Kubernetes（常简称为K8s），Kubernetes的名字来自希腊语，意思是“舵手”或“领航员”。K8s是将8个字母“ubernete”替换为“8”的缩写。
它用于自动部署、扩展和管理容器化（containerized）应用程序的开源系统。它旨在提供“跨主机集群的自动部署、扩展以及运行应用程序容器的平台”。它支持一系列容器工具, 包括Docker等。

通过Kubernetes你可以：

- 快速部署应用
- 快速扩展应用
- 无缝对接新的应用功能
- 优化硬件资源，降低成本

Kubernetes特点：

- 可移植(portable)
- 可扩展( extensible)
- 自动化(automatic)

容器优点：

- 快速创建/部署应用
- 持续开发、集成和部署(CI/CD)
- 开发和运维相分离
- 开发、测试、生产环境的一致性
- 可移植性
- 松耦合、分布式、弹性伸缩、微服务化
- 资源隔离
- 资源利用

<br>

**Kubernetes能做什么**
Kubernetes还允许开发人员从物理和虚拟机脱离，从以主机为中心的基础架构转移到以容器为中心的基础架构。这样可以使用容器固有的全部优点。

Kubernetes满足的应用程序常见需求：

- Pod
- 挂载外部存储
- 分布式secrets
- 应用健康检查
- 副本应用实例
- 横向自动伸缩
- 服务发现
- 负载均衡
- 滚动更新
- 资源监控
- 日志采集和存储
- 自检和调试
- 认证和授权

这提供了**平台即服务(PAAS)**的简单性以及**基础架构即服务(IAAS)**的灵活性，并促进基础设施供应商的可移植性。

<br>

**Kubernetes不是什么**
Kubernetes 不是一个传统意义上，包罗万象的PaaS(平台即服务)系统。

- 不限制支持的应用程序类型，不限制应用程序框架
- 不提供中间件(如消息中间件)、数据处理框架(如spark)，数据库或集群存储系统
- 不提供点击即部署的服务市场
- 不部署代码不构建应用
- 允许用户选择日志、监控和报警
- 不提供或授权一个全面的应用程序配置系统/语言
- 不提供任何机器配置、维护、管理或自我修复系统

你可以自定义你的PAAS，与你选择的CI系统集成，或与Kubernetes一起使用，将你的容器镜像部署到Kubernetes。
由于Kubernetes在应用级别而不仅仅在硬件级别上运行，因此它提供了PAAS产品通用的一些功能。如部署、扩展、负载均衡、日志记录、监控等。


<br/>
<br/>


### k8s组件

Kubernetes Components


Kubernetes 所需的各种二进制组件, 用于提供齐全的功能。


<br/>


#### Master组件

Master组件提供的集群控制面(control plane)。Master作出集群的全局决策，以及检测和相应集群事件。
Master组件可在集群中任何节点上运行。然而，为了简单，通常在一台机器上启动所有Master组件，并且不会在此机器上运行用户容器。
可使用多个机器的设置来构建**高可用性能集群**。

<br>

**kube-apiserver**
`kube-apiserver`对外展示Kubernetes API。它是Kubernetes前端控制层，任何的资源请求/调用都是通过它提供的接口进行。
它被设计为水平扩展，即通过部署更多实例来扩展。

<br>

**etcd**
持久化和高可用的K/V存储，用于Kubernetes所有集群数据的后端存储。
请始终为k8s集群的etcd数据做备份。

<br>

**kube-controller-manager**
Master上运行的控制器组件，它们是集群中处理常规任务的后台线程。
逻辑上讲，每个控制器都是一个单独的进程，但为了降低复杂性，它们都被编译为单个二进制文件并在单个进程中运行。

这些控制器包含：

- 节点控制器(Node Controller): 负责在节点故障时通知和响应
- 副本控制器(Replication Controller): 负责维护系统中每个副本控制器对象正确的pod数
- 端点控制器(Endpoints Controller): 填入端点对象
- 服务账户(service accoute)和令牌控制器(token controller): 为新的命名空间(namespace)创建默认账户和API访问令牌

<br>

**cloud-controller-manager**
云控制器管理器用于与底层云提供商进行交互。它仅运行云提供商特定的控制器循环。你必须在`kube-controller-manager`中禁用这些controller loops，将`--cloud-provider`标志设置为`external`来禁用。

以下控制器具有云提供商依赖关系：

- 节点控制器: 用于检查云服务商提供的程序
- 路由控制器: 用于在底层云基础架构中设置路由
- 服务控制器: 用于创建，更新，删除云服务商提供的负载均衡器
- 数据卷控制器: 用于创建，附件和挂载卷，以及与云服务商提供的卷进行交互

<br>

**kube-scheduler**
监视还未分配节点的新创建的pod，选择一个节点供pod运行。
调度决策所考虑的因素包括： 个体/集体的资源需求，硬件/软件/策略的约束，亲和力/反亲和性的规范，工作负载和期限。


<br/>
<br/>


#### Node组件

节点(node)组件运行在每个节点，维护运行的pod并提供Kubernetes运行时环境。

<br>

**kubelet**
在集群中每个节点上运行的Agent，它确保container运行在pod中。
kubelet采用通过各种机制提供的一组PodSpecs，并确保这些PodSpecs中描述的容器运行且健康。kubelet不管理不是由k8s创建的容器。

提供如下功能：

- 挂载pod所需的数据卷
- 下载pod的secrets
- pod中运行docker容器
- 周期性的容器健康检查
- 如有需要，通过创建`mirror pod`将pod的状态报告回系统的其余部分
- 将节点的状态报告回系统的其余部分

<br>

**kube-proxy**
通过维护主机上的网络规则并执行连接转发，来实现Kubernetes服务抽象。

<br>

**container runtime**
负责运行容器的软件。k8s支持多种runtimes： docker, rkt, runc...

<br>

**docker, rkt, supervisord, fluentd...**


<br/>
<br/>


#### Addons

扩展是实现集群功能的Pod和Service。pod可由Deployment， Replication等管理。命名空间扩展对象在`kube-system`命名空间中创建。

<br>

**DNS**
虽然其它插件并非严格要求，但所有k8s集群都应具有集群DNS，因为许多示例都依赖于它。
集群DNS是一个DNS服务器，除了你环境中的DNS服务器，它还为k8s服务提供DNS记录。
由k8s启动的容器会在DNS搜索中自动包含此DNS服务器。

<br>

**Web UI(dashboard)**
仪表盘。

<br>

**container resource monitoring**
记录有关中央数据库中容器的通用时间序列度量标准，并提供用于浏览该数据的UI。

<br>

**cluster-level logging**
集群级别的日志记录机制，复制将容器日志保存到具有`search/browse`界面的中央日志存储。


<br/>
<br/>


### k8s API

k8s API还可作为系统声明性配置架构的基础。`kubectl`命令行工具可用于创建，更新，删除和获取API对象。
k8s还根据API资源存储其序列化状态(etcd中)。k8s自身被分解为多个组件，这些组件通过其API进行交互。

<br>

**OpenAPI和Swagger定义**
完整的API详细信息记录在`Swagger v1.2`和`OpenAPI`。k8s apiserver(master)公开了一个API，可用于检索位于`/swaggerapi`的`Swagger v1.2 k8s API`.
从k8s 1.10开始，OpenAPI规范在单个`/openapi/v2`端点中提供。单独格式的端点(如`swagger.json...`)已被弃用，后面会被移除。

通过设置HTTP header指定请求格式:

| Header | Possible Values |
| - | - |
| Accept | application/json, application/com.github.proto-openapi.spec.v2@v1.0+protobuf (the default content-type is application/json for */* or not passing this header) |
| Accept-Encoding | gzip (not passing this header is acceptable) |

栗子：

| Before 1.10 | Starting with Kubernetes 1.10 |
| - | - |
| GET /swagger.json	| GET /openapi/v2 Accept: application/json |
| GET /swagger-2.0.0.pb-v1 | GET /openapi/v2 Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf |
| GET /swagger-2.0.0.pb-v1.gz | GET /openapi/v2 Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf Accept-Encoding: gzip |

<br>

```
#查看
curl localhost:8080
{
  "paths": [
    "/api",
    "/api/v1",
    "/apis",
    "/apis/apps",
    "/apis/apps/v1beta1",
    "/apis/authentication.k8s.io",
    "/apis/authentication.k8s.io/v1beta1",
    "/apis/authorization.k8s.io",
    "/apis/authorization.k8s.io/v1beta1",
    "/apis/autoscaling",
    "/apis/autoscaling/v1",
    "/apis/batch",
    "/apis/batch/v1",
    "/apis/batch/v2alpha1",
    "/apis/certificates.k8s.io",
    "/apis/certificates.k8s.io/v1alpha1",
    "/apis/extensions",
    "/apis/extensions/v1beta1",
    "/apis/policy",
    "/apis/policy/v1beta1",
    "/apis/rbac.authorization.k8s.io",
    "/apis/rbac.authorization.k8s.io/v1alpha1",
    "/apis/storage.k8s.io",
    "/apis/storage.k8s.io/v1beta1",
    "/healthz",
    "/healthz/ping",
    "/healthz/poststarthook/bootstrap-controller",
    "/healthz/poststarthook/extensions/third-party-resources",
    "/healthz/poststarthook/rbac/bootstrap-roles",
    "/logs",
    "/metrics",
    "/swaggerapi/",
    "/ui/",
    "/version"
  ]
```

<br>

**API 版本**
为了更容易消除字段或重构资源表示，k8s支持多个API版本，每个版本位于不同的API路径。如`/api/vi`或`/apis/extensions/v1beta1`.

我们选择在API级别，而不是资源级别/字段级别进行版本控制，以确保API提供干净、一致的系统资源和行为视图，并允许控制对生命末端和实验性API的访问。json和protobuf序列化模式都遵循相同的模式更改指南。请注意，API版本和软件版本仅间接相关。

不同的API版本意味着不同级别的稳定性和支持：

- Alpha level
	+ 版本名包含alpha(如 v1aplha1)
	+ 启用该功能可能会暴露bug，默认禁用
	+ 可随时删除对功能的支持，恕不另行通知
	+ 可能会在以后软件版本中以不兼容的方式更改，恕不另行通知
	+ 由于错误风险和缺乏长期支持，建议仅在短期测试集群中使用
- Beta level
	+ 版本名包含beta(如 v2beta3)
	+ 代码经过充分测试，启用该功能被认为是安全的。默认启用
	+ 虽然细节会有所变化，但不会删除对整体功能的支持
	+ 建议仅用于非关键业务，因为后续版本可能会发生不兼容的更改
	+ 请尝试我们测试版功能并提供反馈
- Stable level
	+ 版本名是vx，x为整数
	+ 许多后续版本的软件将出现稳定版的功能

<br>

**API groups**
为了更容易扩展k8s API，我们实施了`API Groups`，它在REST path和序列化对象的apiVersion字段中指定。

目前在使用的几个API groups:

- 核心组(core group)，又称遗留组，位于REST path的`/api/v1`，并使用`apiVersion: v1`
- 命名组(named group)，位于REST path的`/apis/$GROUP_NAME/$VERSION`，并使用`apiVersion: $GROUP_NAME/$VERSION`

两种受支持的自定义资源扩展API的路径：

- 自定义资源(CustomResourceDefiniton) 适用于具有非常基本CRUD需求的用户
- 需要完整k8s API语义的用户可以实现自己的apiserver，并使用聚合器使其无缝连接到客户端

<br>

**启用 API groups**
默认情况下启用某些资源和API groups。通过在apiserver设置`--runtime-config`可启用/禁用它。此配置接收逗号分隔的KV，描述了apiserver运行时配置。

<br>

**在API groups中启用资源**
默认情况下启动 DeamonSets, Deployments, HorizontalPodAutoscalers, Ingress, Jobs, ReplicaSets。其它扩展资源可通过在apiserver上设置`--runtime-config`启用或禁用。



<br/>
<br/>



### k8s 对象

本节解释了如何在k8s API中表示k8s对象，以及如何以`.yaml`格式表示它们。


<br/>


#### 理解k8s对象

在k8s系统中，k8s对象是持久化的实体。k8s使用这些实体来表示整个集群的状态。特别地，它们描述了如下信息：

- 哪些容器化应用程序正在运行(以及运行在哪个节点上)
- 可以被这些应用程序使用的资源
- 应用程序行为方式的策略(重启、升级、容错)

k8s 对象是一个**意图记录(record of intent)** —— 一旦创建了对象，k8s系统将持续工作以确保对象存在。通过创建一个对象，你可以有效地告诉k8s系统你希望集群的工作负载看起来像什么，这是你的集群的**期望状态(desired state)**。
要使用k8s对象(创建, 修改, 删除)，需要使用k8s API。当你使用`kubectl`命令行接口时，CLI会为你进行必要的k8s API调用。

<br>

**对象规约与状态**
Object Spec and Status

每个k8s 对象都包含了两个嵌套的对象字段，用于控制对象的配置：**对象规约**和**对象状态**。
在任何时刻，k8s controller plane都会主动管理对象的实际状态，以匹配你提供的期望状态。

- 规约(spec)，必须提供。描述了对象的期望状态(diresed state)——你希望对象具有的特征。
- 状态(status)，描述对象的实际状态，由k8s系统提供和更新。

例如，k8s Deployment是一个可以表示你集群上运行的应用程序的对象。当你创建一个Deployment，你可以设置部署规约以指定你希望应用程序运行三个副本。k8s系统读取部署规约并启动应用程序所需的三个实例——更新状态以符合你的规范。如果这些事例中的任何一个失败(状态改变)，k8s系统通过进行校正来响应规约和状态之间的差异。在这种情况下，启动替换实例。

<br>

**描述k8s 对象**
在k8s中创建对象时，必须提供描述其期望状态的对象规约，以及有关对象的一些基本信息(如 名称)。当你使用k8s API来创建对象时，API请求必须在请求正文中将信息作为JSON格式。通常，你在`.yaml`文件中向`kubectl`提供信息，`kubectl`在发出API请求时将信息转换为JSON格式。

栗子：

```
# for versions before 1.9.0 use apps/v1beta2
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

使用类似上面的`.yaml`文件创建部署的方法，是在`kubectl`命令行工具中使用`kubectl create`命令，将`.yaml`文件作为参数传递。

```
kubectl create -f https://k8s.io/examples/application/deployment.yaml --record
#deployment "nginx-deployment" created
```

<br>

**必填字段**
在要创建k8s 对象的`.yaml`文件中，必须配置一下字段：

- `apiVersion`： 创建对象的k8s API版本
- `kind`： 创建的对象类型
- `metadata`： 有助于识别对象唯一性的数据，包括name, uid, namespace...

你还需要提供`spec`字段。对于每个k8s对象，对象规约的精确格式是不同的，并且包含特定于该对象的嵌套字段。


<br/>
<br/>


#### Names

Kubernetes REST API中所有对象都用**Name**和**UID**来明确标识。
对于用户提供的非唯一的属性，k8s提供**labels**和**annotations**。

<br>

**Names**
客户端提供的字符串，用于引用资源URL中的对象。如`/api/v1/pods/some-name`.
一个给定`kind`的对象同时只能有一个`name`。但如果你删除了此对象，便可以为新对象赋予此名字。
按照惯例，k8s资源的名称的最大长度应为253个字符，并由`小写字母,数字, -, .`字符组成。但某些资源可能具有更过限制。

<br>

**UIDs**
k8s 系统生成的字符串，用于唯一标识对象。
在k8s集群的整个生命周期中创建的每个对象都具有一个唯一的UID。它旨在区分类似实体的历史事件。


<br/>
<br/>


#### Namespace

k8s支持在物理集群中创建多个虚拟集群，这些虚拟机群称为`namespaces`。命名空间是一种将集群资源划分为多个用途的方法。
命名空间名称满足正则表达式，最大长度为63位。

<br>

**什么时候使用多个命名空间**
命名空间旨在用于多个用户分布在多个团队/多个项目的环境中。对于具有几个到几十个用户的集群，你根本不需要创建和考虑命名空间。
命名空间提供名称范围。资源名称在命名空间中必须唯一，但不能跨命名空间。
命名空间是一种在多个用户之间划分集群资源的方法。
在k8s的未来版本中，默认情况下，同一命名空间中的对象将具有相同的访问控制策略(ACP)。
没有必要使用多个命名空间仅来分隔略有不同的资源。如同一软件的不同版本，使用`labels`来区分同一命名空间内的资源。

<br>

**操作命名空间**

```sh
#查看
kubectl get ns
NAME          STATUS    AGE
default       Active    13d
kube-system   Active    13d


#通过命令创建
kubectl create namespace my-namespace


#或通过文件创建
vim my-namespace.yaml

apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace

kubectl create -f ./my-namespace.yaml


#查看
kubectl get namespace
NAME           STATUS    AGE
default        Active    13d
kube-system    Active    13d
my-namespace   Active    4s

#删除
kubectl delete namespace my-namespace


#设置请求的命名空间
#使用--namespace标志临时设置请求的命名空间
kubectl kubectl get pods --namespace=default

#设置命名空间首选项
kubectl config set-context $(kubectl config current-context) --namespace=my-namespace
kubectl config view
```

Kubernetes有三个初始的命名空间：

- `default`: 没有其它命名空间时，对象的默认命名空间
- `kube-system`: k8s系统创建的对象的命名空间
- `kube-public`: 此命名空间是自动创建的，可供所有用户读取(包括未认证用户)。此命名空间主要用于集群使用，以防止某些资源在整个集群中可见且可公开读取。此命名空间的公共方面只是一个约定，而非要求。

注意：

- 删除一个命名空间会自动删除所有属于该命名空间的资源
- k8s初始化的两个命名空间无法删除
- 持久化卷(persistent volume)不属于任何命名空间，但持久化卷声明(persistent volume claim)是属于某个特定命名空间的
- 事件(event)是否属于命名空间取决于产生事件的对象

<br>

**命名空间和DNS**
当你创建一个服务(service)，它会创建相应的DNS条目(dns entry)。此条目的格式为`<service-name>.<namespace-name>.svc.cluster.local`，这表示如果一个容器只是用`<service-name>`，它将会解析为命名空间本地的服务。这对于在多个命名空间(如 开发/测试/生产)中使用相同的配置非常有用。如果想要扩命名空间访问，则需要使用完全限定的域名(fully qualified domain name)。

<br>

**不是所有对象都在命名空间中**
大多数k8s资源(pods, services, replication controller...)都在某些命名空间中。然而，命名空间资源本身并不在命名空间中。并且，低级资源(node, persistentVolumes)并不在任何命名空间中。

查看k8s资源是否在命名空间中：

```
kubectl api-resources --namespaced=true
kubectl api-resources --namespaced=false
```



<br/>
<br/>


#### Labels和Selectors


标签是被关联到对象上的`key/value`对。标签旨在用于指定对用户有意义且相关的对象的标识属性，但不直接按时核心系统的语义。标签可用于组织和选择对象的子集。标签可在创建时附加到对象，随时可以添加和修改。每个对象可拥有多个标签，对于给定的对象，`key`必须唯一。

```json
"metadata": {
  "labels": {
    "key1" : "value1",
    "key2" : "value2",
    "keyN" : "valueN"
  }
}


#栗子
"labels": {
  "release" : "stable",
  "environment" : "dev",
  "track" : "daily"
}
```

我们最终将**索引(index)**和**反向索引(reverse-index)**标签，用于高效查询和监视，使用它们在UI和CLI中进行排序和分组。我们不希望对非标识(non-identifying)信息使用标签，特别是大型结构化数据。非标识信息应该记录到`annorations`。

标签使用户能够以松散耦合的方式将自己的组织结构映射到系统对象中，而无需客户端存储这些映射。

<br>

**语法和字符集**
有效的label key有两个字段: 可选前缀和名称，用斜杆分隔。
名字字段是必须的，小于等于63个字符，以字母数字开头和结尾，还可使用`-, _, .`三个字符。
前缀可选。如果指定，前缀必须是DNS子域，不超过253个字符，后跟斜杆`/`。如果省略，则假定label key对用户是私有的。向最终用户对象添加标签的自动系统组件(kube-scheduler, kube-apserver...)必须制定前缀。`kuberneter.io/`前缀保留个k8s核心组件。

有效的label value必须小于等于63个字符，可为空，或以字母数字开头和结尾，还可使用`-, _, .`三个字符。

<br>

**label selectors**
标签不提供唯一性。通常，我们希望许多对象携带相同的标签。
通过`label selector`，客户端/用户 可以识别一组对象。标签选择器是k8s中的核心分组原语。

API目前支持两种类型的选择器: `equality-based`和`set-based`。标签选择器可由逗号`,`分隔的多个要求组成。
一个空(empty)标签选择器(zero requirements)，选择集合中的每个对象。
一个空(null)标签选择器(仅可用于选择器字段)不选择任何对象。

**equality-based requirement**
基于平等/不平等的要求允许按标签键和值进行过滤。匹配对象必须满足所有指定的标签约束，尽管它们也可能具有其它标签。
允许三种运算符:`=, ==, !=`。

```
environment = production
tier != frontend
```

**set-based requirement**
基于集合的标签的要求允许根据一组值过滤键。
支持三种操作符: `in, notin, exists`。

```
environment in (production, qa)
tier notin (frontend, backend)
partition
!partition
```

<br>

**API**

LIST and WATCH filtering
`LIST`和`WATCH`操作可以指定标签选择器来过滤使用查询参数返回的对象集。两个要求都是允许的。
两种标签选择器的样式都可使用通过TEST客户端列出或查看资源。

- equality-based requirements: `?labelSelector=environment%3Dproduction,tier%3Dfrontend`
- set-based requirements: `?labelSelector=environment+in+%28production%2Cqa%29%2Ctier+in+%28frontend%29`

```sh
#equality-based
kubectl get pods -l environment=production,tier=frontend


#set-based
kubectl get pods -l 'environment in (production),tier in (frontend)'
kubectl get pods -l 'environment in (production, qa)'
kubectl get pods -l 'environment,environment notin (frontend)'
```

<br>

**Service and ReplicationController**
服务所针对的一组pod使用标签选择器进行定义。类似地，副本控制器应该管理的pod数量也使用标签选择器定义。

```
#json格式
"selector": {
  "component": "redis"
}


#yaml格式
selector:
  component: redis
```


<br/>
<br/>


#### Annotation

你可使用k8s `annotation`(注释)将任意非标识(non-identifying)元数据附加到对象。工具和库等客户端可以检索此元数据。它也是`key/value`对。
Annotations不会被k8s直接使用，其主要目的是方便用户阅读查找。

<br>

**将元数据追加到对象**
你可使用`label`或`annotations`将原数据追加到k8s对象。
标签用于选择对象和查找满足特定条件的对象集合。
相反，注释不用于识别和选择对象。

```json
"metadata": {
  "annotations": {
    "key1" : "value1",
    "key2" : "value2"
  }
}
```


<br/>
<br/>


#### Field Selectors

字段选择器允许你根据一个或多个资源字段的值选择k8s资源。

栗子：

```
#三种操作符
=, ==, !=


metadata.name=my-service
metadata.namespace!=default
status.phase=Pending



#
kubectl get pods --field-selector status.phase=Running
NAME                           READY     STATUS    RESTARTS   AGE
hello-world-3198537413-138pg   1/1       Running   0          5d
hello-world-3198537413-67g6d   1/1       Running   0          5d
hello-world-3198537413-bf73l   1/1       Running   0          5d
hello-world-3198537413-ddgb3   1/1       Running   0          5d
hello-world-3198537413-ffj90   1/1       Running   0          5d

#
kubectl get  ingress --field-selector foo.bar=baz

#
kubectl get pods --field-selector=status.phase!=Running,spec.restartPolicy=Always

#
kubectl get statefulsets,services --field-selector metadata.namespace!=default
```


<br/>
<br/>


#### Recommended Labels

你可以使用比`kubectl`和`dashboard`更多的工具来可视化和管理k8s对象。一组通用的标签允许工具以互操作的方式工作，以所有工具都能理解的通用方式描述对象。
除了支持工具之外，推荐的标签还以可查询的方式描述应用程序。

`shared labels and annotations`共享一个通用的前缀: `app.kubernetes.io`。没有前缀的标签对用户是私有的。共享前缀可确保共享标签不会干扰自定义用户标签。

<br>

为了充分利用这些标签，应将它们应用于每个资源对象。

| Key | Description | Example | Type |
| - | - | - | - |
| app.kubernetes.io/name | The name of the application | mysql | string |
| app.kubernetes.io/instance | A unique name identifying the instance of an application | wordpress-abcxzy | string |
| app.kubernetes.io/version | The current version of the application (e.g., a semantic version, revision hash, etc.) | 5.7.21 | string |
| app.kubernetes.io/component | The component within the architecture | database | string |
| app.kubernetes.io/part-of | The name of a higher level application this one is part of | wordpress | string |
| app.kubernetes.io/managed-by | The tool being used to manage the operation of an application | helm | string |

要说明这些标签的运行情况，请考虑一下`StatefulSet`对象:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  labels:
    app.kubernetes.io/name: mysql
    app.kubernetes.io/instance: wordpress-abcxzy
    app.kubernetes.io/version: "5.7.21"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: wordpress
    app.kubernetes.io/managed-by: helm
```


<br/>
<br/>


### 使用kubectl进行对象管理

`kubectl`命令行工具支持多种方式来创建和管理k8s对象。
应该只使用一种技术来管理k8s对象。对同一个对象的混合和匹配技术会导致未定义的行为。

| Management technique | Operates on | Recommended environment | Supported writers | Learning curve |
| - | - | - | - | - |
| Imperative commands | Live objects | Development projects | 1+ | Lowest |
| Imperative object configuration | Individual files | Production projects | 1 | Moderate |
| Declarative object configuration | Directories of files | Production projects | 1+ | Highest |


<br/>
<br/>


#### 必要的命令

Managing Kubernetes Objects Using Imperative Commands

使用k8s命令行工具内置的必要命令，可直接快速创建、更新、删除k8s对象。

<br>

**权衡**
`kubectl`工具支持三种对象管理：

- Imperative commands(必要的命令)
- Imperative object configuration(必要的对象配置)
- Declarative object configuration(声明的对象配置)


<br/>
<br/>


##### 创建对象

`kubectl`工具支持动词驱动的命令，用以创建一些最常见的对象类型。这些命令被命名为即使不熟悉k8s对象类型的用户也能够识别。

```sh
#创建一个新的Deployment对象，以在一个或多个pod中运行container
run


#创建一个新的Service对象，以在pod间对流量进行负载均衡
expose


#创建一个新的Autoscaler对象，用以自动水平伸缩控制器
autoscale
```

`kubectl`工具还支持由对象类型驱动的创建命令。这些命令支持更多对象类型，并且更明确地表达了它们的意图，但要求用户知道他们打算创建的对象类型。

```sh
create <objecttype> [<subtype>] <instancename>

#栗子
kubectl create service nodeport <service-name>
```


<br/>
<br/>


##### 更新对象

`kubectl`命令支持动词驱动的命令，用于一些常见的更新操作。

```sh
#通过更新控制器的副本数，水平伸缩控制器，以添加或删除pod
scale


#在对象中添加或删除注释
annotate


#在对象中添加或删除标签
label
```

`kubectl`工具还支持由对象的某个驱动的更新命令:

```sh
#设置对象的一个方面
set
```

`kubectl`工具支持这些直接地更新实时对象的额外方法，但他们需要更好地裂解k8s对象模式。

```sh
#通过在编辑器中打开其配置，直接编辑实时对象的原始配置文件
edit


#使用补丁字符串，直接修改实时对象的特定字段
patch
```


<br/>
<br/>


##### 删除对象

```sh
#从集群中删除对象
delete <type>/<name>

kubectl delete deployment/nginx
```


<br/>
<br/>


##### 查看对象

如下这些命令可用于打印除对象信息:

```sh
#打印有关匹配对象的基本信息
get


#打印有关匹配对象的详细信息
describe


#打印运行在pod中容器的stdout和stderr
logs
```

<br/>
<br/>


##### 创建对象前修改对象

有些对象字段没有可在`create`命令汇总使用的标志。在某些情况下，你可使用`set`和`create`的组合在对象创建之前为字段指定值。

```sh
#set命令
kubectl create service clusterip my-svc --clusterip="None" -o yaml --dry-run \
| kubectl set selector --local -f - 'environment=qa' -o yaml \
| kubectl create -f -



#--edit标志
kubectl create service clusterip my-svc --clusterip="None" -o yaml --dry-run > /tmp/srv.yaml
kubectl create --edit -f /tmp/srv.yaml
```


<br/>
<br/>


#### 配置文件

Imperative Management of Kubernetes Objects Using Configuration Files

```
#创建对象
kubectl create -f <file | url>


#更新
kubectl replace -f <file | url>


#删除
kubectl delete -f <file | url>


#查看
kubectl get -f <file | url> -o yaml
```


<br/>
<br/>


#### 使用配置文件声明管理的k8s对象

Declarative Management of Kubernetes Objects Using Configuration Files

可通过在目录中存储多个对象配置文件来创建、更新、删除k8s对象，并使用`kubectl apply`根据递归创建和更新这些对象。
`kubectl apply`不支持对象配置命令`create`和`replace`。

<br>

**开始前**
声明性对象配置需要深入理解k8s对象定义和配置。


<br/>
<br/>


##### 创建对象

使用`kubectl apply`创建除指定目录中的配置文件定义的已存在的所有对象。

```sh
kubectl apply -f <directory>/
```

栗子：

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  minReadySeconds: 5
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80


#创建
kubectl apply -f https://k8s.io/examples/application/simple_deployment.yaml
#查看
kubectl get -f https://k8s.io/examples/application/simple_deployment.yaml -o yaml
```

<br/>
<br/>


##### 更新对象

使用`kubectl apply`更新目录中定义的所有对象，即使这些对象已经存在。

```
kubectl apply -f <directory>/
```

栗子：

```
#伸缩
kubectl scale deployment/nginx-deployment --replicas=2



#更新nginx版本，从1.7.9升级到1.11.9
#删除minReadySeconds字段
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.11.9
        ports:
        - containerPort: 80


#应用更新
kubectl apply -f https://k8s.io/examples/application/update_deployment.yaml
#查看
kubectl get -f https://k8s.io/examples/application/simple_deployment.yaml -o yaml
```


<br/>
<br/>


##### 删除对象

有两种方法:

```
#推荐
kubectl delete -f <filename>

#选择
kubectl apply -f <directory/> --prune -l <labels>

```


<br/>
<br/>


##### 查看对象

```
kubectl get -f <file | url> -o yaml
```



<br/>
<br/>



## 计算,存储和网络


Compute, Storage, and Networking Extensions


<br/>


### 集群管理

Cluster Administration

- 规划集群
- 管理集群
- 保护集群
- 集群服务

详情见配置章节。


<br/>
<br/>


### 证书

Certificates

当使用客户端证书认证时，你可以通过`easyras, openssl, cfssl`手动生成证书。


<br/>


#### openssl

```sh
#Generate a ca.key with 2048bit
openssl genrsa -out ca.key 2048


#According to the ca.key generate a ca.crt
openssl req -x509 -new -nodes -key ca.key -subj "/CN=${MASTER_IP}" -days 10000 -out ca.crt


#Generate a server.key with 2048bit
openssl genrsa -out server.key 2048


#reate a config file for generating a Certificate Signing Request (CSR)
[ req ]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C = <country>
ST = <state>
L = <city>
O = <organization>
OU = <organization unit>
CN = <MASTER_IP>

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = kubernetes
DNS.2 = kubernetes.default
DNS.3 = kubernetes.default.svc
DNS.4 = kubernetes.default.svc.cluster
DNS.5 = kubernetes.default.svc.cluster.local
IP.1 = <MASTER_IP>
IP.2 = <MASTER_CLUSTER_IP>

[ v3_ext ]
authorityKeyIdentifier=keyid,issuer:always
basicConstraints=CA:FALSE
keyUsage=keyEncipherment,dataEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectAltName=@alt_names


#Generate the certificate signing request based on the config file
openssl req -new -key server.key -out server.csr -config csr.conf


#Generate the server certificate using the ca.key, ca.crt and server.csr
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
-CAcreateserial -out server.crt -days 10000 \
-extensions v3_ext -extfile csr.conf


#View the certificate
openssl x509  -noout -text -in ./server.crt
```


<br/>


#### easyrsa


<br/>


#### cfssl


<br/>


#### 分发自签名CA证书

客户端节点可以拒绝将自签名(self-signed)CA 证书识别为有效。对于非生产环境火灾防火墙后面运行的部署，你可以将自签名CA证书分发给客户端，并刷新本地列表以获取有效证书。

```sh
sudo cp ca.crt /usr/local/share/ca-certificates/kubernetes.crt
sudo update-ca-certificates

Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d....
done.
```


<br/>
<br/>



### 云提供商

跳过！



<br/>
<br/>



### 管理资源

可能，你已经部署应用程序并通过服务公开它。接下来怎么办？k8s提供了许多工具来帮助你管理应用程序部署(包括伸缩和更新)。我们将更深入讨论配置文件和标签。


<br/>


#### 组织资源配置

Organizing resource configurations

许多应用程序需要创建多个资源，如Deployment和Service。通过将多个资源组合在同一个文件中(在yaml中以`---`分隔)，可以简化多个资源的管理。

栗子：`nginx-app.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-nginx-svc
  labels:
    app: nginx
spec:
  type: LoadBalancer
  ports:
  - port: 80
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-nginx
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

使用与单个资源相同的方式创建多个资源。
资源将按照它们在文件中出现的顺序创建。因此，最好首先指定Service，因为这将确保Scheduler可以扩展与服务关联的pod，因为它们是由Controller创建的。

```sh
kubectl create -f https://k8s.io/examples/application/nginx-app.yaml

#service "my-nginx-svc" created
#deployment "my-nginx" created



#同样也支持多个-f
kubectl create -f https://k8s.io/examples/application/nginx/nginx-svc.yaml -f https://k8s.io/examples/application/nginx/nginx-deployment.yaml


#或者指定一个目录，读取yaml, yml, json文件
kubectl create -f https://k8s.io/examples/application/nginx/


#url
kubectl create -f https://raw.githubusercontent.com/kubernetes/website/master/content/en/examples/application/nginx/nginx-deployment.yaml

```

**建议的做法是，将与同一微服务或应用程序相关的资源放入同一配置文件中，或将相关联的配置文件分组到同一目录下。**



<br/>
<br/>


#### kubectl批量操作

Bulk operations in kubectl

资源创建并不是`kubectl`可执行的唯一操作。

```sh
kubectl delete -f https://k8s.io/examples/application/nginx-app.yaml

#deployment "my-nginx" deleted
#service "my-nginx-svc" deleted


#分开的资源
kubectl delete deployments/my-nginx    services/my-nginx-svc


#指定label(selector)删除
kubectl delete deployment,services -l app=nginx

#deployment "my-nginx" deleted
#service "my-nginx-svc" deleted


#递归删除--recursive -R
kubectl create -f project/k8s/development --recursive
kubectl create -f project/k8s/namespaces -f project/k8s/development --recursive
```


<br/>
<br/>


#### 高效使用label

Using labels effectively

到目前为止，我们使用的示例最多只能将一个标签应用于任意资源。在许多情况下，应该使用多个标签来区分集合。

```yaml
     labels:
        app: guestbook
        tier: backend
        role: master


#查看
kubectl get pods -Lapp -Ltier -Lrole

kubectl get pods -l app=guestbook,role=master
```


<br/>
<br/>


#### Canary deployments

需要多个标签的另一种情况是区分不同版本的部署，或同一组件的配置。通常的做法是将新应用程序版本的canary与先前版本并排部署，以便新版本可以在完全推出前接收实时生产流量。

例如，你可以使用`track`标签来区分不同的版本:

```yaml
#stable version
     name: frontend
     replicas: 3
     ...
     labels:
        app: guestbook
        tier: frontend
        track: stable
     ...
     image: gb-frontend:v3


#new version
     name: frontend-canary
     replicas: 1
     ...
     labels:
        app: guestbook
        tier: frontend
        track: canary
     ...
     image: gb-frontend:v4


#前端服务将通过选择其标签的公共子集(`track`)来跨越两组副本，以便将流量定向到两个应用程序。
  selector:
     app: guestbook
     tier: frontend
```


<br/>
<br/>


#### 更新标签

Updating labels

有时，在创建新资源之前，需要重新标记现有的pod和其它资源。这可使用`kubectl label`来完成。

```
#更新
kubectl label pods -l app=nginx tier=fe

#查看
kubectl get pods -l app=nginx -L tier
```


<br/>
<br/>


#### 更新注释

Updating annotations

有时，你会想要将注释附加到资源。这个使用`kubectl annotatie`来完成。

```
kubectl annotate pods my-nginx-v4-9gw19 description='my frontend running nginx'

#查看
kubectl get pod my-nginx-v4-9gw19 -o yaml
```


<br/>
<br/>


#### 伸缩应用程序

Scaling your application

当应用程序上的负载增大或缩小时，可以使用`kubectl`轻松扩展。

```sh
kubectl scale deployment/my-nginx --replicas=2

kubectl get pods -l app=nginx


#自动伸缩
kubectl autoscale deployment/my-nginx --min=1 --max=3
```


<br/>
<br/>


#### 就地更新资源

In-place updates of resources

有时，需要对创建的资源进行简单，无中断(non-disruptive)的更新。

**kubectl apply**
建议在源代码管理中维护一组配置文件，以便可以对它们配置的资源的代码进行维护和版本化。这样，你可以使用`kubectl apply`将更改的配置推送的集群。
`kubectl apply`会将注释附加到资源，以便确定自上次调用以来对配置所做的更改。在调用它是，`kubectl apply`会在先前的配置，提供的输入和资源的当前配置之间进行差异比较，已确定如何修改资源。

<br>

**kubectl edit**
或者，你可使用`kubectl edit`来更新资源。

```
kubectl edit deployment/my-nginx
#这样就和vim差不多，可修改此部署
```

<br>

**kubectl patch**
你可使用`kubectl patch`来更新API对象。此命令支持JSON patch, JSON merge patch和 strategic merge patch。


<br/>
<br/>


#### 破坏性更新

Disruptive updates

在某些情况下，你可能需要更新初始化后无法更新的资源字段，或者你可能只想立即进行递归更改，例如修复部署创建的损坏的pod。要更改此类资源，请使用`replace --force`——它将删除并重新创建资源。

```
kubectl replace -f https://k8s.io/examples/application/nginx/nginx-deployment.yaml --force
deployment "my-nginx" deleted
deployment "my-nginx" replaced
```


<br/>
<br/>


#### 在服务没有中断的情况下更新应用程序

Updating your application without a service outage

在某些时候，你最终需要更新已部署的应用程序，通常是指定新的image或image tag。`kubectl`支持多种更新操作，每种操作都适用于不同的场景。

```
kubectl run my-nginx --image=nginx:1.7.9 --replicas=3
#deployment "my-nginx" created

#更新nginx版本为: 1.9.1
kubectl edit deployment/my-nginx
#修改镜像那一行
```

部署将以声明的方式逐步更新已部署的nginx应用程序。它确保在更新时只有一定数量的旧副本可能会关闭，并且在所需数量的pod之上只能创建一定数量的新副本。



<br/>
<br/>



### 集群网络

Cluster Networking

默认情况下，k8s与docker的网络方式有所不同。有4个网络问题需要解决：

- **高度耦合的容器到容器的通信**: 这通过pod和localhost通信解决
- **pod到pod的通信**： 这是侧重点
- **pod到service的通信**： 这包含在Service中
- **external到service的通信**： 这包含在service中

k8s假设pod与pod间是可以通信的，无论它们位于哪个主机。每个pod都有自己的IP地址，因此你无需在pod之间明确创建链接，也几乎不需要处理映射容器端口到主机端口。这创建了一个干净的向后兼容的模型，从端口分配、命名、服务发现、负载均衡、应用程序配置和迁移的角度来看，pod可以像VM或物理主机一样。

为实现此目的，你需要设置集群网络。


<br/>


#### Docker模型

在讨论k8s网络方法之前，有必要回顾Docker网络方式。默认情况下，Docker使用`host-private`网络。它创建一个虚拟网桥(称为docker0)，并从RFC1918中为该网桥定义的一个专用地址块中分配一个子网。对于Docker创建的每个容器，它分配一个连接到网桥的虚拟以太网设备(称为veth)。使用Linux命名空间将`veth`映射为容器中的`eth0`。容器内的`eth0`网口从桥接器的地址范围获取IP地址。
为了使Docker容器跨节点进行通信，必须在计算机自己的IP地址上分配端口，然后将这些端口转发/代理到容器。这意味着容器必须小心地使用端口，或动态分配端口。


<br/>
<br/>


#### k8s模型

跨多开发者协调端口非常难以大规模地进行，并使用户暴露在他们无法控制的集群级别问题之外。动态端口分配给系统带来了很多复杂性——每个应用程序都必须将端口作为标志，API server必须知道如何将动态端口号插入配置块，服务必须知道如何找到彼此。与此相关，k8s采取了不同的方法。

k8s对任何网络实施都强加了一下基本要求：

- 容器间可互相通信而无需NAT
- 所有节点都可与所有容器通信而无需NAT
- 容器看到的IP与其他人看到的IP相同

实际上，k8s在pod范围应用IP地址，pod中的容器共享其网络命名空间(包括IP地址)。这意味着pod中的容器都可以在localhost上彼此通信。这被称为`ip-per-pod`模型。

```
#在Docker中查看
docker network inspect bridge

#可看到副本集的容器，都是pod，而非container
#这也证明container共享pod的网络空间
#注意它的网关便是docker0
[
    {
        "Name": "bridge",
        "Id": "68bc0cf07a4d7666e1d35f2c1cf179ae8605b431353ba93446abc898de086a9c",
        "Created": "2018-07-23T17:45:54.42038221+08:00",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.254.76.0/24",
                    "Gateway": "10.254.76.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Containers": {
            "7d2e6561fa81730ae05743f78871666df75cf5e6f483b71da33137823c172333": {
                "Name": "k8s_POD.24f70ba9_hello-world-3198537413-138pg_default_adb8f0fe-8fea-11e8-b10b-000c29aa7e75_785c4a84",
                "EndpointID": "bf50c5a71ad26531a370a73ce8da5903d32b9e2f8b8397d7405b914203071c45",
                "MacAddress": "02:42:0a:fe:4c:06",
                "IPv4Address": "10.254.76.6/24",
                "IPv6Address": ""
            },
            "ea9fbf660f27943b866759a084dc26457474d73c50082939f157ed1dfe0bc806": {
                "Name": "k8s_POD.24f70ba9_hello-world-3198537413-ddgb3_default_adb90c8c-8fea-11e8-b10b-000c29aa7e75_0452e1f4",
                "EndpointID": "e83401827e0e6d2896eb46c7b252594c1694ca119d0cbd74c29383209b80a128",
                "MacAddress": "02:42:0a:fe:4c:02",
                "IPv4Address": "10.254.76.2/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.bridge.default_bridge": "true",
            "com.docker.network.bridge.enable_icc": "true",
            "com.docker.network.bridge.enable_ip_masquerade": "true",
            "com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
            "com.docker.network.bridge.name": "docker0",
            "com.docker.network.driver.mtu": "1500"
        },
        "Labels": {}
    }
]
```


<br/>
<br/>


#### 如何实现k8s网络模型

How to implement the Kubernetes networking model

有多种方式实现此网络模型，以下做一个概述。

- ACI
- AOS from Apstra
- Big Cloud Fabric from Big Switch Networks
- Cilium
- CNI-Genie from Huawei
- Contiv
- Contrail
- Flannel
- Google Compute Engine
- Kube-router
- L2 networks and linux bridging
- Multus
- NSX-T
- Nuage Networks VCS
- OpenVSwitch
- OVN
- Project Calico
- Romana
- Weave Net from Weaveworks



<br/>
<br/>



### 日志架构

Logging Architecture

应用程序和系统日志可以帮助你了解集群内部发生的情况。大多数现代应用程序都有某种日志机制，因此，大多数容器化引擎同样设计来支持多种日志。容器化应用程序最简单、最受欢迎的日志方法是写入`stdout`和`stderr`。

但是，容器引擎或`runtime`提供的本地(native)功能通常不足以构建完整的日志解决方案。例如，如果container crashe、pod evicted、node dies，你通常仍然希望访问应用程序的日志。因此，日志应独立于container、pod、node，并具有单独存储(separate storage)和生命周期(lifecycle)。这个概念称为集群级日志(cluster-level-loggin)。集群级日志需要单独的后端来**存储(store)、分析(analyze)、查询(query)**日志。k8s不提供日志数据的本地存储解决方案，但你可以将许多现有的日志解决方案集成到k8s集群中。

集群级日志架构假设在集群内部或外部存在日志记录后端。


<br/>
<br/>


#### k8s基本日志

Basic logging in Kubernetes

本节中，k8s将日志记录到到标准输出。

```
vim /etc/k8s/test/counter-pod.yaml
#此pod每秒输出一条信息

apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: count
    image: busybox
    args: [/bin/sh, -c,
            'i=0; while true; do echo "$i: $(date)"; i=$((i+1)); sleep 1; done']

#创建
#kubectl create -f /etc/k8s/test/counter-pod

#不指定命名空间，则默认default
#也可在配置文件里指定命名空间
#kubectl create -f /etc/k8s/test/counter-pod --namespace=test

#查看
#如果pod有多个容器，则应该指定容器名称
kubectl logs counter

0: Fri Aug 10 07:43:09 UTC 2018
1: Fri Aug 10 07:43:10 UTC 2018
2: Fri Aug 10 07:43:11 UTC 2018
3: Fri Aug 10 07:43:12 UTC 2018
4: Fri Aug 10 07:43:13 UTC 2018
5: Fri Aug 10 07:43:14 UTC 2018
6: Fri Aug 10 07:43:15 UTC 2018
7: Fri Aug 10 07:43:16 UTC 2018
8: Fri Aug 10 07:43:17 UTC 2018
9: Fri Aug 10 07:43:18 UTC 2018
......
```


<br/>
<br/>


#### 节点级日志记录

Logging at the node level


![节点级日志](/images/K8s/logging-node-level.png)

<br>

容器化应用程序写入`stdout`, `stderr`的所有内容，都由容器引擎处理并重定向到某处。Docker容器引擎可修改日志驱动程序，将日志写入到其它地方(file, json, fluent...)。

>注意
>Docker json日志驱动将每一行视为单独的消息，它没有直接支持多行消息，你需要使用更高级别来处理它。

默认情况下，如果容器重启，`kubelet`会使用其日志保留一个已终止(terminated)的容器。如果从节点上驱逐pod，则所有相应的容器也会被驱逐(包括日志)。

节点级日志记录中，一个重要考虑因素是实现日志轮询(log rotation)，以便日志不会占用节点所有可用存储。k8s目前不负责轮询日志，但部署工具应该配置方案来解决日志轮询问题。
例如，在k8s集群中，部署一个脚本程序，用于日志轮询。或设置Docker container runtime的`log-opt`标志已自动轮询应用程序日志。

当在基本日志记录中运行`kubectl logs`命令时，节点上的`kubelet`会处理请求直接从日志文件读取，返回响应的内容。
注意： 如果某个外部系统已执行轮询，则`kubectl  logs`只能获取到最新的日志文件。

<br>

**system component logs**
有两种类型的系统组件:

- **run in container**: 如`kube-proxy`
- **not run in container**: 如`kubelet`, Docker

在使用`systemd`的机器上，`kubelet`和`container runtime`将日志写到`journald`。如果没有`systemd`，则写到`/var/log/`下。容器内的系统组件始终将日志写入`/var/log`目录下，绕过默认的日志机制。
与容器日志类似，在`/var/log/`目录下的系统组件日志也应该被轮询。


<br/>
<br/>


#### 集群级日志架构

Cluster-level logging architectures

k8s官方没有提供原生的集群级日志记录，但你可以考虑集中常见方法：

- 在每个节点上使用`node-level logging agent`
- 用于记录应用程序pod的专用`sidecar container`
- 将日志直接从应用程序推送到后端

<br>

**Using a node logging agent**

![](/images/K8s/logging-with-node-agent.png)

你可以通过在每个节点上包含一个 节点级日志记录代理 来实现集群级日志记录。它是一个用于公开日志或将日志推送到后端的专用工具。
通常，此日志代理是一个容器，它可以访问该节点上所有应用程序容器的日志文件的目录。

由于日志记录代理必须在每个节点上运行，因此，将其实现为节点上的`DaemonSet replica`, `manifest pod`, `dedicated native process`是很常见的。然后，后两种方法已被弃用，并且非常不建议。

对于k8s集群，使用节点级日志代理是最常见和鼓励的方法，因为它在每个节点上只创建一个Agent，并且不需要对节点上运行的应用程序进行任何更改。然而，节点级日志仅适用于应用程序的`stdout`和`stderr`。

k8s并未指定logging Agent，但有两个可选的日志代理与k8s一同打包。两者都使用`fluentd`的自定义配置作为节点上的代理。

- Stackdriver Logging: 用于Google Cloud Platform
- Elasticsearch

<br>

**Using a sidecar container with the logging agent**
你可通过以下方式使用`sidecar container`:

- `sidecar container`将应用程序的日志传输到自己的`stdout`
- `sidecar container`容器运行一个`Logging Agent`，此代理从应用程序容器中获取日志

![](/images/K8s/logging-with-streaming-sidecar.png)

<br>

通过让`sidecar container`的stream流向他们自己的`stdout/stderr`，你可利用已经在每个节点上运行的`kubelet`和`logging agent`。`sidecat container`从file、socket、journald读取日志。每个单独的`sidecar container`将日志打印到自己的`stdout/stderr`。
此方法允许你从应用程序的不同部分分离多个日志流，其中一些可能缺乏对写入`stdout/stderr`的支持。重定向日志背后的逻辑是最小的，因此它几乎不是一个重要的开销。此外，因为`stdout/stderr`由kubelet处理，所以你可以使用如`kubectl logs`这样的内置工具。

<br>

考虑如下栗子，pod运行单个容器，此容器使用两种不同的日志格式写入两个不同的日志。

two-files-counter-pod.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: count
    image: busybox
    args:
    - /bin/sh
    - -c
    - >
      i=0;
      while true;
      do
        echo "$i: $(date)" >> /var/log/1.log;
        echo "$(date) INFO $i" >> /var/log/2.log;
        i=$((i+1));
        sleep 1;
      done
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  volumes:
  - name: varlog
    emptyDir: {}
```

即使你设法将两个组件重定向到容器的`stdout`，在同一个日志流中包含不同格式的日志条目也会很麻烦。相反，你可以引入两个`sidecar container`。每个`sidecar container`可以从共享卷(shared volume)中`tail`特定的日志文件，然后将日志重定向到自己的`stdout`。

<br>

这是pod运行两个`sidecat container`的配置文件。
三个容器共享了`/var/log`。

two-file-counter-pod-streaming-sidecar.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: count
    image: busybox
    args:
    - /bin/sh
    - -c
    - >
      i=0;
      while true;
      do
        echo "$i: $(date)" >> /var/log/1.log;
        echo "$(date) INFO $i" >> /var/log/2.log;
        i=$((i+1));
        sleep 1;
      done
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  - name: count-log-1
    image: busybox
    args: [/bin/sh, -c, 'tail -n+1 -f /var/log/1.log']
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  - name: count-log-2
    image: busybox
    args: [/bin/sh, -c, 'tail -n+1 -f /var/log/2.log']
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  volumes:
  - name: varlog
    emptyDir: {}
```

<br>

现在运行此pod，并单独访问每个日志流:

```sh
#run
kubectl create -f /etc/k8s/test/two-file-counter-pod-streaming-sidecar.yaml



#get
kubectl get pod/counter -o wide
NAME      READY     STATUS    RESTARTS   AGE       IP           NODE
counter   3/3       Running   0          9m        10.244.2.9   salt01


#
kubectl logs counter
Error from server (BadRequest): a container name must be specified for pod counter, choose one of: [count count-log-1 count-log-2]



#logs
kubectl logs counter count-log-1

0: Tue Aug 14 02:58:29 UTC 2018
1: Tue Aug 14 02:58:30 UTC 2018
2: Tue Aug 14 02:58:31 UTC 2018
3: Tue Aug 14 02:58:32 UTC 2018



kubectl logs counter count-log-2

Tue Aug 14 02:58:29 UTC 2018 INFO 0
Tue Aug 14 02:58:30 UTC 2018 INFO 1
Tue Aug 14 02:58:31 UTC 2018 INFO 2
Tue Aug 14 02:58:32 UTC 2018 INFO 3

```

集群中安装的节点级代理会自动获取这些日志流，而无需进一步配置。如果愿意，可将代理配置为根据源容器解析日志行。

注意，进错CPU和内存使用率很低，将日志写入文件然后将它们流式传输到`stdout`会使磁盘使用量增加一倍。如果你有一个应用程序将日志写到单个文件，通常最好将`/dev/stdout`设置为目标，而不是实现流式`sidecar container`方法。

`sidecar container`还可用于应用程序本身日志轮询。然而，建议直接使用`stdout/stderr`并将日志的轮询和保留交给`kubelet`。

<br>

**Sidecar container wiht a logging agent**

![官方栗子](/images/K8s/logging-with-sidecar-agent.png)

<br>

![额外栗子](/images/K8s/filebeat-log-collector-arch.png)

<br>

如果节点级日志记录代理对你来说不够灵活，你可以创建一个带有单独日志记录代理程序的`sidecar container`，该代理可专门配置来与你的程序一起运行。

> 注意：
> 在`sidecar container`使用日志记录代理将会消耗大量资源。此外，你将无法使用`kubectl logs`命令访问这些日志，因为它们不受kubelet控制。

栗子使用`fluentd`作为`logging agent`。有两个可用于实现此方法的配置文件：

- ConfigMap
使用`ConfigMap`来配置fluentd。具体配置参考fluentd官方文档。

`fluentd-sidecat-config.yaml`

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluentd.conf: |
    <source>
      type tail
      format none
      path /var/log/1.log
      pos_file /var/log/1.log.pos
      tag count.format1
    </source>

    <source>
      type tail
      format none
      path /var/log/2.log
      pos_file /var/log/2.log.pos
      tag count.format2
    </source>

    <match **>
      type google_cloud
    </match>
```

- pod
运行fluentd的`sidecat container`的pod。它挂载一个volume让fluentd获取配置数据。
下面需要用到`k8s.gcr.io/fluentd-gcp:1.30`镜像，请提前准备。要挂载目录，请创建。


`two-files-counter-pod-agent-sidecar.yaml`

```
apiVersion: v1
kind: Pod
metadata:
  name: counter
spec:
  containers:
  - name: count
    image: busybox
    args:
    - /bin/sh
    - -c
    - >
      i=0;
      while true;
      do
        echo "$i: $(date)" >> /var/log/1.log;
        echo "$(date) INFO $i" >> /var/log/2.log;
        i=$((i+1));
        sleep 1;
      done
    volumeMounts:
    - name: varlog
      mountPath: /var/log
  - name: count-agent
    image: k8s.gcr.io/fluentd-gcp:1.30
    env:
    - name: FLUENTD_ARGS
      value: -c /etc/fluentd-config/fluentd.conf
    volumeMounts:
    - name: varlog
      mountPath: /var/log
    - name: config-volume
      mountPath: /etc/fluentd-config
  volumes:
  - name: varlog
    emptyDir: {}
  - name: config-volume
    configMap:
      name: fluentd-config
```

这仅仅是一个栗子。你可以使用其它`logging agent`取代`fluentd`，如`filebeat`, `logstash`...

<br>

**Exposing logs directly from the application**

![](/images/K8s/logging-from-application.png)

<br>

你可以通过直接公开每个应用程序的日志或push日志来实现集群级日志记录。就相当于在写得程序中加入日志收集和处理。
但是，这种日志记录机制超出了k8s的范围。



<br/>
<br/>



### kubelet垃圾回收

Configuring kubelet Garbage Collection


垃圾回收是一个有用的kubelet功能，它将清理未使用的镜像和容器。每分钟对容器执行垃圾回收，每五分钟对镜像进行垃圾回收。
不推荐使用额外的垃圾回收工具，因为这可能会破坏`kubelet`的行为。


<br/>


#### 镜像回收

Image Collection

k8s在`cadvisor`的配合下，通过`imageManager`管理所有镜像的生命周期。
镜像垃圾回收策略考虑了两个要素：

- HighThresholdPercent
- LowThresholdPercent

磁盘使用率高于高阈值将触发垃圾回收，垃圾回收将删除最近最少使用的镜像，直到满足低阈值。

<br>

镜像垃圾回收的kubelet flag:

```
#触发镜像垃圾回收的磁盘使用率百分比
#默认值 90%
image-gc-high-threshold



#镜像垃圾回收尝试释放磁盘使用的百分比
#默认值 80%
image-gc-low-threshold
```




<br/>
<br/>


#### 容器回收

Container Collection

容器垃圾回收策略考虑了三个用户定义的变量：

- MinAge
- MaxPerPodContainer
- MaxContainers

`MinAge`是容器可以被垃圾回收的最小年龄。设置为0可禁用。
`MaxPerPodContainer`是允许每个pod对允许拥有的最大死容器数。设置小于0可禁用。
`MaxContainers`是总死亡容器的最大数量。设置小于0可禁用。

kubelet将对未识别、删除或标志设置的边界之外的容器起作用。通常首先移除最旧的容器。
不受kubelet管理的容器不受容器垃圾回收的限制。

<br>

容器垃圾回收的kubelet flag:

```
#完成的容器在垃圾回收之前的最低年龄
#默认值 0min，意味着每个完成的容器都将被垃圾回收
minimum-container-ttl-duration



#每个容器要保留的最大旧实例数
#默认值 1
#强烈建议使用足够大的值，以允许每个预期容器保留至少1个死亡容器
maximum-dead-containers-per-container



#全局要保留的最大容器实例数
#默认值 -1，意味着禁用
#处于类似的原因，同样建议使用较大的值
maximum-dead-containers
```


<br/>
<br/>


#### 启用

一些kubelet垃圾回收标志未来将被启用或取代。

| Existing Flag | New Flag | Rationale |
| - | - | - |
| --image-gc-high-threshold | --eviction-hard or --eviction-soft | existing eviction signals can trigger image garbage collection |
| --image-gc-low-threshold | --eviction-minimum-reclaim | eviction reclaims achieve the same behavior |
| --maximum-dead-containers | xxx  | deprecated once old logs are stored outside of container’s context |
| --maximum-dead-containers-per-container | xxx | deprecated once old logs are stored outside of container’s context |
| --minimum-container-ttl-duration | xxx | deprecated once old logs are stored outside of container’s context |
| --low-diskspace-threshold-mb | --eviction-hard or eviction-soft | eviction generalizes disk thresholds to other resources |
| --outofdisk-transition-frequency | --eviction-pressure-transition-period | eviction generalizes disk pressure transition to other resources |



<br/>
<br/>



### Federation

先跳过，后面来学习。



<br/>
<br/>



### Proxy

Proxies in Kubernetes

使用Kubernetes时可能会遇到几种不同的代理。
代理已经取代了重定向功能，重定向已被弃用。


<br>


#### kubectl proxy

1. runs on a user’s desktop or in a pod
2. proxies from a localhost address to the Kubernetes apiserver
3. client to proxy uses HTTP
4. proxy to apiserver uses HTTPS
5. locates apiserver
6. adds authentication headers


<br/>
<br/>


#### apiserver proxy

1. is a bastion built into the apiserver
2. connects a user outside of the cluster to cluster IPs which otherwise might not be reachable
3. runs in the apiserver processes
4. client to proxy uses HTTPS (or http if apiserver so configured)
5. proxy to target may use HTTP or HTTPS as chosen by proxy using available information
6. can be used to reach a Node, Pod, or Service
7. does load balancing when used to reach a Service


<br/>
<br/>


#### kube proxy

1. runs on each node
2. proxies UDP and TCP
3. does not understand HTTP
4. provides load balancing
5. is just used to reach services


<br/>
<br/>


#### A Proxy/Load-balancer in front of apiserver

1. existence and implementation varies from cluster to cluster(e.g. nginx)
2. sits between all clients and one or more apiservers
3. acts as load balancer if there are several apiservers


<br/>
<br/>


#### 云负载均衡器

1. 由云服务商提供
2. 当k8s服务有LoadBalancer类型时自动创建
3. 仅使用udp/tcp
4. 具体详情因云服务商而异



<br/>
<br/>



### 控制器管理器指标

Controller manager metrics

控制器管理器指标，提供有关控制器管理器性能和运行状况的重要信息。

这些指标包括常见的Go语言运行时指标、控制器特定指标。可用于衡量集群的运行状况。

在集群中，当控制器管理器运行时，可从`http://localhost:10252/metrics`获取控制器管理器指标。

```
netstat -nltup | grep 10252
tcp        0      0 127.0.0.1:10252         0.0.0.0:*               LISTEN      11088/kube-controll 


curl http://localhost:10252/metrics
```

这些指标以`prometheus format`格式发出，并且是人类可读的。



<br/>
<br/>


### 附加组件

Installing Addons


附加组件扩展了k8s的功能。


<br/>


#### 网络和网络策略

Networking and Network Policy

- ACI： 通过 Cisco ACI提供集成的容器网络和网络完全
- Calico： 是一个安全的L3网络和网络策略提供商
- Canal: 将Flannel和Calico联合起来，提供网络和网络策略
- Cilium： 是一个L3网络和网络策略插件
- CNI-Genie： 使k8s能够无缝连接到各种CNI插件
- Contiv： 提供可配置的网络，用于各种用例和丰富的策略框架
- Flannel： 是一个可以与k8s一起使用的overlay网络提供商
- Knitter： 是一个支持k8s多个网络的网络解决方案
- Multus： 是一个用于k8s中多个网络支持，以支持所有CNI插件的多插件
- NSX-T： 提供VMware NSX-T与容器协调器之间的集成
- Nuage： 是一个SDN平台，可在k8s Pod和non-k8s环境之间提供基于策略的网络，并提供可见性和安全性监控
- Romana： 用于Pod网络的L3网络解决方案
- Weave Net： 提供网络和网络策略，将在网络分区的两侧进行工作，而不需要外部数据库


<br/>
<br/>


#### 服务发现

Service Discovery

- [CoreDNS](https://coredns.io/)： 是一个灵活，可扩展的DNS服务器，可作为用于pod的集群DNS。


<br/>
<br/>


#### 可视化，控制

Visualization, Control

- [Dashboard](https://github.com/kubernetes/dashboard#kubernetes-dashboard)： k8s的Dashboard Web Interface
- [Weave Scope](https://www.weave.works/docs/scope/latest/installing/#k8s)： 是一个用于以图形可视化显示container, pod, service...



<br/>
<br/>
<br/>



## k8s架构

Kubernetes Architecture


<br/>


### Node

node是k8s中的工作机器，以前称为minion。也就是集群中的一台主机。节点可以是VM或物理机。每个节点都具有用于运行pod所需的服务，并由master组件管理。节点上的服务包括`docker`, `kubelet`, `kube-proxy`。


<br/>


#### 节点状态

Node Status

节点的状态包含以下信息：

- 地址(Address)
- 条件(Condition)
- 容量(Capacity)
- 信息(Info)

<br>

**地址**
这些字段的使用取决于机器配置。

- HostName： 节点内核报告的主机名
- ExternalIP： 通常是可从外部路由的节点IP地址
- InternalIP： 通常是仅在集群内可路由的节点IP地址

```
kubectl get node -o wide
NAME      STATUS    ROLES     AGE       VERSION   INTERNAL-IP      EXTERNAL-IP   OS-IMAGE                KERNEL-VERSION              CONTAINER-RUNTIME
master    Ready     master    7d        v1.11.1   192.168.31.49    <none>        CentOS Linux 7 (Core)   3.10.0-862.9.1.el7.x86_64   docker://1.13.1
node      Ready     <none>    7d        v1.11.1   192.168.31.174   <none>        CentOS Linux 7 (Core)   3.10.0-862.9.1.el7.x86_64   docker://1.13.1
salt01    Ready     <none>    1d        v1.11.1   192.168.31.159   <none>        CentOS Linux 7 (Core)   3.10.0-862.9.1.el7.x86_64   docker://1.13.1



kubectl describe node/salt01
Addresses:
  InternalIP:  192.168.31.159
  Hostname:    salt01
```

<br>

**条件**
该字段描述了所有运行中节点的状态。节点条件使用JSON对象表示。

| 条件 | 描述 |
| - | - |
| OutOfDisk | True(节点上的可用空间不足以添加新pod), 否则为False |
| Ready | True(节点健康并准备好接受pod) <br> False(节点不健康且不接受pod) <br> Unknown(节点控制器在最后一个`node-monitor-grace-period`期限内没有从节点收到消息。默认40s) |
| MemoryPressure | True(节点内存有压力，即内存不足)，否则为False |
| PIDPressure | True(进程存在压力，即节点上有太多进程)，否则为False |
| DiskPressure | True(磁盘大小存在压力，即磁盘容量较低), 否则为False |
| NetworkUnavailable | True(节点网络配置错误)，否则为False |
| ConfigOK | True(kubelet配置正确)，否则为False |

```
kubectl describe node/salt01
Conditions:
  Type             Status  LastHeartbeatTime                 LastTransitionTime                Reason                       Message
  ----             ------  -----------------                 ------------------                ------                       -------
  OutOfDisk        False   Wed, 15 Aug 2018 11:10:49 +0800   Mon, 13 Aug 2018 15:51:40 +0800   KubeletHasSufficientDisk     kubelet has sufficient disk space available
  MemoryPressure   False   Wed, 15 Aug 2018 11:10:49 +0800   Mon, 13 Aug 2018 15:51:40 +0800   KubeletHasSufficientMemory   kubelet has sufficient memory available
  DiskPressure     False   Wed, 15 Aug 2018 11:10:49 +0800   Mon, 13 Aug 2018 15:51:40 +0800   KubeletHasNoDiskPressure     kubelet has no disk pressure
  PIDPressure      False   Wed, 15 Aug 2018 11:10:49 +0800   Mon, 13 Aug 2018 15:51:40 +0800   KubeletHasSufficientPID      kubelet has sufficient PID available
  Ready            True    Wed, 15 Aug 2018 11:10:49 +0800   Mon, 13 Aug 2018 15:53:00 +0800   KubeletReady                 kubelet is posting ready status

```

<br>

**容量**
描述节点上的可用资源：CPU，内存，可调度到节点上的最大pods数。

```
kubectl describe node/salt01
Capacity:
 cpu:                2
 ephemeral-storage:  49250820Ki
 hugepages-2Mi:      0
 memory:             3881332Ki
 pods:               110

```

<br>

**信息**
关于节点的一般信息，如Kernel版本，Kubernetes版本，Docker版本，OS...

```
kubectl describe node/salt01
System Info:
 Machine ID:                 e48d6bf22f9b4c8da5cb1a07b2fec730
 System UUID:                564D1413-905B-64D6-E9A2-92E37F9B5BDA
 Boot ID:                    1df89a81-77a4-44a0-9241-e6d766795e32
 Kernel Version:             3.10.0-862.9.1.el7.x86_64
 OS Image:                   CentOS Linux 7 (Core)
 Operating System:           linux
 Architecture:               amd64
 Container Runtime Version:  docker://1.13.1
 Kubelet Version:            v1.11.1
 Kube-Proxy Version:         v1.11.1

```


<br/>
<br/>


#### 管理

Management

与Pod与Service不同，k8s本身并不创建节点： 它由云服务商创建，或存在于物理机/虚拟机的pool中。
当k8s创建节点时，它实际上只是创建了一个表示节点的对象。创建之后，k8s将检查节点是否有效。

栗子：

```json
{
  "kind": "Node",
  "apiVersion": "v1",
  "metadata": {
    "name": "10.240.79.157",
    "labels": {
      "name": "my-first-k8s-node"
    }
  }
}
```

k8s将在内部创建节点对象，并通过基于`metadata.name`字段的运行状况检查来验证节点。
如果节点有效(valid)，即所有必要的服务都已运行，它就符合了运行pod的条件。否则它将被所有的集群动作忽略，直到它变为有效。请注意，Kubernetes将保持无效(invalide)节点的对象，除非它被手动删除。Kubernetes将持续检查节点是否变得可用。

目前，有3个组件与k8s节点接口交互：

- Node Controller
- kubelet
- kubectl

<br>

**节点控制器**
节点控制器是一个k8s Master组件，用于管理节点的各个方面。

节点控制器在节点的生命周期中具有多个角色(role)。第一个便是在节点注册时为其分配CIDR地址块。
第二个是使节点控制器的内部节点列表与可用机器保持一致。只要节点不健康，节点控制器就会询问该节点是否仍然可用。如果不是，则节点控制器从其节点列表中删除该节点。
第三个是监控节点的健康状况。当节点不可达时，节点控制器负责更新节点的条件(condition)状态，从`Ready`变为`Unknown`。如果节点继续无法访问，则稍后从节点中驱逐(evict)所有pod(graceful termination)。默认超时时间为40s开始上报`Unknown`，然后5min之后开始驱逐pods。节点控制器通过`--node-nonitor-period`秒检查每个节点的状态。

在大多数情况下，节点控制器将驱逐率(evication rate)限制为`--node-eviction-rate`(默认值 0.1)每秒。这意味着它将不会每10s从超过1个节点驱逐pod。

当给定可用区域中的节点变得不健康时，节点驱逐行为会发生变化。同时，节点控制器检查此区域中不健康节点的百分比。
如果节点不健康比例至少为`--unhealthy-zone-threshold`(默认值 0.55)，那么驱逐率会降低；
如果集群很小，小于或等于`--large-cluster-size-threshold`(默认值 50)，则停止驱逐；
否则，驱逐率减小到每秒`--secondary-node-eviction-rate`(默认值 0.01)。
每个可用区域实施这些策略的原因是，一个可用区域可能与其它可用区域保持连接。

在可用区域之间传播节点的一个关键原因是，当整个区域出现故障时，工作负载可以转移到健康区域。因此，如果区域中的全部节点都不健康，则节点控制器以正常速率`--node-eviction-rate`驱逐。
The corner case是当所有区域都不健康时。在这种情况下，节点控制器假定Master连接存在一些问题，并在某些连接恢复之前停止所有驱逐。

<br>

**节点自注册**
Self-Registration of Nodes

当`kubelet`标志`--register-node`为true(默认)时，它会尝试向API server注册自己。这是大多数发行版使用的首选模式。

对于自注册，kubelet使用如下选项：

```
#向API server验证自身的凭据路径
--kubeconfig


#r如何与云服务商交流
--cloud-provider


#向API server自动注册
--register-node


#节点IP地址
--node-ip


#集群中注册节点时要添加的标签
--node-labels


#指定kubelet将节点状态发送到master的频率
--node-status-update-frequency
```

目前，任何kubelet都有权 create/modify 任何节点资源，但实际上它只 创建/修改 自己的节点资源。(将来，k8s打算只允许kubelet修改自己的节点资源)

**手动管理节点**

如果希望手动创建节点对象，请设置`kubelet`标志`--register-node=false`。
修改包括在节点上设置标签(label)并将其标记为不可调度(unschedulable)。

<br>

**节点容量**
Node Capacity

节点容量(cpu, memory)是节点对象的一部分。通常，当创建节点对象时，节点注册自己并上报其容量。如果是手动管理节点，则需要你在添加节点时设置节点容量。
k8s调度器确保节点上的所有pod都有足够的资源。它检查节点上容器请求的总和不大于节点容量。它包括由kubelet启动的所有容器，但不包括由容器运行时直接启动的容器，也不包括容器外部的任何进程。所以，尽量不要在k8s集群节点上运行额外进程。

如果要为`non-pod`进程保留资源，你可以创建保留(placeholder)pod。将内存和CPU的值设置为要保留的资源量。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: resource-reserver
spec:
  containers:
  - name: sleep-forever
  - image: k8s.gcr.io/pause:0.8.0
  - resources:
      requests:
	    cpu: 100m
		memory: 100Mi

```


<br/>
<br/>


#### API对象

Node is a top-level resource in the Kubernetes REST API.



<br/>
<br/>



### 节点通信

Master-Node communication


Master(APIserver)与k8s cluster之间的通信。
目的是允许用户自定义其安装以强化网络配置，以便集群可在不受信任的网络上运行。


<br>


#### Cluster->Master

从Cluster到Master的所有通信路径都终止于API server。在典型部署中，API server配置为在安全的HTTPS(443)端口上监听远程连接，并启用一种或多种形式的Client认证。
应该为节点配置集群的公共根证书，以便他们可以使用有效证书安全地连接到API server。
希望连接到API server的Pod可以利用Service Account安全地执行此操作，这样k8s在实例化时自动将公共根证书和有效bearer token注入到Pod中。`the kubernetes service`配置了一个虚拟IP地址，该地址被重定向到API server的HTTPS endpoint。
Master组件还通过安全端口与Cluster API server通信。

```
kubectl get service
NAME         TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                         AGE
kubernetes   ClusterIP   10.96.0.1     <none>        443/TCP                         8d
```

因此，默认情况下，从Cluster到Master的连接的默认操作模式是安全的，可在不受信任网络/公共网络上运行。


<br/>
<br/>


#### Master->Cluster

从Master(API server)到Cluster有两条主要通信路径：

- API server `->` kubelet
- API server `->` node, pod, service

<br>

**API server -> kubelet**
从API server到kubelet(它运行在集群中的每个节点上)。

从API server到kubelet的连接用于：

- 获取Pod的日志
- 附加到运行的Pod
- 提供kubelet的端口转发功能

这些连接终止于kubelet的HTTPS endpoint。默认情况下，API server不会验证kubelet的证书，这会使连接可能受到中间人工具，并且不安全地运行在不受信任/公共的网络上。
要验证此连接，使用`--kubelet-certificate-authority`标志位API server提供根证书，用于验证kubelet的证书。

如果无法做到，请在API server和kubelet之间使用SSH隧道保障连接安全。

<br>

**API server -> node, pod, service**
从API server到node, pod, service的连接默认为纯HTTP，因此既不需要认证也未加密。他们可以通过在API URI的前缀使用<https://>来运行安全的HTTPS，但他们不会验证HTTPS endpoint提供的证书，也不会提供客户端凭据。因此连接将被加密，它不会提供任何完整性保证。



<br/>
<br/>



### 云控制器管理器

Cloud Controller Manager


暂时跳过！



<br/>
<br/>
<br/>



## 扩展k8s


<br/>


### 扩展k8s集群

Extending your Kubernetes Cluster


k8s具有高度可配置化和可扩展化。

定制方法可大致分为配置，只涉及更改标志，本地配置文件或API资源；扩展，设计运行其它程序或服务。


<br/>


#### 扩展模式

Extensions Patterns

k8s旨在通过编写客户端程序实现自动化。任意 read/write k8s API的程序都可以提供有用的自动化。自动化可在集群上启用或关闭。自动化通常适用于k8s集群，包括托管集群和管理安装。

有一种编写与k8s一起使用的称为控制器模式(Controller Pattern)客户端程序的特定模式。控制器通常读取对象的`.spec`，可能做些事情，然后更新对象的`.status`。
控制器(Controller)是一个k8s client。当k8s为client并调用远程服务时，它被称为`Webhook`。远程服务被称为`Webhook Backend`。与控制器一样，`Webhook`确实增加了一个失败点。

在webhook模式中，k8s 向远程服务发出网络请求。在二进制插件模型中，k8s执行二进制程序。二进制插件由kubelet和kubectl使用。

![k8s扩展](/images/K8s/k8s_extensions.png)


<br/>


#### 扩展点

Extension Points

k8s 系统的扩展点:

![k8s 扩展点](/images/K8s/k8s_extension_points.png)

<br>

1. 用户使用`kubectl`与k8s API进行交互
2. API server处理所有请求
3. API server提供各种资源
4. k8s调度器决定将pod放在哪个节点上
5. k8s大部分行为都是由控制器实现的
6. kubelet帮助pod在集群网络上显示为具有自己IP的虚拟服务
7. kubelet还可挂载和解挂容器的卷

<br>

如果你不确定如何开始，查看如下流程图：

![](/images/K8s/k8s_extensions_start.png)


<br/>


#### API扩展

API Extensions

<br>

**User-Defined Types**
如果想要定义新的控制器、应用程序配置对象、声明性API并管理他们，请考虑向k8s添加自定义资源。
不要讲自定义资源用作应用程序、用户、监控数据的数据存储。

<br>

**Combining New APIs with Automation**
通常，当添加新API时，还会添加一个 read/write 新API的控制循环。当自定义API和控制循环的组合用于管理特定的，通常是有状态的应用程序时，这被称为操作者模式(Operator Pattern)。

<br>

**Changing Built-in Resources**
通过自定义资源添加扩展k8s API时，添加的资源始终属于新的API组。你无法替换或修改已经存在的API组。添加API不会直接影响现有API的行为，但API Access Extensions会影响现有API的行为。

<br>

**API Access Extensions**
当请求到达k8s API server时，它首先进行身份验证，然后授权，然后进行各种准入控制。每个步骤都提供了扩展点。

<br>

**Authentication**
身份验证将所有请求中的Header或证书映射到发出请求的客户端的用户名中。

<br>

**Authorization**
授权确定特定用户是否可以对API资源进行读写和其它操作。它只是在整个资源的层面上工作，不基于任意对象字段进行区分。

<br>

**Dynamic Admission Control**
当请求授权之后，如果它是一个写操作，它还需要通过`Admission Control`步骤。除了内建步骤之外，还有其它扩展：

- `Image Policy webhook`限制可在容器中运行的镜像
- 为了做出任意的`admission control`决策，可使用普通`admission webhook`
- 初始化程序可在创建对象之前修改对象的控制器


<br/>


#### 基础设施扩展

Infrastructure Extensions

<br>

**Storage Plugins**
`Flex Volumes`允许用户通过`kubelet`调用二进制插件来安装卷，来安装没有内置支持的卷类型

<br>

**Device Plugins**
设备插件允许节点通过设备发现插件发现新的节点资源

<br>

**Network Plugins**
支持不同的网络结构

<br>

**Scheduler Extensions**
调度器是一种特殊类型的控制器，用于监视Pod，并将Pod分配给节点。


<br/>
<br/>


### 扩展k8s API

Extending the Kubernetes API


<br/>


#### 在聚合层扩展k8s API

Extending the Kubernetes API with the aggregation layer


聚合层允许在集群中安装其它k8s-style的API。


<br/>


#### 自定义资源

Custom Resources


自定义资源是k8s API的扩展，包括何时向k8s集群添加自定义资源以及何时使用独立服务。

资源是k8s API中的端点(endpoint)，用于存储某种API对象的集合。如，内建的pods资源包含了Pod对象的集合。
自定义资源是k8s API的扩展，不一定在每个k8s集群上都可用。换句话说，它代表了特定k8s的定制安装。
自定义资源可通过动态注册在正在运行的集群中出现和消失，集群管理员可独立于集群本身更新自定义资源。安装自定义资源后，用户可使用`kubectl`创建和访问其对象。

<br>

Custom controllers

自定义字段本身可让你存储和检索结构化数据。只有与控制器结合使用才能成为真正的声明性API。declare API允许你声明或指定资源的所需状态，并尝试将实际状态与此期望状态相匹配。这里，控制器将结构化的数据解释为用户期望状态的记录，并且不断采取行动以实现和维护该状态。
自定义控制器是一种用户可在正在运行的集群上进行部署和更新，而与集群自身的生命周期无关的控制器。自定义控制器可使用任何类型的资源，但与自定义资源结合使用时，它们更有效。

<br>

Should I add a custom resource to my Kubernetes Cluster?

当创建新的API时，考虑是使用k8s cluster API还是让API独立运行。

| Consider API aggregation if: | Prefer a stand-alone API if: |
| - | - |
| Your API is Declarative. | Your API does not fit the Declarative model. |
| You want your new types to be readable and writable using kubectl. | kubectl support is not required |
| You want to view your new types in a Kubernetes UI, such as dashboard, alongside built-in types. | Kubernetes UI support is not required. | 
| You are developing a new API. | You already have a program that serves your API and works well. |
| You are willing to accept the format restriction that Kubernetes puts on REST resource paths, such as API Groups and Namespaces. (See the API Overview.) | You need to have specific REST paths to be compatible with an already defined REST API. |
| Your resources are naturally scoped to a cluster or to namespaces of a cluster. | Cluster or namespace scoped resources are a poor fit; you need control over the specifics of resource paths. |
| You want to reuse Kubernetes API support features. | You don’t need those features |

<br>

**声明性API**
Declarative APIs

在一个声明性API中，通常：

- 你的API由相对较少的相对较小的对象组成
- 应用程序或基础结构的对象定义配置
- 对象很少更新
- 人们通常需要读写对象
- 对象的主要操作时CRUD
- 跨对象的事务不是必需的：API表示期望状态，而不是精确的状态

imperative API不是声明性的，你的API可能不是声明性的标志包括：

- 客户端说执行此操作，完成后获得同步响应
- 客户端说执行此操作，然后获取操作ID，并且必须检查单独的Operation对象以确定请求的完成
- 谈论Remote Procedure Calls(RPCs)
- 直接存储大量数据
- 需要高带宽访问
- 存储最终用户数据，或应用程序处理的其它大规模数据
- 对象非CRUD的自然操作
- API不容易建模为对象
- 使用操作ID或操作对象表示挂起的操作

<br>

Should I use a configMap or a custom resource?

如果符合以下任意条件，请使用ConfigMap:

- 存在现有的，记录完备的配置文件格式
- 你希望将整个配置文件放入ConfigMap的一个key中
- 配置文件的主要用途是在集群上的Pod中运行的程序使用该文件来配置自身
- 文件的消费者更喜欢使用Pod中的文件或环境变量，而不是k8s API
- 你希望在文件更新时通过部署执行滚动升级

如果符合以下大部分情况，请使用自定义资源：

- 你希望使用k8s client library和CLI来创建和更新新资源
- 你希望来自`kubectl`的顶级支持
- 你希望构建新的自动化，监视新对象的更新，然后CRUD其它对象
- 你希望编写处理对象更新的自动化
- 你希望使用k8s API约定，如`.spec, .status, .metadata`
- 你希望对象是受控资源集合的抽象，或其它资源的汇总

<br>

**添加自定义资源**
k8s提供了两种方式来向你的集群中添加自定义资源：

- CRD很简单，无需任何编程即可创建
- API聚合需要编程，但允许更多控制API行为，如数据的存储方式和API版本间的转换

聚合API是位于主API server后面的从属API server，它充当代理。这种安排称为API聚合(AA, API Aggregation)。
CRD允许用户添加新类型的资源，而无需添加其它API server，你无需了解API聚合即可使用CRD。
无论如何安装，新资源都成为自定义资源，以区别于内置的k8s 资源。

<br>

**自定义资源定义**
自定义资源定义 API资源允许你去定义自定义资源。定义CRD对象会创建一个新的自定义资源，其中包含指定的名称和架构。k8s API提供并处理自定义资源的存储。
这使你无需编写自己的API server来处理自定义资源，但实现的一般特性意味着你的灵活性低于API server聚合。

<br>

**API server aggregation**
通常，k8s API中的每个资源都需要处理REST 请求的代码并管理对象的持久化存储。k8s API server处理pod等内建资源，还可通过CRD处理自定义资源。
聚合层允许你通过编写和部署自己的独立API server为自定义资源提供专门的实现。API server将请求委托给你处理的自定义资源，使其对所有客户端可用。

为添加自定义资源选择一个方法
通常情况下，CRD很适合，如果：

- 你有少数几个领域
- 你正在使用公司内的资源，或作为小型开源项目的一部分

<br>

易用性比较：

| CRDs | Aggregated API |
| - | - |
| Do not require programming. Users can choose any language for a CRD controller. | Requires programming in Go and building binary and image. Users can choose any language for a CRD controller. |
| No additional service to run; CRs are handled by API Server. | An additional service to create and that could fail. |
| No ongoing support once the CRD is created. Any bug fixes are picked up as part of normal Kubernetes Master upgrades. | May need to periodically pickup bug fixes from upstream and rebuild and update the Aggregated APIserver. |
| No need to handle multiple versions of your API. For example: when you control the client for this resource, you can upgrade it in sync with the API. | You need to handle multiple versions of your API, for example: when developing an extension to share with the world. |

<br>

高级功能和灵活性：

| Feature | Description | CRDs | Aggregated API | 
| - | - | - | - |
| Validation | Help users prevent errors and allow you to evolve your API independently of your clients. These features are most useful when there are many clients who can’t all update at the same time. | Yes. Most validation can be specified in the CRD using OpenAPI v3.0 validation. Any other validations supported by addition of a Validating Webhook. | Yes, arbitrary validation checks | 
| Defaulting | See above | Yes, via a Mutating Webhook; Planned, via CRD OpenAPI schema. | Yes | 
| Multi-versioning | Allows serving the same object through two API versions. Can help ease API changes like renaming fields. Less important if you control your client versions. | No, but planned | Yes | 
| Custom Storage | If you need storage with a different performance mode (for example, time-series database instead of key-value store) or isolation for security (for example, encryption secrets or different | No | Yes | 
| Custom Business Logic | Perform arbitrary checks or actions when creating, reading, updating or deleting an object | Yes, using Webhooks. | Yes | 
| Scale Subresource | Allows systems like HorizontalPodAutoscaler and PodDisruptionBudget interact with your new resource | Yes | Yes | 
| Status Subresource |  | 
| Finer-grained access control: user writes spec section, controller writes status section. | 
| Allows incrementing object Generation on custom resource data mutation (requires separate spec and status sections in the resource) | 
| Yes | Yes | 
| Other Subresources | Add operations other than CRUD, such as “logs” or “exec”. | No | Yes | 
| strategic-merge-patch | The new endpoints support PATCH with Content-Type: application/strategic-merge-patch+json. Useful for updating objects that may be modified both locally, and by the server. For more information, see “Update API Objects in Place Using kubectl patch” | No, but similar functionality planned | Yes | 
| Protocol Buffers | The new resource supports clients that want to use Protocol Buffers | No | Yes | 
| OpenAPI Schema | Is there an OpenAPI (swagger) schema for the types that can be dynamically fetched from the server? Is the user protected from misspelling field names by ensuring only allowed fields are set? Are types enforced (in other words, don’t put an int in a string field?) | No, but planned | Yes | 

<br>

一般功能：

| Feature | What it does | 
| - | - |
| CRUD | The new endpoints support CRUD basic operations via HTTP and kubectl | 
| Watch | The new endpoints support Kubernetes Watch operations via HTTP | 
| Discovery | Clients like kubectl and dashboard automatically offer list, display, and field edit operations on your resources | 
| json-patch | The new endpoints support PATCH with Content-Type: application/json-patch+json | 
| merge-patch | The new endpoints support PATCH with Content-Type: application/merge-patch+json | 
| HTTPS | The new endpoints uses HTTPS | 
| Built-in Authentication | Access to the extension uses the core apiserver (aggregation layer) for authentication | 
| Built-in Authorization | Access to the extension can reuse the authorization used by the core apiserver (e.g. RBAC) | 
| Finalizers | Block deletion of extension resources until external cleanup happens. | 
| Admission Webhooks | Set default values and validate extension resources during any create/update/delete operation. | 
| UI/CLI Display | Kubectl, dashboard can display extension resources. | 
| Unset vs Empty | Clients can distinguish unset fields from zero-valued fields. | 
| Client Libraries Generation | Kubernetes provides generic client libraries, as well as tools to generate type-specific client libraries. | 
| Labels and annotations | Common metadata across objects that tools know how to edit for core and custom resources |

<br>

**安装自定义资源**
在向集群添加自定义资源之前，需要注意几点

- 第三方代码和新的失败点
- 存储
- 认证，授权，审计

<br>

**访问自定义资源**
k8s client library可用于访问自定义资源。并非所有client library都支持自定义资源，但go和python client library可以。

当你添加一个自定义资源时，你可以使用如下方式访问：

- kubectl
- k8s dynamic client
- REST client
- 由k8s client 生成工具生成的client



<br/>
<br/>



### 计算，存储和网络插件

Compute, Storage, and Networking Extensions


<br>


#### 网络插件

Network Plugins

> Notice:
> FEATURE STATE: Kubernetes v1.11 alpha
> Alpha features change rapidly

k8s中的网络插件有几种风格：

- CNI plugins: 遵守appc/CNI规范，旨在实现互操作性
- Kubenet plugin: 使用`bridge`和`host-local` CNI plugins实现基本的`cbr0`

<br>

**安装**
kubelet有一个默认的网络插件，以及整个集群的默认网络。它在启动时探测插件，记住它找到的内容，并在pod声明周期中的适当时间执行所选插件。
使用插件时，请记住两个`kubelet`命令行参数：

- `cni-bin-dir`: kubelet在启动时检测此目录以获取插件
- `network-plugin`： 从`cni-bin-dir`使用的网络插件

```
ps -ef | grep kubelet

/usr/bin/kubelet xxx --cni-bin-dir=/opt/cni/bin --cni-conf-dir=/etc/cni/net.d --network-plugin=cni
```

<br>

**网络插件需求**
除了提供网络插件接口来配置和清理pod网络外，该插件还可能需要对kube-proxy提供特定支持。iptables proxy依赖于iptables，插件可能需要确保容器流量可用于iptables。
默认情况下，如果未指定kubelet网络插件，则使用noop插件，它设置`net/bridge-nf-call-iptables=1`来确保简单配置与iptables proxy正常工作。

**CNI**
通过kubelet传递`--network-plugin=cni`选项来选择CNI插件。kubelet从`cni-conf-dir`(默认`/etc/cni/net.d`)中读取文件，并使用该文件中的CNI配置来设置每个pod的网络。引用的插件必须存在于`--cni-bin-dir`(默认`/opt/cni/bin`)中。
如果目录中有多个CNI配置文件，则使用文件名的词典顺序的第一个。
除了配置文件指定的CNI插件外，k8s还需要标准的CNI lo插件(loopback)，最低版本 v0.2.0

**kubenet**
kubelet是一个仅使用与Linux的基本和简单的网络插件。它本身并不实现高级的功能，如跨节点网络或网络策略。kubenet创建一个名为`cbr0`的Linux bridge，并为每个pod创建一个`veth`对，每对的主机端连接到连接到`cbr0`。通过配置或控制器管理器为该对的pod端分配范围内的IP地址。为cbr0分配一个MTU，该MTU与主机上启用的普通接口的最小MTU相匹配。

此插件需要一些东西：

- 需要标准的CNI `bridge`, `lo`, `host-local`插件，最小版本 v0.2.0。首先从`/opt/cni/bin`查找。
- kubelet必须使用`--network-plugin=kubenet`参数来启用此插件
- kubelet应该指定`--non-masquerade-cidr=<clusterCidr>`参数确保超出范围的IP流量将使用IP masquerade。
- 必须通过kubelet的`--pod-cidr`选项或控制器管理器的`--allocate-node-cidrs=true --cluster-cidr=<cidr>`选项来为节点分配IP子网

**自定义MTU(kubenet)**
应该始终正确配置MTU以获得最佳网络性能。网络插件通常会推断合理的MTU，但有时不会产生最佳的MTU。
如果需要，你可使用kubenet的`network-plugin-mtu`选项来明确指定MTU，仅有kubenet插件支持此选项。

<br>

**使用摘要**

```
--network-plugin=cni
--network-plugin=kubenet
--network-plugin-mtu=9001
```



<br/>
<br/>


#### 设备插件

Device Plugins

从v1.8开始，k8s为Vendors提供了设备插件框架，以便在不更改k8s核心代码的情况下将资源通知到kubelet，Vendor可实现手动部署或作为DaemonSet部署的设备插件，而不是编写自定义的k8s插件。目标设备包括GPU，高性能NIC， FPGA， InfiniBand和其它计算资源。

<br>

**设备插件注册**
设备插件功能由`DevicePlugins`功能控制，默认在 v1.10之前禁用。当启用设备插件功能，kubelet将导出Registration gRPC服务:

```
service Registration {
  rpc Register(RegisterRequest) returns (Empty) {}
}
```

设备插件可通过gRPC服务向kubelet注册自己。在注册中，它需要发送：

- Unix socket名
- 设备插件API版本
- 想要告知的ResourceName

栗子：

```
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod
spec:
  containers:
    - name: demo-container-1
      image: k8s.gcr.io/pause:2.0
      resources:
        limits:
          vendor-domain/resource: 2 # requesting 2 vendor-domain/resource
```

<br>

**设备插件实现**
设备插件的一般工作流包括如下步骤：

- 初始化
- 插件启动gRPC服务
- 插件使用kubelet的Unix socket注册自己
- 注册成功之后，设备插件以服务模式运行，在此期间，它会持续监控设备运行状况，并在任何设备状况发生变化时向kubelet报告

<br>

**设备插件部署**
设备插件可手动或作为DaemonSet来部署。
k8s 设备插件的支持人处于alpha状态。



<br/>
<br/>



### 服务目录

Service Catalog

服务目录是一种扩展API，它使在k8s集群中运行的应用程序能够轻松使用外部托管软件。
它提供了从Service Broker 列出，配置和绑定外部托管服务的方法，而无需详细了解如何创建或管理这些服务。
使用服务目录，集群操作人员可以浏览服务代理提供的托管服务列表，配置托管服务的实例，并与其绑定以使其可供k8s集群中应用程序使用。



<br/>
<br/>
<br/>



## Containers


<br>


### Images

你创建Docker image并将其push到registry，然后在k8s pod中引用它。
容器的镜像属性支持与Docker命令相同的语法，包括私有注册表和标记。

<br>

**更新镜像**
默认的拉取策略是`ifNotPresent`，这会导致kubelet跳过拉取镜像(如果镜像已存在)。所以在网络不好时，我们可以首先将镜像拉取下来。
如果你总想强制拉取镜像，可以执行如下操作：

- 设置容器`imagePullPolicy`为`Always`
- 使用`:latest`作为镜像的标记
- 启用`AlwaysPullImages`准入控制器

如果没有对镜像指定标记，则假定为`:latest`标记。

<br>

**使用私有注册表**
Using a Private Registry

私有注册表有：

- Docker Hub
- Aliyun
- Tencent yun
- Google Container Registry
- AWS Container Registry
- Azure Container Registry
- ...

以下是配置节点已使用私有注册表的推荐步骤：

```
1. 运行 docker login


2. 查看 ~/.docker/config.json
{
        "auths": {
                "https://index.docker.io/v1/": {
                        "auth": "xxxxxxxxxxxxxxx"
                }
        },
        "HttpHeaders": {
                "User-Agent": "Docker-Client/18.03.1-ce (linux)"
        }


3. 获取节点列表
#name
nodes=$(kubectl get nodes -o jsonpath='{range.items[*].metadata}{.name} {end}')

#IPs
nodes=$(kubectl get nodes -o jsonpath='{range .items[*].status.addresses[?(@.type=="ExternalIP")]}{.address} {end}')


4. 复制 .docker/config.json 到上面的搜索路径列表

for n in $nodes; do scp ~/.docker/config.json root@$n:/var/lib/kubelet/config.json; done
```

<br>

通过创建pod来验证私有镜像：

```
kubectl create -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: private-image-test-1
spec:
  containers:
    - name: uses-private-image
      image: $PRIVATE_IMAGE_NAME
      imagePullPolicy: Always
      command: [ "echo", "SUCCESS" ]
EOF
pod "private-image-test-1" created

```

<br>

**预拉取镜像**
Pre-pulling Images

默认情况下，kubelet将尝试从指定的注册表中拉取镜像。但是，如果容器的`imagePullPolicy`属性为`ifNotPresent`或`Never`，则会使用本地镜像。
如果你希望依赖于预先拉取的镜像作为注册表身份验证的替代，则必须确保集群中的所有节点都具有相同的预拉取镜像。
这可以用于预加载某些镜像以提高速度，或者作为对私有注册表进行身份认证的替代方法。
请确保所有的pods都对预拉取的镜像由访问权限。

<br>

**Specifying ImagePullSecrets on a Pod**
k8s支持在pod上指定registry keys。

```
#使用Docker config创建secret
kubectl create secret docker-registry -h
#Create a new secret for use with Docker registries.

kubectl create secret docker-registry zhang21-secret --docker-server=DOCKER_REGISTRY_SERVER --docker-username=DOCKER_USER --docker-password=DOCKER_PASSWORD --docker-email=DOCKER_EMAIL
secret "myregistrykey" created.


kubectl get secret
NAME                  TYPE                                  DATA      AGE
zhang21-secret        kubernetes.io/dockerconfigjson        1         22s


#查看和修改
kubectl edit secret/zhang21-secret
```

如果需要访问多个注册表，你可以为每个注册表创建一个secret。当为pod来取镜像时，kubelet会将`imagePullSecret`合并到 一个虚拟的`.docker/config.json`文件中。
pod只能在自己的命名空间中引用image pull secret，因此每个命名空间都需要执行一次此过程。

<br>

pod上的imagePullSecret

```
apiVersion:
kind: Pod
xxx
spec:
  container:
    xxx
  imagePullSecretes:
    name: zhang21-secret
```


<br/>
<br/>


### 容器环境变量

Container Environment Variables


k8s容器环境为容器提供了几个重要资源：

- 文件系统(是镜像和卷的组合)
- 容器自身信息
- 集群中对象的信息



<br/>
<br/>


### 容器生命周期钩子

Container Lifecycle Hooks


本节描述了kubelet如何使用容器生命周期钩子框架来运行在管理生命周期中由事件触发的代码。
与许多具有组件生命周期钩子的编程语言框架类似，k8s为容器提供了生命周期钩子。钩子使容器能够了解其生命周期中的事件，并在执行相应的生命周期钩子时运行在处理程序中实现的代码。


<br/>


#### 容器钩子

有两个公开给容器的钩子：

- **PostStart**
此钩子在容器创建后立即执行。但是，无法保证钩子将在容器`ENTRYPOINT`之前执行。没有参数传递给处理程序。

- **PreStop**
此钩子在容器终止前立即调用。它是阻塞的，意味着它是同步的。所以它必须在调用删除容器之前完成才能发送。没有参数传递给处理程序。

<br>

**Hook handler implementations**
容器可以通过实施和注册该钩子的处理程序来访问钩子。可为容器实施两种类型的钩子处理程序：

- Exec： 在cgroup和namespace内执行特定的命令
- HTTP： 在容器的特定端点上执行一个HTTP请求

<br>

**Hook handler exection**
调用容器生命周期管理钩子时，k8s管理系统会在为钩子注册的容器中执行处理程序。

钩子处理程序调用包含在容器的Pod的上下文中是同步的。这意味着对**PostStart钩子**，容器`ENTRYPOINT`和钩子异步启动。但是，如果钩子 运行/挂起 太长时间，则容器无法达到`running state`。
**PreStop钩子**的行为类似。如果钩子在执行期间挂起，则pod阶段将保持在`Terminating state`，并在pod结束的`terminationGracePeriodSeconds`之后被杀掉。
如果**PostStart**或**PreStop**钩子失败，则会杀掉容器。

用户应该使他们的钩子处理程序尽可能的轻量化。

<br>

**Hook delivery guarantees**
钩子交付至少是一次，这意味着对于任何给定的事件可以多次调用钩子。由钩子实现来正确处理这个问题。
通常，只进行当次交付。在一些罕见的情况下，可能会发生双重交付。

<br>

**Debugging Hook handlers**
钩子处理程序的日志并不会在Pod事件中公开。如果处理程序由于某种原因失败，它会广播这个事件。



<br/>
<br/>
<br/>



## 工作负载

Workloads


### Pods

Pod是k8s的基本构建块，是你创建和部署k8s对象模型中最小和最简单的单元。Pod代表了集群上正在运行的进程。
Pod封装了(encapsulates) 一个/多个 应用程序容器，存储资源，唯一的IP地址(集群内)以及控制容器运行需要的选项。Pod代表了一个部署单元，k8s中的单个应用程序实例可能包含单个或少量紧密耦合且共享资源的容器。
Docker是k8s Pod中最常使用的容器运行环境(runtime)，Pod同样也支持其它容器运行环境。

k8s 集群中的Pods可以用两种主要方法来使用：

- **运行单个容器的Pod**
Pods that run a single container
`one-container-per-pod`模型时最常见的k8s用例。在这种情况下，你可将Pod视为单个容器的包装，而k8s直接管理Pod而不是容器。

- **运行多个需要协同工作的容器的Pod**
Pods that run multiple containers that need to work together
Pod可能封装了由多个协同定位(co-located)容器组成的应用程序，这些容器紧密耦合并且需要共享资源。这些协同的容器可能形成一个统一的服务单元——一个容器从共享卷向公众提供文件，而一个单独的`sidecar`容器刷新或更新这些文件。Pod将这些容器和资源作为单个可管理的实体包装在一起。

<br>

每个Pod都用于运行给定应用程序的单个实例。如果你想要水平扩展应用程序，你可以使用多个Pods(每个实例一个)。在k8s中，这通常称为**副本(replication)**。 `Replicated Pods`通常通过称为**控制器(Controller)**的抽象来创建和管理。

<br>

**Pod如何管理多个容器**
Pods旨在支持多个协作进程(as container)，形成一个具有凝聚力的服务单元。Pod中的容器将自动协同定位(co-located)，并在集群中的同一主机上协同调度(co-scheduled)。容器可以共享资源和依赖，彼此通信，并协调它们何时以及如何终止。

注意，将多个协同定位和协同管理的容器分组到一个Pod中是一个相对高级的栗子。你应该仅在容器紧密耦合的特定实例中使用此模式。
例如，你可能有一个容器充当共享卷中文件的Web Server，以及一个单独的`sidecat`容器——用于从远程更新这个文件：

![多容器Pod](/images/K8s/pod_multi_container.png)

<br>

**Pod共享资源**
Pod为其组成容器提供了两种共享资源：

- **Networking**
每个Pod都被分配了一个唯一的IP地址(within cluster)。Pod中的每个容器都共享网络命名空间，包括IP地址和网络端口。Pod内的容器可使用`localhost`相互通信。当Pod内的容器与Pod外的实体通信时，它们必须协调如何使用共享网络资源。

- **Storage**
Pod可以指定一组共享存储卷。Pod中的所有容器都可以访问这个共享卷，允许这些容器共享数据。还是关于数据持久化的卷。

<br>

**使用Pods**
你很少直接在k8s(甚至是单例Pod)中创建单独的Pod。这是因为Pod被设计为相对短暂的一次性实体，即用后即焚。当Pod被创建后，都会被调度到集群中的节点上运行。Pod保留在该节点上，知道进程终止，Pod对象被删除，Pod因资源不足而被驱逐，或节点失效。Pod不会自愈。
注意： 重启Pod中的容器与重启Pod不是一回事。Pod本身不运行，它只提供容器的运行环境并保持容器的运行状态。但是容器运行的环境会持续存在，直到删除为止。

Pod本身不提供自我修复(self-heal)。如果将Pod调度到一个失败的节点，或调度操作本身失败，则会删除Pod。同样，由于缺乏资源或节点维护中，Pod将无法在驱逐中存活。k8s使用一个高更级别的抽象，称为控制器(Controller)。它管理相对可处理的Pod实例的工作。因此，尽管可以直接使用Pod，但在k8s中使用控制器管理Pod更为常见。
控制器可为你创建和管理多个Pod，处理副本和上线，并在集群范围内提供自我修复功能。例如，如果节点故障，控制器可能会通过在不同节点上安排相同的替换来自动替换Pod。
通常，控制器使用你提供的Pod模板来创建它负责的Pod。

<br>

**Pod Templates**
Pod模板是Pod规范，包含在其它对象中。控制器使用Pod模板制作实际的Pod。

栗子：

```json
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo Hello Kubernetes! && sleep 3600']
```

Pod模板不是指定所有副本的当前所需状态，而是像饼干切割器。饼干被切割后，饼干与切割器无关。


<br/>
<br/>


#### Pod

Pod是可在k8s中创建和管理的最小可部署的计算单元。

<br>

**Pod是什么**
Pod是一组 一个/多个容器，具有共享存储/网络，以及如何运行容器的规范。Pod中的容器总是`co-located`和`co-scheduler`，并在共享上下文中运行。一个pod模拟特定应用程序的逻辑主机，它包含一个/多个紧密耦合的应用程序容器。
Pod的共享上下文十一组Linux namespace， cgroup，以及隔离方面。在Pod的上下文中，各个应用程序科恩能够回应用进一步的子隔离。
Pod中的容器共享IP地址和端口空间，并且可通过`localhsot`找到彼此。它们还可使用IPC相互通信。不同Pod中的容器具有不同的IP地址，默认情况下无法通信，需要进行额外配置。
Pod中的应用程序还可访问共享卷，共享卷被定义为Pod的一部分，可挂载到每个应用程序的文件系统中。
就Docker构造而言，Pod被建模为一组具有共享命名空间和共享卷的Docker容器。
与单个应用程序容器类似，Pod被认为是相对短暂(非持久)的实体。

<br>

**Pod动机**

- 管理(Management)
Pod是多个协作过程进程模式的模型，形成了一个有凝聚力的服务单元。它们通过提供更高级别的抽象来简化应用程序部署和管理。Pod提供用于部署，水平扩展，副本的单元。对于Pod中的容器，它们将自动处理协同调度， 共享命运， 协同副本，资源共享和依赖管理...

- 资源共享和交流
Pod可以实现成员之间的数据共享和通信。
Pod中的应用程序都是用相同的网络命名空间，因此可通过`localhost`进行通信。因此，Pod中的应用程序必须协调对端口的使用。
主机名设置为Pod中应用程序容器的Pod名。
除了定义在Pod中运行的应用程序容器，Pod还制定了一组共享存储卷(持久化)。

```sh
kubectl -n kube-system get pod -o wide
NAME                                   READY     STATUS    RESTARTS   AGE       IP               NODE
kubernetes-dashboard-6948bdb78-tdh5v   1/1       Running   0          8d        10.244.2.3       salt01
metrics-server-85ff8f7b84-72rd4        1/1       Running   0          9d        10.244.2.2       salt01


kubectl -n kube-system exec -it metrics-server-85ff8f7b84-72rd4 /bin/sh
/ # hostname
metrics-server-85ff8f7b84-72rd4
/ # ifconfig
eth0 10.244.2.2
/ # ping 10.244.2.3
PING 10.244.2.3 (10.244.2.3): 56 data bytes
64 bytes from 10.244.2.3: seq=0 ttl=64 time=0.115 ms
64 bytes from 10.244.2.3: seq=1 ttl=64 time=0.062 ms
```

<br>

**Pod使用**
Pod可用于托管垂直集成的应用程序栈，但主要动机是用于支持协同共处，协同管理的应用程序。如：

- 内容管理系统，文件和数据加载器，本地缓存管理器
- 日志和检查点的备份、压缩、轮询、快照
- 数据变更观察器，日志和监控适配器，事件发布器
- 代理，网桥和适配器
- 控制器，管理器，配置器和更新器

通常，单个Pod不用于运行同一程序的多个实例。

<br>

**替代考虑**
为什么不在单个容器中运行多个程序？

1. 透明度
2. 解耦软件依赖关系
3. 使用方便
4. 效率

<br>

**Pod耐久性**
Pod不应被视为耐用实体。它们不会在 调度失败，节点故障，驱逐，节点维护等情况下存活。
通常，用户不需要直接创建Pod。而应该(几乎总是)使用控制器。控制器提供了集群范围内的自修复(self-healing)，副本和上线管理。

Pod公开为一个原语以便于使用：

- 调度器和控制器可插拔
- 支持Pod级操作，而无需通过控制器API代理
- 将Pod寿命与控制器寿命分离
- 控制器和服务的分离
- kubelet实际是Pod控制器
- 高可用应用程序

<br>

**Pod终止**
由于Pod表示集群中节点上正在运行的进程，因此允许这些进程在不需要时优雅地终止(gracefully terminate)非常重要。用户应该能够请求并指导进程何时终止，但也要确保删除最终完成。当用户请求删除Pod时，系统会在允许Pod强制终止之前记录预期的宽限期(grace period)，并将`TERM`信号(-15)发送到每个容器的主进程中。宽限期到期后，`KILL`信号(-9)发送到这些进程，然后从API server中删除该Pod。如果在等待进程终止时Kubelet或容器管理器重启了，则将在完整的宽限期内重试终止。

流程：

1. 用户发送删除Pod的命令，默认宽限期(30s)
2. API server中的Pod随着时间的推移而更新，在此之后，除了宽限期外，Pod被认为死亡
3. 列出客户端命令时，Pod显示为`Terminating`
4. 当Kubelet发现Pod被标记为`Terminating`，它将开始Pod关闭过程
	4.1 如果Pod定义了`preStop hook`，则会在Pod内调用
	4.2 Pod中的进程发送`TERM`信号
5. Pod将从端点列表中删除，并且不再被视为副本控制器中运行的Pod的一部分。缓慢关闭的Pod无法继续为流量提供服务，因为负载均衡器会将其从轮询中删除
6. 当宽限期到期后，仍在Pod中运行的任何进程都将被`KILL`信号杀死
7. Kubelet通过设置宽限期0（立即删除）完成删除API server上的Pod。Pod从API中消失，客户端不在可见

默认情况下，所有删除都有30s的宽限期。`kubectl delete`命令支持指定`--grace-period=`选项。设置为0表示强制删除Pod。`--force --grace-period=0`强制删除。

**强制删除Pod**
强制删除Pod被定义为立即从集群状态和etcd中删除Pod。当执行强制删除时，API server不会等待来自Kubelet的确认——确认该Pod已在运行的节点上终止。它会立即删除API中的Pod，以便可使用相同的名称创建新的Pod。在节点上，设置为立即终止的Pod在被强制终止之前仍被授予一个小的宽限期。
强制删除可能会对某些Pod有潜在危险，请谨慎执行。

<br>

**Pod容器的特权模式(Privileged mode)**
在容器 spec的`SecurityContext`中使用`privileged`标志，来启用Pod中容器的特权模式。这对于想要使用Linux功能的容器非常有用。容器内的进程获得与可访问的容器外进程几乎相同的权限。使用特权模式，可以更容易的编写网络和卷插件，而不需要编译到kubelet。

<br>

**API对象**
Pod是k8s REST API中的顶级资源, `/pod/xxx`。


<br/>
<br/>


#### Pod生命周期

Pod Lifecycle

<br>

**阶段(phase)**
Pod的`status`字段是一个`PodStatus`对象，它有一个`phase`字段。

阶段可能的值：

| Value | Description |
| - | - |
| Pending | The Pod has been accepted by the Kubernetes system, but one or more of the Container images has not been created. This includes time before being scheduled as well as time spent downloading images over the network, which could take a while. |
| Running | The Pod has been bound to a node, and all of the Containers have been created. At least one Container is still running, or is in the process of starting or restarting. |
| Succeeded | All Containers in the Pod have terminated in success, and will not be restarted. |
| Failed | All Containers in the Pod have terminated, and at least one Container has terminated in failure. That is, the Container either exited with non-zero status or was terminated by the system. |
| Unknown | For some reason the state of the Pod could not be obtained, typically due to an error in communicating with the host of the Pod.  |

<br>

**状况(conditions)**
Pod有一个`PodStatus`，它有一个`PodConditions`数组，表示Pod是否通过。每个`PodCondition`数字的每个元素都有六个可能的字段：

- `lastProbeTime`: 最后一次探测Pod状况的字段
- `lastTransitionTime`: Pod最后从一个状态转换到另一个状态的时间戳的字段
- `message`: 有关转换的人类可读的详细信息的字段
- `reason`: 一个独特的，单字的最后转换的原因的字段
- `status`: 字段值可能为`True, False, Unknown`
- `type`: 字段可能有如下值:
	+ `PodScheduled`: Pod已被调度到一个节点
	+ `Ready`: Pod能提供请求，并应该添加到所有匹配服务的负载均衡池中
	+ `Initialized`: 所有的初始化容器已成功启动
	+ `Unschedulable`: 调度器现在无法调度Pod，如缺乏资源...
	+ `ContainersReady`: Pod中的所有容器都已准备好了

<br>

**探测(probes)**
探测是由容器上的kubelet定期执行的诊断。为了执行诊断，kubelet调用容器执行处理器(Handler)。有三种类型的处理器:

- `ExecAction`: 在容器内执行指定命令。如果状态码为0，则认为诊断成功
- `TCPSocketAction`: 在指定端口的容器IP地址执行TCP检查。如果端口打开，则认为诊断成功
- `HTTPGetAction`: 在容器IP的特定端口的路径下执行HTTP GET请求。如果请求成功，则认为诊断成功

每个探测可能有三种结果:

- Success
- Failure
- Unknown

kubelet可选择在运行容器上执行两种探测并对其作出反应:

- `livenessProbe`: 确定容器是否正在运行
- `readinessProbe`: 确定容器是否准备好为请求提供服务

什么时候使用这两中探测？
When should you use liveness or readiness probes?

如果容器中的进程在遇到问题或变得不健康时会自行崩溃(crash)，则你不一定需要`livenessProbe`。kubelet将根据Pod的`restartPolicy`自动执行正确的操作。
如果希望在探测失败时杀死并重启容器，则请指定`livenessPorbe`和指定`restartPolicy`为`Always`

如果只想在探测成功时向Pod发送流量，请指定`readinessProbe`。
如果容器需要在启动期间除了大型数据，配置文件或迁移，请指定`readnessProbe`。
如果你希望容器能够自行维护，你可指定一个`readnessProbe`，它检查特定端点。

注意，如果你只想在删除Pod时排除请求，则不一定需要`readnessProbe`。无论是否存在`readnessProbe`，Pod都会自动将其置于未准备状态。Pod在等待Pod中容器停止时仍处于未准备状态。

<br>

**Pod readiness gate**
FEATURE STATE: Kubernetes v1.11 alpha

为了通过向PodStatus调价额外的反馈或信号来增加`Pod readness`的可扩展性，k8s v1.11引入了一个名为`Pod ready++`的功能。你可在`PodSpec`中使用新字段`ReadinessGate`来指定要为Pod准备情况评估的其它条件。如果k8s在Pod的`status.conditions`字段找不到这样的状况，则状况的状态默认为`False`。

```
Kind: Pod
...
spec:
  readinessGates:
    - conditionType: "www.example.com/feature-1"
status:
  conditions:
    - type: Ready  # this is a builtin PodCondition
      status: "True"
      lastProbeTime: null
      lastTransitionTime: 2018-01-01T00:00:00Z
    - type: "www.example.com/feature-1"   # an extra PodCondition
      status: "False"
      lastProbeTIme: null
      lastTransitionTime: 2018-01-01T00:00:00Z
  containerStatuses:
    - containerID: docker://abcd...
      ready: true
...
```

<br>

**重启策略**
`PodSpec`有一个`restartPolicy`字段，其值可能是`Always(默认值), OnFailure, Never`。此策略应用于Pod中的所有容器，它仅指由同一节点上的kubelet重启的容器。退出的容器将由kubelet以指定退避延迟(10s, 20s, 40s...)重新启动，上限5分钟，并在成功执行十分钟后重置。

<br>

**寿命(lifetime)**
一般来说，Pod不会消失，直到有人摧毁它们。唯一的例外是，具有成功或失败超过一段时间的阶段的Pod将过期并自动销毁。

有三种类型的控制器可用：

- Use a Job for Pod
- Use a  ReplicationController/ReplicaSet/Deployment for Pod
- Use a DaemonSet for Pod

所有三种类型的控制器都包含了PodTemplate。推荐创建适当的控制器并让它创建Pod，而不是自己直接创建Pod。这是因为Pod单独对机器故障没有弹性，但控制器不会。
如果节点死亡或与集群的其余部分断开连接，k8s会应用策略将丢失节点上的所有Pod的阶段设置为Failed。


<br/>
<br/>


#### Init Containers

本节提供了初始容器(init container)的概述，它是在应用程序容器运行之前的专用容器，可包含应用程序镜像中不存在的实用程序或脚本设置。

<br>

**理解初始容器**
Pod可以有多个容器在其中运行应用程序，但它同样可以有一个或多个初始容器——它在应用程序容器启动前运行。
初始容器与常规容器一样，除了：

- They always run to completion.
- 每一个必须在下一个启动之前成功完成

如果Pod的初始容器失败，则k8s会重复重启直到初始容器成功。但是，如果Pod的`restartPolicy`为`Never`，则不会重启。
要将容器指定为初始容器，请将`PodSpec`上的`initContainers`字段添加为应用程序`container`数组旁边的容器类型对象的JSON数组。初始容器的状态在`.status.initContainerStatuses`字段中作为容器状态数据返回。

**与常规容器的不同**
初始容器支持应用程序容器的所有字段和功能，包括资源限制，卷和安全设置。但资源请求和处理方式略有不同。此外，初始容器不支持`readiness probes`，因为它必须在Pod准备好之前运行完成。
如果为Pod指定了多个初始容器，则按顺序依次运行一个容器。每个必须在下一个运行之前完成。当所有初始容器都运行完毕时，k8s会初始化Pod并像往常一样运行应用程序容器。

<br>

**初始容器可用于什么**
由于初始容器具有来自应用程序容器的单独镜像，因此它们对于启动相关代码具有一些优势：

- 出于安全原因，它们可以包含并运行不希望包含在应用程序容器镜像中的使用程序
- 它可以包含应用程序镜像中不存在的实用程序或自定义代码。例如，在配置过程中，无需为了使用其他工具(sed, awk, dig...)而专门使用`FROM`创建一个镜像
- 应用程序镜像构建器和部署器角色可独立工作，而无需共同构建单个应用程序镜像
- 它们使用Linux命名空间，以便从应用程序容器中获得不同的文件系统视图。因此，它们可以访问应用程序容器无法访问的`Secrets`
- 它们在应用程序容器启动前运行完成，因此初始容器提供了一种简单的方法来阻止或延迟应用程序容器的启动，知道满足一组前置条件。

<br>

**栗子**
这有些初始容器的使用案例:

- 等待使用shell命令创建服务: `for in in {1..100}; do sleep 1; if dig myservice; then exit 0; fi; done; exit 1`
- 使用API从远程服务器注册此Pod: `curl -XPOST http://host:port/register -d 'instance=$()&ip=$()'`
- 在启动应用程序之前等待一段时间: `sleep 60`
- 克隆一个git repo到某个卷
- 替换配置文件中的值并运行模板来动态生成应用程序容器的配置文件

<br>

**使用初始容器**
两个初始容器。第一个等待`myservice`，第二个等待`mydb`。一旦两个容器完成，Pod将开始。

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'until nslookup myservice; do echo waiting for myservice; sleep 2; done;']
  - name: init-mydb
    image: busybox
    command: ['sh', '-c', 'until nslookup mydb; do echo waiting for mydb; sleep 2; done;']
```

创建:

```
kubectl create -f /etc/k8s/test/init-container.yaml
pod/myapp-pod created


kubectl get pod
NAME             READY     STATUS     RESTARTS   AGE
init-container   0/1       Init:0/2   0          6s



kubectl describe -f /etc/k8s/test/init-container.yaml
Init Containers:
  init-myservice:
    Container ID:  docker://f9ca73d4d2c8903a1fe84937e34ae27b909a691d2e524254b8f4aec9d5cc754c
    Image:         busybox
    Image ID:      docker-pullable://docker.io/busybox@sha256:cb63aa0641a885f54de20f61d152187419e8f6b159ed11a251a09d115fdff9bd
    Port:          <none>
    Host Port:     <none>
    Command:
      sh
      -c
      until nslookup myservice; do echo waiting for myservice; sleep 2; done;
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Fri, 24 Aug 2018 16:31:13 +0800
      Finished:     Fri, 24 Aug 2018 16:31:18 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-69vgk (ro)
  init-mydb:
    Container ID:  docker://a9946122976ff70ff1dd874299e3e63f4b07f2758f5e6518b84343c58daa3506
    Image:         busybox
    Image ID:      docker-pullable://docker.io/busybox@sha256:cb63aa0641a885f54de20f61d152187419e8f6b159ed11a251a09d115fdff9bd
    Port:          <none>
    Host Port:     <none>
    Command:
      sh
      -c
      until nslookup mydb; do echo waiting for mydb; sleep 2; done;
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Fri, 24 Aug 2018 16:31:24 +0800
      Finished:     Fri, 24 Aug 2018 16:31:29 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-69vgk (ro)
Containers:
  myapp-container:
    Container ID:  docker://b2c7a1f32d65dd41fa439d1f6879824b40c3014b32b15d61fed0cda171144a1b
    Image:         busybox
    Image ID:      docker-pullable://docker.io/busybox@sha256:cb63aa0641a885f54de20f61d152187419e8f6b159ed11a251a09d115fdff9bd
    Port:          <none>
    Host Port:     <none>
    Command:
      sh
      -c
      echo The app is running! && sleep 3600
    State:          Running
      Started:      Fri, 24 Aug 2018 16:31:34 +0800
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-69vgk (ro)
```

![初始容器](/images/K8s/init_container.png)

<br>

**详细行为**
在Pod启动期间，初始化网络和卷后，初始容器将按顺序启动。每个容器必须在下一个容器启动前成功退出。如果容器由于运行环境未能启动或失败退出而启动失败，则它根据Pod的`restartPolicy`重试。如果Pod的`restartPolicy`为`Always(默认)`，则初始容器使用`restartPolicy`为`OnFailure`。
在所有初始容器都成功之前，Pod无法变为`Ready`。初始容器上的端口无法聚合到服务下。正在初始化的Pod处于`Pending`状态，但应该具有`Initializing`设置为`true`的条件。
如果Pod重启，则所有初始都要执行一遍。
`init container spec`的更改仅限于容器镜像字段。更改初始容器镜像字段相当于重启Pod。
由于初始容器可重启，重试或重新执行，因此初始容器代码应该是幂等的。In particular, code that writes to files on EmptyDirs should be prepared for the possibility that an output file already exists.
在Pod上使用`activeDeadlineSeconds`，在容器上使用`livenessProbe`，以防止初始容器永远失败。
Pod中每个应用程序和初始容器的名称必须是唯一的，否则会引发验证错误。

**资源**
给定初始容器的排序和执行，适用一下资源使用规则：

- 在所有初始容器上定义的任何特定资源请求或限制的最高值是有效的初始 请求/限制
- Pod对资源的有效请求/限制是以下值中的较高者:
	+ 所有的应用程序容器对资源请求/限制的总和
	+ 对资源的有效初始请求/限制
- 调度是基于有效请求/限制完成的，这意味着初始容器可以保留在Pod生命周期内未使用的初始化资源
- Pod的有效QoS层与初始容器和应用程序容器一样

Pod级别的cgroup基于有效的Pod请求和限制，与调度程序相同。

<br>

**Pod重启原因**
由于以下原因，Pod可重新启动，导致重新执行初始容器：

- 用户更新了`PodSpec`，导致初始容器镜像发生噶变。应用程序容器镜像的更改仅重启应用程序容器
- Pod的基础架构容器重启
- Pod的所有容器都终止，而`restartPolicy`设置为`Always`，强制重启，并且初始容器完成记录由于垃圾回收而丢失



<br/>
<br/>


#### Pod预设

Pod Preset

Pod Presets是对象，在创建时将特定信息注入Pod。
Pod Preset是一种API资源，用于在创建时将其它运行时的需求写入到Pod。你可使用`label selectors`指定应用于Pod的给定Pod Preset。
使用Pod Preset允许pod template作者不必显示提供每个pod的所有信息。这样，作者不需要知道有关该服务的所有详细信息。

<br>

**它如何工作**
k8s提供了一个`admission controller(Pod Preset)`，启用后，会将Pod Preset应用于传入的pod创建请求。当Pod创建请求发生时，系统会执行一下操作：

1. 检索所有可供使用的Pod Preset
2. 检查任何Pod Preset的`label selector`是否与正在创建的Pod上的标签匹配
3. 尝试将Pod Preset定义的各种资源合并到正在创建的Pod中
4. 出错时，抛出一个记录Pod 合并错误的事件，然后创建不从Pod Preset写入任何资源的pod
5. 注释生成的修改后的Pod spec，以表明它已被Pod Preset修改——`podpreset.admission.kubernetes.io/podpreset-<pod-preset name>: "<resource version>"`

每个Pod能够被零个或多个PodPreset匹配，每个PodPreset可以被应用到零个或多个Pod。当PodPreset应用于一个或多个Pod时，k8s会修改Pod spec。对于`Env, EnvFrom, VolumeMounts`，k8s修改Pod中所有容器的`container spce`；对于`Volume`的更改，k8s修改`Pod spec`。

**为指定Pod禁用PodPreset**
在某些情况下，你希望Pod不被任何PodPreset修改。你可修改: `podpreset.admission.kubernetes.io/exclude: "true"`

<br>

**启用PodPreset**
要在集群中使用PodPreset，你必须确保以下内容：

1. 你已启用API类型: `settings.k8s.io/v1alpha1/podpreset`
2. 你已经启动`admission controller` PodPreset
3. 你已通过在将使用的命名空间中创建PodPreset对象来定义PodPreset



<br/>
<br/>


#### 中断

Disruptions

本节适用于想要构建高可用性应用程序的用户，因此需要了解Pod可能发生的中断类型。
这同样适用于希望执行自动化集群操作的集群管理员，例如升级或自动伸缩集群。

<br>

**自愿和非自愿中断**
Voluntary and Involuntary Disruptions



<br/>
<br/>



### Controller


<br>


#### ReplicaSet

副本集是下一个副本控制器。现在副本集和副本控制器之间的唯一区别是`selector`的支持。副本集支持`labels user guide`中描述的新的基于集合`selector`的要求，而副本控制器仅支持基于等同`selector`的要求。

<br>

**如何使用副本集**
大多数支持副本控制器的`kubectl`命令也支持副本集。一个例外是`rolling-update`命令。如果你想要滚动更新功能，请考虑使用Deployments代替。
虽然副本集可独立使用，但它主要被Deployment用作协调Pod创建，删除和更新的机制。使用部署时，你不必担心管理它们创建的副本集，部署拥有并管理其副本集。

<br>

**何时使用副本集**
副本集确保在任何给定时间运行指定数量的Pod副本。但是，部署是一个更高级别的概念，它管理副本集并为Pod提供声明性更新以及许多其它有用的功能。因此，除非你需要自定义更新或无需更新，否则建议你使用部署而不是直接使用副本集。
这实际上意味着，你不需要操作副本集对象：改为使用部署，并在`spec`部分定义你的应用程序。

<br>

**栗子**

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend
  labels:
    app: guestbook
    tier: frontend
spec:
  # modify replicas according to your case
  replicas: 3
  selector:
    matchLabels:
      tier: frontend
    matchExpressions:
      - {key: tier, operator: In, values: [frontend]}
  template:
    metadata:
      labels:
        app: guestbook
        tier: frontend
    spec:
      containers:
      - name: php-redis
        image: gcr.io/google_samples/gb-frontend:v3
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
        env:
        - name: GET_HOSTS_FROM
          value: dns
          # If your cluster config does not include a dns service, then to
          # instead access environment variables to find service host
          # info, comment out the 'value: dns' line above, and uncomment the
          # line below.
          # value: env
        ports:
        - containerPort: 80
```

```
kubectl create -f /etc/k8s/test/frontend.yaml

```

<br>

**编写副本集`spec`**
与所有其它k8s API对象一样，副本集需要`apiVersion`, `kind`, `metadata`字段，副本集还需要一个`.spce`部分。

```
#Pod Template
.spec.template是.spec唯一必需的字段
除了pod的必须字段，副本集中的Pod模板还必须指定适当的`label`和`restart policy`


#Pod Selector
.spec.selector字段是一个label selector。副本集使用与selector匹配的label来管理所有pod。
它不区分创建或删除的Pod以及人或进程创建或删除的pod。这允许替换副本集而不会影响正在运行的Pod。
.spec.template.metadata.labels 必须匹配 .spec.selector，否则它将被API拒绝。
此外，你通常不应创建任何label与selector匹配的pod。如果你这样做了，副本集会认为它创建了其它pod，k8s并没有阻止你这样做。


#Labels on a ReplicaSet
副本集本身可以有标签(.metadata.labels)。通常，你可将其设置为与 .spec.template.metadata.labels 一致。但，允许他们不同，并且 .metadata.labels 不会影响副本集的行为


#Replicas
你可通过设置 .spec.replicas 来指定应同时运行的pod数量。如果未指定，默认为1
```

<br>

**使用副本集**

```
#删除副本集和它的pods
kubectl delete replicaset/xxx
#或
kubectl proxy --port=8080
curl -XDELETE 'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
-H "Content-Type: application/json"


#仅删除副本集
kubectl delete rs/xxx --cascade=false
#或
kubectl proxy --port=8080
curl -X DELETE  'localhost:8080/apis/extensions/v1beta1/namespaces/default/replicasets/frontend' \
-d '{"kind":"DeleteOptions","apiVersion":"v1","propagationPolicy":"Foreground"}' \
-H "Content-Type: application/json"


#从副本隔离pods
可通过更改label从副本集的目标中删除Pod。此技术可用于从服务中删除pod以进行调试，数据恢复等。以这种方式删除的pod将自动替换


#伸缩副本集
只需更新副本集的 .spec.replicas 字段轻松伸缩副本集。副本集控制器确保具有匹配 label selector 所需数量的pod可用且可操作。


#作为水平pod自动伸缩目标的副本集
Horizontal Pod Autoscalers(HPA)，意味着副本集可通过HPA自动伸缩。
#栗子
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: frontend-scaler
spec:
  scaleTargetRef:
    kind: ReplicaSet
    name: frontend
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 50

kubectl create -f /path/xx/hpa.rs.yaml
#此外，可使用kubectl命令来自动伸缩
#kubectl autoscale rs frontend
```

<br>

**替代副本集**

- Deployment(推荐)
- Bare Pods
- Job
- DaemonSet


<br/>
<br/>


#### ReplicationController

**注意：现在，配置副本集的推荐方法是使用部署。**

副本控制器确保一次运行指定数量的Pod副本。换言之，副本控制器确保一个Pod或一组同类Pod总是可用。


<br/>
<br/>


#### Deployments

部署控制器为Pod和ReplicaSet提供了声明性更新。
在部署对象中描述所需的状态，部署控制器以受控速率将实际状态更改为所需状态。你可定义部署来创建新的副本集，或删除现有的部署并使用新的部署收纳所有资源。
你不应该直接管理部署所拥有的副本集，应该通过操作部署对象来涵盖所有用例。

<br>

**栗子**
以下是部署的典型案例：

- 创建部署来上线副本集
- 声明Pod的新状态
- 回滚到早期的部署版本
- 伸缩部署
- 暂定部署
- 使用部署的状态
- 清理旧的副本集

<br>

**创建一个部署**
下面的栗子，创建一个3个Nginx pods的副本集:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.7.9
        ports:
        - containerPort: 80
```

```sh
kubectl create -f ./nginx-deployment.yaml

kubectl get deployment
kubectl get rs
kubectl get pod --show-labels
```

<br>

**更新部署**
当且仅当部署的pod template发生更改时，才会触发部署更新上线。
假如我们要更新Nginx的版本为`1.9.1`:

```
kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
deployment.extensions/nginx-deployment image updated

#或者
kubectl edit deployment/nginx-deployment
deployment.extensions/nginx-deployment edited


#查看上线状态
kubectl rollout status deployment/nginx-deployment
Waiting for deployment "nginx-deployment" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 1 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 2 out of 3 new replicas have been updated...
Waiting for deployment "nginx-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "nginx-deployment" rollout to finish: 1 old replicas are pending termination...
deployment "nginx-deployment" successfully rolled out


#新旧副本集副本数
kubectl get rs
NAME                          DESIRED   CURRENT   READY     AGE
nginx-deployment-67594d6bf6   0         0         0         16m
nginx-deployment-d78fcfc84    3         3         3         3m
```

部署可以确保在更新时只有一定数量的Pod可能会关闭。默认情况下，它确保最大不可用率25%。
部署确保在所需数量的Pod之上只能创建一定数量的Pod。默认情况下，它确保比最大数多25%。
例如，如果仔细查看上面的部署，你将看到它首先创建了一个新的Pod，然后删除了一些旧的Pod并创建新的Pod。在有足够数量的新Pod出现之前，它不会杀死旧的Pod，并且在足够数量的旧Pod被杀死之前不会创建新的Pod。

通常不鼓励进行`label selector`的更改，建议你事先规划好`selector`。

<br>

**回滚(rolling back)部署**
有时可能需要回滚部署，当部署不稳定时，如崩溃循环(crash looping)。默认情况下，所有的部署上线历史都保留在系统中，以便可以随时回滚。

假设我之间将`nginx:1.7.1`更新到`nginx:1.9.1`的时候错误的写成了`nginx:1.91`:

```
kubectl set image deployment/nginx-deployment nginx=nginx:1.91


#上线就会卡在此处
kubectl rollout status deployments nginx-deployment
Waiting for deployment "nginx-deployment" rollout to finish: 1 out of 3 new replicas have been updated...
error: deployment "nginx-deployment" exceeded its progress deadline


#查看容器错误，它会报镜像拉取错误
kubectl get pod
nginx-deployment-58c7645486-s5t6t   0/1       ImagePullBackOff   0          3m        <none>        node
#UI里面的报错
#Failed to pull image "nginx:1.91": rpc error: code = Unknown desc = manifest for docker.io/nginx:1.91 not found
```

部署控制器将自动停止错误的`rollout`，并将停止扩展新的副本集。这取决于滚动升级的参数(`maxUnavailable`)。默认情况下，k8s将值设置为1，将`.spec.replicas`设置为1，因此你无需关心设置这些参数。你的部署可能具有100%的不可用性。

要修复它，你需要回滚到先前稳定的部署版本。

```
#检查上线历史
kubectl rollout history deployment/nginx-deployment
deployments "nginx-deployment"
REVISION    CHANGE-CAUSE
1           kubectl create -f ./nginx-deployment.yaml --record
2           kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1
3           kubectl set image deployment/nginx-deployment nginx=nginx:1.91

#查看某个上线历史
rollout history deployment/nginx-deployment --revision=2


#回滚

#回滚到前一个版本
kubectl rollout undo deployment/nginx-deployment
deployment.extensions/nginx-deployment

#回滚到指定版本
kubectl rollout undo deployment/nginx-deployment --to-revision=2


#查看事件
kubectl describe deployment/nginx-deployment
Events:
  Type    Reason              Age                From                   Message
  ----    ------              ----               ----                   -------
  Normal  DeploymentRollback  2m                 deployment-controller  Rolled back deployment "nginx-deployment" to revision 3
  Normal  ScalingReplicaSet   2m                 deployment-controller  Scaled down replica set nginx-deployment-58c7645486 to 0
```

<br>

**伸缩副本**

```
#扩展部署
kubectl scale deployment nginx-deployment --replicas=5


#水平伸缩
kubectl autoscale deployment nginx-deployment --min=3 --max=6 --cpu-percent=80

#查看
kubectl get horizontalpodautoscaler.autoscaling
NAME               REFERENCE                     TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
nginx-deployment   Deployment/nginx-deployment   <unknown>/80%   3         6         5          1m

```

**比例伸缩(proportional scaling)**
滚动升级部署支持同时运行多个版本的应用程序。当你或自动伸缩器正在上线滚动更新的部署时，部署控制器将平衡现有活动的副本集中的其它副本，以降低风险。这称为比例缩放。

```
kubectl get deploy
NAME               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   5         5         5            5           1h


#更新一个错误镜像，它会卡住
kubectl set image deploy/nginx-deployment nginx=nginx:sometag

kubectl get rs -o wide
NAME                         DESIRED   CURRENT   READY     AGE       CONTAINERS   IMAGES          SELECTOR
nginx-deployment-895bd59bc   3         3         0         1m        nginx        nginx:sometag   app=nginx,pod-template-hash=451681567
nginx-deployment-d78fcfc84   5         5         5         1h        nginx        nginx:1.7.1     app=nginx,pod-template-hash=834979740


kubectl get deploy -o wide
NAME               DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE       CONTAINERS   IMAGES          SELECTOR
nginx-deployment   6         8         3            5           1h        nginx        nginx:sometag   app=nginx
```

<br>

**暂停和恢复部署**
你可以在触发一个或多个更新之前暂停(pause)部署，然后恢复(resume)它。这允许你在暂停和恢复之间应用多个修复，而不会触发不必要的上线。
注意： 在恢复暂停部署之前，无法执行回滚操作。

```
#暂停
kubectl rollout pause deployment/nginx-deployment
deployment.extensions/nginx-deployment paused


kubectl set image deploy/nginx-deployment nginx=nginx:1.9.1
deployment.extensions/nginx-deployment image updated

kubectl set resources deployment nginx-deployment -c=nginx --limits=cpu=200m,memory=128Mi
deployment.extensions/nginx-deployment resource requirements updated


#恢复
kubectl rollout resume deployment/nginx-deployment
deployment.extensions/nginx-deployment resumed

```

<br>

**部署状态**
部署在其生命周期内会进入各种状态--`kubectl rollout status`

- Progessing Deployment
	+ 部署创建一个新的副本集
	+ 部署伸缩到新的/旧的副本集
	+ 新的Pod可用

- Complete Deployment
	+ 所有与部署关联的副本都已完成
	+ 所有与部署关联的副本都可用
	+ 没有正在运行的旧的部署副本

- Failed Deployment
	+ 配额不足
	+ 准备探针失败
	+ 镜像拉取失败
	+ 权限不足
	+ 限制范围
	+ 应用程序运行时配置错误

- Operating on a failed deployment

<br>

**Clean up Policy**
可在部署中设置`.spec.revisionHistoryLimit`字段来指定需要保留的旧副本集数。其余的将在后台被垃圾回收，默认为10。

**注意：**将此字段设置为0会导致清理部署的所有历史记录，从而部署将无法回滚。

<br>

**Deployment Spec**
与其它k8s配置一样，Deployment需要`apiVersion`, `kind`, `metadata`字段。但部署还需要`.spec`

```
#pod template
#必填字段
.spec.template


#Replicas
.spec.replicas


#Selector
#它必须匹配.spec.template.metadata.labels，否则会被API拒绝
.spec.selector


#Strategy
.spec.strategy

#Recreate deployment
.spec.strategy.type==Recreate

#Rolling Update Deployment
.spce.stratefy.type==RollingUpdate
#Max Unavailable
.spec.strategy.rollingUpdate.maxUnavailable
#Max Surge
.specstrategy.rollingUpdate.maxSurge


#Progress Deadline Seconds
.spec.progressDeadlineSeconds


#Min Ready Seconds
.spec.minReadySeconds


#Rollback To
.spec.rollbackTo


#Revision History Limit
.spec.revisionHistoryLimit


#Paused
.spec.paused

```

<br>

**替代方案**

- kubectl rolling update
`kubetl rolling update`以类似的方式更新Pod和副本集控制器。但建议使用部署，因为它是声明性的。



<br/>
<br/>


#### StatefulSets

`StatefulSet`是用于管理有状态应用程序的工作负载的API对象。
**Note: StatefulSets are stable (GA) in 1.9.**

管理一组Pod的部署和伸缩，并提供有关这些Pod的序列和唯一性的保证。
与部署类似，有状态集管理基于相同容器规范(spec)的Pod；与部署不同，有状态集为其每个Pod维护一个粘性(sticky)标识。这些Pod根据相同的规范创建，但不可互换，每个Pod都有一个持久的标识符，它可在任何重新调度时保留。
有状态集与任何其它控制器相同的模式运行。你在有状态集对象中定义所需的状态，有状态集控制器进行任何必要的更新以从当前状态到达期望状态。

<br>

**使用有状态集**
有状态集对于需要以下一个或多个应用程序非常有用：

- 稳定，唯一的网络标识
- 稳定，持久存储
- 有序，优雅的部署和伸缩
- 有序，优雅的删除和终止
- 有序，自动的滚动更新

如果应用程序不需要任何稳定标识或有序部署、删除、伸缩，则应该使用提供一组无状态副本的控制器来部署你的应用程序。如部署或副本集这样的控制器可能更适合无状态需求。

<br>

**局限(limitations)**

- k8s v1.9+
- 给定Pod的存储必须由`PersistentVolume Provisioner`根据请求的存储类进行配置，或由管理员预先配置
- 删除/伸缩有状态集将不会删除与有状态集相关联的卷。这是为了确保数据安
- 有状态集目前要求`headless service`负责Pod的网络身份，你有责任创建此服务

<br>

**组件(components)**

- `headless service`，用于控制网络域
- `StatefulSet`
- `volumeClaimTemplates`，使用持久化卷提供稳定存储

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # has to match .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3 # by default is 1
  template:
    metadata:
      labels:
        app: nginx # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: k8s.gcr.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```

<br>

**Pod Selector**
必须设置有状态集的`.spec.selector`字段以匹配`.spec.template.metadata.labels`的标签。

<br>

**Pod Identity**
有状态集Pod有一个唯一的标识，由序数、稳定的网络表示和稳定的网络存储组成。

- Ordinal Index
对于有多个副本的有状态集，有状态集中的每个Pod将被分配一个唯一的整数序数(ordinal)，从0--(N-1)。

- Stable Network ID
有状态集中的每个Pod都从有状态集的名称和Pod的序号中派生其主机名。构造的主机名的模式时`$(statefulset name)-$(ordinal)`。

- Stable Storage
k8s为每个`VolumeClaimTemplate`创建一个`PersistentVolume`。

- Pod Name Label
当有状态集控制器创建Pod时，它会添加一个标签`statefulset.kubernetes.io/pod-name`，该标签设置为Pod的名称。该标签允许你将服务附加到有状态集中的特定Pod。

<br>

**部署和伸缩保证(guarantees)**

- 对于有多个副本的有状态集，当Pod被部署时，它们按顺序从{0...N-1}被创建
- 但Pod被删除，它们将以{N-1...0}的相反顺序终止
- 在伸缩操作应用于Pod之前，所有的前置任务(predecessors)必须是Running和Ready
- 在终止Pod之前，其所有后继者(successors)必须完全关闭

有状态集不应该指定`pod.Spec.TerminationGracePeriodSeconds`为0，这很不安全，强烈建议不要这么做。

k8s v1.7+，有状态集允许你放宽Pod管理策略的排序保证，同时通过其`.spec.podManagementPolicy`字段保留期唯一性和身份保证。
`OrderedReady` pod管理是有状态集的默认设置。
`Parallel` pod管理告诉有状态集控制器并行(parallel)启动或终止所有Pod，并且在启动或终止另一个Pod之前不等待Pod变为Running、Ready或完全终止。

<br>

**更新策略**
有状态集的`.spec.updateStrategy`字段允许你为有状态集中的Pod配置和禁用容器、标签、资源请求/限制、注释的自动更新。



<br/>
<br/>


#### DaemonSet

守护进程集确保所有(或某些)节点运行Pod的副本。随着节点添加到集群中，会将Pod添加到集群中。随着节点从集群中移除，Pod将被垃圾回收。删除一个守护进程集会清除它创建的Pod。

守护进程集的一些典型用法：

- 在每个节点上运行集群存储守护进程
- 在每个节点上运行日志收集守护进程
- 在每个节点上运行一个节点监控守护进程

<br>

**Writing a DaemonSet Spec**

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-elasticsearch
  namespace: kube-system
  labels:
    k8s-app: fluentd-logging
spec:
  selector:
    matchLabels:
      name: fluentd-elasticsearch
  template:
    metadata:
      labels:
        name: fluentd-elasticsearch
    spec:
      tolerations:
      - key: node-role.kubernetes.io/master
        effect: NoSchedule
      containers:
      - name: fluentd-elasticsearch
        image: k8s.gcr.io/fluentd-elasticsearch:1.20
        resources:
          limits:
            memory: 200Mi
          requests:
            cpu: 100m
            memory: 200Mi
        volumeMounts:
        - name: varlog
          mountPath: /var/log
        - name: varlibdockercontainers
          mountPath: /var/lib/docker/containers
          readOnly: true
      terminationGracePeriodSeconds: 30
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
      - name: varlibdockercontainers
        hostPath:
          path: /var/lib/docker/containers
```

```
#创建守护进程集
kubectl create -f ./daemonset.yaml
```

- Required Fields
与其它k8s配置一样，守护进程集需要`apiVersion`, `kind`, `metadata`, `.spec`字段。

- Pod Template
`.spec.template`是`.spec`的必要字段。
守护进程集中的人Pod模板必须要`RestartPolicy: Always(默认)`。

- Pod Selector

- 仅在某些节点上运行Pod
如果指定了`.spec.template.spce.nodeSelector`，则守护进程控制器将在`node selector`匹配的节点上创建Pod。同样，如果指定了`.spec.template.spec.affinity`，则守护进程控制器将在与该节点关联匹配的节点上创建Pod。
如果未指定任何一个，则守护进程控制器将在所有节点上创建Pod。

<br>

**Daemon Pods如何调度**

- 由守护进程集控制器调度（默认）
通常，Pod运行的机器由k8s调度程序选择。然而，由守护进程集控制器创建的Pod已经选择了机器(`.spec.nodeName`)。

- 由默认调度器调度
功能阶段： k8s v1.11 `alpha`
守护进程集确保所有符合条件的节点都运行Pod的副本。

- Taints and Tolerations

<br>

**Daemon Pods间通信**
守护进程集中Pod通信的一些可能模式：

- Push
- NodeIP and Known Port
- DNS
- Service

<br>

**更新DaemonSet**
如果更改了节点标签，守护进程集会立即将Pod添加到新匹配的节点，并从新匹配的节点中删除Pod。
可以修改守护进程集创建的Pod。然而，Pod不允许更新所有字段。同样，守护进程集控制器在下次创建节点时使用原始模板。
你也可以删除守护进程集，若指定了`--cascade=false`，则会在节点上保留Pod。

<br>

**守护进程集的替代方案**

- Init Scripts
- Bare Pods
- Static Pods
- Deployments


<br/>
<br/>


#### 垃圾回收

Garbage Collection

k8s垃圾回收的作用是删除曾经拥有所有者，但不再拥有所有者的某些对象。

<br>

**Owners and dependents**
一些k8s对象是其它对象的所有者。如副本集是一组Pod的所有者。拥有的对象称为所有者的依赖项(dependents)。每个依赖对象都有一个`metadata.ownerReferences`字段来指向所有者。

<br>

**控制垃圾回收器如何删除依赖项**
删除对象时，可以指定是否也自动删除对象的依赖项。
删除对象而不自动删除依赖项，则称依赖项为孤立对象(orphaned)。
自动删除依赖项被称为级联删除(cascading deletion)，这有两种级联删除模式：

- Foreground
- Background

<br>

**设置级联删除策略**
删除对象时，设置`deleteOptions`参数的`propagationPolicy`字段来控制级联删除策略。


<br/>
<br/>


#### Jobs

Jobs - Run to Completion

作业创建一个或多个Pod，并确保指定数量的Pod成功终止。随着Pod成功完成，作业跟踪也成功完成。删除作业将清除它创建的Pod。
作业还可用于并行运行多个Pod。

<br>

**栗子**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: pi
spec:
  template:
    spec:
      containers:
      - name: pi
        image: perl
        command: ["perl",  "-Mbignum=bpi", "-wle", "print bpi(2000)"]
      restartPolicy: Never
  backoffLimit: 4
```

```
kubectl create -f ./job.yaml
job.batch/pi created


kubectl get job
kubectl describe job/pi
kubectl get pod

kubectl logs pi-xxx
```

<br>

**Job Spec**
与其它k8s配置一样，Job也需要`apiVersion`, `kind`, `metadata`, `.spec`字段。

- Pod Template
`.spec.template`是`.spce`字段的必要项。

- Pod Selector
`.spec.selector`字段可选。

- Parallel Jobs: 有三种主要类型作业
	+ Non-parallel Jobs
		+ 通常指启动一个Pod，除非Pod失败
		+ Pod成功终止后，作业即告完成
	+ Parallel Jobs with a fixed completion count
		+ 为`.spec.completions`指定非零正值
		+ 当1-`.spec.completions`范围内的每个值都有一个成功的Pod时，作业就完成了
		+ 尚未实施，每个Pod都传递了1-`.spec.completions`范围内不同的索引
	+ Parallel Jobs with a work queue
		+ 每个Pod独立地确定是否所有对等都完成，因此整个Job完成
		+ 当任何Pod成功终止，不会创建新的Pod
		+ 一旦至少一个Pod成功终止并且所有Pod终止，则作业成功完成
		+ 一旦任意Pod已成功退出，其它任何Pod都不应该做任何工作或输出

**控制并行**
Controlling Parallelism

请求的并行性(`.spec.parallelism`)可以设置为任何非负值。如果未指定，则默认为1.如果指定为0，则作业将暂停，直至其增加。
由于各种原因，实际并行性(在任何时刻运行的Pod数量)可能多于或少于请求的并行度：

- 对于固定完成计数的作业，并行运行的实际Pod数不会超过剩余的Pod数
- 对于工作多列作业，任何Pod成功后都不会启动新的Pod，但允许剩余的Pod完成
- 如果控制器没有时间做出反应
- 如果控制器因任何原因无法创建Pod
- 由于同一作业中过多的先前Pod故障，控制器可能会限制新的Pod创建
- 当Pod正常关闭时，停止需要一些时间

<br>

**处理Pod和Container失败**
Pod中的容器可能由于多种原因而失败，如果发生此情况，并且`.spec.template.spec.restartPolicy = "OnFailure"`，那么Pod会留在节点上，但容器会重新运行。因此，你的程序需要在本地处理此情况，或指定`.spec.template.spec.restartPolicy = "Never"`。

一个完整的Pod也可能由于多种原因而失败。当Pod失败时，作业控制器启动一个新的Pod。因此，你的程序需要在新Pod重启时处理此情况。

<br>

**Pod Backoff failure policy**
在某些情况下，由于配置中的逻辑错误等原因，你需要在重试一段时间后使作业失败。为此，可设置`.spec.backoffLimit`将作为视为失败前的重试次数。默认值为6s。与作业关联的失败的Pod由作业控制器重新创建，指数退避延迟(10s, 20s, 40s...)，上限6分钟。如果在作业的下一次状态检查之前没有出现新的故障Pod，则重置退避计数。

<br>

**作业终止和清理**
Job Termination and Cleanup

作业完成后，不会再创建Pod，也不会删除Pod。保持它们可让你仍然能查看已完成的Pod的日志以检查error, warning, 或其它诊断性输出。作业对象在完成后也会保留，以便可查看其状态。在注意到其状态后，用户可删除旧的作业。

```
#一并删除作业创建的Pod
kubectl delete jobs/xxx

#不删除作业创建的Pod
kubectl delete jobs/xxx --
```

默认情况下，除非Pod失败，否则作业将不间断运行，此时作业将延迟到上述的`.spec.backoffLimit`。终止作业的另一种方法是设置活动截止日期，通过设置`.spec.activateDeadlineSeconds`字段来执行此操作。请注意，作业的`.spec.activateDeadlineSeconds`优先于`.spec.backoffLimit`。因此，重试一个或多个失败的Pod的作业在达到`activeDeadlineSeconds`指定的时间限制后将不会重置其它Pod，即使尚未达到`backoffLimit`也是如此。

<br>

**作业模式**
Job Patterns

作业对象可用于支持Pod的可靠并行执行，它不是为了支持紧密通信的并行进程而设计。
在复杂系统中，可能存在多组不同的工作项。这里只考虑一组工作项——批处理作业

并行计算有几种不同的模式，每种模式都有有点和缺点：

- 一个工作项一个作业对象 vs 所有工作项一个作业对象
- 创建的Pod数等于工作项数 vs 每个Pod可以处理多个工作项
- 多个方法使用一个工作队列

<br>

**高级用法**
Advanced Usage

- 指定自己的Pod selector
通常，创建作业对象时，不会指定`.spec.selector`。系统默认在创建作业时添加此字段。然而，在某些情况下，你可能需要设置它。这样做的时候要非常小心，如果你指定的label selector不是该作业的Pod所独有，并且与不想关的Pod匹配，则可能会删除不相关作业的Pod。如果选择了non-unique selector，则其它控制器及其Pod也可能以不可预测的方式进行。在指定`.spec.selector`时，k8s不会阻止你犯错误。

<br>

**替代方案**
Alternatives

- Bare Pods
- Replication Controller
- Single Job starts Controller Pod

<br>

**Cron Jobs**
在指定的时间/日期创建作业。



<br/>
<br/>


#### CronJob

Cron Job基于时间调度创建作业。
一个定时任务对象类似于crontab中的一行。它以给定的时间周期性运行作业。

**注意： 所有定时作业调度， 时间以UTC表示。**

<br>

**定时作业局限**
Cron Job Limitations

定时作业在其计划的每个执行时间创建一个作业对象。
如果`startingDeadlineSeconds`被设置为较大值或未设置(默认值)，并且`concurrencyPolicy`设置为Allow，则作业将始终至少运行一次。
如果设置了`startDeadlineSeconds`字段，则控制器会计算从`startingDeadlineSeconds`的值到现在发生的错过的作业数，而不是从上一个计划时间到现在。
如果定时作业未能在其预定时间创建，则将其视为未命中。

定时作业仅负责创建与其计划相匹配的作业，而作业则负责管理它所代表的Pod。



<br/>
<br/>
<br/>



## 配置

Configuration


<br/>


### 配置最佳实践

Configuration Best Practices


<br>


#### 一般配置技巧

General Configuration Tips

- 定义配置时，请指定最新的稳定的API版本
- 在推送到集群之前，配置文件应存储在版本控制系统中。这允许你在必要时快速回滚配置，有助于集群重建和恢复
- 使用YMAL而不是JSON来编写配置文件，YAML格式更用户友好
- 只要有意义，就将相关对象分组到一个文件中。管理一个文件比管理一堆文件更便捷
- 可以在目录上调用许多`kubectl`命令。例如，你可在配置文件目录上调用`kubectl create`
- 不要不必要地指定默认值
- 将对象描述写在注释中，以便更好进行内省


<br/>
<br/>


#### Naked Pod vs 副本集，部署和作业

“Naked” Pods vs ReplicaSets, Deployments, and Jobs

- 不要使用Naked Pods(即未绑定到副本集或部署的Pod)
如果节点发生故障，裸Pod将不会被重新调度。


<br/>
<br/>


#### 服务

Service

- 在相应的后端工作负载(部署或副本集)访问它之前创建服务
当k8s启动容器时，它提供指向启动容器时正在运行的所有服务的环境变量。

- 除非绝对必要，否则不要为Pod指定hostPort
将Pod绑定到hostPort时，它会限制Pod可调度的位置数。因为每个`hostIP, hostPort, protocol`的组合必须是独特的。如果没有指定hostIp和protocol，k8s将使用`0.0.0.0`作为默认的hostIP，使用TCP作为默认协议。

如果你只需要访问端口以进行调试，可使用`apiserver proxy`或`kubectl port-forward`。
如果你需要公开节点上Pod的端口，考虑使用`NodePort`服务。

- 避免使用hostNetwork， 原因与hostPort类似
- 当不需要`kube-proxy`负载均衡时，使用 headless Services可轻松服务发现


<br/>
<br/>


#### 使用标签

Using Labels

- 为你的应用程序或部署定义和使用标签
你可使用这些标签为其它资源筛选合适的Pod


<br/>
<br/>


#### 容器镜像

Container Images

- 默认的镜像拉取策略。对于容器是`ifNotPresent`，kubelet只有在本地镜像不存在时才拉取镜像。如果希望每次k8s启动容器时都拉取镜像，请指定`imagePullPolicy: Always`。
一个已弃用的替代方案。设置k8s总是拉取镜像的`:latest`标记，它会隐式地将`imagePullPolicy`设置为`Always`。

**注意： 在生产环境中部署容器时，你应该避免使用`:latest`标记，因为这使得正在运行的镜像版本难以回滚。**
如果镜像使用`:latest`标记，回滚的话其实需要回滚代码，然后打包上线，然后触发动态更新，之后就还原成了之前的版本。这样确实要复杂很缓慢一些。

- 确保容器使用使用相同版本的镜像


<br/>
<br/>


#### 使用kubectl

- 使用`kubectl apply -f <directory>` 或 `kubectl create -f <directory>`
它在此目录中所有`.yaml`, `.yml`, `.json`文件汇总寻找k8s配置配置文件，并将其传递给kubectl。

- 使用label selectors进行`get`和`delete`操作，而不是特定的对象名称
- 使用`kubectl run`和`kubectl expose`快速创建单容器部署和服务



<br/>
<br/>



### 管理容器的计算资源

Managing Compute Resources for Containers


指定Pod时，可以选择指定每个容器需要多少CPU和MEM。当容器指定了请求(requests)的资源时，调度器可以更好地决定将Pod放在哪个节点上。当容器指定了限制(limit)时，可以以指定的方式处理节点上资源的争用。


<br/>
<br/>


#### 资源类型

Resource types

CPU和MEM都是资源类型。资源类型具有基本单元(unix)。CPU以核(`cores`)为指定单位，MEM以字节(`Byte`)为指定单位。
CPU和MEM统称为计算资源，或资源。计算资源是可以请求，分配和使用的可测量数据。它们与API资源不同。API资源(如Pod和Service)，是可通过k8s APIserver读取和修改的对象。


<br/>
<br/>


#### 资源的请求和限制

Resource requests and limits of Pod and Container

Pod中的容器都可指定一个或多个限制：

- `spec.containers[].resources.limits.cpu`
- `spec.containers[].resources.limits.memory`
- `spec.containers[].resources.requests.cpu`
- `spec.containers[].resources.requests.memory`

虽然只能在单独的容器上指定请求和限制，但是讨论Pod资源的请求和限制很方便。特定资源类型的Pod资源 请求/限制 是Pod中每个容器的该类型的资源 请求/限制 的总和。


<br/>
<br/>


#### CPU

Meaning of CPU

CPU资源的限制和请求以CPU单位进行测量。在k8s中，1 cpu等于：

- 1 AWS vCPU
- 1 GCP Core
- 1 Azure vCore
- 1 IBM vCPU
- 1 Hyperthread on a bare-metal Intel processor with Hyperthreading

允许分数请求。如`spec.containers[].resources.requests.cpu: 0.5`。表达式`0.1`相当于表达式`100m`。具有小数点的请求资源(如`0.1`)由API转换为`100m`，不允许精度小于`1m`。
始终要求CPU作为绝对数量，而不是相对数量。因此，`0.1`单元对于单核，双核，八核机器上的CPU资源时相同的。


<br/>
<br/>


#### Memory

Meaning of memory

内存的限制和请求以字节为单位。
你可使用以下后缀来表示整数内存: `E, P, T, G, M, K`；
你还还可以使用2的幂等: `Ei, Pi, Ti, Gi, Mi, Ki`。

```
#相同值的不同表达
128974848
129e6
129M
123Mi
```

栗子：

```
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: db
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: "password"
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
  - name: wp
    image: wordpress
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
```


<br/>
<br/>


#### 如何调度具有资源请求的Pod

How Pods with resource requests are scheduled

创建Pod时，k8s调度器会选择要运行Pod的节点。每个节点都具有每种资源类型的最大容量，它可为Pod提供CPU和MEM。调度程序确保对于每种资源类型，调度的容器的资源请求总和小于节点的容量。请注意，即使节点上的实际内存或CPU资源使用率非常低，但如果容量检查失败，调度器扔拒绝在节点上放置Pod。当资源使用随后增加时，这可以防止节点上的资源短缺。


<br/>
<br/>


#### 如何运行具有资源限制的Pod

How Pods with resource limits are run

当`kubelet`启动Pod中的容器时，它会将CPU和MEM限制传递给容器运行环境。

当使用Docker时：

- `spec.container[].resources.requests.cpu`被转换成core value，分数的话会乘以1024。此数字中的较大值用作`docker run`命令中`--cpu-shares`标志的值

- `spec.container[].resources.limits.cpu`被转换为millicore value并乘以100。结果值代表容器每100ms可以使用的CPU时间总量。
在此间隔期间，容器不能使用超过其CPU时间的份额。
默认配额时间是100ms，CPU配额的最小解析为1ms。


- `spec.containers[].resources.limits.memory`被转换为整数，并用作`docker run`命令中`--memory`标志的值

如果容器超出其内存限制(mem limit)，则容器可能会终止。如果它可以重启，则kubelet将重启它；
如果容器超出其内存请求(mem request)，当节点内存不足时，它的Pod可能会被驱逐；
容器可能会/可能不会被允许在较长时间内超过其CPU限制。但是，它不会因CPU使用率过高而被杀死。


<br/>
<br/>


#### 监控计算资源使用

Monitoring compute resource usage

Pod的资源使用情况将作为Pod Status的一部分进行上报。


<br/>
<br/>


#### 本地短暂存储

Local ephemeral storage

FEATURE STATE: Kubernetes v1.11 beta

k8s v1.8介绍了一种新资源，用于管理本地短暂存储的短暂存储(ephemeral-storage)。在每个k8s 节点上，kubelet的根目录(默认`/var/lib/kubelet`)和日志目录(`/var/log`)存储在节点的根分区上。Pod还通过`emptyDir volume`，容器日志，镜像层，容器可写层共享和使用此分区。
此分区是短暂的，应用程序不能指望来自此分区的任何SLA(如磁盘IO)。本地临时存储仅适用于根分区，镜像层和可写层的可选分区超出了范围。

<br>

**本地短暂存储的请求和限制设置**
Requests and limits setting for local ephemeral storage

Pod中的容器可指定一个或多个短暂存储：

- `spec.containers[].resources.limits.ephemeral-storage`
- `spec.containers[].resources.requests.ephemeral-storage`

短暂存储的限制和请求以字节(`Byte`)为单位。
你可以使用一下后缀表示整数存储: `E, P, T, G, M, K`；
你也可以使用2的幂等: `Ei, Pi, Ti, Gi, Mi, Ki`。

```
128974848
129e6
129M
123Mi
```

<br>

栗子： Pod由两个容器，每个容器都有2GiB的本地短暂存储请求，4GiB的本地短暂存储限制。因此，总共是4GiB请求，8GiB限制。

```
apiVersion: v1
kind: Pod
metadata:
  name: frontend
spec:
  containers:
  - name: db
    image: mysql
    env:
    - name: MYSQL_ROOT_PASSWORD
      value: "password"
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
  - name: wp
    image: wordpress
    resources:
      requests:
        ephemeral-storage: "2Gi"
      limits:
        ephemeral-storage: "4Gi"
```

<br>

**如何调度具有本地短暂存储的Pod**
How Pods with ephemeral-storage requests are scheduled

对于容器级的隔离，如果容器的可写层和日志使用量超过其存储限制，则Pod将被驱逐。对于Pod级别的隔离，如果所有容器的本地短暂存储使用量与Pod的`emptyDir volume`的总和超过了限制，则Pod将被驱逐。


<br/>
<br/>


#### 扩展的资源

Extended resources

扩展资源是`kubernetes.io`域之外的完全限定资源名称。它们允许集群操作者通告和用户使用非k8s内置资源。
使用扩展资源需要两个步骤，首先，集群操作者必须通告扩展资源；其次，用户必须在Pod中请求扩展资源。

<br>

**节点级扩展资源**
节点级扩展资源与节点相关联。

<br>

**集群级扩展资源**
集群级扩展资源不依赖与节点。它们通常由调度器扩展程序管理——它处理资源消耗和资源配额。

<br>

**使用扩展资源**
用户可以在`pod spec`中项CPU和MEM一样使用扩展资源。调度程序负责资源核算，以便不会同时为Pod分配可用的数量。
API server将扩展资源的数量限制为整数。

要在Pod中使用扩展资源，在`container spec`中的`spec.container[].resources.limits`映射中包含资源名称作为键。
只有满足所有请求资源时，才会调度Pod。只要无法满足资源请求，Pod就会保持在`PENDING status`。

```
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: my-container
    image: myimage
    resources:
      requests:
        cpu: 2
        example.com/foo: 1
      limits:
        example.com/foo: 1
```


<br/>
<br/>


### 分配Pod到节点

Assigning Pods to Nodes


你可以将Pod约束为只能在特定节点上运行，或更喜欢在特定节点上运行。有几种方法做到这一点，它们都使用`label selector`来进行选择。通常这种约束是不必要的，因为调度程序将自动进行合理的放置。但在某些情况下，你可能希望对Pod放置的节点进行更多控制。如确保Pod放置在安装有SSD的计算机上...


<br/>
<br/>


#### 节点选择器

nodeSelector

节点选择器是最简单的约束形式。`nodeSelector`是`PodSpecs`的一个字段，它指定了一个键值对的映射。要使Pod有资格在节点上运行，该节点必须将每个指示的的键值对作为标签。最常见的用法是一个键值对。

- Prerequisites
k8s 集群

- Attach label to the node

```
#获取节点名
kubectl get node
NAME      STATUS    ROLES     AGE       VERSION
master    Ready     master    33d       v1.11.1
node      Ready     <none>    33d       v1.11.1
salt01    Ready     <none>    27d       v1.11.1


#打标签
kubectl label nodes <node-name> <label-key>=<label-value>

#查看标签
kubectl get node --show-labels
```

- Add a nodeSelector field to your pod configuration

```
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    <label-key>: <label-value>
```

当创建这个资源时，Pod将调度到附加此标签的节点上。


<br/>
<br/>


#### 内置节点标签

built-in node labels

除了你附加的标签之外，节点还有一些预先填充的标准标签。

- `kubernetes.io/hostname`
- `failure-domain.beta.kubernetes.io/zone`
- `failure-domain.beta.kubernetes.io/region`
- `beta.kubernetes.io/instance-type`
- `beta.kubernetes.io/os`
- `beta.kubernetes.io/arch`


<br/>
<br/>


#### 亲和力和反亲和力

Affinity and anti-affinity

节点选择器提供了一种非常简单的方法，使用特定标签约束Pod到特定节点。目前处于测试阶段的亲和力/反亲和力功能，极大地扩展了你可以表达的约束类型。关键的改进有：

- 语言更具表达性
- 你可以指示规则是`soft/preference`而不是硬性要求，因此如果调度程序不能满足，也仍然会调度Pod
- 你可以约束运行在节点上的其它Pod的标签，而不是对节点本身的标签进行约束

亲和力有两种类型：

- node-affinity
- inter-pod affinity/anti-affinity

<br>

**节点亲和力**
节点亲和力在概念上类似于nodeSelector，它允许你根据节点标签约束pod调度的节点。
目前有两种类型的节点亲和力：

- `requiredDuringSchedulingIgnoredDuringExecution`
- `preferredDuringSchedulingIgnoredDuringExecution`

你可将它们分别是为`hard`和`soft`，前者指定了将Pod调度到节点上必须满足的规则，后者指定调度程序将尝试执行但不保证的首选项。名称的`IgnoredDuringExecution`部分意味着，与节点选择器的工作方式类似，如果节点标签在运行时更改，而不再满足Pod的亲和力规则，则Pod将继续在节点上运行。
未来，我们计划提供`requiredDuringSchedulingRequiredDuringExecution`，就像Ignored一样，它将从不再满足Pod的亲和力要求的节点中驱逐Pod。

节点亲和力在`spec.affinity.nodeAffinity`字段中指定：

```
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/e2e-az-name
            operator: In
            values:
            - e2e-az1
            - e2e-az2
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
  containers:
  - name: with-node-affinity
    image: k8s.gcr.io/pause:2.0
```

此节点亲和力规则表示，Pod只能防止在`kubernetes.io/e2e-az-name`标签键，值为`e2e-az1`或`e2e-az2`的节点上。此外，在满足条件的节点中，应优先选择具有`another-node-label-key`键，值为`another-node-label-value`的节点。
节点亲和力语法支持如下操作符: `In, NotIn, Exists, DoesNotExist, Gt, Lt`。

如果你同时指定了`nodeSelector`和`nodeAffinity`，则必须满足两者以将Pod调度到候选节点上；
如果你指定了与`nodeAffinity`类型关联的多个`nodeSelectorTerms`。那么，如果满足其中一个`nodeSelectorTerms`，则可以将Pod调度到节点上；
如果你指定了与`nodeSelectorTerms`关联的多个`matchExpressions`。那么，只有满足所有`matchExpressions`的情况下，才能将Pod安排到节点上；
如果删除或更改调度Pod的节点标签，则Pod不会被删除。换句话说，亲和力仅在调度Pod时起作用。

<br>

**Pod间亲和力和反亲和力**
Pod间亲和力和反亲和力，你可以根据已在节点上运行的Pod上的标签(而不是节点标签)，来约束Pod可以调度的节点。与节点不同，Pod有命名空间，Pod标签的标签选择器必须指定选择器应该应用于哪些命名空间。

注意： Pod间亲和力和反亲和力需要大量的处理，可会显著减慢大型集群中的调度。因此，不建议在大于几百个节点的集群中使用；
注意： Pod反亲和力要求节点一致地标签节点，即集群中的每个节点都必须具有匹配的`topologyKey`标签，如果某些节点缺少，可能会导致意外情况。

目前有两种类型的Pod亲和力和反亲和力:

- `requiredDuringSchedulingIgnoredDuringExecution`
- `preferredDuringSchedulingIgnoredDuringExecution`

同样表示`hard`和`soft`要求。

```
apiVersion: v1
kind: Pod
metadata:
  name: with-pod-affinity
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
          - key: security
            operator: In
            values:
            - S1
        topologyKey: failure-domain.beta.kubernetes.io/zone
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: security
              operator: In
              values:
              - S2
          topologyKey: kubernetes.io/hostname
  containers:
  - name: with-pod-affinity
    image: k8s.gcr.io/pause:2.0
```

Pod亲和力和反亲和力的有效操作符有: `In, NotIn, Exists, DoesNotExist`
原则上，`topologyKey`可以是任一合法的`label-key`。但是，出于性能和安全的原因，它也有一些限制：

- 对于亲和力和`requiredDuringSchedulingIgnoredDuringExecution`的Pod的反亲和力，不允许使用空的`topologykey`
- 对于`requiredDuringSchedulingIgnoredDuringExecution`的Pod的反亲和力，引入控制器`LimitPodHardAntiAffinityTopology`是为了将`topologyKey`限制为`kubernetes.io/hostname`。如果要使其可用于自定义，可修改控制器，或禁用它
- 对于`preferredDuringSchedulingIgnoredDuringExecution`的Pod的反亲和力，空的`topologyKey`被解释为`all topologies`
- 除了上面提到的，`topologyKey`可以是任一合法的`label-key`

除了`labelSelector`和`topologyKey`之外，你还可以选择指定`labelSelector`应匹配的命名空间。如果为空或省略，则默认为Pod的亲和力/反亲和力的命名空间。



<br/>
<br/>



### 污点和容忍

Taints and Tolerations


节点亲和力是Pod的属性，它将它们吸引到节点；Taints则相反——它允许节点排斥Pod。
Taints 和 Tolerations 一起工作以确保Pod不被安排的不适当的节点上。将一个或多个污点(taints)应用于节点，这标志着节点不应该接受任何不能容忍污点的Pod。容忍(tolerations)应用于Pod，并允许Pod安排到具有匹配污点的节点上。


























<br/>
<br/>
<br/>



## 服务，负载均衡和网络

Services, Load Balancing, and Networking













<br/>
<br/>
<br/>



## 存储

Storage


<br/>
<br/>


### Volumes

容器中的磁盘文件是短暂的，这在容器中运行时会给重大的应用程序带来一些问题。首先，当一个容器奔溃时，kubelet将重启它，但文件会丢失，容器将以干净的状态启动。其次，在Pod中一起运行容器时，通常需要在这些容器间共享文件。k8s volume抽象解决这些问题。


<br/>
<br/>


#### Background

Docker也有关于卷的概念，虽然它有点宽松和管理较少。在Docker中，卷是磁盘上或其它容器中的目录，声明周期不受管理。Docker提供了卷驱动，但目前功能非常有限。

另一方面，k8s的卷具有明确的生命周期。因此，卷可以比Pod中运行的任何容器活得更久，并且可在容器重启之间保留数据。当然，当Pod不再存在时，卷也将不复存在。更重要的是，k8s支持多种类型的卷，Pod可以同时使用任意数量的卷。
从本质上讲，卷只是一个目录，可能包含一些数据，Pod中的容器可以访问它。该目录如何形成，支持它的介质以及它的内容都由所用特定卷的类型决定。
要使用卷，Pod Spec要指定提供的卷(`.spec.volumes`字段)，以及将这些卷挂载到容器中的位置(`.spec.containers.volumeMounts`字段)。

容器中的进程可以看到由Docker镜像和卷组成的文件系统视图。Docker镜像位于文件系统层次结构的根下，任何卷都挂载到镜像中的指定路径。卷不能挂载到其它卷或其它卷的硬链接上，Pod中的每个容器必须独立的指定每个卷的挂载位置。


<br/>
<br/>


#### 卷类型

k8s支持如下卷类型：

- awsElasticBlockStore
- azureDisk
- azureFile
- cephfs
- configMap
- csi
- downwardAPI
- emptyDir
- fc (fibre channel)
- flocker
- gcePersistentDisk
- gitRepo (deprecated)
- glusterfs
- hostPath
- iscsi
- local
- nfs
- persistentVolumeClaim
- projected
- portworxVolume
- quobyte
- rbd
- scaleIO
- secret
- storageos
- vsphereVolume

具体例子请参考: <https://kubernetes.io/docs/concepts/storage/volumes/#types-of-volumes>


<br/>
<br/>


#### 使用子路径

Using subPath

有时，在单个Pod中共享一个卷用于多个用途是很有用的。`volumeMounts.subPath`属性可用于指定引用卷内的子路径，而不是根路径。

使用单个共享卷的Pod与LAMP Stack的示例，HTML内容被映射到html目录中，数据库存储在mysql目录中：

```
apiVersion: v1
kind: Pod
metadata:
  name: my-lamp-site
spec:
    containers:
    - name: mysql
      image: mysql
      env:
      - name: MYSQL_ROOT_PASSWORD
        value: "rootpasswd" 
      volumeMounts:
      - mountPath: /var/lib/mysql
        name: site-data
        subPath: mysql
    - name: php
      image: php:7.0-apache
      volumeMounts:
      - mountPath: /var/www/html
        name: site-data
        subPath: html
    volumes:
    - name: site-data
      persistentVolumeClaim:
        claimName: my-lamp-site-data
```

<br>

**使用带有扩展环境变量的子路径**
Using subPath with expanded environment variables

FEATURE STATE: `k8s v1.11 alpha`

`subPath`目录名也可从Downward API环境变量构造。在使用此功能之前，必须启用`VolumeSubpathEnvExpansion`。
下例中，Pod使用`subPath`在主机路径卷`/var/log/pods`中创建`pod1`目录，使用Downward API中的Pod名。主机目录`/var/log/pods/pod1`被挂载到容器中的`/logs`目录。

```
apiVersion: v1
kind: Pod
metadata:
  name: pod1
spec:
  containers:
  - name: container1
    env:
    - name: POD_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.name
    image: busybox
    command: [ "sh", "-c", "while [ true ]; do echo 'Hello'; sleep 10; done | tee -a /logs/hello.txt" ]
    volumeMounts:
    - name: workdir1
      mountPath: /logs
      subPath: $(POD_NAME)
  restartPolicy: Never
  volumes:
  - name: workdir1
    hostPath:
      path: /var/log/pods
```


<br/>
<br/>


#### 资源

`emptyDir`卷的存储介质(磁盘，SSD...)由kubelet根目录的文件系统的介质确定。`emptyDir`或`hostPath`卷可以占用多少空间没有限制，容器之间或Pod之间没有隔离。


<br/>
<br/>


####挂载传播

Mount propagation

FEATURE STATE: `k8s v1.10 beta`

挂载传播允许将容器挂载的卷共享到同一Pod的其它容器，或同一节点的其它Pod。
如果`MountPropagation`功能被禁用，或Pod未指明特定的挂载环境，则不会传播Pod的容器中的挂载卷。
卷的挂载传播由`Container.volumeMounts`中的`mountPropagation`字段控制。它的值为：

- `None`
此卷的挂载不会接收主机挂载到此卷或任何子目录的任何后续挂载。此模式等同于于Linux kernel中描述的`private`挂载传播。

- `HostToContainer`
此卷的挂载将接收安装到此卷或其任何子目录的所有后续挂载。换句话说，如果主机在卷挂载中挂载任何内容，则容器将看到它挂载在那里。
类似地，如果任何具有双向挂载传播的Pod挂载到同一个卷中，那么具有`HostToContainer`挂载传播的容器将看到它。此模式等同于Linux Kernel中描述的`rslave`挂载传播。

- `Bidirectional`
此卷的挂载行为与`HostToContainer`相同。此外，容器创建的所有卷 挂载都将传播会主机和所有使用相同卷的Pod中的容器。此模式等同于Linux kernel中描述的`rshared`挂载传播。

<br>

**配置**
在挂载传播可以在某些部署上正常工作之前，必须在Docker中正确配置挂载共享，修改`docker systemd`服务文件，设置`MountFlags`：

```
MountFlags=shared
```

重启Docker：

```
systemctl daemon-reload
systemctl restart docker
```



<br/>
<br/>



### 持久化卷

Persistent Volumes






























<br/>
<br/>
<br/>



## 垃圾收集


Kubernetes 垃圾收集器的角色是删除指定的对象，这些对象曾经有但以后不再拥有 Owner 了。

某些Kubernetes对象是其它一些对象的Owner。如，一个副本集是一组pod的Owner。
具有Owner的对象被称为是Owner的**Dependent**。每个Dependent对象具有一个执行所属对象的`metadata.ownerReference`字段。

有时，Kubernetes会自动设置`ownerReference`的值。
也可以手动设置`ownerReference`的值，来指定Owner和Dependent之间的关系。

<br>

**控制垃圾收集器删除Dependent**

- 级联删除
	+ background
	+ foreground
删除对象时自动删除Dependent。
在bg级联删除模式下，k8s会立即删除Owner对象，然后垃圾收集器会在后台删除这些Dependent。
在fg级联删除模式下，根对象首先进入删除中状态。一旦对象被设置为删除中状态，垃圾收集器会删除对象的所有Dependent。

- 孤儿
删除对象时，不自动删除它的Dependent。这些Dependent就被称作孤儿。垃圾收集器在删除了所有 “Blocking” 状态的 Dependent（对象的 ownerReference.blockOwnerDeletion=true）之后，它会删除 Owner 对象。










<br/>
<br/>

---

<br/>




# 教程

Tutorials


教程展示了如何实现比单个任务更大的目标(task)。


<br/>


## k8s基本


<br/>


### 综述


本教程提供了Kubernetes集群编排系统基础知识的介绍。

你将学到：

- 在集群上部署容器化服务
- 伸缩部署
- 使用新软件版本更新容器化应用程序
- 调试容器化应用程序

<br>

**k8s能为你做什么？**
容器化有助于打包软件以实现这些目标，是应用程序能够以简单快速的方式发布和更新，而无需停机。k8s可帮助你确保这些容器化应用程序随时随地运行，并帮助它们找到运行所需的资源。

<br>

**k8s 基础模块**

1. 创建(create)一个k8s集群
2. 部署(deploy)应用程序
3. 探索(explore)应用程序
4. 公开(expose)展示应用程序
5. 伸缩(scale)应用程序
6. 升级(update)应用程序


<br/>
<br/>


### 创建集群

Create a Cluseter

详情见安装部分。


<br/>
<br/>



### 部署应用程序

Deploy an APP


<br/>


#### 使用kubectl创建部署

Using kubectl to create a Deployment


目标：

- 了解应用程序部署
- 在k8s上使用`kubectl`部署你的第一个应用程序

<br>

**k8s Deployments**
一旦运行了k8s集群，就可在其上部署容器化应用程序。为此，你需要创建Kubernetes Deployment configuration。它指示k8s 如何创建和更新应用程序实例。创建部署后，k8s master将应用程序实例调度到各个node上。
创建应用程序实例后，Kubernetes Deployment Controller会持续监控这些实例。如果主机节点上的实例关闭或删除，Deployment Controller会替换它。这提供了一种自我修复(self-healing)机制来解决机器故障或维护。

<br>

**部署应用程序**
可使用`kubectl`(使用k8s api与集群交互)来创建和管理Deployment。下面有一些关于使用kubectl在k8s集群上创建和管理Deployment的基础命令。

创建部署时，你需要指定应用程序的容器镜像(image)，以及要运行的副本数(replicas)。你可在以后改变这些信息来更新你的部署。

栗子：
第一个部署，k8s使用一个Docker容器的`Node.js`应用程序包。

```
kubectl version
#client
#server

kubectl get nodes

#创建名为k8s-bootcamp的deployment
kubectl run kubernetes-bootcamp --image=gcr.io/google-samples/kubernetes-bootcamp:v1 --port=8080
#这是国内镜像: docker.io/jocatalin/kubernetes-bootcamp:v1

kubectl get deployments
NAME           DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubenetes-bootcamp   1         1        1           1          1h
#表示 希望副本数，当前副本数，最新副本数，可用副本数


#由于pod被封装在集群私网，没有对外开放
#proxy将通信转发到集群内私网
kubectl proxy
curl http://localhost:8081/version
curl http://localhost:8001/api/v1/namespaces/default/pods/$POD_NAME/proxy/
#Hello Kubernetes bootcamp!
```

此处我遇到一个错误，`replicats unavailable`:
原因是拉取的镜像在谷歌云上，无法访问<gcr.io>，拉取失败所以导致部署失败。
gcr(google container Registry)

```
#查看部署信息
 kubectl get deployment kubernetes-bootcamp -o yaml
    message: 'unable to create pods: No API token found for service account "default",
      retry after the token is automatically created and added to the service account'
    reason: FailedCreate
    status: "True"
    type: ReplicaFailure



kubectl get deployments
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   1         0         0            0           33m


kubectl describe deployments kubernetes-bootcamp
Replicas:               1 desired | 0 updated | 0 total | 0 available | 1 unavailable
StrategyType:           RollingUpdate
ReplicaFailure   True    FailedCreate
```

针对**unable to create pods: No API token found for service account "default"**这个问题，需要修改kube-apiserver配置文件：

```
#去掉 KUBE_ADMISSION_CONTROL中的SecurityContextDeny,ServiceAccount
KUBE_ADMISSION_CONTROL="--admission-control=NamespaceLifecycle,NamespaceExists,LimitRanger,ResourceQuota"


#重启kube-apiserver
systemctl restart kube-apiserver

#之后查看副本数就正常了
kubectl get deployments
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   1         1         1            0           8m


#这里available还是0
kubectl get pods
NAME                                  READY     STATUS              RESTARTS   AGE
kubernetes-bootcamp-390780338-6x48n   0/1       ContainerCreating   0          21h
#pod处于创建状态

#查看详情
kubectl describe pods
#错误信息
  Warning  FailedSync  4m (x258 over 21h)   kubelet, 192.168.31.159  Error syncing pod, skipping: failed to "StartContainer" for "POD" with ErrImagePull: "image pull failed for registry.access.redhat.com/rhel7/pod-infrastructure:latest, this may be because there are no credentials on this request.  details: (open /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt: no such file or directory)"
  Warning  FailedSync  9s (x5728 over 21h)  kubelet, 192.168.31.159  Error syncing pod, skipping: failed to "StartContainer" for "POD" with ImagePullBackOff: "Back-off pulling image \"registry.access.redhat.com/rhel7/pod-infrastructure:latest\""

#在node上查看此文件，发现它指向了一个空链接
#并不存在/etc/rhsm目录
ll /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt
lrwxrwxrwx. 1 root root 27 7月  16 16:58 /etc/docker/certs.d/registry.access.redhat.com/redhat-ca.crt -> /etc/rhsm/ca/redhat-uep.pem

#在node安装此rhsm
yum search rhsm
#python-rhsm-certificates.x86_64
#python-rhsm.x86_64
yum install -y python-rhsm.x86_64 python-rhsm-certificates.x86_64
#之后在node上手动拉取下image便可看到pod正常运行
```



<br/>
<br/>


### 探索应用程序

Explore Your App


<br/>


#### 查看Pods和Nodes


目标：

- 了解k8s Pods
- 了解k8s Nodes
- 部署应用的故障解决(troubleshoot)

<br>

**k8s Pods**
当你创建一个部署时，k8s创建了一个pod来托管你的应用程序实例。pod是k8s的一个抽象，表示一组(一个/多个)应用程序容器，以及这些容器的共享资源。
pod有一个唯一的IP地址，甚至是同一节点上的pod。pod中的容器共享IP地址和端口，始终位于同一位置并共同调度，并在同一节点上共享上下文中运行。
这些资源包括：

- 共享存储(volumes)
- 网络(唯一的集群内ip)
- 运行容器的相关信息

<br>

**Nodes**
pod总是运行在node上，一个node上可运行多个pod。每个node由master管理，master自动处理在node上调度pod。
node至少运行如下组件：

- kubelet
- container runtime(如docker)

<br>

**Troubleshooting with kubectl**
最常用的`kubectl`命令：

```
#列出资源
kubectl get
#kubectl get nodes


#某个资源的详细信息
kubectl describe
#kubectl describe deployments kubernetes-bootcamp


#pod中容器日志
kubectl logs
#kubectl logs $pod --since=1h


#在pod的容器执行命令
kubectl exec
#kubectl ecec $pod env
#kubectl exec -it $pod /bin/bash
```


<br/>
<br/>


### 公开展示应用程序

Expose Your App Publicly


<br/>


#### 使用服务来展示应用程序

Using a Service to Expose Your App


目标：

- 了解k8s中的服务(service)
- 理解labels和LabelSelector对象如何关联服务
- 使用服务将应用程序展示在集群外部

<br>

**k8s Service**
事实上，pods有一个生命周期。当工作node死亡，node上运行的pods也会丢失。ReplicationController可以通过创建新的Pod来动态地将集群驱动会所需状态，以使应用程序保持运行。
k8s的服务是一个抽象概念，它定义了一组逻辑Pod和一个访问pods的策略。服务使用YAML或JSON来定义。由一组pods所构成的服务通常由LabelSelector来确定。
尽管每个Pod都有一个唯一的IP地址，但如果没有服务，这些IP就不会在集群外公开。
通过指定ServeceSpec中的type，可以不同方式公开服务:

- ClusterIP(默认方式)
在集群内部IP公开服务，只可内部访问

- NodePort
使用NAT在集群的指定节点上公开服务

- LoadBalancer
创建一个外部负载均衡器，并给服务分配一个外部IP

- ExternalName
通过返回带有名称的CNAME(k8s-dns)记录，使用任意名称公开服务

<br>

**Services和Labels**
服务使用labels和selectors匹配一组pod这是一个允许对k8s的对象进行逻辑操作的分组原语。
Label是附件到对象的键/值对，随时随地可修改。有多种方式可使用：

- 指定用于开发(development)、测试(test)、生产(procuct)的对象
- 嵌入版本tag
- 使用tag对对象进行分类

<br>

栗子：

```
kubectl get pods
#NAME                                  READY     STATUS    RESTARTS   AGE
#kubernetes-bootcamp-390780338-6x48n   1/1       Running   0          22h


kubectl get services
#NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
#kubernetes   ClusterIP   10.254.0.1   <none>        443/TCP   1d


#公开展示应用程序
kubectl expose deployment/kubernetes-bootcamp --type="NodePort" --port 8080
#service "kubernetes-bootcamp" exposed


kubectl get services
#NAME                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
#kubernetes            ClusterIP   10.254.0.1     <none>        443/TCP          1d
#kubernetes-bootcamp   NodePort    10.254.11.76   <none>        8080:31514/TCP   2m


kubectl describe services/kubernetes-bootcamp


kubectl describe deployment
#Labels:                 run=kubernetes-bootcamp
#使用label查询
kubectl get pods -l run=kubernetes-bootcamp
kubectl get services -l run=kubernetes-bootcamp
#使用label删除
kubectl delete service -l run=kubernetes-bootcamp

kubectl describe pods kubernetes-bootcamp-390780338-6x48n

kubectl exec -it kubernetes-bootcamp-390780338-6x48n /bin/bash
```


<br/>
<br/>


### 扩展应用程序

Scale Your App

Running Multiple Instances of Your App


目标：

- 使用`kubectl`伸缩应用程序

<br>

**伸缩应用程序**
前面通过部署创建的服务仅有一个pod，当遇到流量激增，我们便需要扩展应用程序。
通过更改部署中的副本数来完成扩展。

扩展部署将确保使用可用资源(available resource)创建新的pod并将其调度到node。k8s支持Pod的自动伸缩，缩放到0(也就是没有pod)也是可能的，它将终止指定部署的所有Pod。
对应用程序运行多个实例需要一种方法将流量分配给所有这些实例。服务有集成的负载均衡器(load-blancer)，可将网络流量分配到公开部署的所有Pod。服务将使用endpoint持续监控运行的Pod，以确保网络流量发送到可用的Pods。

一旦运行的应用程序有了多个实例，你就可以在不停机(downtime)的情况下执行滚动更新(rolling update)。

```
kubectl get deployments
#1个


#扩展实例
kubectl scale deployments/kubernetes-bootcamp --replicas=4
#deployment.extensions "kubernetes-bootcamp" scaled


kubectl get deployments
#4个
kubectl get pods -o wide
#4个


kubectl describe deployment/kubernetes-bootcamp
kubectl describe services/kubernetes-bootcamp


#缩放实例
kubectl scale deployments/kubernetes-bootcamp --replicas=2
#deployment.extensions "kubernetes-bootcamp" scaled


kubectl get deployments
#2个

#有两个pods正在关闭中
kubectl get pods -o wide
NAME                                  READY     STATUS        RESTARTS   AGE       IP            NODE
kubernetes-bootcamp-390780338-1zgvs   1/1       Terminating   0          7m        10.254.76.5   192.168.31.159
kubernetes-bootcamp-390780338-6x48n   1/1       Running       0          2d        10.254.76.2   192.168.31.159
kubernetes-bootcamp-390780338-bqztg   1/1       Running       0          7m        10.254.76.4   192.168.31.159
kubernetes-bootcamp-390780338-hkwfd   1/1       Terminating   0          7m        10.254.76.3   192.168.31.159

#关闭完成
kubectl get pods -o wide
NAME                                  READY     STATUS    RESTARTS   AGE       IP            NODE
kubernetes-bootcamp-390780338-6x48n   1/1       Running   0          2d        10.254.76.2   192.168.31.159
kubernetes-bootcamp-390780338-bqztg   1/1       Running   0          15m       10.254.76.4   192.168.31.159
```


<br/>
<br/>


### 升级应用程序

Update your App
Performing a Rolling Update

目标：

- 使用`kubectl`执行滚动升级

<br>

**滚动更新**
用户希望应用程序始终可用，可发人员可能会多次部署新版本应用程序。在k8s中，这都可以通过滚动更新(rolling update)完成。
滚动更新允许通过使用新的实例逐步更新Pod来实现部署的更新，而不需停机(downtime)。新的Pod将在具有可用资源的node上进行调度。
在k8s中，更新是版本化的，任何部署更新都可以恢复到以前的版本。

与应用程序扩展类似，服务在更新期间仅会将流量负载均衡到可用的Pod(应用实例)。

滚动更新允许以下操作：

- 将应用程序从一个环境推到另一个环境
- 回滚(rollback)到之前的版本
- 无需停机的持续集成(CI)和持续交付(CD)

```
kubectl get deployments
kubectl get pods
#2个


#更新镜像
kubectl set image deployments/kubernetes-bootcamp  kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2
deployment.apps "kubernetes-bootcamp" image updated

#
kubectl get pods
NAME                                  READY     STATUS        RESTARTS   AGE
kubernetes-bootcamp-390780338-6x48n   1/1       Terminating   0          3d
kubernetes-bootcamp-390780338-bqztg   1/1       Terminating   0          38m
kubernetes-bootcamp-472176051-m6h1q   1/1       Running       0          29s
kubernetes-bootcamp-472176051-z4wqs   1/1       Running       0          29s

#
kubectl get pods
NAME                                  READY     STATUS    RESTARTS   AGE
kubernetes-bootcamp-472176051-m6h1q   1/1       Running   0          42s
kubernetes-bootcamp-472176051-z4wqs   1/1       Running   0          42s


#检查回滚状态
kubectl rollout status deployments/kubernetes-bootcamp
deployment "kubernetes-bootcamp" successfully rolled out


#更新
kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v10
deployment.apps "kubernetes-bootcamp" image updated


#有错
kubectl get deployments
NAME                  DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
kubernetes-bootcamp   2         3         2            1           3d


#有错
kubectl get pods
NAME                                  READY     STATUS             RESTARTS   AGE
kubernetes-bootcamp-384357858-7kjx1   0/1       ErrImagePull       0          2m
kubernetes-bootcamp-384357858-t0wmt   0/1       ImagePullBackOff   0          2m
kubernetes-bootcamp-472176051-m6h1q   1/1       Running            0          9m


#
kubectl describe pods



#回滚
kubectl rollout undo deployments/kubernetes-bootcamp
deployment.apps "kubernetes-bootcamp"


#查看
kubectl get pods
kubectl decribe pods
#Image:          docker.io/jocatalin/kubernetes-bootcamp:v2
#回到了V2版
```



<br/>
<br/>



## 配置

Configuration


<br>


### 使用ConfigMap配置Redis


**目标(Objective)**

- 创建ConfigMap
- 使用ConfigMap创建Pod规范
- 创建Pod
- 验证配置是否正确应用

<br>

**开始之前**
需要有k8s集群，并且安装了`kubectl`命令行工具。

<br>

**栗子：使用ConfigMap配置Redis**

```
#Master
#创建redis的ConfigMap
kubectl create configmap redis-config --from-file=xxx/redis-config
kubectl get configmap redis-config -o yaml


#创建redis-pod.yaml文件
apiVersion: v1
kind: Pod
metadata:
  name: redis
spec:
  containers:
  - name: redis
    image: kubernetes/redis:v1
    env:
    - name: MASTER
      value: "true"
    ports:
    - containerPort: 6379
    resources:
      limits:
        cpu: "0.1"
    volumeMounts:
    - mountPath: /redis-master-data
      name: data
    - mountPath: /redis-master
      name: config
  volumes:
    - name: data
      emptyDir: {}
    - name: config
      configMap:
        name: redis-config
        items:
        - key: redis-config
          path: redis.conf


#创建pod
kubectl create -f /etc/k8s/pods/config/redis-pod.yaml

kubectl exec -it redis redis-cli

```



<br/>
<br/>


## 无状态应用程序

Stateless Applications


<br/>


### 公开外物IP以访问集群中的应用程序

Exposing an External IP Address to Access an Application in a Cluster


**目标**

- 为一个Hello World应用程序运行五个实例
- 创建一个展示外部IP的服务对象
- 使用服务对象去访问运行的应用程序

<br>

**为运行五个pods的应用程序创建一个服务**

```
#运行hello world
kubectl run hello-world --replicas=5 --labels="run=load-balancer-example" --image=gcr.io/google-samples/node-hello:1.0  --port=8080
#--image=docker.io/jocatalin/hellonode:v1


#查看信息
kubectl get deployments hello-world
kubectl describe deployments hello-world

kubectl get replicasets
kubectl describe replicasets


#创建展示部署的服务对象
kubectl expose deployment hello-world --type=LoadBalancer --name=my-service
#如果外部地址显示为pending，请等待几分钟


#查看信息
kubectl get services my-service
kubectl describe services my-service
#可看到LoanBlancer Ingress

kubectl get pods --output=wide


#访问外部地址(LoadBalancer Ingress)
curl http://<external-ip>:<port>
```

<br>

**清理**

```
#删除服务
kubectl delete services my-service


#删除正在运行的程序的Deployment，ReplicaSet，Pods
kubectl delete deployment hello-world
```


<br/>
<br/>

---

<br/>



# 状态集应用程序

StatefulSet Basics





































<br/>

---

<br/>
<br/>




































