# Bug修复计划

## 目标
1. 修复 main.cpp 中的所有bug
2. 修复 fd-mod.py 中的bug
3. 修复 fd-item.py 中的bug
4. 让main.cpp能够在任何运行目录下找到Python文件

---

## 修复任务列表

### 任务1: 修复 main.cpp
- [ ] 1.1 使用 `getline()` 读取完整命令（包括参数）
- [ ] 1.2 正确传递参数给Python脚本
- [ ] 1.3 修复Python文件路径（使用相对路径确保在任何目录都能找到）
- [ ] 1.4 改进命令解析逻辑

### 任务2: 修复 fd-mod.py
- [ ] 2.1 添加UUID生成到函数内部
- [ ] 2.2 添加 `models/items` 目录创建
- [ ] 2.3 改进错误处理

### 任务3: 修复 fd-item.py
- [ ] 3.1 确保 `models` 父目录存在
- [ ] 3.2 改进目录创建逻辑

### 任务4: 验证测试
- [ ] 4.1 测试从任何目录运行mft程序
- [ ] 4.2 测试完整命令流程

---

## 详细修复方案

### main.cpp 修复方案

#### 1. 使用 getline() 读取完整命令
```cpp
// 原来
cin >> in;

// 修复后
getline(cin, in);
```

#### 2. 解析命令和参数
```cpp
// 解析命令名和参数
string cmd = in;
string params = "";

// 提取花括号内的参数
size_t brace_start = cmd.find('{');
size_t brace_end = cmd.find('}');
if(brace_start != string::npos && brace_end != string::npos){
    params = cmd.substr(brace_start + 1, brace_end - brace_start - 1);
    cmd = cmd.substr(0, brace_start);
}

// 去除命令名两端的空格
trim(cmd);
```

#### 3. 使用正确路径查找Python脚本
```cpp
// 使用当前程序所在目录作为基准
string base_path = get_program_path();
string py_path = base_path + "/../src/py/";

// 或者使用标准方法获取脚本路径
```

#### 4. 正确传递参数
```cpp
// 将参数以正确格式传递给Python
FILE* pipe = popen(("python3 " + py_path + "fd-mod.py " + params).c_str(), "r");
```

---

## 验证步骤

1. 编译程序
2. 从不同目录运行mft
3. 测试fd-mod命令
4. 测试fd-block命令
5. 测试fd-item命令

