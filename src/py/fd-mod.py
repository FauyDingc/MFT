import os
import sys
import uuid

def _main_():
    print("Founding mod...")
    
    if len(sys.argv) < 2:
        print("Error: No arguments provided!")
        return
    
    # 在函数内部生成UUID，确保每次调用都生成新的UUID
    uuid1 = uuid.uuid4()
    uuid2 = uuid.uuid4()
    
    par = sys.argv[1]
    size = len(par)
    
    # 解析mod名称
    nameStart = par.find("name=\"") + 6
    if nameStart == 5:  # 没有找到name="
        print("Error: name parameter not found!")
        return
    
    for j in range(nameStart, size):
        if par[j] == '"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("mod name: " + name)
    
    # 解析mod描述
    desStart = par.find("des=\"") + 5
    if desStart == 4:  # 没有找到des="
        print("Error: des parameter not found!")
        return
    
    for j in range(desStart, size):
        if par[j] == '"':
            desEnd = j
            break
    des = par[desStart:desEnd]
    print("mod des: " + des)
    
    # 创建模组目录结构
    try:
        os.makedirs(name + "/textures/blocks", exist_ok=True)
        os.makedirs(name + "/textures/items", exist_ok=True)
        os.makedirs(name + "/models/block", exist_ok=True)
        os.makedirs(name + "/models/items", exist_ok=True)
        os.makedirs(name + "/blocks", exist_ok=True)
        os.makedirs(name + "/items", exist_ok=True)
        os.makedirs(name + "/texts", exist_ok=True)
        os.makedirs(name + "/scripts", exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return
    
    # 创建manifest.json
    manifest_content = f'''{{
    "format_version": 2,
    "header": {{
        "name": "{name}",
        "description": "{des}",
        "uuid": "{uuid1}",
        "version": [1, 0, 0],
        "min_engine_version": [1, 14, 0]
    }}, 
    "modules": [
        {{
            "type": "script",
            "entry": "scripts/mod.js",
            "version": [1, 0, 0]
        }}
    ],
    "dependencies": [
        {{
            "uuid": "{uuid2}",
            "version": [1, 14, 0]
        }}
    ]
}}'''
    
    try:
        with open(name + "/manifest.json", "w") as file:
            file.write(manifest_content)
        print("manifest.json created successfully!")
    except Exception as e:
        print(f"Error writing manifest.json: {e}")
        return
    
    # 创建基础mod脚本
    script_content = f'''// Mod: {name}
// Description: {des}

console.log("Mod {name} loaded!");
'''
    
    try:
        with open(name + "/scripts/mod.js", "w") as file:
            file.write(script_content)
        print("mod.js created successfully!")
    except Exception as e:
        print(f"Error writing mod.js: {e}")
        return
    
    # 创建初始语言文件
    try:
        with open(name + "/texts/zh_CN.lang", "w", encoding='utf-8') as file:
            file.write(f"mod.name={name}\n")
            file.write(f"mod.description={des}\n")
        print("Language file created successfully!")
    except Exception as e:
        print(f"Error writing language file: {e}")
        return
    
    print("name:" + name)

if __name__ == "__main__":
    _main_()
