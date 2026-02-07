# MFT Shell Bug 修复总结

## 已修复的Bug

### 1. ✅ handleExit 返回类型错误 (main.cpp)
**问题**: `return 0;` 但函数声明返回 `bool`
**修复**: 改为 `return false;`

### 2. ✅ 参数分隔符不匹配 (main.cpp)
**问题**: `toArgString()` 使用分号 `;`，但解析器搜索逗号 `,`
**修复**: 将 `;` 改为 `,` 使分隔符一致

### 3. ✅ fd-block.py 变量遮蔽问题
**问题**: `mod_name` 和 `block_name` 都从 `params.get('name', '')` 获取
**修复**: 
- Python端: 使用 `params.get('block', '')` 获取方块名称
- C++端: 添加 `args = "block=\"" + name + "\"," + args;` 传递参数

### 4. ✅ fd-item.py 变量遮蔽问题
**问题**: `mod_name` 和 `item_name` 都从 `params.get('name', '')` 获取
**修复**:
- Python端: 使用 `params.get('item', '')` 获取物品名称
- C++端: 添加 `args = "item=\"" + name + "\"," + args;` 传递参数

### 5. ✅ Python脚本转义处理改进
**问题**: 简单的 `value += params_str[i + 1]` 不完整
**修复**: 改进为处理 `\n`, `\t`, `\"`, `\'` 等转义字符

## 修复文件清单
- `/media/ljz/LJZ/MFT/src/main/main.cpp`
- `/media/ljz/LJZ/MFT/script/py/fd-block.py`
- `/media/ljz/LJZ/MFT/script/py/fd-item.py`

## 参数传递说明
- **fd-mod**: `name="mod_name", des="description"` → Python使用 `name` 作为模组名
- **fd-block**: `name="block_name"` + 额外传递 `block="block_name"` → Python使用 `name` 作为模组名, `block` 作为方块名
- **fd-item**: `name="item_name"` + 额外传递 `item="item_name"` → Python使用 `name` 作为模组名, `item` 作为物品名

