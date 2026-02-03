import os
import sys
import uuid

uuid1=uuid.uuid4()
uuid2=uuid.uuid4()
def _main_():
    print("Founding mod...")
    par=sys.argv[1]
    size=len(par)
    for i in range(1):
        nameStart = par.find("name=")+5
        for j in range(nameStart,size):
            if par[j]=='"':
                nameEnd = j
                break
        name = par[nameStart:nameEnd]
        print("mod name: "+name)
            
        desStart = par.find("des=")+5
        for j in range(desStart,size):
            if par[j]=='"':
                desEnd = j
                break
        des = par[desStart:desEnd]

        print("mod des: "+des)

        os.system("mkdir "+name)
        with open(name+"/manifest.json","w") as file:
            file.write('''
            {
                "format_version": 2,
                "header": {
                    "name": "''' + name + '''",
                    "description": "''' + des + '''",
                    "uuid": "''' + str(uuid1) + '''",
                    "version": [1, 0, 0],
                    "min_engine_version": [1, 14, 0]
                }, 
                "modules": [
                    {
                        "type": "client_script",
                        "entry": "mod.lua",
                        "version": [1, 0, 0]
                    }
                ]
                "dependencies": [
                    {
                        "uuid": "''' + str(uuid2) + '''",
                        "version": [1, 14, 0]
                    }
                ]
            }
            ''')
            file.close()
        os.makedirs(name+"/textures")
        os.makedirs(name+"/entities")
        os.makedirs(name+"/blocks")
        os.makedirs(name+"/recipes")
        os.makedirs(name+"/functions")
        os.makedirs(name+"/loot_tables")
        os.makedirs(name+"/spawn_rules")
        return "name:"+name

_main_()