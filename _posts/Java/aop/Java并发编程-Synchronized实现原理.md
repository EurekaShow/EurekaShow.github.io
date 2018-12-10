# Java并发编程-Synchronized实现原理

用事实说话，用代码演示，先请出我们的基础：

```java

public class SynchronizedTest {

    public void operation() {

        synchronized (this) {
            try{
            System.out.println("operation-start...");
            System.out.println("operation-execute...");
            Thread.sleep(3000);
            System.out.println("operation-end...");
            }catch (Throwable ex){}
        }
    }

    public void operationD() {

        synchronized (this) {
            try{
            System.out.println("operationD-start...");
            System.out.println("operationD-execute...");
            Thread.sleep(3000);
            System.out.println("operationD-end...");
            }catch (Throwable ex){}
        }
    }

    public synchronized void  operationS(){
        try{
            System.out.println("operationS-start...");
            System.out.println("operationS-execute...");
            Thread.sleep(3000);
            System.out.println("operationS-end...");
        }catch (Throwable ex){}
    }

    public synchronized void  operationSD() {
        try{
            System.out.println("operationSD-start...");
            System.out.println("operationSD-execute...");
            Thread.sleep(3000);
            System.out.println("operationSD-end...");
        }catch (Throwable ex){}
    }

    public static synchronized void  operationSS(){
        try{
            System.out.println("operationSS-start...");
            System.out.println("operationSS-execute...");
            Thread.sleep(3000);
            System.out.println("operationSS-end...");
        }catch (Throwable ex){}

    }

    public static synchronized void  operationSSD(){
        try{
            System.out.println("operationSSD-start...");
            System.out.println("operationSSD-execute...");
            Thread.sleep(3000);
            System.out.println("operationSSD-end...");
        }catch (Throwable ex){}
    }

}
```

代码编译后通过我们来看下字节码，直接执行javap反编译字节码：

```java
javap -c -verbose SynchronizedTest.class
```

把具有代表性的三个方法operation/operationS/operationSS拿出来，字节码如下：

```java
  public void operation();
    descriptor: ()V
    flags: ACC_PUBLIC
    Code:
      stack=2, locals=4, args_size=1
         0: aload_0
         1: dup
         2: astore_1
         3: monitorenter
         4: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
         7: ldc           #3                  // String operation-start...
         9: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        12: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
        15: ldc           #5                  // String operation-execute...
        17: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        20: ldc2_w        #6                  // long 3000l
        23: invokestatic  #8                  // Method java/lang/Thread.sleep:(J)V
        26: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
        29: ldc           #9                  // String operation-end...
        31: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        34: goto          38
        37: astore_2
        38: aload_1
        39: monitorexit
        40: goto          48
        43: astore_3
        44: aload_1
        45: monitorexit
        46: aload_3
        47: athrow
        48: return
      Exception table:
         from    to  target type
             4    34    37   Class java/lang/Throwable
             4    40    43   any
            43    46    43   any
      LineNumberTable:
        line 7: 0
        line 9: 4
        line 10: 12
        line 11: 20
        line 12: 26
        line 13: 34
        line 14: 38
        line 15: 48
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
           38       0     2    ex   Ljava/lang/Throwable;
            0      49     0  this   Lcom/training/thread/SynchronizedTest;
      StackMapTable: number_of_entries = 4
        frame_type = 255 /* full_frame */
          offset_delta = 37
          locals = [ class com/training/thread/SynchronizedTest, class java/lang/Object ]
          stack = [ class java/lang/Throwable ]
        frame_type = 0 /* same */
        frame_type = 68 /* same_locals_1_stack_item */
          stack = [ class java/lang/Throwable ]
        frame_type = 250 /* chop */
          offset_delta = 4
public synchronized void operationS();
    descriptor: ()V
    flags: ACC_PUBLIC, ACC_SYNCHRONIZED
    Code:
      stack=2, locals=2, args_size=1
         0: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
         3: ldc           #14                 // String operationS-start...
         5: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
         8: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
        11: ldc           #15                 // String operationS-execute...
        13: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        16: ldc2_w        #6                  // long 3000l
        19: invokestatic  #8                  // Method java/lang/Thread.sleep:(J)V
        22: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
        25: ldc           #16                 // String operationS-end...
        27: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        30: goto          34
        33: astore_1
        34: return
      Exception table:
         from    to  target type
             0    30    33   Class java/lang/Throwable
      LineNumberTable:
        line 31: 0
        line 32: 8
        line 33: 16
        line 34: 22
        line 35: 30
        line 36: 34
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
           34       0     1    ex   Ljava/lang/Throwable;
            0      35     0  this   Lcom/training/thread/SynchronizedTest;
      StackMapTable: number_of_entries = 2
        frame_type = 97 /* same_locals_1_stack_item */
          stack = [ class java/lang/Throwable ]
        frame_type = 0 /* same */
  public static synchronized void operationSS();
    descriptor: ()V
    flags: ACC_PUBLIC, ACC_STATIC, ACC_SYNCHRONIZED
    Code:
      stack=2, locals=1, args_size=0
         0: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
         3: ldc           #20                 // String operationSS-start...
         5: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
         8: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
        11: ldc           #21                 // String operationSS-execute...
        13: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        16: ldc2_w        #6                  // long 3000l
        19: invokestatic  #8                  // Method java/lang/Thread.sleep:(J)V
        22: getstatic     #2                  // Field java/lang/System.out:Ljava/io/PrintStream;
        25: ldc           #22                 // String operationSS-end...
        27: invokevirtual #4                  // Method java/io/PrintStream.println:(Ljava/lang/String;)V
        30: goto          34
        33: astore_0
        34: return
      Exception table:
         from    to  target type
             0    30    33   Class java/lang/Throwable
      LineNumberTable:
        line 49: 0
        line 50: 8
        line 51: 16
        line 52: 22
        line 53: 30
        line 55: 34
      LocalVariableTable:
        Start  Length  Slot  Name   Signature
           34       0     0    ex   Ljava/lang/Throwable;
      StackMapTable: number_of_entries = 2
        frame_type = 97 /* same_locals_1_stack_item */
          stack = [ class java/lang/Throwable ]
        frame_type = 0 /* same */

```

开始测试前，通过字节码我们得出如下结论：

- 1. **synchronized应用在代码块的时候，是通过MONITORENTER、MONITOREXIT实现的同步。**
- 2. **synchronized应用在方法的时候，是对方法生成一个ACC_SYNCHRONIZED的flags来实现。**
        *synchronized应用在方法的时候，字节码中已经没有了MONITORENTER、MONITOREXIT的影子，仔细观察后，*
        *不过相对于普通方法，其常量池中多了ACC_SYNCHRONIZED标示符。JVM就是根据该标示符来实现方法的同步的：*
        *当方法调用时，调用指令将会检查方法的 ACC_SYNCHRONIZED 访问标志是否被设置，*
        *如果设置了，执行线程将先获取monitor，获取成功之后才能执行方法体，*
        *方法执行完后再释放monitor。在方法执行期间，其他任何线程都无法再获得同一个monitor对象。*
        *其实本质上没有区别，只是方法的同步是一种隐式的方式来实现，无需通过字节码来完成。*

然后是我们的测试代码，实践检验真知：

```java

    public static void main(String[] args) {

        /**
         *P1 
        */
        final SynchronizedTest test = new SynchronizedTest();

        new Thread(() -> test.operation()).start();

        new Thread(() -> test.operationD()).start();

        /**
        *P2 
         */
        final SynchronizedTest testF = new SynchronizedTest();

        new Thread(() -> testF.operationS()).start();

        new Thread(() -> testF.operationSD()).start();

        /**
         *P3
         */
        final SynchronizedTest testE = new SynchronizedTest();
        final SynchronizedTest testE1 = new SynchronizedTest();

        new Thread(() -> testE.operationS()).start();

        new Thread(() -> testE1.operationSD()).start();

        /**
         *P4
         */
        new Thread(() -> SynchronizedTest.operationSS()).start();

        new Thread(() -> SynchronizedTest.operationSSD()).start();

     }
```

根据执行结果，我们得出如下结论：

- **P1代码块正常按照顺序执行。**

*通过字节码可以看出来，是通过MONITORENTER、MONITOREXIT，实现同步，*
*如果代码块没有try/catch,编译后会自动添加try/catch，所以，在字节码中能看到两个MONITOREXIT。*

- **P2 正常顺序执行。**

*但是字节码中已经没有了MONITORENTER、MONITOREXIT的影子，仔细观察后，*
*不过相对于普通方法，其常量池中多了ACC_SYNCHRONIZED标示符。JVM就是根据该标示符来实现方法的同步的：*
*当方法调用时，调用指令将会检查方法的 ACC_SYNCHRONIZED 访问标志是否被设置，*
*如果设置了，执行线程将先获取monitor，获取成功之后才能执行方法体，*
*方法执行完后再释放monitor。在方法执行期间，其他任何线程都无法再获得同一个monitor对象。*
*其实本质上没有区别，只是方法的同步是一种隐式的方式来实现，无需通过字节码来完成。*

- **P3 同时执行。**
  
*因为每个对象有一个监视器锁（monitor）。当monitor被占用时就会处于锁定状态，*
*线程执行monitorenter指令时尝试获取monitor的所有权，过程如下：*
*1、如果monitor的进入数为0，则该线程进入monitor，然后将进入数设置为1，该线程即为monitor的所有者。*
*2、如果线程已经占有该monitor，只是重新进入，则进入monitor的进入数加1.*
*3.如果其他线程已经占用了monitor，则该线程进入阻塞状态，直到monitor的进入数为0，再重新尝试获取monitor的所有权。*
*这段代码我们同时实例化了两个对象，monitor是属于对象的，故此针对不同的对象不存在锁竞争问题，所以没有阻塞。*

- **P4 正常顺序执行。**
  
*普通方法的同步锁在头文件，静态方法的同步锁则是基于类型，所以相同类的静态方法会按顺序依次执行。*

[代码下载地址](https://github.com/EurekaShow/daily-practice/tree/master/primer/java-primer/src/main/java/com/training/thread)