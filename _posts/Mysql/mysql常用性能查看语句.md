### 常用性能查看语句
```sql
-- 查询锁信息
 SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS
 SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS
 SELECT * FROM INFORMATION_SCHEMA.INNODB_TRX


-- 查看死锁的id
- SHOW PROCESSLIST;

--  根据id Kill 死锁。
- Kill 18;

-- 显示引擎的详细数据，如果有死锁，显示最近的一次死锁数据。
SHOW ENGINE INNODB STATUS;

— 查看是否开启profiles
SHOW VARIABLES LIKE "%pro%";
-- 显示执行时间，用来分析执行效率
SHOW PROFILES;

-- 查看是否开启了慢查询
SHOW VARIABLES  LIKE '%slow_query_log%'

-- 开启慢查询设置／数据库重启后失效
set global slow_query_log=1;

-- 用久开启慢查询，设置my.cnf
slow_query_log =1
slow_query_log_file=/tmp/mysql_slow.log

-- 默认情况下，慢查询的阀值是10秒
show variables like 'long_query_time%';
set global long_query_time=4;

-- 慢查询的log可以保存成文件，也可以保存到数据库，值为【FILE,TABLE】但数据库更耗费资源
show variables like '%log_output%';
set global log_output='TABLE';
```

### 日志分析工具mysqldumpslow