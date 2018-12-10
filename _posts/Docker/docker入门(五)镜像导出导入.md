# docker入门(五)镜像导出导入
本来想升华下，整理下批量管理docker run命令的，忽然发现，在批量自动化之前，有一个不得不解决的问题，我们辛辛苦苦做的镜像文件，我们辛辛苦苦升级的镜像文件，怎么才能导出复用变成重要起来。那么我们来看下docker的两种处理方式：

### - 1.容器导出导入命令：export 和 improt
```bash
# 将容器导出到文件
[root@localhost Downloads]# docker export 1b8dc93ddae5 > java-tomcat-8.tar

# 创建一个新镜像从基于导出的文件
[root@#localhost /]# docker import - java-tomcat-8 < java-tomcat-8.tar
```

### - 2.镜像文件的保存和恢复命令：save 和 load
```bash
#执行完该命令后，在Downloads目录下即可找到java-tomcat-8.tar
[root@localhost Downloads]# docker save -o java-tomcat-8.tar java8-tomcat8

[root@localhost Downloads]# ls
java-tomcat-8.tar

#在其他机器上执行load即可
[root@localhost Downloads]# docker load < java-tomcat-8.tar
Loaded image: java8-tomcat8:latest
[root@localhost Downloads]# docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
java8-tomcat8       latest              1b8dc93ddae5        4 hours ago         804.5 MB
docker.io/centos    latest              ff426288ea90        4 weeks ago         207.2 MB
```
