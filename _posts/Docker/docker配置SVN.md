# docker 配置SVN

### 创建容器
```bash
docker run \
-d -p 9200:80 -p 9201:443 \
-v /data/svn/repo:/var/local/svn \
-v /data/svn/svn-backup:/var/svn-backup \
-v /data/svn/dav_svn2/:/etc/apache2/dav_svn/ \
-v /data/svn/dav_svn/:/etc/apache/dav_svn/ \
--privileged=true \
--name svn marvambass/subversion
```
- 直接run会自动pull对应的images，所以，无需担心。

### 添加权限配置文件
```bash
# cd /data/svn/dav_svn2/
# vi dav_svn.authz
```
- 目录根据宿主机挂载不同会有所不同，请根据自己挂载目录操作。

添加如下内容：

```conf
[groups]
admin = user1,user2,user3
devgroup =

[repository:/doc]
@admin = rw
@devgroup = r

# devgroup members are able to read and write on project2
[repository:/doc2]
@admin = rw
@devgroup = rw

# # admins have control over every project - and can list all projects on the root point
[/]
@admin = rw
*= r
```
说明：
- groups 下添加角色名称和用户名称
- doc和doc2分别是两个项目仓库，需要到/data/svn/repo/目录下创建仓库文件夹。
- *= r 表示所有人都可以浏览查看

### 创建仓库文件夹

```bash
# cd /data/svn/repo/
# mkdir doc
# mkdir doc2
```
- 目录根据宿主机挂载不同会有所不同，请根据自己挂载目录操作。
- 挂在的外部系统如果是centOS，可能会报文件系统之类错误。粗暴的解决办法是，给挂接的目录开放所有权限
```bash
# chmod -R 777 ./repo
#或者
# chmod -R 777 /data/svn/repo/
```

### 给用户添加密码
```bash
#如果htdigest提示command not found，先安装
# yum -y install httpd

#给用户增加密码
# htdigest dav_svn.passwd Subversion user1
```
根据提示输入密码即可。

### 最后，输入http://ip:9200/svn/
是不是可以看到doc和doc2两个仓库目录啦？恭喜啦。。。
- ip为宿主机IP地址

使用的docker images地址为：
[marvambass/subversion](https://hub.docker.com/r/marvambass/subversion/)