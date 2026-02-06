import os
import sys
import json

sys.stdout.flush()

def _main_():
    print("Founding block...")
    
    if len(sys.argv) < 2:
        print("Error: No arguments provided!")
        return
    
    par = sys.argv[1]
    size = len(par)
    
    # 获取shell的传参
    mod_name_Start = par.find("/;name=") + 7
    if mod_name_Start == 6:  #这要是错了就是shell传参的问题了
        print("Error: mod name not found in parameters!")
        return
    
    for j in range(mod_name_Start, size):
        if par[j] == ';':
            mod_nameEnd = j
            break
    mod_name = par[mod_name_Start:mod_nameEnd]
    print("mod name: " + mod_name)
   
    nameStart = par.find("name=\"") + 6
    if nameStart == 5:  # 方块名称->die
        print("Error: name parameter not found!")
        return
    
    for j in range(nameStart, size):
        if par[j] == '"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("block name: " + name)
    
    desStart = par.find("des=\"") + 5
    if desStart == 4:  # 方块描述->die too
        print("Error: des parameter not found!")
        return
    
    for j in range(desStart, size):
        if par[j] == '"':
            desEnd = j
            break
    des = par[desStart:desEnd]
    print("block des: " + des)
    
    iconStart = par.find("icon=\"") + 6
    if iconStart == 5:  # 方块纹理->die tooooo
        print("Error: icon parameter not found!")
        return
    
    for j in range(iconStart, size):
        if par[j] == '"':
            iconEnd = j
            break
    icon = par[iconStart:iconEnd]
    print("block icon: " + icon)

    # 解析可选参数：爆炸抗性、发光等级
    explosion_resistance = 1.0
    light_level = 0

    # 看看有没有传过来
    expStart = par.find("explosion=\"") + 11
    if expStart != 10:
        for j in range(expStart, size):
            if par[j] == '"':
                expEnd = j
                break
        try:
            explosion_resistance = float(par[expStart:expEnd])
            print("explosion resistance: " + str(explosion_resistance))
        except ValueError:
            print("Warning: Invalid explosion resistance value, using default 1.0")

    # 看看发光等级有没有传过来:)
    lightStart = par.find("light=\"") + 7
    if lightStart != 6:
        for j in range(lightStart, size):
            if par[j] == '"':
                lightEnd = j
                break
        try:
            light_level = int(par[lightStart:lightEnd])
            if light_level < 0 or light_level > 15:
                print("Warning: Light level must be between 0-15, using 0")
                light_level = 0
            else:
                print("light level: " + str(light_level))
        except ValueError:
            print("Warning: Invalid light level value, using default 0")

    # 创建文件
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
    
  
    blocks_path = mod_name + "/blocks"
    try:
        os.makedirs(blocks_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating blocks directory: {e}")
        return
    
    
    block_data = {
        "format_version": "1.16.0",
        "minecraft:block": {
            "description": {
                "identifier": f"{mod_name}:{name}",
                "is_experimental": False,
                "register_to_creative_menu": True
            },
            "components": {
                "minecraft:destroy_time": 1.5,
                "minecraft:explosion_resistance": explosion_resistance,
                "minecraft:friction": 0.6,
                "minecraft:map_color": icon
            }
        }
    }

    if light_level > 0:
        block_data["minecraft:block"]["components"]["minecraft:light_emission"] = light_level

    block_content = json.dumps(block_data, indent=4, ensure_ascii=False)
    
    try:
        with open(blocks_path + "/" + name + ".json", "w") as file:
            file.write(block_content)
        print("Block definition created successfully!")
    except Exception as e:
        print(f"Error writing block definition: {e}")
        return
    
    # 更新语言文件
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


#为了追加参数更方便具体的json配置就分开来了