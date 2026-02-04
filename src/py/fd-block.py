import sys
import os

def _main_():
    print("Founding block...")
    par=sys.argv[1]
    size=len(par)
    nameStart = par.find("name=")+5
    for j in range(nameStart,size):
        if par[j]=='"':
            nameEnd = j
            break
    name = par[nameStart:nameEnd]
    print("block name: "+name+'\n')
        
    desStart = par.find("des=")+4
    for j in range(desStart,size):
        if par[j]=='"':
            desEnd = j
            break
    des = par[desStart:desEnd]

    print("block des: "+des+'\n')

    iconStart = par.find("icon=")+5
    for j in range(iconStart,size):
        if par[j]=='"':
            iconEnd = j
            break
    icon = par[iconStart:iconEnd]
    print("block icon: "+icon+'\n')

_main_()