# 一些配置与工具

<br/>

```yaml
env: centos7x86_64
```


<br/>
<br/>


## 一些源

```sh
# EPEL
sudo yum install -y epel-release

# REMI
sudo yum install -y  http://rpms.famillecollet.com/enterprise/remi-release-7.rpm


# RPMForge
rpm -ivh http://repository.it4i.cz/mirrors/repoforge/redhat/el7/en/x86_64/rpmforge/RPMS/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm
```



<br/>
<br/>



## Python环境

```sh
# python2
sudo yum install python-pip  python-devel

# python3.6
sudo yum -y install python36 python36-pip python36-devel


# PIP SOURCE
# global
vim ~/.pip/pip.conf

[global]
trusted-host =  mirrors.aliyun.com
index-url=https://mirrors.aliyun.com/pypi/simple/

# temporary
pip install xxx -i https://mirrors.aliyun.com/pypi/simple/
```



<br/>
<br/>



## 生成随机密码

```sh
# 数字表示密码长度
openssl rand -base64 16
```



<br/>
<br/>



## 显示git分支名

参考: <https://gist.github.com/yisibl/8281454>

```sh
vim ~/.bashrc

# 添加如下内容
function git_branch {
   branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
   if [ "${branch}" != "" ];then
       if [ "${branch}" = "(no branch)" ];then
           branch="(`git rev-parse --short HEAD`...)"
       fi
       echo " ($branch)"
   fi
}

export PS1='\u@\h \[\033[01;36m\]\W\[\033[01;32m\]$(git_branch)\[\033[00m\] \$ '


# 生效
source ~/.bashrc
```


<br/>
<br/>


## httpie工具

```sh
sudo yum install httpie
```
