# MFT
一个类似shell的我的世界mod生成器
可以使用类似cmd的指令去生成模组和添加模组功能

## 指令示例：
```
fd-mod {name:" ",des:" "}  --- 创建模组（会自动编写manifest.json）
fd-block {name:" ",des:\" \",icon:\" \"}  --- 添加新方块
```

## 使用说明：
1. 图标不需要添加'.png'后缀
2. 需要将纹理文件放在'textures/*'的相应子文件夹中
3. 先创建模组，再添加方块

## 环境要求：
- Python 3.x
- C++ 编译器（用于编译shell程序）

