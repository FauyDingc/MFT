import os
import sys
import json

sys.stdout.flush()

def parse_params(params_str):
    """解析参数字符串，返回字典"""
    params = {}
    if not params_str:
        return params
    
    i = 0
    length = len(params_str)
    
    while i < length:
        # 跳过空白和逗号
        while i < length and (params_str[i].isspace() or params_str[i] == ','):
            i += 1
        if i >= length:
            break
        
        # 找等号
        eq_pos = params_str.find('=', i)
        if eq_pos == -1:
            break
        
        key = params_str[i:eq_pos].strip()
        i = eq_pos + 1
        
        # 跳过空白
        while i < length and params_str[i].isspace():
            i += 1
        if i >= length:
            break
        
        # 解析值
        value = ""
        if params_str[i] in ('"', "'"):
            quote = params_str[i]
            i += 1
            while i < length:
                # 处理转义字符
                if params_str[i] == '\\' and i + 1 < length:
                    next_char = params_str[i + 1]
                    if next_char == 'n':
                        value += '\n'
                    elif next_char == 't':
                        value += '\t'
                    elif next_char == '"':
                        value += '"'
                    elif next_char == "'":
                        value += "'"
                    else:
                        value += next_char
                    i += 2
                elif params_str[i] == quote:
                    i += 1
                    break
                else:
                    value += params_str[i]
                    i += 1
        else:
            while i < length and params_str[i] not in ',;':
                value += params_str[i]
                i += 1
        
        if key:
            params[key] = value.strip()
    
    return params


def main():
    print("Founding block...")
    
    if len(sys.argv) < 2:
        print("Error: No arguments provided!")
        return
    
    params = parse_params(sys.argv[1])
    
    # 获取输出路径
    out_path = params.get('out', 'output/')
    if out_path and not out_path.endswith('/'):
        out_path += '/'
    print(f"Output path: {out_path}")
    
    # 获取模组名称
    mod_name = params.get('name', '')
    if not mod_name:
        print("Error: 'mod_name' parameter not found!")
        return
    print(f"Mod name: {mod_name}")
    
    # 获取方块名称
    block_name = params.get('block', '')
    if not block_name:
        print("Error: 'block' parameter not found!")
        return
    print(f"Block name: {block_name}")
    
    # 获取描述
    des = params.get('des', '')
    print(f"Block description: {des}")
    
    # 获取纹理
    icon = params.get('icon', '')
    if not icon:
        print("Error: 'icon' parameter not found!")
        return
    print(f"Block icon: {icon}")
    
    # 可选参数
    explosion = float(params.get('explosion', 1.0))
    print(f"Explosion resistance: {explosion}")
    
    light = int(params.get('light', 0))
    if light < 0 or light > 15:
        print("Warning: Light level must be 0-15, using 0")
        light = 0
    print(f"Light level: {light}")
    
    # 创建目录
    mod_path = os.path.join(out_path, mod_name)
    textures_path = os.path.join(mod_path, 'textures', 'blocks')
    
    try:
        os.makedirs(textures_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating textures directory: {e}")
        return
    
    # 创建纹理JSON
    texture_content = '''{
    "resource_pack_name": "''' + mod_name + '''",
    "texture_name": "atlas.terrain",
    "padding": 16,
    "resource_pack_format_version": 1,
    "texture_data": {
        "''' + block_name + '''": {
            "textures": "textures/blocks/''' + icon + '''"
        }
    }
}'''
    
    try:
        with open(os.path.join(textures_path, block_name + "_texture.json"), "w") as f:
            f.write(texture_content)
        print("Texture JSON created successfully!")
    except Exception as e:
        print(f"Error writing texture JSON: {e}")
        return
    
    # 创建方块定义
    blocks_path = os.path.join(mod_path, 'blocks')
    try:
        os.makedirs(blocks_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating blocks directory: {e}")
        return
    
    block_data = {
        "format_version": "1.16.0",
        "minecraft:block": {
            "description": {
                "identifier": f"{mod_name}:{block_name}",
                "is_experimental": False,
                "register_to_creative_menu": True
            },
            "components": {
                "minecraft:destroy_time": 1.5,
                "minecraft:explosion_resistance": explosion,
                "minecraft:friction": 0.6,
                "minecraft:map_color": icon
            }
        }
    }
    
    if light > 0:
        block_data["minecraft:block"]["components"]["minecraft:light_emission"] = light
    
    try:
        with open(os.path.join(blocks_path, block_name + ".json"), "w") as f:
            json.dump(block_data, f, indent=4, ensure_ascii=False)
        print("Block definition created successfully!")
    except Exception as e:
        print(f"Error writing block definition: {e}")
        return
    
    # 更新语言文件
    try:
        with open(os.path.join(mod_path, "texts", "zh_CN.lang"), "a", encoding='utf-8') as f:
            f.write(f"tile.{mod_name}:{block_name}.name={block_name}\n")
            f.write(f"tile.{mod_name}:{block_name}.desc={des}\n")
        print("Language file updated successfully!")
    except Exception as e:
        print(f"Error writing language file: {e}")
        return
    
    print("Block creation completed!")


if __name__ == "__main__":
    main()

