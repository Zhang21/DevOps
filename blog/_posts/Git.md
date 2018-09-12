---
title: Git
date: 2017-11-07 17:45:42
tags: Git
categories: Linux

---


参考：

- [廖雪峰Git教程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)



<br>
<br/>

<!--more-->

---

<br>



# Git介绍


git(/ɡɪt/)是一个分布式版本控制软件,最初由林纳斯·托瓦兹（Linus Torvalds）创作，于2005年以GPL发布。Git是免费的。

林纳斯·托瓦兹自嘲地取了这个名字“git”，该词源自英国俚语，意思大约是“混账”。

<br>

![Git](/images/git.jpg)



<br>



## 集中式与分布式

集中式版本控制系统，版本库是集中存放在中央服务器的，而干活的时候，用的都是自己的电脑，所以要先从中央服务器取得最新的版本，然后开始干活，干完活了，再把自己的活推送给中央服务器。
集中式版本控制系统最大的毛病就是必须联网才能工作。
常用集中式版本控制系统有：CVS、SVN。

分布式版本控制系统根本没有“中央服务器”，每个人的电脑上都是一个完整的版本库，这样，你工作的时候，就不需要联网了，因为版本库就在你自己的电脑上。既然每个人电脑上都有一个完整的版本库，那多个人如何协作呢？比方说你在自己电脑上改了文件A，你的同事也在他的电脑上改了文件A，这时，你们俩之间只需把各自的修改推送给对方，就可以互相看到对方的修改了。
常用分布式版本控制系统有：Git。

和集中式版本控制系统相比，分布式版本控制系统的安全性要高很多，因为每个人电脑里都有完整的版本库，某一个人的电脑坏掉了不要紧，随便从其他人那里复制一个就可以了。而集中式版本控制系统的中央服务器要是出了问题，所有人都没法干活了。


<br>
<br/>



# Git常用命令


<be>


## 创建版本库


```

#--global全局配置
git config --global user.name "Username"
git config --globla user.email "Email"



#创建版本库
#虽然在任意目录下都可创建git-repo，但还是建议在一个空目录下创建git-repo
mkdir gitest&&cd gitest

#init, Create an empty Git repository or reinitialize an existing one
git init
#生成了一个.git目录，这个目录是git用来追踪管理版本库的，不要随意修改此目录的内容

echo "First Git test" > README



#所有的版本控制系统，只能跟踪文本文件的改动

#把文件添加到仓库
#git add file1 file2...
git add　README


#把文件提交到仓库
#-m, 为本次提交的说明信息
git commit -m "Update Readme"


#为什么Git添加文件需要add, commit一共两步呢？
#因为commit可以一次提交很多文件，所以你可以多次add不同的文件。
git add file1 file2 file3
git commit -m "add 3files"

```


<br>
<br/>

---

<br>



# 时光穿梭机



```

#查看repo当前状态
git status



#查看改变
git diff

```


<br>


## 版本回退


每当文件修改到一定程度的时候，就可以提交一次。这样即使误操作后，还可以从最近的`commit`中恢复，而不是把工作成果全部丢失。


```
#查看提交记录
#git的commit id是一个SHA1的16进制散列
git log

    Update README.md

commit e89d28373c19321466f99e15cd3cdcc5fffe868f
Author: zhang21 <elite_zhang21@163.com>
Date:   Thu Apr 5 23:40:13 2018 +0800



#版本回退，如果文件误删，可以从commit中恢复
#查看提交记录，能看到Commit ID(sha1sum散列值)
#在Git中，用HEAD表示当前版本，也就是最新的Commit ID
#上一版本HEAD^, 上上版本HEAD^^, 倒数第十个版本HEAD~100



#HEAD指的是当前版本
#重置当前HEAD到指定状态
git reset --hard HEAD^

#也可以利用commit id回退
git reset --hard $commit_id



#查看历史命令
git reflog

```


<br>
<br/>


## 工作区和暂存区


- `git add`实质是吧文件修改添加到**暂存区**
- `git commit`实质是把暂存区的所有内容提交到当前分支


<br>
<br/>


## 管理修改


为什么git比其它版本控制系统设计的更优秀，因为它跟踪并管理的是修改，而非文件。
如果修改后的文件没有使用`git add`放入暂存区的话，那么`git commit`也不会生效的。


<br>
<br/>


## 撤销修改

如果要纠正文件，可以手动修改文件并恢复到上一版本状态。
但也可以使用git命令。


```

#丢弃工作区的修改
#--很重要，没有--就变成了切换分支的命令
git checkout -- filename



#当你不但改乱了工作区某个文件的内容，还添加到了暂存区时。想丢弃修改，分两步。
#第一步用命令git reset HEAD file，就回到了场景1，第二步git checkout --file。
git reset HEAD file && git checkout -- file

```


<br>
<br/>


## 删除文件


在git中，删除也是一个修改操作。

有两种情况：

- 误删除
- 真删除

```

#rm，从工作区和索引中删除文件
#如果一个文件已经被提交到版本库，那么你永远不用担心误删
git rm README


#误删某文件，需要恢复
git checkout -- README

```


<br>
<br/>

---

<br>



# 远程仓库


用于验证推送，GitHub与本地仓库使用SSH加密传输，所以这需要创建一对密钥。


```
#生成SSH Key
ssh-keygen -t rsa -C "email-address"

#会生成.ssh目录，里面包含公私钥
#将公钥id_ras.pub填入GitHub

```


<br>
<br/>


## 添加远程仓库


```

#origin是默认的远程仓库名，你可以修改
git remote add origin git@xxx.com:username/xxx.git



#推动本地仓库到远程
#实际上是推动本地的master分支到远程
#-u关联了本地master和远程master
git push -u origin master

#之后
git push origin master

```


<br>
<br/>


## 从远程库克隆


```
#将远程仓库克隆到本地
#如果是多人协作开发，那么每个人各自从远程克隆一份就可以了
#可以使用ssh协议或https协议(每次都要输入口令)
git clone git@xxx.com:username/xxx.git

#克隆指定分支
git clone -b test URL

```



<br>
<br/>

---

<br>



# 分支管理


你可以创建一个自己的分支，别人看不到，还继续在原来的分支上正常工作。而你在自己的分支上干活，想提交就提交，而不会影响到其他人。


<br>
<br/>


## 创建于合并分支


`HEAD`严格来说不是指向提交，而是指向分支(如`master`)，分支才是指向提交。

当工作完成后，便可合并分支，然后删除额外的分支。

```

#查看分支
#*代表当前工作分支
git branch



#创建分支
git branch <branch-name>
#切换分支
git checkout <branch-name>



#创建并切换分支，等于上面的创建和切换分支
git checkout -b <branch-name>



#在test分支下新建test.txt
git checkout test
echo 'Just a test' > ./test.txt
git add test.txt
git commit -m 'Just a test branch'



#回到master
git checkout master
#此分支下并没有test.txt
#也就是说并没有其它分支提交的内容



#合并分支到当前分支
git merge <branch-name>

#合并test分支到当前的master分支
git merge test



#删除分支
git branch -d <branch-name>

#合并完成后删除test分支
git brancd -d test

```


<br>
<br/>


## 解决冲突


合并分支玩玩也不是一帆风顺的！

可能在你创建了新分支后，master分支又进行了提交，而你的新分支也做了提交，这是合并分支便会带了问题。
当git分支无法合并时，就必须首先要解决冲突。解决冲突后，再提交和合并。

```

#查看分支合并图
git log --graph

```


<br>
<br/>


## 分支管理策略


- 在实际开发中，`master`分支应该是非常稳定的。也就是只用来发布新版本，不能在上面干活
- 干活应在其它分支上(如`dev`)，干完后合并到`master`
- 工作人员都在`dev`上干活，每个人都有自己的分支，然后将自己的分支合并到`dev`就可以了

![分支策略](/images/gitbranch.png)

<br>

> 合并分支时，加上`--no-ff`参数就可以用普通模式合并，合并后的历史有分支，能看出来曾经做过合并，而`fast forward`合并就看不出来曾经做过合并。


<br>
<br/>


## Bug分支


Git提供了一个`stash`功能，可以把工作现场**储藏**起来，等以后恢复现场后继续工作。

```
git stash

#创建debug分支
git checkout -b 'issue-25'

git checkout master
git merge --no-ff -m "debug 25" 'issue-25'



#切回工作区
git stash list
git stash apply stash@xxx

#手动删除stash
git stash drop


#恢复同时也删除stash
git stash pop
```


<br>
<br/>


## Feature分支


添加一个新功能时，你肯定不希望因为一些实验性质的代码，把主分支搞乱了，所以，每添加一个新功能，最好新建一个feature分支，在上面开发，完成后，合并，最后，删除该feature分支。

丢弃一个没有被合并过得分支，可通过`git branch -D <branch-name>`强行删除。


<br>
<br/>


## 多人协作


```
#查看远程仓库
git remote

#显示远程仓库详细信息
git remote -v



#推送指定分支
git push origin test



#抓取分支
git clone

#更新分支
git pull

#合并分支
git merge

#推送分支
git push
```


<br>

## 版本库（Repository）

隐藏目录.git是Git的版本库。
Git版本库里面存放了很多东西，其中最重要的就是 stage(或index)的暂存区，还有Git为我们自动创建的第一个分支`master`，以及指向master的一个指针叫`HEAD`。

- 用`git add`把文件添加进去，实际是把文件添加到暂存区；
- 用`git commit`提交更改，实际是把暂存区的所有内容提交到当前分支。默认`git commit`就是往`master`上提交更改。



<br>
<br/>

---

<br>



# SSHKey


1. 创建SSHKey并在本地关联多个SSH

```
#把你的github邮箱地址
ssh-keygen -t rsa -C "email@example.com"
#会生成 ~/.ssh，包含 私钥：id_rsa，公钥：id_rsa.pub
```

2. 将公钥写入Github
在Github--Account settings--SSH Keys--Add SSH Key里面，添加你的id_rsa.pub公钥文件。
当然，你可以添加多个Key哦，毕竟可能你有多台登陆设备。
这个就相当于SSH无密钥认证。

3. 在主机上关联多个git

```sh
vim ~/.ssh/config


#One
Host git.xxx.com
        IdentityFile ~/.ssh/id_rsa
        Hostname IP
        User git
        Port 10022
#two
Host github
	IdentityFile ~/.ssh/id_rsa
	Hostname github.com
	User git
	Port 22
#three
#这样可用于ssh登录
Host zhang21
	Hostname ip
    User username
    Port 22
    IdentityFile ~/.ssh/id_rsa



#一定要记着修改权限
chmoe 600 ~/.ssh/*


#测试连接
ssh -T git@github.com
```



<br>
<br/>

---

<br>



# 标签管理


发布一个新版本时，通常先在版本库中打一个标签(tag)，这样，就唯一确定了打标签时刻的版本。
将来无论什么时候，取某个标签的版本，就是把那个打标签的时刻的历史版本取出来。所以，标签也是版本库的一个快照。

`tag`其实是指向 `commit id`的。
git有commit，为什么还要引入tag? commit id 是一串散列值，并不简单明了。但是tag,我可以写为"v1.0","v1.2"...
让`tag`，"v1.0"指向对应的`commit id`，很方便明了。


<br>
<br/>


## 创建标签


```
#切换到需要打tag的分支上
git brach test



#创建tag
默认tag是打在最新提交的commit上
#git tag <tag-name>
git tag v1.0



#查看所有tag
git tag



#指定tag对应的commit
#git tag <tag-name> <commit_id>
git tag v1.0 65432ba



#标签不是按时间顺序列出的，而是按照字母排序
git show $tag-name
git show v1.0



#创建带有说明的标签
#git tag -a <tag-name> -m "v1.1 released" <commit-id>
git tag -a v1.1 -m "V1.1" 6543bb


#查看标签说明
git show <tag-name>



#用私钥签名一个标签
#依赖GPG
#git tag -s <tag-name> -m "pri-key" <commit-id>
git tag -s v1.2 -m "pri-key v1.2" 6543bc

```


<br>
<br/>


## 操作标签


```

#删除标签
#git tag -d <tag-name>
git tag -d v1.2



#推送某个标签到远程
#git pust origin <tag-name>
git push origin v1.0



#推送全部标签
git push origin --tags



#删除远程标签
git push origin :refs/tags/<tag-name>

```


<br>
<br/>

---

<br>



# 搭建Git服务器


常见的Git服务器有：

- GitLab: <https://gitlab.com/>
- Gogs（go git service）: <https://gogs.io/>




















