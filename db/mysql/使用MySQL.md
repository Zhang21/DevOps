# 使用MySQL


<br/>
<br/>


## 连接

在执行命令之前需要登录到DBMS。为了连接到MySQL，需要以下信息:
- hostname
- port
- username
- passwd(可选)


<br/>
<br/>


## 选择数据库

选择数据库有两种方式:
- 在连接是指定数据库名
- 登录后选择数据库

```
# 1
mysql -h xxx -P xxx -u xxx -p dbName


# 2
mysql> USE dbName;
```


<br/>
<br/>


## 了解数据库和表

数据库、表、列、用户、权限等的信息被存储在数据库和表中。不过，内部表一般不直接访问，可用`SHOW`命令来显示这些信息。

```sql
HELP SHOW;

SHOW DATABASES;

SHOW TABLES;

SHOW COLUMNS FROM tableName;

# 显示服务器信息
SHOW STATUS;

# 显式创建
SHOW CREATE DATABASE xxx;
SHOW CREATE TABLE xxx;

# 查看权限
SHOW GRANTS;

# 显示Server错误或警告信息
SHOW ERRORS;
SHOW WARNINGS;
```


