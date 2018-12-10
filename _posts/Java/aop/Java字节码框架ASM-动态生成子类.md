# Java字节码框架ASM-动态生成子类

在现实的coding中，有一个场景会频繁的出现。
当一部分业务逻辑实现后，为了安全或者其他什么原因，我们需要往业务代码类里面插入一些和业务无关但又必须的代码。
如果把代码直接写到业务方法里面，会污染我们的业务代码，关键是，它会让我们的强迫症发作阿。这是最严重的后果。
解决方案有很多，最简单的是用JDK自带的Proxy，但是我们知道JDK的Proxy这个必须依赖接口实现，并且反射的效率比较差。
还有什么好办法？
AOP中提供了两个思路，动态织入和静态织入。
而Spring中用的cglib就是动态织入的经典，cglib中使用的ASM，通过动态字节码，继承已有类并实现已有类所有方法来实现非常灵活的操作。
让我们来看看ASM是怎么实现AOP功能的。

在[Java字节码框架ASM-自身增强](Java字节码框架ASM-自身增强.md)中，简单实现了逻辑方法前后动态插入日志记录操作，除了增强自身，
我们还可以通过继承来更完美的实现。接下来我们通过动态修改字节码实现继承，实现更加完美的操作， **这个实例我们实现操作类前增加安全验证**：

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

然后，我们需要对Account的操作做一个安全检查/权限限制，具体的安全检查类代码如下：

```java
public class SecurityChecker {
    public static void checkSecurity() {
        System.out.println("SecurityChecker.checkSecurity ...");
        //TODO some real security check
    }
}
```

然后，手术刀准备好我们就要开始我们的操作了。

首先，还是确认下ASM库是否引入：

```xml
<dependency>
    <groupId>asm</groupId>
    <artifactId>asm</artifactId>
    <version>3.3.1</version>
</dependency>

```

因为ASM库应用广泛，spring或者是日常高频使用的库，基本上都依赖它。所以，你的项目可能已经间接引入了ASM的jar包。

- 1.我们用ASM动态生成一个Account类的子类

```java

public class AddSecurityCheckClassAdapter extends ClassAdapter {

    public AddSecurityCheckClassAdapter(ClassVisitor cv) {
        //Responsechain 的下一个 ClassVisitor，这里我们将传入 ClassWriter，
        // 负责改写后代码的输出
        super(cv);
    }

    String enhancedSuperName;
    public void visit(final int version, final int access, final String name,
                      final String signature, final String superName,
                      final String[] interfaces) {
        // 改变类命名
        String enhancedName = name + "$EnhancedByASM";  
        // 改变父类，这里是”Account”
        enhancedSuperName = name; 
        //在这里我们就要开启我们的乾坤大挪移第8层功法：根据导入类的字节码，通过ASM修改类和父类名称达到生成子类的目的。
        super.visit(version, access, enhancedName, signature,
                enhancedSuperName, interfaces);
    }


    // 重写 visitMethod，访问到 "operation" 方法时，
    // 给出自定义 MethodVisitor，实际改写方法内容
    public MethodVisitor visitMethod(final int access, final String name,
                                     final String desc, final String signature, final String[] exceptions) {
        MethodVisitor mv = cv.visitMethod(access, name, desc, signature,exceptions);
        MethodVisitor wrappedMv = mv;
        if (mv != null) {
            // 对于 "operation" 方法
            if (name.equals("operation")) {
                // 使用自定义 MethodVisitor，实际改写方法内容
                //在这里移花接木，在原方法上动手术，修改成我们想要的。
                wrappedMv = new AddSecurityCheckMethodAdapter(mv);
            }else if (name.equals("<init>")) {
                //需要修改构造函数
                wrappedMv = new ChangeToChildConstructorMethodAdapter(mv,
                        enhancedSuperName);
            }
        }
        return wrappedMv;
    }
}
```

我们看下AddSecurityCheckMethodAdapter类的内容

```java
public class AddSecurityCheckMethodAdapter extends MethodAdapter {
    public AddSecurityCheckMethodAdapter(MethodVisitor mv) {
        super(mv);
    }

    public void visitCode() {
        //在原方法中增加了安全验证。
        visitMethodInsn(Opcodes.INVOKESTATIC, "com/training/aop/asm/aop/entity/SecurityChecker",
                "checkSecurity", "()V");
    }
}
```

然后再来看看ChangeToChildConstructorMethodAdapter是如果改变继承类的初始化

```java
public class ChangeToChildConstructorMethodAdapter extends MethodAdapter {
    private String superClassName;

    public ChangeToChildConstructorMethodAdapter(MethodVisitor mv,
                                                 String superClassName) {
        super(mv);
        this.superClassName = superClassName;
    }

    public void visitMethodInsn(int opcode, String owner, String name,
                                String desc) {
        // 调用父类的构造函数时
        if (opcode == Opcodes.INVOKESPECIAL && name.equals("<init>")) {
            owner = superClassName;
        }
        // 改写父类为superClassName
        super.visitMethodInsn(opcode, owner, name, desc);
    }
}

```

最后，我们看下如何通过AddSecurityCheckClassAdapter把Account的字节码改成我们想要的效果：

```java

public class Generator{

    private static AccountGeneratorClassLoader classLoader;

    //实现我们自己的类加载器
    private class AccountGeneratorClassLoader extends ClassLoader {

        public AccountGeneratorClassLoader() {
            super(Thread.currentThread().getContextClassLoader());
        }

        public Class defineClassFromClassFile(String className, byte[] classFile) throws ClassFormatError {
            return defineClass(className, classFile, 0,
                    classFile.length);

        }
    }


        private Class secureAccountClass;

        public void testAsmClassLoader() throws Exception {
            //加载Account类
            ClassReader cr = new ClassReader(Account.class.getName());

            ClassWriter cw = new ClassWriter(ClassWriter.COMPUTE_MAXS);
            ClassAdapter classAdapter = new AddSecurityCheckClassAdapter(cw);
            cr.accept(classAdapter, ClassReader.SKIP_DEBUG);
            byte[] data = cw.toByteArray();

            classLoader = new AccountGeneratorClassLoader();

            secureAccountClass = classLoader.defineClassFromClassFile(Account.class.getName()+"$EnhancedByASM", data);

            Object account = secureAccountClass.newInstance();

            Account ac = (Account) account;

            ac.operation();
        }

        public static void main(String[] args) throws Exception {
            new Generator().testAsmClassLoader();
        }

}
```

执行输出如下：

```java
SecurityChecker.checkSecurity ...
operation...
```

正是我们想要的效果，方法执行前执行了验证的方法。
[代码下载地址](https://github.com/EurekaShow/daily-practice/tree/master/primer/java-primer/src/main/java/com/training/aop/asm/subclass)