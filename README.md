# MFT
一个类似shell的我的世界mod生成器
可以使用类似cmd的指令去生成模组和添加模组功能

## 指令示例：
```
fd-mod {name:"我的模组",des:"模组描述"}  --- 创建模组（会自动编写manifest.json）
fd-block {name:"石头",des:"一个垃圾方块",icon:"lajiiiiiii",explosion:"2.0",light:"0"}  --- 添加新方块
fd-item {name:"C60剑",des:"C60剑",type:"2d",texture:"C60_sword",edible:"false",hand:"sword"}  --- 添加新物品
```

## 详细参数说明：

### setout 命令
- setout {path:"output/"} 

### fd-mod 命令：
- `name`: 模组名称
- `des`: 模组描述

### fd-block 命令：
- `name`: 方块名称
- `des`: 方块描述
- `icon`: 方块纹理名称（不需要.png后缀,本来想加，后面觉得写入文件方便就没加
                        因为方块配置文件里是不需要后缀的）
- `explosion`: 爆炸默认为1.0
- `light`: 发光等级（可选，0-15，默认为0）

### fd-item 命令：
- `name`: 物品名称
- `des`: 物品描述
- `type`: 物品类型（"2d" 或 "3d"）
- `texture`: 纹理/模型名称
- `edible`: 是否可食用（可选，"true"/"false"，默认为"false"）
- `effect`: 食用效果（可选，仅在edible="true"时有效）
- `hand`: 手持效果（可选，如"sword"）

## 使用说明：
1. 图标和纹理不需要添加'.png'后缀
2. 需要将纹理文件放在正确的子文件夹中：
   - 方块纹理：`textures/blocks/`
   - 物品纹理：`textures/items/`
3. 先创建模组，再添加方块或物品
4. 3D物品需要额外的模型文件，自己做，别想着让作者搞
5. 这个shell软件只能做一些比较简单的操作，如果想做动作优化渲染优化之类的还是自己老老实实去敲代码吧

## 环境要求：
- Python 3.x
- C++ 编译器（用于编译shell程序）

#### 作者的日记
1. 二月四日：开干
2. 二月五日：完成了基本的文件操作
3. 二月六日：润滑了一下，能跑了（天大的喜事）but->二月六日：出现了一些交互的bug,输出没有立即显示，shell找不到脚本，便加了sys.stdout.flush(),暂时用了绝对路径，后面再改
4. 二月七日：有一些输出格式的问题，修复。输出还是被卡在后面，怀疑是ios::sync_with_stdio(0);cin.tie(0);出问题了，删了这段。最后也是成功了（开心）
5. 二月七日too：把绝对路径替换成了相对路径，能用了，但是模组不知道飞哪去了。严重的bug，全局变量污染太大，改为类。重构了。重构内容见 ' TODO.md ',然后发现免费的AI并不好用:）发现了解析有问题，Parser不支持不带引号的参数值,所以程序识别不出参数，我又给代码锻造了一下子。见BUGFIX_TODO.md


注: 为了这个作品作者还是去自学了很多的语法，真挺累的，要是有些地方还是有逻辑小bug就自己改改或者告诉我。作者邮箱：                                 edwin23578164@outlook.com
                                     fddddddd0@outlook.com
                                     m18667909625@163.com
别问为啥我有这么多：）：）