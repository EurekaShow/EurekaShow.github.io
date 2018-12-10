# 部署 LAMP （CentOS 7） 搭建Wordpress

### 简介
LAMP指Linux+Apache+Mysql/MariaDB+Perl/PHP/Python是一组常用来搭建动态网站或者服务器的开源软件，本身都是各自独立的程序，但是因为常被放在一起使用，拥有了越来越高的兼容度，共同组成了一个强大的Web应用程序平台。

### 部署方式
安装包部署以及手动部署适合对Linux命令有基本了解的用户，可以满足用户个性化部署的要求。本教程主要介绍手动部署的方式。

### 手动部署
- 系统平台：CentOS 7.2
- Apache版本：2.4.23
- Mysql 版本：5.7.17
- Php版本：7.0.12
- Wrodpress 最新版本

####  安装前准备
CentOS 7系统默认开启了防火墙，需关闭后外部才可访问本机的80、21等端口，如需做安全类配置可自行参考官方文档。

关闭防火墙：
```
systemctl stop firewalld.service
```
关闭防火墙开机自启动:
```
systemctl disable firewalld.service
```
安装vim及unzip：
```
yum install -y vim unzip
```

#### 编译安装apache准备
编译安装apache前需要安装apr、apr-util和pcre软件包和相关依赖包。
``` cmd
yum install -y gcc gcc-c++ autoconf libtool
```
#### 安装apr
``` cmd
cd /usr/local/src/

wget http://oss.aliyuncs.com/aliyunecs/onekey/apache/apr-1.5.0.tar.gz

tar zxvf apr-1.5.0.tar.gz

cd apr-1.5.0

./configure --prefix=/usr/local/apr

make && make install
```

#### 安装apr-util
``` cmd
cd /usr/local/src/

wget http://oss.aliyuncs.com/aliyunecs/onekey/apache/apr-util-1.5.3.tar.gz

tar zxvf apr-util-1.5.3.tar.gz 

cd apr-util-1.5.3

./configure --prefix=/usr/local/apr-util --with-apr=/usr/loca/apr

make && make install
```

#### 安装pcre
``` cmd
cd /usr/local/src/

wget http://zy-res.oss-cn-hangzhou.aliyuncs.com/pcre/pcre-8.38.tar.gz 

tar zxvf pcre-8.38.tar.gz

cd pcre-8.38

./configure --prefix=/usr/local/pcre

make && make install
```

#### 编译安装Apache
``` cmd
cd /usr/local/src/

wget http://zy-res.oss-cn-hangzhou.aliyuncs.com/apache/httpd-2.4.23.tar.gz 

tar zxvf httpd-2.4.23.tar.gz

cd httpd-2.4.23

./configure \
--prefix=/usr/local/apache --sysconfdir=/etc/httpd \
--enable-so --enable-cgi --enable-rewrite \
--with-zlib --with-pcre=/usr/local/pcre \
--with-apr=/usr/local/apr \
--with-apr-util=/usr/local/apr-util \
--enable-mods-shared=most --enable-mpms-shared=all \
--with-mpm=event

make && make install
```

#### 为apache添加组／添加用户
groupadd apache
useradd -g apache -s /sbin/nologin apache

#### 修改httpd.conf配置文件参数
``` cmd
cd /etc/httpd/
vim httpd.conf
```
+  查找并设置User／Group为上面设置好的用户

+  找到Directory参数，注释掉Require all denied添加Require all granted。
``` xml
<Directory>
    AllowOverride none
    #Require all denied
    Require all granted
</Directory>
```
+ 找到ServerName参数，添加ServerName localhost:80 

+ 设置PidFile路径,在配置文件最后添加以下内容:
``` 
 PidFile  "/var/run/httpd.pid"
```

#### 启动Apache服务并验证
``` cmd
cd /usr/local/apache/bin/
./apachectl start
netstat -tnlp                             #查看服务是否开启
```
在本地浏览器中输入云服务器的公网IP地址验证，出现 It works! 表示安装成功。

#### 设置开机自启
在rc.local文件中添加/usr/local/apache/bin/apachectl start，然后输入:wq保存退出。
``` cmd
vim /etc/rc.d/rc.local
```

#### 设置环境变量
``` cmd
vim /root/.bash_profile
```
在PATH=$PATH:$HOME/bin添加参数为
``` cmd
PATH=$PATH:$HOME/bin:/usr/local/apache/bin
```
然后输入:wq保存退出，执行：
``` cmd
source /root/.bash_profile
```

#### 编译安装MySQL前预准备
首先检查系统中是否存在使用rpm安装的mysql或者mariadb，如果有需要先删除后再编译安装。
``` cmd
rpm -qa | grep mysql               #由下至上依次卸载
rpm -qa | grep mariadb
rpm -e xxx                           #一般使用此命令即可卸载成功    
rpm -e --nodeps xxx                  #卸载不成功时使用此命令强制卸载
```

卸载完以后用 rpm -qa|grep mariadb 或者 rpm -qa|grep mysql 查看结果。

#### 安装mysql

``` cmd
yum install -y libaio-*                         #安装依赖

mkdir -p /usr/local/mysql

cd /usr/local/src

wget http://zy-res.oss-cn-hangzhou.aliyuncs.com/mysql/mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz 

tar -xzvf mysql-5.7.17-linux-glibc2.5-x86_64.tar.gz

mv mysql-5.7.17-linux-glibc2.5-x86_64/* /usr/local/mysql/
```

#### 建立mysql组和用户，并将mysql用户添加到mysql组
``` cmd
groupadd mysql

useradd -g mysql -s /sbin/nologin mysql
```

#### 初始化mysql数据库
``` cmd
/usr/local/mysql/bin/mysqld --initialize-insecure --datadir=/usr/local/mysql/data/ --user=mysql
```

#### 更改mysql安装目录的属主属组
``` cmd
chown -R mysql:mysql /usr/local/mysql
```

#### 设置开机自启
``` cmd
cd /usr/local/mysql/support-files/

cp mysql.server  /etc/init.d/mysqld

chmod +x /etc/init.d/mysqld             # 添加执行权限

vim /etc/rc.d/rc.local     
```
添加/etc/init.d/mysqld start到rc.local文件中，然后输入:wq保存退出。

#### 设置环境变量
``` cmd
vi /root/.bash_profile
```
在PATH=$PATH:$HOME/bin添加参数为：
``` cmd
PATH=$PATH:$HOME/bin:/usr/local/apache/bin:/usr/local/mysql/bin:/usr/local/mysql/lib
```
然后输入:wq保存退出，输入:
``` cmd
source /root/.bash_profile
```
#### 启动Mysql
``` cmd
/etc/init.d/mysqld start
```
#### 修改Mysql的root用户密码
初始化后mysql为空密码可直接登录，为了保证安全性需要修改mysql的root用户密码。
``` cmd
mysqladmin -u root password 'xxxx'
```
#### 测试登录MySQL数据库
``` cmd
mysql -uroot -p密码                           #-p和密码之间无空格
```
#### 测试登录MySQL数据库
``` cmd
mysql -uroot -p                          #-p和密码之间无空格
```
#### 编译安装php
依赖安装：
``` cmd
yum install php-mcrypt libmcrypt libmcrypt-devel  libxml2-devel  openssl-devel  libcurl-devel libjpeg.x86_64 libpng.x86_64 freetype.x86_64 libjpeg-devel.x86_64 libpng-devel.x86_64 freetype-devel.x86_64  libjpeg-turbo-devel   libmcrypt-devel   mysql-devel  -y
```
如果提示找不到Libmcrypt,mhash,mcrypt包，怎需要手动下载，然后上传到服务器src目录。

##### 1 先安装Libmcrypt
``` cmd
cd /usr/local/src/

tar -zxvf libmcrypt-2.5.8.tar.gz

cd libmcrypt-2.5.8

./configure

make
make install 说明：libmcript默认安装在/usr/local 
```
##### 2 安装mhash
``` cmd
cd /usr/local/src/

tar -zxvf mhash-0.9.9.9.tar.gz

cd mhash-0.9.9.9

./configure

make
make install
```
##### 2 安装mcrypt
``` cmd
tar -zxvf mcrypt-2.6.8.tar.gz

cd mcrypt-2.6.8

LD_LIBRARY_PATH=/usr/local/lib ./configure

make
make install
```

``` cmd
wget http://zy-res.oss-cn-hangzhou.aliyuncs.com/php/php-7.0.12.tar.gz

tar zxvf php-7.0.12.tar.gz

cd php-7.0.12

./configure \
--prefix=/usr/local/php \
--enable-mysqlnd \
--with-mysqli=mysqlnd --with-openssl \
--with-pdo-mysql=mysqlnd \
--enable-mbstring \
--with-freetype-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib --with-libxml-dir=/usr \
--enable-xml  --enable-sockets \
--with-apxs2=/usr/local/apache/bin/apxs \
--with-mcrypt  --with-config-file-path=/etc \
--with-config-file-scan-dir=/etc/php.d \
--enable-maintainer-zts \
--disable-fileinfo

make && make install
```


#### 复制配置文件
``` cmd
cd php-7.0.12
cp php.ini-production /etc/php.ini
```

#### 编辑apache配置文件httpd.conf，以apache支持php
``` cmd
vim /etc/httpd/httpd.conf
```
在配置文件最后添加如下二行：
``` cmd
AddType application/x-httpd-php  .php 
AddType application/x-httpd-php-source  .phps
```
定位到 DirectoryIndex index.html修改为：
``` cmd
DirectoryIndex  index.php  index.html
```
#### 重启apache服务
``` cmd
/usr/local/apache/bin/apachectl restart
```
#### 测试是否能够正常解析PHP
``` php
 cd  /usr/local/apache/htdocs/

 vim index.php                #添加如下内容

<?php
phpinfo();
?>
```
#### 安装phpmyadmin
``` cmd
mkdir -p /usr/local/apache/htdocs/phpmyadmin

cd /usr/local/src/

wget http://oss.aliyuncs.com/aliyunecs/onekey/phpMyAdmin-4.1.8-all-languages.zip

unzip phpMyAdmin-4.1.8-all-languages.zip

mv phpMyAdmin-4.1.8-all-languages/* /usr/local/apache/htdocs/phpmyadmin
```

### 搭建Wordpress平台
#### 下载最新版本的Wordpress
``` cmd
cd /usr/local/src/

wget http://wordpress.org/latest.zip
```
#### 解压
``` cmd
unzip latest.zip

mv wordpress/* /usr/local/apache/htdocs/wordpress
```
#### 设置文件夹权限
``` cmd
cd /usr/local/apache/htdocs/

chown -R apache:apache wordpress/
```

#### 创建一个可以上传的目录upload
``` cmd
mkdir -p /usr/local/apache/htdocs/wordpress/wp-content/uploads
```
#### 修改配置文件，以便可以访问数据库
``` cmd
cd /usr/local/apache/htdocs/wordpress/

cp wp-config-sample.php wp-config.php

vim wp-config.php
```
修改红色字体部分，分别为数据库名称、数据库用户名、数据库用户密码，大家根据实际修改
``` cmd
define('DB_NAME', 'wp_database'); 

define('DB_USER', 'root'); 

define('DB_PASSWORD', 'root'); 
```
#### 浏览器浏览  浏览器输入http://127.0.0.1/wordpress/wp-admin/install.php 后就可以进行最后的登陆安装，输入站点名称，登陆户名，密码，邮箱就可以完成Wordpress安装！
#### 开启支持网站固定链接修改和重定向功能。  编辑主配置文件：
``` cmd
vim /etc/httpd/conf/httpd.conf
```
``` cmd
#AllowOverride None 
AllowOverride All
```
保存退出，重启服务
``` cmd
/usr/local/apache/bin/apachectl start
```
#### 创建.htaccess文件：
``` cmd
cd /usr/local/apache/htdocs/wordpress/

touch .htaccess
```
#### 编辑.htaccess文件：
``` cmd
vim .htaccess

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /wordpress/
    RewriteRule ^index\.php$ - [L]
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /wordpress/index.php [L]
</IfModule>
```
#### 修改.htaccess文件权限：
chmod 664 .htaccess

至此，完成LAMP搭建，并顺利安装wordpress。
