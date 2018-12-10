# Nginx连接超时配置

## Nginx的配置里，设置如下：

```conf
 upstream  sfeng.me {  #服务器集群名字
        server    192.168.88.103:8080  weight=1 ;    #tomcat1
        server    192.168.88.103:8082  weight=1 ;   #tomcat2
        server    192.168.88.103:8084  backup ;     #tomcat3
    }

location / {  
            proxy_pass http://sfeng.me;  
            proxy_redirect default;  
   proxy_connect_timeout 10;
        }  
```

此配置意思是，每个从Nginx分发的请求，连接到后台（tomcat X）的连接如果超过10秒，则视为连接失败，Nginx会将此请求分发到另一台tomcat。在一段时期内（现在不知道有多长），后续的请求都不会再发送到tomcat X了。过了一段时期后再送请求，又有可能把请求发送到tomcat X。此时，只要超时一次，则在往后一段时间内不再往tomcatX分发。

现在，如果我把tomcat1关闭，获取页面的请求用了10.033秒时间。我的理解是，这个请求被分发到tomcat1，然而此机已经关闭了，所以等了10秒。10秒后Nginx还没收到响应，则将请求往另一台机分发（tomcat2），而另一台机只用了0.033秒的时间就响应了。而页面里的css文件和js文件都在这时间基础上往tomcat2发送请求获取。

## 如果我将Nginx的配置改成如下：

```conf
 #服务器的集群  
    upstream  sfeng.me {  #服务器集群名字
        #server    192.168.218.129:8080  weight=1 max_fails=2 fail_timeout=600s;  
        #server    192.168.218.131:8080  weight=1 max_fails=2 fail_timeout=600s;  
        server    192.168.88.103:8080  weight=2 max_fails=2;  #tomcat1
        server    192.168.88.103:8082  weight=2 max_fails=2;  #tomcat2
        server    192.168.88.103:8084  backup ;    #tomcat3
    }

location / {  
            proxy_pass http://sfeng.me;  
            proxy_redirect default;  
    proxy_connect_timeout 10;
        }  
```

在分发的机子后面多了max_fails=2的配置。请求主页面的时候用了11.037秒，即首先Nginx把请求分发给tomcat1,由于tomcat1已经关闭，所以Nginx等了10秒都没得到响应，于是把原请求分发到tomca2，tomcat2用了1.037秒就响应了。然后在此时间基础上，页面并发地向Nginx发请求获取静态资源，这时有4个js请求首次是发向tomcat1。

对此，我猜测是这样。Nginx是按10秒作为监测间隔。第一个10秒内，发向tomcat1有一个请求超时，所以此时tomcat1仍生效。到了第二个10秒内，有4个请求发往tomcat1，且都超时，因为超时次数大于2次，所以后续页面其他的静态资源全部没再往tomcat1分发。但过一段时间后，我如果刷新页面，依旧有请求会被分发到tomcat1去。

也就是说，过了一段时间后，Nginx会把tomcat1当作正常的服务器，往它发分请求。而从上次认为异常到下次重新视为正常状态这个时间段有多长，我现在不知道。

这样的优点是，tomcat1挂掉了，但后续修复好后，直接重启tomcat1就行了。但缺点也很明显，在未修复重启前，每隔一段时间都会有某些请求会往tomcat1发送，这样就总会有某些请求要等至少10秒。如果没有设置max_fails值，则每10秒内只有一个请求要等10秒，如果设置为2以上，则就会很多了。

## 如果我再修改下Nginx配置如下：

```conf
#服务器的集群  
    upstream  netitcast.com {  #服务器集群名字
        server    192.168.88.103:8080  weight=2 max_fails=2 fail_timeout=20s;  #tomcat1
        server    192.168.88.103:8082  weight=2 max_fails=2 fail_timeout=20s;  #tomcat2

         server    192.168.88.103:8084  backup ;    #tomcat3

    }
```

这次配置多了fail_timeout属性。也就是说，在20秒内，后续的请求都不再往tomcat1分发了。无论刷多少遍都一样。从页面显示的机子号可看得出来。
所以多了fail_timeout属性后，在指定的时间段内连接超时次数达到max_fails次数后，这台机子就临时被判了死刑。
这样配置的优点是，第一个10秒内分发到tomcat1的请求要等至少10秒，当机子被判死刑后，所有请求都往活着的机子分发了。而当tomcat1机子修复后并重启，就能正常使用了。
针对这种配置，假如我设置fail_timeout=600s，继续关闭tomcat2，则由tomcat3这后备机来处理请求。如果tomcat3也关闭，会报505网关异常。

[引用](https://blog.csdn.net/yyb_gz/article/details/55004967)