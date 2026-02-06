# MFT
一个类似shell的我的世界mod生成器
可以使用类似cmd的指令去生成模组和添加模组功能

## 指令示例：
```
fd-mod {name:"我的模组",des:"模组描述"}  --- 创建模组（会自动编写manifest.json）
fd-block {name:"石头",des:"一个石头方块",icon:"stone",explosion:"2.0",light:"0"}  --- 添加新方块
fd-item {name:"钻石剑",des:"锋利的钻石剑",type:"2d",texture:"diamond_sword",edible:"false",hand:"sword"}  --- 添加新物品
```

## 详细参数说明：

### fd-mod 命令：
- `name`: 模组名称
- `des`: 模组描述

### fd-block 命令：
- `name`: 方块名称
- `des`: 方块描述
- `icon`: 方块纹理名称（不需要.png后缀）
- `explosion`: 爆炸抗性（可选，默认为1.0）
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
4. 3D物品需要额外的模型文件

## 环境要求：
- Python 3.x
- C++ 编译器（用于编译shell程序）

