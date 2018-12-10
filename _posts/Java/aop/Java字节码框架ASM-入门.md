# Java字节码框架之ASM入门

ASM 是一个 Java 字节码操纵框架。它可以直接以二进制形式动态地生成子类或其他代理类，或者在装载时动态地修改类。ASM 提供类似于 BCEL 和 SERP 之类的工具包的功能，但是被设计得更小巧、更快速，这使它适用于实时代码插装。

依赖环境

```xml
<dependency>
    <groupId>asm</groupId>
    <artifactId>asm</artifactId>
    <version>3.3.1</version>
</dependency>
```

接着，我们在开始我们惊险刺激的coding历程。

首先，我们创建一个最简单的Java类

```java
package com.training.aop.asm.t1;

public class AsmTester {

        public void run()
        {
            System.out.println("This is my first ASM test");
        }
}
```

接着，我们编译这个类得到一个class文件。编译过程省略，我们接着要把class类转换成字节码代码：
在class类所在的目录，放一个我们要用的转换成字节码工具的jar文件：asmtools.jar，该jar文件为OpenJDK自带的工具，可以自己编译，也直接直接到这里下载编译好的：

[asmtools.jar下载](https://github.com/EurekaShow/notebook/blob/master/Java/bytecode/asmtools.jar)

接着，我们打开终端工具，cd到我们class文件的目录下，前提条件是已经下载了asmtools.jar并且已经放置在该目录下(不放置class文件目录下也可以，需要配置文件所在位置到系统的环境变量)。

```java
java -cp asmtools.jar org.openjdk.asmtools.jdis.Main AsmTester.class > AsmTester.jasm
```

用vscode打开AsmTester.jasm文件：

```java
package  com/training/aop/asm/t1;

super public class AsmTester
	version 52:0
{


public Method "<init>":"()V"
	stack 1 locals 1
{
		aload_0;
		invokespecial	Method java/lang/Object."<init>":"()V";
		return;
	
}

public Method run:"()V"
	stack 2 locals 1
{
		getstatic	Field java/lang/System.out:"Ljava/io/PrintStream;";
		ldc	String "This is my first ASM test";
		invokevirtual	Method java/io/PrintStream.println:"(Ljava/lang/String;)V";
		return;
	
}

} // end Class AsmTester
```

接着我们要用代码生成一个和AsmTester类相同的字节码文件：

- 首先，要定义一个类

```java
/**
         * 动态创建一个类，有一个无参数的构造函数
         */
        static ClassWriter createClassWriter(String className)
        {
            ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
            //声明一个类，使用JDK1.8版本，public的类，父类是java.lang.Object，没有实现任何接口
            cw.visit(52, Opcodes.ACC_PUBLIC, className, null, "java/lang/Object", null);
            //初始化一个无参的构造函数，根据上面的字节码可以看出来，即使我们没有声明无参构造函数，编译器也会给我们默认生成一个。
            MethodVisitor constructor = cw.visitMethod(Opcodes.ACC_PUBLIC, "<init>", "()V", null, null);
            //这里请看字节码代码
            constructor.visitVarInsn(Opcodes.ALOAD, 0);
            //执行父类的init初始化
            constructor.visitMethodInsn(Opcodes.INVOKESPECIAL, "java/lang/Object", "<init>", "()V");
            //从当前方法返回void
            constructor.visitInsn(Opcodes.RETURN);
            constructor.visitMaxs(1, 1);
            constructor.visitEnd();
            return cw;
        }
```

- 接着，我们来定义run方法：

```java
/**
         * 创建一个run方法，里面只有一个输出
         * public void run()
         * {
         * 		System.out.println(message);
         * }
         * @return
         * @throws Exception
         */
        static byte[] createVoidMethod(String className, String message) throws Exception
        {
            //注意，这里需要把classname里面的.改成/，如com.asm.Test改成com/asm/Test
            ClassWriter cw = createClassWriter(className.replace('.', '/'));

            //创建run方法
            //()V表示函数，无参数，无返回值
            MethodVisitor runMethod = cw.visitMethod(Opcodes.ACC_PUBLIC, "run", "()V", null, null);
            //先获取一个java.io.PrintStream对象
            runMethod.visitFieldInsn(Opcodes.GETSTATIC, "java/lang/System", "out", "Ljava/io/PrintStream;");
            //将int, float或String型常量值从常量池中推送至栈顶  (此处将message字符串从常量池中推送至栈顶[输出的内容])
            runMethod.visitLdcInsn(message);
            //执行println方法（执行的是参数为字符串，无返回值的println函数）
            runMethod.visitMethodInsn(Opcodes.INVOKEVIRTUAL, "java/io/PrintStream", "println", "(Ljava/lang/String;)V");
            runMethod.visitInsn(Opcodes.RETURN);
            runMethod.visitMaxs(1, 1);
            runMethod.visitEnd();

            return cw.toByteArray();
        }

```

- 自定义我们的类加载器，用来加载我们生成的字节码类

```java
 public class MyClassLoader extends ClassLoader {

        public MyClassLoader() {
            super(Thread.currentThread().getContextClassLoader());
        }

        public Class defineClassFromClassFile(String className, byte[] classFile) throws ClassFormatError {
            return defineClass(className, classFile, 0,
                    classFile.length);

        }
    }
```

- 最后，是字节码类的实例化和调用。

```java
 public static void main(String[] args) throws Exception
        {
            String className = "com.training.aop.asm.t1.AsmTester2";
            byte[] classData = createVoidMethod(className, "This is my first ASM test2");
            Class<?> clazz = new MyClassLoader().defineClassFromClassFile(className, classData);
            clazz.getMethod("run",null).invoke(clazz.newInstance());
        }
```

[代码下载地址](https://github.com/EurekaShow/daily-practice/tree/master/primer/java-primer/src/main/java/com/training/aop/asm/bytecode)