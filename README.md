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

## 环境要求：
- Python 3.x
- C++ 编译器（用于编译shell程序）



注: 为了这个作品作者还是去自学了很多的语法，真挺累的，要是有些地方还是有逻辑小bug就自己改改或者告诉我。作者邮箱：edwin23578164@outlook.com
                                     fddddddd0@outlook.com
                                     m18667909625@163.com
别问为啥我有这么多：）：）