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
    print("Creating item...")
    
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
        print("Error: 'name' parameter not found (mod_name)!")
        return
    print(f"Mod name: {mod_name}")
    
    # 获取物品名称
    item_name = params.get('item', '')
    if not item_name:
        print("Error: 'item' parameter not found!")
        return
    print(f"Item name: {item_name}")
    
    # 获取描述
    des = params.get('des', '')
    print(f"Item description: {des}")
    
    # 获取类型
    item_type = params.get('type', '2d').lower()
    if item_type not in ['2d', '3d']:
        print("Error: type must be '2d' or '3d'")
        return
    print(f"Item type: {item_type}")
    
    # 获取纹理
    texture = params.get('texture', '')
    print(f"Item texture: {texture}")
    
    # 可选参数
    edible = params.get('edible', 'false').lower() == 'true'
    print(f"Edible: {edible}")
    
    edible_effect = params.get('effect', '')
    if edible and edible_effect:
        print(f"Edible effect: {edible_effect}")
    
    hand_effect = params.get('hand', '')
    print(f"Hand effect: {hand_effect}")
    
    # 创建目录
    mod_path = os.path.join(out_path, mod_name)
    items_path = os.path.join(mod_path, 'items')
    textures_items_path = os.path.join(mod_path, 'textures', 'items')
    
    try:
        os.makedirs(items_path, exist_ok=True)
        os.makedirs(textures_items_path, exist_ok=True)
        os.makedirs(os.path.join(mod_path, 'models'), exist_ok=True)
        if item_type == '3d':
            os.makedirs(os.path.join(mod_path, 'models', 'items'), exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return
    
    # 创建物品定义
    item_data = {
        "format_version": "1.16.0",
        "minecraft:item": {
            "description": {
                "identifier": f"{mod_name}:{item_name}",
                "category": "items"
            },
            "components": {
                "minecraft:icon": {
                    "texture": f"{item_name}"
                },
                "minecraft:display_name": {
                    "value": f"item.{mod_name}:{item_name}.name"
                }
            }
        }
    }
    
    if edible:
        item_data["minecraft:item"]["components"]["minecraft:food"] = {
            "nutrition": 4,
            "saturation_modifier": "normal"
        }
        if edible_effect:
            item_data["minecraft:item"]["components"]["minecraft:food"]["effects"] = [
                {
                    "name": edible_effect,
                    "chance": 1.0,
                    "duration": 30,
                    "amplifier": 0
                }
            ]
    
    if hand_effect:
        item_data["minecraft:item"]["components"]["minecraft:hand_equipped"] = True
        if hand_effect == "sword":
            item_data["minecraft:item"]["components"]["minecraft:damage"] = 5
            item_data["minecraft:item"]["components"]["minecraft:durability"] = {
                "max_durability": 1561
            }
    
    try:
        with open(os.path.join(items_path, item_name + ".json"), "w", encoding='utf-8') as f:
            json.dump(item_data, f, indent=4, ensure_ascii=False)
        print("Item definition created successfully!")
    except Exception as e:
        print(f"Error writing item definition: {e}")
        return
    
    # 创建纹理JSON
    if item_type == '2d':
        texture_content = '''{
    "resource_pack_name": "''' + mod_name + '''",
    "texture_name": "atlas.items",
    "texture_data": {
        "''' + item_name + '''": {
            "textures": "textures/items/''' + texture + '''"
        }
    }
}'''
    else:
        texture_content = '''{
    "resource_pack_name": "''' + mod_name + '''",
    "texture_name": "atlas.items",
    "texture_data": {
        "''' + item_name + '''": {
            "textures": {
                "up": "textures/items/''' + texture + '''_up",
                "down": "textures/items/''' + texture + '''_down",
                "north": "textures/items/''' + texture + '''_side",
                "south": "textures/items/''' + texture + '''_side",
                "east": "textures/items/''' + texture + '''_side",
                "west": "textures/items/''' + texture + '''_side"
            }
        }
    }
}'''
    
    try:
        with open(os.path.join(textures_items_path, item_name + "_texture.json"), "w") as f:
            f.write(texture_content)
        print("Texture JSON created successfully!")
    except Exception as e:
        print(f"Error writing texture JSON: {e}")
        return
    
    # 如果是3D物品，创建模型文件
    if item_type == '3d':
        model_content = '''{
    "format_version": "1.12.0",
    "minecraft:geometry": [
        {
            "description": {
                "identifier": "geometry.''' + mod_name + '''.''' + item_name + '''",
                "texture_width": 32,
                "texture_height": 32
            },
            "bones": [
                {
                    "name": "body",
                    "pivot": [0, 0, 0],
                    "cubes": [
                        {
                            "origin": [-4, 0, -4],
                            "size": [8, 8, 8],
                            "uv": {
                                "north": {"uv": [0, 0], "uv_size": [8, 8]},
                                "east": {"uv": [0, 0], "uv_size": [8, 8]},
                                "south": {"uv": [0, 0], "uv_size": [8, 8]},
                                "west": {"uv": [0, 0], "uv_size": [8, 8]},
                                "up": {"uv": [0, 0], "uv_size": [8, 8]},
                                "down": {"uv": [0, 0], "uv_size": [8, 8]}
                            }
                        }
                    ]
                }
            ]
        }
    ]
}'''
        try:
            with open(os.path.join(mod_path, 'models', 'items', item_name + ".json"), "w") as f:
                f.write(model_content)
            print("3D model created successfully!")
        except Exception as e:
            print(f"Error writing 3D model: {e}")
            return
    
    # 更新语言文件
    try:
        with open(os.path.join(mod_path, "texts", "zh_CN.lang"), "a", encoding='utf-8') as f:
            f.write(f"item.{mod_name}:{item_name}.name={item_name}\n")
            if des:
                f.write(f"item.{mod_name}:{item_name}.desc={des}\n")
        print("Language file updated successfully!")
    except Exception as e:
        print(f"Error writing language file: {e}")
        return
    
    print("Item creation completed!")


if __name__ == "__main__":
    main()

