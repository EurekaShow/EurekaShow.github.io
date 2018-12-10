# JDK中的动态代理Proxy

## 为什么用动态代理？

在日常的业务逻辑中方法中，出于安全考录，我们往往需要做一个安全验证获取权限验证，而这些方法又和业务逻辑没有太强的关联，更有甚者，没有任何关系。无论是洁癖还是强迫症复发，我们总希望把和业务无关的这部分剥离出来，玻璃的办法有很多，JDK代理就是其中之一。

## 准备业务类

Proxy 是面向接口的，所有使用 Proxy 的对象都必须定义一个接口，而且用这些对象的代码也必须是对接口编程的：Proxy 生成的对象是接口一致的而不是对象一致的。

我们开始准备用户接口：
```java
public interface Account {
    void operation();
}
```
业务实现类
```java
public class AccountImpl implements Account {
    public void operation() {
        System.out.println("some operation...");
        //TODO there are some real operation
    }
}
```
安全验证类
```java
public class SecurityChecker {
    public static void checkSecurity() {
        System.out.println("SecurityChecker.checkSecurity ...");
        //TODO there are  real security check
    }
}

```
Proxy 编程是面向接口的。Proxy 并不负责实例化对象，要把 Account定义成一个接口，然后在 AccountImpl里实现 Account接口，接着实现一个 InvocationHandler Account方法被调用的时候，虚拟机都会实际调用这个 InvocationHandler的 invoke方法：

```java
public class SecurityProxyInvocationHandler implements InvocationHandler {
    private Object proxyedObject;
    public SecurityProxyInvocationHandler(Object o) {
        proxyedObject = o;
    }

    public Object invoke(Object object, Method method, Object[] arguments)
            throws Throwable {
        if (object instanceof Account && method.getName().equals("operation")) {
            SecurityChecker.checkSecurity();
        }
        return method.invoke(proxyedObject, arguments);
    }
}
```
最后，在应用程序中指定 InvocationHandler生成代理对象：

```java
    public static void main(String[] args) {

        Account account = (Account) Proxy.newProxyInstance(
                Account.class.getClassLoader(),
                new Class[] { Account.class },
                new SecurityProxyInvocationHandler(new AccountImpl())
        );

        account.operation();
    }
```

 不足之处在于：

- 1.Proxy 是面向接口的，所有使用 Proxy 的对象都必须定义一个接口，而且用这些对象的代码也必须是对接口编程的：Proxy 生成的对象是接口一致的而不是对象一致的：例子中 Proxy.newProxyInstance生成的是实现 Account接口的对象而不是 AccountImpl的子类。这对于软件架构设计，尤其对于既有软件系统是有一定掣肘的。

- 2.Proxy 是通过反射实现的，必须在效率上付出代价：有实验数据表明，调用反射比一般的函数开销至少要大 10 倍。而且，从程序实现上可以看出，对 proxy class 的所有方法调用都要通过使用反射的 invoke 方法。因此，对于性能关键的应用，使用 proxy class 是需要精心考虑的，以避免反射成为整个应用的瓶颈。

[代码下载](https://github.com/EurekaShow/daily-practice/tree/master/primer/java-primer/src/main/java/com/training/aop/jdkproxy)