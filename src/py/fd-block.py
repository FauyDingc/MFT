import sys
import os

def _main_():
    print("Founding block...")
    par=sys.argv[1]
    size=len(par)

    mod_name_Start = par.find("/;name=")+7
    for j in range(mod_name_Start,size):
        if par[j]==';':
            mod_nameEnd = j
            break
    mod_name = par[mod_name_Start:mod_nameEnd]

    nameStart = par.find("name=\"")+6
    for j in range(nameStart,size):
        if par[j]=='"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("block name: "+name+'\n')
        
    desStart = par.find("des=\"")+5
    for j in range(desStart,size):
        if par[j]=='"':
            desEnd = j
            break
    des = par[desStart:desEnd]

    print("block des: "+des+'\n')

    iconStart = par.find("icon=\"")+6
    for j in range(iconStart,size):
        if par[j]=='"':
            iconEnd = j
            break
    icon = par[iconStart:iconEnd]
    print("block icon: "+icon+'\n')

    with open(mod_name+"/textures/"+name+"_texture.json","w") as file:
        file.write('''
        {
            "resource_pack_name": "''' + mod_name + '''",
            "texture_name": "''' + name + '''.blocks",
            "textures": [
               "'''+ name +'''''' + icon + '''"
            ]
        }
        ''')
        file.close()
    with open(mod_name+"/texts/zh_CN.lang","w") as file:
        file.write('''
        block.''' + mod_name + '''.''' + name + '''=''' + name + '''
        ''')

_main_()