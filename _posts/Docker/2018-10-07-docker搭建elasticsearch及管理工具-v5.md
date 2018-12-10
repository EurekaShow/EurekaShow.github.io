## elasticsearch
```bash
# docker run -d --name es5 -p 9200:9200 -p 9300:9300 -m 2G --privileged=true -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e "discovery.type=single-node" elasticsearch:5-alpine

# docker run -d --name es_amdin -p 9100:9100  --privileged=true mobz/elasticsearch-head:5-alpine
```
### elasticsearch需要修改配置文件，否则会由于内存负载过大造成宕机。

```conf 
# cd config
# vi jvm.options


## 默认设置是
-Xms2g
-Xmx2g

##修改 -Xms 和 -Xmx,根据系统剩余内存自己感觉配置 我还剩了四个g 所以都分配为1个G
-Xms1g
-Xmx1g
```
### 修改跨域，保证head能正常调用

```conf 
# cd config
# vi elasticsearch.yml

# 加入跨域配置
http.cors.enabled: true
http.cors.allow-origin: "*"
```
重启docker容器即可。



