# 汉字转仓颉码

```
python3 c_transform.py --input <input_file> --output <output_file> --mode <0: 汉字转仓颉; 1: 仓颉转汉字>
```


这是一个将中文转为仓颉码的脚本

也是受最近读到的character level的论文启发，从汉字的形码入手引入新的汉字处理方式。

之前有查到 https://github.com/arcsecw/chinese_wubi，用的时候也是发现一些问题。不过给了我一个现有的思路做这么一个转换工具。

形码比较常用的是五笔和仓颉，其中仓颉是以繁体为基础兼容简体的，设计上也比五笔要科学一些，所以这里就选用的仓颉码。

任何有问题发issues

最后，感谢Jackchows的分享仓颉字表 https://github.com/Jackchows/Cangjie5/
