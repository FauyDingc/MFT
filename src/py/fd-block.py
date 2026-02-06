import os
import sys

def _main_():
    print("Founding block...")
    
    if len(sys.argv) < 2:
        print("Error: No arguments provided!")
        return
    
    par = sys.argv[1]
    size = len(par)
    
    # 解析mod名称（从参数末尾获取）
    mod_name_Start = par.find("/;name=") + 7
    if mod_name_Start == 6:  # 没有找到";name="
        print("Error: mod name not found in parameters!")
        return
    
    for j in range(mod_name_Start, size):
        if par[j] == ';':
            mod_nameEnd = j
            break
    mod_name = par[mod_name_Start:mod_nameEnd]
    print("mod name: " + mod_name)
    
    # 解析方块名称
    nameStart = par.find("name=\"") + 6
    if nameStart == 5:  # 没有找到name="
        print("Error: name parameter not found!")
        return
    
    for j in range(nameStart, size):
        if par[j] == '"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("block name: " + name)
    
    # 解析方块描述
    desStart = par.find("des=\"") + 5
    if desStart == 4:  # 没有找到des="
        print("Error: des parameter not found!")
        return
    
    for j in range(desStart, size):
        if par[j] == '"':
            desEnd = j
            break
    des = par[desStart:desEnd]
    print("block des: " + des)
    
    # 解析图标名称
    iconStart = par.find("icon=\"") + 6
    if iconStart == 5:  # 没有找到icon="
        print("Error: icon parameter not found!")
        return
    
    for j in range(iconStart, size):
        if par[j] == '"':
            iconEnd = j
            break
    icon = par[iconStart:iconEnd]
    print("block icon: " + icon)
    
    # 创建纹理JSON文件
    textures_path = mod_name + "/textures/blocks"
    try:
        os.makedirs(textures_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating textures directory: {e}")
        return
    
    texture_content = f'''{{
    "resource_pack_name": "{mod_name}",
    "texture_name": "atlas.terrain",
    "padding": 16,
    "resource_pack_format_version": 1,
    "texture_data": {{
        "{name}": {{
            "textures": "textures/blocks/{icon}"
        }}
    }}
}}'''
    
    try:
        with open(textures_path + "/" + name + "_texture.json", "w") as file:
            file.write(texture_content)
        print("Texture JSON created successfully!")
    except Exception as e:
        print(f"Error writing texture JSON: {e}")
        return
    
    # 创建方块定义JSON文件
    blocks_path = mod_name + "/blocks"
    try:
        os.makedirs(blocks_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating blocks directory: {e}")
        return
    
    block_content = f'''{{
    "format_version": "1.16.0",
    "minecraft:block": {{
        "description": {{
            "identifier": "{mod_name}:{name}",
            "is_experimental": false,
            "register_to_creative_menu": true
        }},
        "components": {{
            "minecraft:destroy_time": 1.5,
            "minecraft:explosion_resistance": 1.0,
            "minecraft:friction": 0.6,
            "minecraft:map_color": "{icon}"
        }}
    }}
}}'''
    
    try:
        with open(blocks_path + "/" + name + ".json", "w") as file:
            file.write(block_content)
        print("Block definition created successfully!")
    except Exception as e:
        print(f"Error writing block definition: {e}")
        return
    
    # 创建语言文件
    try:
        with open(mod_name + "/texts/zh_CN.lang", "a") as file:
            file.write(f"tile.{mod_name}:{name}.name={name}\n")
            file.write(f"tile.{mod_name}:{name}.desc={des}\n")
        print("Language file updated successfully!")
    except Exception as e:
        print(f"Error writing language file: {e}")
        return
    
    print("Block creation completed!")

if __name__ == "__main__":
    _main_()

