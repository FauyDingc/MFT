import os
import sys
import uuid

sys.stdout.flush()

def parse_params(params_str):
    """解析参数字符串，返回字典"""
    params = {}
    if not params_str:
        return params

    # Strip outer {}
    if params_str.startswith('{') and params_str.endswith('}'):
        params_str = params_str[1:-1]

    # Split by ,
    parts = params_str.split(',')
    for part in parts:
        part = part.strip()
        if ':' in part:
            key, value = part.split(':', 1)
            key = key.strip()
            value = value.strip()
            # Remove quotes
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            params[key] = value

    return params


def main():
    print("Founding mod...")
    
    if len(sys.argv) < 2:
        print("Error: No arguments provided!")
        return
    
    # 获取输出路径
    out_path = args.out
    if out_path and not out_path.endswith('/'):
        out_path += '/'

    print(f"输出路径: {out_path}")

    # 获取模组名称
    name = args.name
    print(f"模组名称: {name}")

    # 获取描述
    des = args.des
    print(f"模组描述: {des}")
    
    # 生成UUID
    uuid1 = str(uuid.uuid4())
    uuid2 = str(uuid.uuid4())
    
    # 创建目录结构
    mod_path = os.path.join(out_path, name)
    directories = [
        os.path.join(mod_path, 'textures', 'blocks'),
        os.path.join(mod_path, 'textures', 'items'),
        os.path.join(mod_path, 'models', 'block'),
        os.path.join(mod_path, 'models', 'items'),
        os.path.join(mod_path, 'blocks'),
        os.path.join(mod_path, 'items'),
        os.path.join(mod_path, 'texts'),
        os.path.join(mod_path, 'scripts'),
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            print(f"Error creating directory {directory}: {e}")
            return
    
    # 创建manifest.json
    manifest = '''{
    "format_version": 2,
    "header": {
        "name": "''' + name + '''",
        "description": "''' + des + '''",
        "uuid": "''' + uuid1 + '''",
        "version": [1, 0, 0],
        "min_engine_version": [1, 14, 0]
    }, 
    "modules": [
        {
            "type": "script",
            "entry": "scripts/mod.js",
            "version": [1, 0, 0]
        }
    ],
    "dependencies": [
        {
            "uuid": "''' + uuid2 + '''",
            "version": [1, 14, 0]
        }
    ]
}'''
    
    try:
        with open(os.path.join(mod_path, "manifest.json"), "w") as f:
            f.write(manifest)
        print("manifest.json创建成功！")
    except Exception as e:
        print(f"写入manifest.json时出错: {e}")
        return

    # 创建mod脚本
    script_content = '''// Mod: ''' + name + '''
// Description: ''' + des + '''

console.log("Mod ''' + name + ''' loaded!");
'''

    try:
        with open(os.path.join(mod_path, "scripts", "mod.js"), "w") as f:
            f.write(script_content)
        print("mod.js创建成功！")
    except Exception as e:
        print(f"写入mod.js时出错: {e}")
        return

    # 创建语言文件
    try:
        with open(os.path.join(mod_path, "texts", "zh_CN.lang"), "w", encoding='utf-8') as f:
            f.write(f"mod.name={name}\n")
            f.write(f"mod.description={des}\n")
        print("语言文件创建成功！")
    except Exception as e:
        print(f"写入语言文件时出错: {e}")
        return

    print(f"name:{name}")


if __name__ == "__main__":
    main()

