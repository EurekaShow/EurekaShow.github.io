# raspberry启动root账号

如果你需要使用sftp，那么你一定很需要root账号，开启root账号方法如下：

- 设置密码以激活root账号

默认的root账号是被禁用的，而启用的是pi账号。

```bash
pi@raspberrypi:~# sudo passwd root
Enter new UNIX password:   #输入第一遍密码
Retype new UNIX password:  #输入第二遍密码

pi@raspberrypi:~# sudo passwd --unlock root
passwd: password expiry information changed.
```
输入上面第一行代码 第二行是提示错误的代码
原因是 【新版本ssh默认关闭root登陆】 你可以修改一下ssh的配置文件

``` bash
pi@raspberrypi:~# sudo vim /etc/ssh/sshd_config
```

```conf
#修改
#PermitRootLogin without-password
#为
PermitRootLogin yes
```

如果没有PermitRootLogin without-password，则直接添加上面一行内容即可。