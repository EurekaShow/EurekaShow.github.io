---
author: XiaoFeng
date: 2018-10-07
layout: post
title: docker配置Jira
header-img: img/tag-bg-o.jpg
catalog: true
tags:
    - Docker
    - Jira
---

# docker配置Jira

### pull镜像文件，创建容器启动
方法一：编排YAML文件，通过docker-compose生成。
```yaml
version: '2.1'

services:
  jira:
    image: lowmem0ry/jira
    container_name: jira
    restart: always
    ports:
      - '9205:8080'
    links:
      - 'dbserver:mysql'
  dbserver:
    image: mysql:5.6
    container_name: mysql-jira
    restart: always
    ports:
      - 9206:3306
    volumes:
      - /data/docker/mysql/jira/db:/var/lib/mysql
      - /data/docker/mysql/jira/conf:/etc/mysql/conf.d
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: jira
      MYSQL_USER: jira
      MYSQL_PASSWORD: jira
```
方法二：通过docker run命令生成：
```bash
# docker run -d \
    --name=mysql-jira \
    --hostname=mysql \
    --restart=always \
    --privileged=true \
    --character-set-server=utf8mb4 \
    --collation-server=utf8mb4_unicode_ci \
    -p 9206:3306 \
    -v /data/docker/mysql/jira/db:/var/lib/mysql \
    -v /data/docker/mysql/jira/conf:/etc/mysql/conf.d \
    -e MYSQL_ROOT_PASSWORD=123456 \
    -e MYSQL_DATABASE=jira \
    -e MYSQL_USER=jira \
    -e MYSQL_PASSWORD=jira \
    mysql:5.6

# docker run -d \
    --name=jira \
    --hostname=jira \
    --link=mysql-jira:mysql \
    --restart=always \
    --privileged=true \
    -p 9205:8080 \
    lowmem0ry/jira

```
- 5.7的mysql会报如下错误：
```
Unknown system variable 'storage_engine'
```
5.6一切正常，建议使用5.6.

### 破解 jira

[破解文件](http://pan.baidu.com/s/1dEXwA21) 密码：d10q 包含两个破解文件和一个汉化文件，一起下载即可。

```bash
#进入docker
# docker exec -it jira /bin/sh

#备份文件
# mv /opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-2.2.2.jar /opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-2.2.2.jar.bak
# mv /opt/atlassian/jira/atlassian-jira/WEB-INF/atlassian-bundled-plugins/atlassian-universal-plugin-manager-plugin-2.19.1.jar /opt/atlassian/jira/atlassian-jira/WEB-INF/atlassian-bundled-plugins/atlassian-universal-plugin-manager-plugin-2.19.1.jar.bak

#拷贝破解文件覆盖系统文件
# sudo docker cp /home/gench/atlassian-extras-2.2.2.jar jira:/opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-2.2.2.jar
# sudo docker cp /home/gench/atlassian-universal-plugin-manager-plugin-2.19.1.jar jira:/opt/atlassian/jira/atlassian-jira/WEB-INF/atlassian-bundled-plugins/atlassian-universal-plugin-manager-plugin-2.19.1.jar
#或者当前目录执行拷贝
# sudo docker cp ./atlassian-extras-2.2.2.jar jira:/opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-2.2.2.jar
# sudo docker cp ./atlassian-universal-plugin-manager-plugin-2.19.1.jar jira:/opt/atlassian/jira/atlassian-jira/WEB-INF/atlassian-bundled-plugins/atlassian-universal-plugin-manager-plugin-2.19.1.jar

#拷贝mysql驱动文件，如果不用mysql，可以忽略此步。
# sudo docker cp /home/gench/mysql-connector-java-5.1.42.jar jira:/opt/atlassian/jira/lib/mysql-connector-java-5.1.42.jar
#或者在当前目录拷贝
# docker cp ./mysql-connector-java-5.1.42.jar jira:/opt/atlassian/jira/lib/mysql-connector-java-5.1.42.jar
```
如果下载的破解文件和目标文件版本不一致，手工修改成目标版本文件再拷贝覆盖目标系统文件即可。
重启容器。

### 打开http://localhost:9205配置Jira

一路选择：
- I'll set it up myself
- My Own Database
Database setup：
```bash
Database Type：MySQL
Hostname：mysql
Port：3306
Database：jira
Username：jira
Password：jira
```
- Set up application properties
这里请勿输入中文，会报错。
- Specify your license key
```bash
Description=JIRA: Commercial,
CreationDate=2017-03-25,
jira.LicenseEdition=ENTERPRISE,
Evaluation=false,
jira.LicenseTypeName=COMMERCIAL,
jira.active=true,
licenseVersion=2,
MaintenanceExpiryDate=2099-12-31,
Organisation=GENCH,
SEN=SEN-L9480575,
ServerID=BTTV-B5E7-W7QX-ZYT0,
jira.NumberOfUsers=-1,
LicenseID=LIDSEN-L2651368,
LicenseExpiryDate=2099-12-31,
PurchaseDate=2017-05-25,
```
Organisation改成你自己的组织，可以随便写 SEN ，ServerID在授权信息上有的，改掉 确定就可以了
- Set up administrator account
例如：输入你的全称：root、邮件：xxx@xxx.com、用户名：root、密码：123456

- 其他的没有特殊设置，一路next下来即可。

### 中文汉化
 右上角的【系统设置】图标->【Add-ons】->【manage add-ons】->右侧边的【Upload add-on】在弹出的窗口中，选择前面下载的中文包->【Upload】
 耐心等待弹出【Installed and ready to go！】提示框，说明安装成功。

 右上角的【系统设置】图标->【System】->右侧边【Edit Settings】，找到【Internationalization】，将【Indexing language】->【Chinese】，将【Default language】->【中文(中国)】->最下方的【Update】。

 Ok，这时Jira将变成中文界面了。