import os
import sys
import json

def _main_():
    print("Creating item...")

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

    # 解析物品名称
    nameStart = par.find("name=\"") + 6
    if nameStart == 5:  # 没有找到name="
        print("Error: name parameter not found!")
        return

    for j in range(nameStart, size):
        if par[j] == '"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("item name: " + name)

    # 解析物品描述
    desStart = par.find("des=\"") + 5
    if desStart == 4:  # 没有找到des="
        print("Error: des parameter not found!")
        return

    for j in range(desStart, size):
        if par[j] == '"':
            desEnd = j
            break
    des = par[desStart:desEnd]
    print("item des: " + des)

    # 解析物品类型 (2d/3d)
    typeStart = par.find("type=\"") + 6
    if typeStart == 5:  # 没有找到type="
        print("Error: type parameter not found! Use '2d' or '3d'")
        return

    for j in range(typeStart, size):
        if par[j] == '"':
            typeEnd = j
            break
    item_type = par[typeStart:typeEnd].lower()
    if item_type not in ['2d', '3d']:
        print("Error: type must be '2d' or '3d'")
        return
    print("item type: " + item_type)

    # 解析纹理/模型名称
    textureStart = par.find("texture=\"") + 9
    if textureStart == 8:  # 没有找到texture="
        print("Error: texture parameter not found!")
        return

    for j in range(textureStart, size):
        if par[j] == '"':
            textureEnd = j
            break
    texture = par[textureStart:textureEnd]
    print("item texture/model: " + texture)

    # 解析可选参数
    edible = False
    edible_effect = ""
    hand_effect = ""

    # 检查是否可食用
    if "edible=\"true\"" in par:
        edible = True
        # 解析食用效果
        effectStart = par.find("effect=\"") + 8
        if effectStart != 7:
            for j in range(effectStart, size):
                if par[j] == '"':
                    effectEnd = j
                    break
            edible_effect = par[effectStart:effectEnd]
            print("edible effect: " + edible_effect)

    # 解析手持效果
    handStart = par.find("hand=\"") + 6
    if handStart != 5:
        for j in range(handStart, size):
            if par[j] == '"':
                handEnd = j
                break
        hand_effect = par[handStart:handEnd]
        print("hand effect: " + hand_effect)

    # 创建物品目录结构
    items_path = mod_name + "/items"
    textures_items_path = mod_name + "/textures/items"
    models_items_path = mod_name + "/models/items"

    try:
        os.makedirs(items_path, exist_ok=True)
        os.makedirs(textures_items_path, exist_ok=True)
        # 确保models父目录存在
        os.makedirs(mod_name + "/models", exist_ok=True)
        if item_type == '3d':
            os.makedirs(models_items_path, exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        return

    # 创建物品定义JSON文件
    item_content = {
        "format_version": "1.16.0",
        "minecraft:item": {
            "description": {
                "identifier": f"{mod_name}:{name}",
                "category": "items"
            },
            "components": {
                "minecraft:icon": {
                    "texture": f"{name}"
                },
                "minecraft:display_name": {
                    "value": f"item.{mod_name}:{name}.name"
                }
            }
        }
    }

    # 添加可选组件
    if edible:
        item_content["minecraft:item"]["components"]["minecraft:food"] = {
            "nutrition": 4,
            "saturation_modifier": "normal"
        }
        if edible_effect:
            item_content["minecraft:item"]["components"]["minecraft:food"]["effects"] = [
                {
                    "name": edible_effect,
                    "chance": 1.0,
                    "duration": 30,
                    "amplifier": 0
                }
            ]

    if hand_effect:
        item_content["minecraft:item"]["components"]["minecraft:hand_equipped"] = True
        if hand_effect == "sword":
            item_content["minecraft:item"]["components"]["minecraft:damage"] = 5
            item_content["minecraft:item"]["components"]["minecraft:durability"] = {
                "max_durability": 1561
            }

    try:
        with open(items_path + "/" + name + ".json", "w", encoding='utf-8') as file:
            json.dump(item_content, file, indent=4, ensure_ascii=False)
        print("Item definition created successfully!")
    except Exception as e:
        print(f"Error writing item definition: {e}")
        return

    # 创建纹理JSON文件
    if item_type == '2d':
        texture_content = f'''{{
    "resource_pack_name": "{mod_name}",
    "texture_name": "atlas.items",
    "texture_data": {{
        "{name}": {{
            "textures": "textures/items/{texture}"
        }}
    }}
}}'''
    else:  # 3d
        texture_content = f'''{{
    "resource_pack_name": "{mod_name}",
    "texture_name": "atlas.items",
    "texture_data": {{
        "{name}": {{
            "textures": {{
                "up": "textures/items/{texture}_up",
                "down": "textures/items/{texture}_down",
                "north": "textures/items/{texture}_side",
                "south": "textures/items/{texture}_side",
                "east": "textures/items/{texture}_side",
                "west": "textures/items/{texture}_side"
            }}
        }}
    }}
}}'''

    try:
        with open(textures_items_path + "/" + name + "_texture.json", "w") as file:
            file.write(texture_content)
        print("Texture JSON created successfully!")
    except Exception as e:
        print(f"Error writing texture JSON: {e}")
        return

    # 如果是3D物品，创建模型文件
    if item_type == '3d':
        model_content = f'''{{
    "format_version": "1.12.0",
    "minecraft:geometry": [
        {{
            "description": {{
                "identifier": "geometry.{mod_name}.{name}",
                "texture_width": 32,
                "texture_height": 32
            }},
            "bones": [
                {{
                    "name": "body",
                    "pivot": [0, 0, 0],
                    "cubes": [
                        {{
                            "origin": [-4, 0, -4],
                            "size": [8, 8, 8],
                            "uv": {{
                                "north": {{"uv": [0, 0], "uv_size": [8, 8]}},
                                "east": {{"uv": [0, 0], "uv_size": [8, 8]}},
                                "south": {{"uv": [0, 0], "uv_size": [8, 8]}},
                                "west": {{"uv": [0, 0], "uv_size": [8, 8]}},
                                "up": {{"uv": [0, 0], "uv_size": [8, 8]}},
                                "down": {{"uv": [0, 0], "uv_size": [8, 8]}}
                            }}
                        }}
                    ]
                }}
            ]
        }}
    ]
}}'''

        try:
            with open(models_items_path + "/" + name + ".json", "w") as file:
                file.write(model_content)
            print("3D model created successfully!")
        except Exception as e:
            print(f"Error writing 3D model: {e}")
            return

    # 更新语言文件
    try:
        with open(mod_name + "/texts/zh_CN.lang", "a", encoding='utf-8') as file:
            file.write(f"item.{mod_name}:{name}.name={name}\n")
            if des:
                file.write(f"item.{mod_name}:{name}.desc={des}\n")
        print("Language file updated successfully!")
    except Exception as e:
        print(f"Error writing language file: {e}")
        return

    print("Item creation completed!")

if __name__ == "__main__":
    _main_()
