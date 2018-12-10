# MySql:charset和collation的设置

### charset 和 collation 有多个级别的设置：服务器级、数据库级、表级、列级和连接级 

### 1.服务器级 
  - 查看设置：
  ```sql
  show global variables like 'character_set_server'; 
  show global variables like 'collation_server';
  ```
 - 修改设置：在OPTION FILE （/etc/mysql/my.cnf）里设置：
 ```conf
   [mysqld] 
    character_set_server=utf8 
    collation_server=utf8_general_ci 
 ```
### 2. 数据库级 
   查看设置：
```sql
   select * from information_schema.schemata where schema_name = 'cookbook'; 
```
   设置： 
     1.若没有显式设置，则自动使用服务器级的配置 
     2.显式设置：在创建库时指定 
```sql
       create database playUtf8  DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
```
### 3.表级 
   查看设置：show create table course; 
   设置： 
     1.若没有显式设置，则自动使用数据库级的配置 
     2.显式设置：在创建表时指定 
```sql
       create table utf ( id int ) default charset=utf8 default collate=utf8_bin; 
```
### 4.列级 
   - 查看设置：show create table course; 
   - 设置： 
     1.若没有显式设置，则自动使用表级的配置 
     2.显式设置： 
```sql
     CREATE TABLE Table1(column1 VARCHAR(5) CHARACTER SET latin1 COLLATE latin1_german1_ci); 
```
### 5.连接级别 
  - 查看设置： 
  ```sql
     show variables like 'character_set_client';  # 服务端使用这个编码来理解客户端发来的statements 
     show variables like 'character_set_connection' ; # 我还不知道什么意思，等看了mysql源码再说 
     show variables like 'character_set_results'; # 服务端使用这个编码回送结果集和错误信息 
```
  - 设置： 
     客户端在连接时可以指定这些参数；同时，服务端也提供了一个Global范围的值，客户端未指定这些参数时，服务端就使用这个Global值。这个global值怎么设置的？　我查遍了很多文档，似乎还没看到设置的办法　（有人说通过my.cnf，或者在启动mysqld时指定命令行参数，其实都是错的） 
 
### 附：connector/j传输SQL时用什么编码？ 
  答案： "The character encoding between client and server is automatically detected upon connection. The encoding used by the driver is specified on the server using the character_set_server system variable for server versions 4.1.0 and newer." 
   也就是说，是在连接时查询服务器端的character_set_server值，再确定连接将使用的编码。 
   不过，官方文档还说，"要想覆盖客户端上的自动检测编码功能，可在用于连接到服务器的URL中使用“characterEncoding”属性。"