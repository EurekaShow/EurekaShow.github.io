1. #表示Header1，显示效果如下：
# 这里是#，这里是Header1
## 这里是##，这里是Hedaer2

2. 超链接也很简单，格式／示例：

```
[要显示的文字](这里填写url地址)
```

[点击查看我的博客](http://www.itxiaofeng.com)

3. 图片的展示类似于上面的超链接，格式／示例：

```
![](这里是图片的url地址)
```

![](http://www.itxiaofeng.com/wp-content/uploads/2017/07/shouwang.jpeg)

4. >引用块，效果如下：

5. *表示斜体
> *一盏灯， 一片昏黄； 一简书， 一杯淡茶。*

6. **表示加粗
> **守着**那一份淡定， 品读属于自己的寂寞。 保持淡定， 才能欣赏到最美丽的风景！ 保持淡定， 人生从此不再寂寞。

7. -表示无序列表，效果如下：
- 星期一
- 星期天
- 星期2⃣
- 星期六

8. 数字+.表示有序列表，效果如下：

``` xml
1. hello
2. hi
3. hai
```

9. ~~表示删除线

这就是 ~~删除线~~

10. 代码块及高亮渲染使用\```开始和\```结束表示，开始位置可以标明你想渲染的代码类型，如：js，java，那么就这样表示：``` js,效果如下：
``` xml
define service{
        use                     generic-service,service-pnp
        host_name               win-172.16.100.136
        service_description     D:\ Drive Space
        check_command           check_nt!USEDDISKSPACE!-l d -w 80 -c 90
        }
```
js 高亮渲染
``` js
window.addEventListener('load', function() {
  console.log('window loaded');
});
```
java高亮渲染
``` java

public class abc{
    private String str;
}

```

11. 表格
```
1. :--- 左对齐
2. :---: 居中对齐
3. ---: 右对齐
```

```
| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |
```
效果如下：

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

```
dog | bird | cat
----|------|----
foo | foo  | foo
bar | bar  | bar
baz | baz  | baz
```
效果如下：
dog | bird | cat
----|------|----
foo | foo  | foo
bar | bar  | bar
baz | baz  | baz

12. 最后推荐一款Markdown编辑器 - VSCode
安VSCode后，去安装对应的插件即可一边编辑，一边查看效果了。
我安装的VSCode Markdown插件有：
Markdown Theme Kit
Auto-Open Markdown Preview