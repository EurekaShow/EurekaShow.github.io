- 1、显示数据库
```
 show databases;
```

- 2、选择数据库
```
use 数据库名;
```

- 3、显示数据库中的表
```
show tables;
```

- 4、显示数据表的结构 
```
describe 表名;
```

- 5、显示表中记录 
```
SELECT * FROM 表名
```
- 6、建库
```
 create databse 库名;
```

- 7、建表
```
create table 表名 (字段设定列表)；

mysql> create table name(
    -> id int auto_increment not null primary key ,
    -> uname char(8),
    -> gender char(2),
    -> birthday date );
Query OK, 0 rows affected (0.03 sec)

mysql> show tables;
+------------------+
| Tables_in_userdb |
+------------------+
| name             |
+------------------+
1 row in set (0.00 sec)

mysql> describe name;
+----------+---------+------+-----+---------+----------------+
| Field    | Type    | Null | Key | Default | Extra          |
+----------+---------+------+-----+---------+----------------+
| id       | int(11) | NO   | PRI | NULL    | auto_increment |
| uname    | char(8) | YES  |     | NULL    |                |
| gender   | char(2) | YES  |     | NULL    |                |
| birthday | date    | YES  |     | NULL    |                |
+----------+---------+------+-----+---------+----------------+
4 rows in set (0.00 sec)
```
注： auto_increment 自增
     primary key    主键

- 8、增加记录
```
 insert into name(uname,gender,birthday) values('张三','男','1971-10-01');
```

- 9、修改记录
```
update name set birthday='1971-01-10' where uname='张三';
```

- 10、删除记录
```
delete from name where uname='张三';
```

- 11、删除表
```
drop table 表名
```

- 12、删除库
```
 drop database 库名;
```

- 13、备份数据库 
```
mysqldump -u root -p --opt 数据库名>备份名; //进入到库目录
```

- 14、恢复
```
mysql -u root -p 数据库名<备份名; //恢复时数据库必须存在，可以为空数据库
```

- 15、新增用户并授权
```
mysql> create user xxf;

mysql> update user set authentication_string=password("12345678") where user="xxf"; 

mysql> grant all on *.* to 'xxf'@'%';

```

授权格式：grant 权限 on 数据库对象 to 用户

- grant 数据用户，查询、插入、更新、删除 数据库中所有表数据的权利。
```
grant select on dbname.* to username@'%'
grant insert on dbname.* to username@'%'
grant update on dbname.* to username@'%'
grant delete on dbname.* to username@'%'
```

- grant 创建、修改、删除 MySQL 数据表结构权限。
```
grant create on dbname.* to username@'192.168.0.%';
grant alter  on dbname.* to username@'192.168.0.%';
grant drop   on dbname.* to username@'192.168.0.%';
```
*基于mysql5.7

[more grant](http://www.cnblogs.com/hcbin/archive/2010/04/23/1718379.html)

