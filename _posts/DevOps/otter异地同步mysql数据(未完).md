# otter异地同步mysql数据

### 创建mysql

- 创建mysql

建议mysql版本为5.1~5.6,5.7版本source otter manager的sql文件时会报错,暂时没去细究原因.

 ```bash
 docker run \
    --name=mysql-server1 \
    --hostname=mysql \
    --privileged=true \
    -p 10001:3306 \
    -v /data/docker/otter1/mysql/db:/var/lib/mysql \
    -v /data/docker/otter1/mysql/conf:/etc/mysql/conf.d \
    -e MYSQL_ROOT_PASSWORD=. \
    -e MYSQL_USER=canal \
    -e MYSQL_PASSWORD=. \
    -d mysql:5.6 \
    --character-set-server=utf8 \
    --collation-server=utf8_bin
```

```bash
     docker run \
    --name=mysql-server2 \
    --hostname=mysql \
    --privileged=true \
    -p 10002:3306 \
    -v /data/docker/otter2/mysql/db:/var/lib/mysql \
    -v /data/docker/otter2/mysql/conf:/etc/mysql/conf.d \
    -e MYSQL_ROOT_PASSWORD=. \
    -e MYSQL_USER=canal \
    -e MYSQL_PASSWORD=. \
    -d mysql:5.6 \
    --character-set-server=utf8 \
    --collation-server=utf8_bin 
```
- 创建mysql配置文件

```bash
cd  /data/docker/otter2/mysql/conf
touch my.conf
vim my.conf
```

```conf
# Copyright (c) 2014, Oracle and/or its affiliates. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

#
# The MySQL Community Server configuration file.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

[client]
port        = 3306
socket      = /var/run/mysqld/mysqld.sock

[mysqld_safe]
pid-file    = /var/run/mysqld/mysqld.pid
socket      = /var/run/mysqld/mysqld.sock
nice        = 0

[mysqld]
user        = mysql
pid-file    = /var/run/mysqld/mysqld.pid
socket      = /var/run/mysqld/mysqld.sock
port        = 3306
basedir     = /usr
datadir     = /var/lib/mysql
tmpdir      = /tmp
lc-messages-dir = /usr/share/mysql
explicit_defaults_for_timestamp

log-bin = mysql-bin
server-id = 1

# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
#bind-address   = 127.0.0.1

#log-error  = /var/log/mysql/error.log

# Recommended in standard MySQL setup
sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

# * IMPORTANT: Additional settings that can override those from this file!
#   The files must end with '.cnf', otherwise they'll be ignored.
#
!includedir /etc/mysql/conf.d/
```

### 下载并导入otter manager sql文件
[](https://raw.github.com/alibaba/otter/master/manager/deployer/src/main/resources/sql/otter-manager-schema.sql)

### 更新mysql账号及权限
```mysql
flush PRIVILEGES;
CREATE USER canal IDENTIFIED BY '.'; 
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'canal'@'%';
FLUSH PRIVILEGES;
```

### 创建zookeepr
这里我们创见的为单机版,也可以创建集群
[集群参考这里](https://segmentfault.com/a/1190000006907443)
```bash
docker run --name otter-zookeeper -d -v /data/docker/otter2/zookeeper/zoo.cfg:/conf/zoo.cfg -p 10003:2181 zookeeper
```