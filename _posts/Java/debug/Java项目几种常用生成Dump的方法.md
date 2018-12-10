# Java项目几种常用生成Dump的方法

系统有时会遇到OutOfMemoryError，Java堆溢出了。我们需要找到造成OutOfMemoryError原因。一般有两种情况：

- 1、内存泄露，对象已经死了，无法通过垃圾收集器进行自动回收；

- 2、内存溢出，内存中的对象都还必须存活着，这说明Java堆分配空间不足，检查堆设置大小（-Xmx与-Xms），检查代码是否存在对象生命周期太长、持有状态时间过长的情况。

## 1.想在泄漏未发生前，取堆转储文件分析， 通过jvm参数Dump出当前的内存转储快照。
在tomcat bin目录下找到catalina.bat(windows)/catalina.sh(linux),找到set JAVA_OPTS，
```
set "JAVA_OPTS=%JAVA_OPTS% -Djava.protocol.handler.pkgs=org.apache.catalina.webresources"
```
增加 -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=D:\heapdump,增加后的set项如下。保存文件，重启tomcat。
```
set "JAVA_OPTS=%JAVA_OPTS% -Djava.protocol.handler.pkgs=org.apache.catalina.webresources -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=D:\heapdump"
```
这样，当发生OOME时，会生成名称为 java_pid<pid>.hprof 文件。

## 2.通过用jmap生产dump文件。
windows通过任务管理器查看tomcat的进程pid，linux用ps命令查看进程pid，然后用jmap命令
```
- 1.Java5：jmap -heap:format=b <pid>
- 2.Java6+：jmap -dump:format=b,file=C:\temp\dumpt.bin <pid>
- 3.java8：jmap -dump:live,format=b,file=C:\temp\dumpt.bin <pid>
```
## 3.通过JavaVisualVM生成Dump文件

- 1.启动JvisuvalVM，如果已经安装了JDK，该命令位于bin目录。
- 2.加载正在执行的本地或者远程的Java项目。
- 3.选中项目，右键“生成堆Dump”和“生成线程Dump”及“启用当发生OOME时生成堆Dump”以公选择。
