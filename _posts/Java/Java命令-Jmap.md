# Java命令-Jmap

## 功能简介
jmap命令可以获得运行中的jvm的堆的快照，从而可以离线分析堆，以检查内存泄漏，检查一些严重影响性能的大对象的创建，检查系统中什么对象最多，各种对象所占内存的大小等等。

### 什么是堆Dump
堆Dump是反应Java堆使用情况的内存镜像，其中主要包括系统信息、虚拟机属性、完整的线程Dump、所有类和对象的状态等。 一般，在内存不足、GC异常等情况下，我们就会怀疑有内存泄露。这个时候我们就可以制作堆Dump来查看具体情况。分析原因。

## 命令简介

```
C:\Program Files\jdk1.8\bin>jmap
Usage:
    jmap [option] <pid>
        (to connect to running process)
    jmap [option] <executable <core>
        (to connect to a core file)
    jmap [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)

where <option> is one of:
    <none>               to print same info as Solaris pmap
    -heap                to print java heap summary
    -histo[:live]        to print histogram of java object heap; if the "live"
                         suboption is specified, only count live objects
    -clstats             to print class loader statistics
    -finalizerinfo       to print information on objects awaiting finalization
    -dump:<dump-options> to dump java heap in hprof binary format
                         dump-options:
                           live         dump only live objects; if not specified,
                                        all objects in the heap are dumped.
                           format=b     binary format
                           file=<file>  dump heap to <file>
                         Example: jmap -dump:live,format=b,file=heap.bin <pid>
    -F                   force. Use with -dump:<dump-options> <pid> or -histo
                         to force a heap dump or histogram when <pid> does not
                         respond. The "live" suboption is not supported
                         in this mode.
    -h | -help           to print this help message
    -J<flag>             to pass <flag> directly to the runtime system
```

### 参数说明：

#### 1)、options： 
```
executable     Java executable from which the core dump was produced.(可能是产生core dump的java可执行程序)
core 将被打印信息的core dump文件
remote-hostname-or-IP 远程debug服务的主机名或ip
server-id 唯一id,假如一台主机上多个远程debug服务，用此选项参数标识服务器
```

#### 2）基本参数：
```
<no option> 如果使用不带选项参数的jmap打印共享对象映射，将会打印目标虚拟机中加载的每个共享对象的起始地址、映射大小以及共享对象文件的路径全称。这与Solaris的pmap工具比较相似。
-dump:[live,]format=b,file=<filename> 使用hprof二进制形式,输出jvm的heap内容到文件, live子选项是可选的，假如指定live选项,那么只输出活的对象到文件. 
-finalizerinfo 打印正等候回收的对象的信息.
-heap 打印heap的概要信息，GC使用的算法，heap的配置及wise heap的使用情况.
-histo[:live] 打印每个class的实例数目,内存占用,类全名信息. VM的内部类名字开头会加上前缀”*”. 如果live子参数加上后,只统计活的对象数量. 
-permstat 打印classload和jvm heap长久层的信息. 包含每个classloader的名字,活泼性,地址,父classloader和加载的class数量. 另外,内部String的数量和占用内存数也会打印出来. 
-F 强迫.在pid没有响应的时候使用-dump或者-histo参数. 在这个模式下,live子参数无效. 
-h | -help 打印辅助信息 
-J<flag> 传递参数给jmap启动的jvm. 
pid 需要被打印配相信息的java进程id,可以用jps查问.
```
### 查看内存堆使用情况 jmap -head <pid>

```
C:\Program Files\jdk1.8\bin>jmap -heap 8488
Attaching to process ID 8488, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.31-b07

using thread-local object allocation.
Parallel GC with 4 thread(s)

Heap Configuration:                                   #堆内存初始化配置
   MinHeapFreeRatio         = 0                       #-XX:MinHeapFreeRatio设置JVM堆最小空闲比率  
   MaxHeapFreeRatio         = 100                     #-XX:MaxHeapFreeRatio设置JVM堆最大空闲比率
   MaxHeapSize              = 805306368 (768.0MB)     #-XX:MaxHeapSize=设置JVM堆的最大大小
   NewSize                  = 44564480 (42.5MB)       #-XX:NewSize=设置JVM堆的‘新生代’的默认大小
   MaxNewSize               = 268435456 (256.0MB)     #-XX:MaxNewSize=设置JVM堆的‘新生代’的最大大小
   OldSize                  = 89653248 (85.5MB)       #-XX:OldSize=设置JVM堆的‘老生代’的大小
   NewRatio                 = 2                       #-XX:NewRatio=:‘新生代’和‘老生代’的大小比率
   SurvivorRatio            = 8                       #-XX:SurvivorRatio=设置年轻代中Eden区与Survivor区的大小比值
   MetaspaceSize            = 21807104 (20.796875MB)  
   CompressedClassSpaceSize = 1073741824 (1024.0MB)   
   MaxMetaspaceSize         = 17592186044415 MB       
   G1HeapRegionSize         = 0 (0.0MB)

Heap Usage:
PS Young Generation
Eden Space:
   capacity = 68157440 (65.0MB)
   used     = 6451136 (6.15228271484375MB)
   free     = 61706304 (58.84771728515625MB)
   9.465050330528847% used
From Space:
   capacity = 5242880 (5.0MB)
   used     = 5232464 (4.9900665283203125MB)
   free     = 10416 (0.0099334716796875MB)
   99.80133056640625% used
To Space:
   capacity = 5242880 (5.0MB)
   used     = 0 (0.0MB)
   free     = 5242880 (5.0MB)
   0.0% used
PS Old Generation
   capacity = 89653248 (85.5MB)
   used     = 4362096 (4.1600189208984375MB)
   free     = 85291152 (81.33998107910156MB)
   4.865519205729167% used

7927 interned Strings occupying 660568 bytes.
```
### 手工生成dump文件 jmap -dump:live,format=b,file=<dump file path> <pid>

```
C:\Program Files\jdk1.8\bin>jmap -dump:live,format=b,file=C:\temp\dumpt.bin 8488
Dumping heap to C:\temp\dumpt.bin ...
Heap dump file created
```

然后就可以用JvisualVM或者MAT查看内存占用情况了。
[JvisualVM 入门](http://itxiaofeng.com/2017/java-visualvm-%E7%B3%BB%E5%88%97%E4%B8%80%EF%BC%9A%E5%85%A5%E9%97%A8/)
