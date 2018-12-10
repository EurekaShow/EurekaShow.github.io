# MacOs使用shuttle和sshpass支持多ssh登录信息保存

### 缘起
最近ZOC一直提示注册，各种不舒服，另外一台上一直有问题。决定找一个免费的SSH客户端。
windows上有很多经典的工具，比如我正在用的MobaXterm就是我认为最好用的之一，
可在Mac下就各种不舒服。

### shuttle + sshpass

费了很大劲终于找到一个简洁而又方便的方法，shuttle + sshpass可以轻松胜任。
如果你是处女座，那么还可以再配上iTerm 2 + Oh My Zsh，那滋味，酸爽。

废话少说，先讲怎么用shuttle + sshpass实现多ssh登陆信息保存。

- 1.下载sshpass
[下载请移步这里](http://sourceforge.net/projects/sshpass/files/)

下载后解压，进入目录，执行：

```bash
# ./configure \
make \
make install
```

一般不会有什么错误，接着查看下是否正常即可。

```bash
# sshpass -h
```

- 2.下载安装shuttle
[下载请移步这里](http://fitztrev.github.io/shuttle/)

下载完成后解压拖拽的Application中即可。打开后在顶部有一个小火箭的图表，类似这样的：🚀

单击图标，在弹出菜单上一次选择【settings】-【edit】
跳出的config文件，我们只需要修改该文件，把我们的ssh服务器信息记录在这里即可。

```json
{
  "_comments": [
    "Valid terminals include: 'Terminal.app' or 'iTerm'",
    "In the editor value change 'default' to 'nano', 'vi', or another terminal based editor.",
    "Hosts will also be read from your ~/.ssh/config or /etc/ssh_config file, if available",
    "For more information on how to configure, please see http://fitztrev.github.io/shuttle/"
  ],
  "editor": "default",
  "launch_at_login": false,
  "terminal": "Terminal.app",
  "iTerm_version": "nightly",
  "default_theme": "Homebrew",
  "open_in": "new",  
  "show_ssh_config_hosts": false,
  "ssh_config_ignore_hosts": [  ],
  "ssh_config_ignore_keywords": [  ],
  "hosts": [
    {
      "cmd": "ps aux | grep defaults",
      "name": "Grep - Opens in Default-window-theme-title"
    },

    {
      "Product": [
        {
          "cmd": "sshpass -p xxxx ssh root@1xx.xx.xxx.xx",
          "name": "CI Server"
        }
      ]
    }
  ]
}       
```

Product 即为我添加的内容。-p 后为账号密码，前提是你必须安装了sshpass，否则这里一定会报错。

至此，大功告成，保存配置文件，你再点击小火箭图标，看看有没有多一个Product菜单，展开后有一个CI Server有没有？点击即可使用。
