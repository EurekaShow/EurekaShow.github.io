# vscode调试virtualenv的python代码

- 1.终端激活virtualenv环境，然后用一下指令查看虚拟环境的python地址：

```python
#激活虚拟环境，找到路径。
(facenv) eureka@ubuntu:~/Documents/face/facenc$ which python
/home/eureka/Documents/face/facenv/bin/python
```

- 2.打开vscode,在vscode中的【资源管理器】中打开python项目，打开【调试】添加配置python环境，选择 python当前文件(扩展终端)。

回到【资源管理器】,打开settings.json,检索里面输入python.pythonPath,点击左侧的铅笔，修改配置，在右侧值里面粘贴刚才查到的路径。如下：

```conf
{
    "python.pythonPath": "/home/eureka/Documents/face/facenv/bin/python"
}
```

- 3.回到【调试】，点击顶部配置的调试按钮即可开始调试当前虚拟环境的python当前打开的文件了。