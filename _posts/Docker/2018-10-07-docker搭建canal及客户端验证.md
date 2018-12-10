## docker搭建canal及客户端验证

- 1.首先，我们要搭建mysql

```bash
# docker run --name mysql2 -e MYSQL_ROOT_PASSWORD=. -p 3306:3306 --privileged=true -v /d/mysql/data:/var/lib/mysql -v /d/mysql/conf:/etc/mysql -d mysql:5.7 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
为了方便配置和数据安全管理，我们把mysql的data目录和配置目录全部映射在本地d盘下的mysql对应目录，并且设置用户名和密码，默认字符集为utf8mb4.

- 2.接着配置mysql启用binlog备份，配置主从：

在映射的d：/mysql/conf下新增my.cnf文件，内容如下：
```conf
[mysqld]
log-bin=mysql-bin #添加这一行就ok
binlog-format=ROW #选择row模式
server_id=1 #配置mysql replaction需要定义，不能和canal的slaveId重复
```

- 3.在mysql中 配置canal数据库管理用户，配置相应权限（repication权限）
```sql
CREATE USER canal IDENTIFIED BY 'canal';  
GRANT SELECT, REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO 'canal'@'%';
-- GRANT ALL PRIVILEGES ON *.* TO 'canal'@'%' ;
FLUSH PRIVILEGES;
```

- 4.搭建canal环境，并link到我们的mysql容器

```bash
# docker run -d -p 2222:2222 -p 11111:11111 -p 8000:8000 -p 11112:11112 --name canalServer --privileged=true --link mysql2:mysql2 canal/canal-server
```
- 5.修改canal配置

```conf
# docker exec -it canalServer /bin/sh

# vim canal-server/conf/example/instance.properties
```

配置文件如下
```conf
#################################################
## mysql serverId , v1.0.26+ will autoGen
# canal.instance.mysql.slaveId=18

# enable gtid use true/false
canal.instance.gtidon=false

# position info
canal.instance.master.address=mysql2:3306
canal.instance.master.journal.name=
canal.instance.master.position=
canal.instance.master.timestamp=
canal.instance.master.gtid=

# rds oss binlog
canal.instance.rds.accesskey=
canal.instance.rds.secretkey=
canal.instance.rds.instanceId=

# table meta tsdb info
canal.instance.tsdb.enable=true

# username/password
canal.instance.dbUsername=root
canal.instance.dbPassword=.
canal.instance.connectionCharset = UTF-8
canal.instance.defaultDatabaseName =test
# enable druid Decrypt database password
canal.instance.enableDruid=false
#canal.instance.pwdPublicKey=MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALK4BUxdDltRRE5/zXpVEVPUgunvscYFtEip3pmLlhrWpacX7y7GCMo2/JM
6LeHmiiNdH1FWgGCpUfircSwlWKUCAwEAAQ==

# table regex
canal.instance.filter.regex=.*\\..*
# table black regex
canal.instance.filter.black.regex=
#################################################
```

**需要我们关注并调整的是如下配置：**
```conf
#canal.instance.mysql.slaveId=18

canal.instance.master.address=mysql2:3306

canal.instance.dbUsername=mysql-username
canal.instance.dbPassword=mysql-password
```

- 6.Java代码验证

Java项目引用canal客户端maven配置
```xml
    <dependency>
        <groupId>com.alibaba.otter</groupId>
        <artifactId>canal.client</artifactId>
        <version>1.1.1</version>
    </dependency>
```
Java代码如下：

```java
package com.akt.basics.canal;

/**
 * Created by Eureka 6-11-18.
 */
import java.net.InetSocketAddress;
import java.util.List;

import com.alibaba.otter.canal.client.CanalConnector;
import com.alibaba.otter.canal.common.utils.AddressUtils;
import com.alibaba.otter.canal.protocol.Message;
import com.alibaba.otter.canal.protocol.CanalEntry.Column;
import com.alibaba.otter.canal.protocol.CanalEntry.Entry;
import com.alibaba.otter.canal.protocol.CanalEntry.EntryType;
import com.alibaba.otter.canal.protocol.CanalEntry.EventType;
import com.alibaba.otter.canal.protocol.CanalEntry.RowChange;
import com.alibaba.otter.canal.protocol.CanalEntry.RowData;
import com.alibaba.otter.canal.client.*;

public class SimpleCanalClientExample {

    public static void main(String args[]) {
        // 创建链接
        CanalConnector connector = CanalConnectors.newSingleConnector(new InetSocketAddress(AddressUtils.getHostIp(),
                11111), "example", "", "");
        int batchSize = 1000;
        int emptyCount = 0;
        try {
            connector.connect();
            connector.subscribe(".*\\..*");
            connector.rollback();
            int totalEmtryCount = 1200;
            while (emptyCount < totalEmtryCount) {
                Message message = connector.getWithoutAck(batchSize); // 获取指定数量的数据
                long batchId = message.getId();
                int size = message.getEntries().size();
                if (batchId == -1 || size == 0) {
                    emptyCount++;
                    System.out.println("empty count : " + emptyCount);
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                } else {
                    emptyCount = 0;
                    // System.out.printf("message[batchId=%s,size=%s] \n", batchId, size);
                    printEntry(message.getEntries());
                }

                connector.ack(batchId); // 提交确认
                // connector.rollback(batchId); // 处理失败, 回滚数据
            }

            System.out.println("empty too many times, exit");
        } finally {
            connector.disconnect();
        }
    }

    private static void printEntry(List<Entry> entrys) {
        for (Entry entry : entrys) {
            if (entry.getEntryType() == EntryType.TRANSACTIONBEGIN || entry.getEntryType() == EntryType.TRANSACTIONEND) {
                continue;
            }

            RowChange rowChage = null;
            try {
                rowChage = RowChange.parseFrom(entry.getStoreValue());
            } catch (Exception e) {
                throw new RuntimeException("ERROR ## parser of eromanga-event has an error , data:" + entry.toString(),
                        e);
            }

            EventType eventType = rowChage.getEventType();
            System.out.println(String.format("================> binlog[%s:%s] , name[%s,%s] , eventType : %s",
                    entry.getHeader().getLogfileName(), entry.getHeader().getLogfileOffset(),
                    entry.getHeader().getSchemaName(), entry.getHeader().getTableName(),
                    eventType));

            for (RowData rowData : rowChage.getRowDatasList()) {
                if (eventType == EventType.DELETE) {
                    printColumn(rowData.getBeforeColumnsList());
                } else if (eventType == EventType.INSERT) {
                    printColumn(rowData.getAfterColumnsList());
                } else {
                    System.out.println("-------> before");
                    printColumn(rowData.getBeforeColumnsList());
                    System.out.println("-------> after");
                    printColumn(rowData.getAfterColumnsList());
                }
            }
        }
    }

    private static void printColumn(List<Column> columns) {
        for (Column column : columns) {
            System.out.println(column.getName() + " : " + column.getValue() + "    update=" + column.getUpdated());
        }
    }
}

```

执行后，新增数据库，表，新增一条记录，修改记录，删除数据效果如下：
*test为测试数据库名称，canal-test为测试表名称*

```conf
empty count : 1
empty count : 2
empty count : 3
empty count : 4
empty count : 5
empty count : 6
empty count : 7
empty count : 8
empty count : 9
empty count : 10
================> binlog[mysql-bin.000002:219] , name[,] , eventType : QUERY
empty count : 1
empty count : 2
empty count : 3
empty count : 4
empty count : 5
empty count : 6
empty count : 7
empty count : 8
empty count : 9
empty count : 10
================> binlog[mysql-bin.000002:219] , name[,] , eventType : QUERY
================> binlog[mysql-bin.000002:420] , name[test,canal-test] , eventType : CREATE
empty count : 1
empty count : 2
empty count : 3
empty count : 4
empty count : 5
empty count : 6
empty count : 7
empty count : 8
empty count : 9
empty count : 10
================> binlog[mysql-bin.000002:837] , name[test,canal-test] , eventType : INSERT
id : 1    update=true
name : 测试姓名    update=true
empty count : 1
empty count : 2
empty count : 3
empty count : 4
empty count : 5
empty count : 6
empty count : 7
empty count : 8
empty count : 9
empty count : 10
================> binlog[mysql-bin.000002:1115] , name[test,canal-test] , eventType : UPDATE
-------> before
id : 1    update=false
name : 测试姓名    update=false
-------> after
id : 1    update=false
name : 姓名测试    update=true
empty count : 1
empty count : 2
empty count : 3
empty count : 4
empty count : 5
empty count : 6
empty count : 7
empty count : 8
empty count : 9
empty count : 10
================> binlog[mysql-bin.000002:1413] , name[test,canal-test] , eventType : DELETE
id : 1    update=false
name : 姓名测试    update=false
```



