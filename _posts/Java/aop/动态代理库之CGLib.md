# 动态代理库之CGLib

## 动态代理使用入门

使用CGLib实现动态代理，完全不受代理类必须实现接口的限制，而且CGLib底层采用ASM字节码生成框架，使用字节码技术生成代理类，比使用Java反射效率要高。唯一需要注意的是，CGLib不能对声明为final的方法进行代理，因为CGLib原理是动态生成被代理类的子类。

*net.sf.cglib.proxy.Enhancer* 类提供了非常简洁的API来创建代理对象，有两种回调的防方式：**InvocationHandler**和**MethodInterceptor**。

我们有一个Account类和一个SecurityChecker类，后续的操作都给予该类进行，
Account类详细实现如下：

```java
public class Account {

    public void operation() {
        System.out.println("operation..."+Integer.toString(id));
        //TODO there are some real operation
    }
}
```

SecurityChecker类详细实现如下：

```java
public class SecurityChecker {
    public static void checkSecurity() {
        System.out.println("SecurityChecker.checkSecurity ...");
        //TODO real security check
    }
}
```

### InvocationHandler

```java
public static void InvocationHandlertest() throws Exception {

        Enhancer enhancer = new Enhancer();

        enhancer.setSuperclass(Account.class);

        enhancer.setCallback(new InvocationHandler() {

            @Override
            public Object invoke(Object proxy, Method method, Object[] args)
                    throws Throwable {
                if(proxy instanceof Account && method.getName() == "operation") {
                    SecurityChecker.checkSecurity();
                    return "GClib callback";
                    //这里不能调用 method.invoke CGlib是继承的实现类，调用当前类的方法，并不是父类，会造成无限循环。
                    //return method.invoke(proxy,args);
                } else {
                    throw new RuntimeException("Do not know what to do.");
                }
            }
        });

        Account proxy = (Account) enhancer.create();
        proxy.operation();
    }
```

### MethodInterceptor

```java
public static void MethodInterceptortest() throws Exception {

        Enhancer enhancer = new Enhancer();

        enhancer.setSuperclass(Account.class);

        enhancer.setCallback(new MethodInterceptor() {

            @Override
            public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy)
                    throws Throwable {
                if(obj instanceof Account && method.getName() == "operation") {

                    SecurityChecker.checkSecurity();

                    return proxy.invokeSuper(obj,args);

                } else {

                    return proxy.invokeSuper(obj,args);
                }
            }
        });


        Account proxy = (Account) enhancer.create();
        proxy.operation();
    }

```

- 最终调用

```java
    public static void main(String[] args) {
        try {

            cglibtest.InvocationHandlertest();

            cglibtest.MethodInterceptortest();

        }catch (Throwable a)
        {}
    }
```

- 输出

```bash

SecurityChecker.checkSecurity ...
SecurityChecker.checkSecurity ...
operation...

```

## 回调过滤器CallbackFilter

```java
    public static void CallbackFiltertest() throws Exception {

        Enhancer enhancer = new Enhancer();

        enhancer.setSuperclass(Account.class);

        enhancer.setCallback(new MethodInterceptor() {

            @Override
            public Object intercept(Object obj, Method method, Object[] args, MethodProxy proxy)
                    throws Throwable {
                if(obj instanceof Account && method.getName() == "operation") {

                    return proxy.invokeSuper(obj,args);

                } else {

                    return proxy.invokeSuper(obj,args);
                }
            }
        });

        enhancer.setCallbackFilter(new CallbackFilter() {
            @Override
            public int accept(Method method) {

                if (method.getName() == "operation") {

                    SecurityChecker.checkSecurity();
                    System.out.println("operation - CallbackFilter");
                    //返回的值为数字，代表了Callback数组中的索引位置，要到用的Callback
                    return 0;
                }
                return 0;
            }
        });

        Account pro = (Account) enhancer.create();
        pro.operation();
    }
```

- 调用

```java

    public static void main(String[] args) {
        try {

            cglibtest.CallbackFiltertest();

        }catch (Throwable a)
        {}
    }

```


- 输出

```bash

SecurityChecker.checkSecurity ...
operation - CallbackFilter
operation...

Process finished with exit code 0

```

## 延迟加载对象-LazyLoader

cglib的延迟加载有两种实现，一种是单例模式，当加载一次后，以后一直使用该实例，另一种是每次调用都会生成新的实例。
为了更清楚的看输出结果，我们简单调整下Account类，最终调整后的完整代码如下：

```java

public class Account {

    int id;

    public Account()
    {
        id =new Random().nextInt();
        System.out.println("Account init..."+Integer.toString(id));

    }

    public void operation() {
        System.out.println("operation..."+Integer.toString(id));
        //TODO there are some real operation
    }
}
```

- 延迟加载单例实现-LazyLoader

```java
public class CglibLazyLoaderTest {

    private Object account = null;

    public CglibLazyLoaderTest(){

        try {

            this.account = LazyLoadertest();

            System.out.println("CglibLazyLoaderTest init fun end");

        }catch (Throwable e){}
    }

    public Object getAccount() {
        return account;
    }

    public Object LazyLoadertest() throws Exception {

        Enhancer enhancer = new Enhancer();

        enhancer.setSuperclass(NoOp.class);

        //LazyLoader 继承自CallBack，因此，设置enhancer.setCallback也可以达到相同效果。
        return enhancer.create(Account.class, new LazyLoader() {

            @Override
            public Object loadObject() throws Exception {
                System.out.println("before lazyLoader...");
                Account bean = new Account();
                System.out.println("after lazyLoader...");
                return bean;
            }
        });
    }

    public static void main(String[] args) {
        try {

            CglibLazyLoaderTest test = new CglibLazyLoaderTest();
            System.out.println("CglibLazyLoaderTest init end");
            ((Account)test.getAccount()).operation();
            ((Account)test.getAccount()).operation();

        }catch (Throwable a)
        {}
    }

}
```

- 输出

```bash

Account init...-305699122
CglibLazyLoaderTest init fun end
CglibLazyLoaderTest init end
before lazyLoader...
Account init...-676331066
after lazyLoader...
operation...-676331066
operation...-676331066

Process finished with exit code 0

```

从输出结果中能看到，Account类是在CglibLazyLoaderTest初始化完成之后，实际调用的时候实例化的。在某些情况下我们不能用单例，那么我们需要另一个延迟加载的接口来帮我们实现。


- 延迟加载实现-Dispatcher

Dispatcher和LazyLoader最大的区别就在于，后者是单例模式，前者是每次调用都是实例化一个新的对象。show me you code。

```java

public class CglibDispatcherTest {

    private Object account = null;

    public CglibDispatcherTest(){

        try {

            this.account = LazyLoadertest();

            System.out.println("CglibDispatcherTest init fun end");

        }catch (Throwable e){}
    }


    public Object getAccount() {
        return account;
    }

    public Object LazyLoadertest() throws Exception {

        Enhancer enhancer = new Enhancer();

        enhancer.setSuperclass(NoOp.class);

        //LazyLoader 继承自CallBack，因此，设置enhancer.setCallback也可以达到相同效果。
        return enhancer.create(Account.class, new Dispatcher() {

            @Override
            public Object loadObject() throws Exception {
                System.out.println("before DispatcherLoader...");
                Account bean = new Account();
                System.out.println("after DispatcherLoader...");
                return bean;
            }
        });
    }

    public static void main(String[] args) {
        try {

            CglibDispatcherTest test = new CglibDispatcherTest();
            System.out.println("CglibDispatcherTest init end");
            ((Account)test.getAccount()).operation();
            ((Account)test.getAccount()).operation();

        }catch (Throwable a)
        {}
    }

}
```

- 输出

```bash

Account init...71179224
CglibDispatcherTest init fun end
CglibDispatcherTest init end
before DispatcherLoader...
Account init...-1243509322
after DispatcherLoader...
operation...-1243509322
before DispatcherLoader...
Account init...-90748078
after DispatcherLoader...
operation...-90748078

Process finished with exit code 0

```

从输出中能很明显看出，Account在两次调用中，实例化了两次++~~

[代码下载](https://github.com/EurekaShow/daily-practice/tree/master/primer/java-primer/src/main/java/com/training/aop/cglib)