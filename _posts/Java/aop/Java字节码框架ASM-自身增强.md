# Java字节码框架ASM-自身增强

在[Java字节码框架ASM-动态生成子类](Java字节码框架ASM-动态生成子类.md)中,我们通过继承实现子类再转换为父类类型的方式实现了强化，
是否可以直接通过强化自身来实现呢？答案是可以，通过强化自身来实现调用时无法转换为自身类，也就无法用自身类实例调用，需要一个折中的办法。
下面我们来看下动态给Account方法增加调用前调用后记录日志，通过字节码修改来强化自身。

先上基础的POJO：
我们有一个Account对象，代码如下：

```java
public class Account {

    public Account()
    {}

    public String operation() {
        System.out.println("operation...");
        return "operation...";
        //TODO some real operation
    }

}
```

然后，我们需要对Account的操作做一个日志记录的类如下：

```java
public class Log {
    public static void before() {
        System.out.println("before log ...");
        //TODO real security check
    }

    public static void after() {
        System.out.println("after log ...");
        //TODO real security check
    }
}
```

首先，还是确认下ASM库是否引入：

```xml
<dependency>
    <groupId>asm</groupId>
    <artifactId>asm</artifactId>
    <version>3.3.1</version>
</dependency>

```

因为ASM库应用广泛，spring或者是日常高频使用的库，基本上都依赖它。所以，你的项目可能已经间接引入了ASM的jar包,那么，就不需要专门再引入了。

然后，手术刀准备好我们就要开始我们的操作了。

老规矩先上我们的class-adepter,在visitMethod中，我们对特定方法进行了修改，具体如下：

```java
public class LogClassAdapter extends ClassAdapter {

    public LogClassAdapter(ClassVisitor cv)
    {
        super(cv);
    }

    @Override
    public MethodVisitor visitMethod(final int access, final String name,
                                     final String desc, final String signature, final String[] exceptions) {

        MethodVisitor mv = cv.visitMethod(access, name, desc, signature,exceptions);
         if("operation".equals(name))
        {
            return new LogMethodAdepter(mv);
        }
        return  mv;

    }

}
```

然后是我们的method-adapter，具体的实现动态修改字节码，插入日志的方法就在这里实现：

```java
public class LogMethodAdepter extends MethodAdapter {
    public LogMethodAdepter(MethodVisitor methodVisitor) {
        super(methodVisitor);
    }

    //方法进入前，在原有字节码前面插入日志调用方法
    @Override
    public void visitCode() {
        super.visitMethodInsn(Opcodes.INVOKESTATIC, "com/training/aop/asm/selfenhancer/entity/Log", "before", "()V");
    }

    //方法调用结束的位置，在原有字节码后面插入日志调用方法
    @Override
    public void visitInsn(int opcode) {

        super.visitMethodInsn(Opcodes.INVOKESTATIC, "com/training/aop/asm/selfenhancer/entity/Log", "after", "()V");
        super.visitInsn(opcode);

    }

}
```

最后，我们要把实现的class-adapter应用到我们的Account类中：

```java

public class Generator{

    //我们的类加载器
    private class MyClassLoader extends ClassLoader {

        public MyClassLoader() {
            super(Thread.currentThread().getContextClassLoader());
        }

        public Class defineClassFromClassFile(String className, byte[] classFile) throws ClassFormatError {
            return defineClass(className, classFile, 0,
                    classFile.length);

        }
    }


    public void testAsmClassLoader() throws Exception {

        ClassReader cr = new ClassReader(Account.class.getName());

        ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);

        //加入我们自定义的class-adapter，改写account的字节码内容，达到动态调用效果。
        cr.accept(new LogClassAdapter(cw), ClassReader.SKIP_DEBUG);

        Class<?> clazz = new MyClassLoader().defineClassFromClassFile(Account.class.getName(), cw.toByteArray());

        clazz.getMethod("operation").invoke(clazz.newInstance());
    }

    public static void main(String[] args) throws Exception {
        new Generator().testAsmClassLoader();
    }

}
```

执行输出如下：

```java
before log ...
operation...
after log ...
```

正是我们想要的效果，方法执行前后执行个对应的日志记录方法。
[代码下载地址](https://github.com/EurekaShow/daily-practice/tree/master/primer/java-primer/src/main/java/com/training/aop/asm/selfenhancer)

降龙十八掌，打完收工~