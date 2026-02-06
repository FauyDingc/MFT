import os
import sys
import uuid

sys.stdout.flush()

def _main_():
    print("Founding mod...")
    
    if len(sys.argv) < 2:
        print("Error: No arguments provided!")
        return
    
    # uuid4
    uuid1 = uuid.uuid4()
    uuid2 = uuid.uuid4()
    
    par = sys.argv[1]
    size = len(par)
    
    nameStart = par.find("name=\"") + 6
    if nameStart == 5:  # 模组名->die
        print("Error: name parameter not found!")
        return
    
    for j in range(nameStart, size):
        if par[j] == '"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("mod name: " + name)
    
    desStart = par.find("des=\"") + 5
    if desStart == 4:  # it is die too
        print("Error: des parameter not found!")
        return
    
    for j in range(desStart, size):
        if par[j] == '"':
            desEnd = j
            break
    des = par[desStart:desEnd]
    print("mod des: " + des)
    
    # 必要的目录结构
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
    
    # 创建manifest.json，形似身份证一样的东西，uuid唯一
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
    
    # 创建mod脚本，没有细写
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
    
    # 创建语言文件，游戏里有这个东西才能正确显示物品和方块的名称
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
