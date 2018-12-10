# Java VisualVM 系列一：入门

####下载地址
各版本的JDK安装后都附带有该工具，位置在JDK目录下的bin目录下。
单独下载安装地址：
[最新版本下载地址](https://visualvm.github.io/)
[各版本下载地址列表](https://visualvm.github.io/releases.html)

####启动
windwos/macOS系统中，打开bin文件夹，双击执行jvisualvm即可，或者命令行调用。
![visualVM启动界面](http://itxiaofeng.com/wp-content/uploads/2017/10/startup.png)

####插件安装
我们使用JVisualVM都是要先安装插件的.VisualVM打开后，会发现功能比较单一，只有概述、监视、线程、抽样器、Profiler五个选项卡，只能对JVM进行内存和线程的基础监控和分析。so不装各种功能强大牛x闪闪的插件还玩什么那？
启动jvisualvm后，
- 1. 从主菜单中选择“工具（Tools）/插件（Plugins）”。
- 2. 在“可用插件（available plugins）”标签中，选中对应的插件，单击“安装”。
- 3. 等待插件更新安装完成。

####插件安装-解决JDK自带的jvisualvm无法获取插件问题（java.net网站已关闭）
由于java.net网站已经关闭，jvisualvm已经移到Github，JDK1.8及以前自带的jvisualvm的插件地址已经无法获取到插件。我们需要修改插件地址：
修改插件地址的方法：
- 1. 从主菜单中选择“工具（Tools）/插件（Plugins）”。
- 2. 在“设置（Settings）”标签中，单击右下方的“添加（add）”按钮，输入名称和对应的url地址。
![配置完成后](http://itxiaofeng.com/wp-content/uploads/2017/10/settings.png)
[各版本对应的插件更新URL地址](https://visualvm.github.io/pluginscenters.html)。
- 3. 添加成功后，回到“可用插件（available plugins）”标签，这时就可以看到许许多多的可用插件了。选中安装即可。
![插件添加成功后](http://itxiaofeng.com/wp-content/uploads/2017/10/pluginsinstalled.png)

####可以使用咯
完成后的我们打开看看。
![安装成功后如图](http://itxiaofeng.com/wp-content/uploads/2017/10/allok.png)




