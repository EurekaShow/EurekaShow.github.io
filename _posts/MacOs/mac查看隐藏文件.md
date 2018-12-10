# mac查看隐藏文件

配置文件的时候，会有dot开头的二班文件/文件夹名，可在Finder里面就是看不到，有时候我们希望看到直接修改它。

- 打开终端。
- 输入如下命令：

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean true ; killall Finder
```

早期版本用如下指令：

```bash
defaults write com.apple.finder AppleShowAllFiles TRUE ; killall Finder
```

回车后你会发现弹出了一个Finder，里面多了很多灰蓝色的文件夹和灰色的文件。呐，就它们了。

当你看过瘾后觉得这个天天看到影响心情，那就还隐藏掉。

- 打开终端
- 输入如下命令：

```bash
defaults write com.apple.finder AppleShowAllFiles -boolean false ; killall Finder
```

早期版本用如下指令：

```bash
defaults write com.apple.finder AppleShowAllFiles FALSE ; killall Finder
```