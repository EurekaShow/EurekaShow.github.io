# Java中的协变和逆变

## 问题开篇
首先看一段代码
```java
Number num = new Integer(1);  

//type mismatch
ArrayList<Number> list = new ArrayList<Integer>(); 

List<? extends Number> list = new ArrayList<Number>();
//error
list.add(new Integer(1));
//error
list.add(new Float(1.2f));  
```
有人会纳闷：
1.为什么Number的对象可以由Integer实例化，而ArrayList<Number>的对象却不能由ArrayList<Integer>实例化？
2.list中的<? extends Number>声明其元素是Number或Number的派生类，为什么不能add Integer和Float?
为了解决这些问题，我们需要了解Java中的协变和逆变以及泛型中通配符用法。

## Liskov替换原则
LSP由Barbara Liskov于1987年提出，其定义如下：
所有引用基类（父类）的地方必须能透明地使用其子类的对象。

LSP包含以下四层含义：
1.子类完全拥有父类的方法，且具体子类必须实现父类的抽象方法。
2.子类中可以增加自己的方法。
3.当子类覆盖或实现父类的方法时，方法的形参要比父类方法的更为宽松。
4.当子类覆盖或实现父类的方法时，方法的返回值要比父类更严格。

前面的两层含义比较好理解，后面的两层含义会在下文中详细解释。根据LSP，我们在实例化对象的时候，可以用其子类进行实例化，比如：
Number num = new Integer(1); 

## 协变逆变定义
逆变与协变用来描述类型转换（type transformation）后的继承关系，其定义：
Integer继承自Number，Number是父类，简称F，Integer为子类，简称为C，这个继承派生关系我们表示为F<|C.
List，List类型我们简记为f(F),f(C)。那么：
当F<|C时,并且f(F)<|f(C) 那么f叫协变。
当F<|C时,并且f(C)<|f(F) 那么f叫逆变。
如果以上两种关系都不存在则为不变。

## 数组
```
Number[] numbers = new Integer[3]; 
```
根据以上定位，这种情况说明是协变。
## 方法返回值

在Java 1.4中，子类覆盖（override）父类方法时，形参与返回值的类型必须与父类保持一致：
```java
class Super {
    Number method(Number n) { ... }
}

class Sub extends Super {
    @Override 
    Number method(Number n) { ... }
}
```
从Java 1.5开始，子类覆盖父类方法时允许协变返回更为具体的类型：
```
class Super {
    Number method(Number n) { ... }
}

class Sub extends Super {
    @Override 
    Integer method(Number n) { ... }
}
```

## 泛型
Java中泛型是不变的，可有时需要实现逆变与协变，怎么办呢？Java中通过通配符?实现协变和逆变：
```java
//<? extends>实现了泛型的协变，比如：
List<? extends Number> list = new ArrayList<Integer>();

//<? super>实现了泛型的逆变，比如：
List<? super Number> list = new ArrayList<Object>();
```

为什么（开篇代码中）List<? extends Number> list在add Integer和Float会发生编译错误？首先，我们看看add的实现：
```java
public interface List<E> extends Collection<E> {
    boolean add(E e);
}
```
在调用add方法时，泛型E自动变成了<? extends Number>，其表示list所持有的类型为在Number与Number派生子类中的***某一类型***，***其中包含Integer类型却又不特指为Integer类型***，故add Integer时发生编译错误，为了能正常调用add方法，可以用super关键字实现：

```java
List<? super Number> list = new ArrayList<Object>();
list.add(new Integer(1));
list.add(new Float(1.2f));
```
<? super Number>表示list所持有的类型为在Number与Number的基类中的某一类型，其中Integer与Float必定为这某一类型的子类；所以add方法能被正确调用。从上面的例子可以看出，extends确定了泛型的上界，而super确定了泛型的下界。

开篇的代码中能add什么值？Java为了保护类型一致，禁止添加任何类型，却允许添加null：
```java 
List<? extends Number> exlist = new ArrayList<Integer>();
exlist.add(null);
```

## PECS
现在问题来了：究竟什么时候用extends什么时候用super呢？《Effective Java》给出了答案：

PECS: producer-extends, consumer-super.

比如，一个简单的Stack API：
```java
public class Stack<E>{
    public Stack();
    public void push(E e);
    public E pop();
    public boolean isEmpty();
}
```
要实现pushAll(Iterable<E> src)方法，将src的元素逐一入栈：
```java
public void pushAll(Iterable<E> src){
    for(E e : src)
        push(e)
}
```
假设有一个实例化Stack<Number>的对象stack，src有Iterable<Integer>与 Iterable<Float>；在调用pushAll方法时会发生type mismatch错误，因为Java中泛型是不可变的，Iterable<Integer>与 Iterable<Float>都不是Iterable<Number>的子类型。因此，应改为
```java
// Wildcard type for parameter that serves as an E producer
public void pushAll(Iterable<? extends E> src) {
    for (E e : src)
        push(e);
}
```
要实现popAll(Collection<E> dst)方法，将Stack中的元素依次取出add到dst中，如果不用通配符实现：
```java
// popAll method without wildcard type - deficient!
public void popAll(Collection<E> dst) {
    while (!isEmpty())
        dst.add(pop());   
}
```
同样地，假设有一个实例化Stack<Number>的对象stack，dst为Collection<Object>；调用popAll方法是会发生type mismatch错误，因为Collection<Object>不是Collection<Number>的子类型。因而，应改为：
```java
// Wildcard type for parameter that serves as an E consumer
public void popAll(Collection<? super E> dst) {
    while (!isEmpty())
        dst.add(pop());
}
```
在上述例子中，在调用pushAll方法时生产了E 实例（produces E instances），在调用popAll方法时dst消费了E 实例（consumes E instances）。Naftalin与Wadler将PECS称为***Get and Put Principle***。

java.util.Collections的copy方法(JDK1.7)完美地诠释了PECS：
```java
public static <T> void copy(List<? super T> dest, List<? extends T> src) {
    int srcSize = src.size();
    if (srcSize > dest.size())
        throw new IndexOutOfBoundsException("Source does not fit in dest");

    if (srcSize < COPY_THRESHOLD ||
        (src instanceof RandomAccess && dest instanceof RandomAccess)) {
        for (int i=0; i<srcSize; i++)
            dest.set(i, src.get(i));
    } else {
        ListIterator<? super T> di=dest.listIterator();
        ListIterator<? extends T> si=src.listIterator();
        for (int i=0; i<srcSize; i++) {
            di.next();
            di.set(si.next());
        }
    }
}
```
PECS总结：

要从泛型类取数据时，用extends；
要往泛型类写数据时，用super；
既要取又要写，就不用通配符（即extends与super都不用）。

## 参考资料
[coder blog](http://www.cnblogs.com/en-heng/p/5041124.html)
