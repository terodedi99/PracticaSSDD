#!/usr/bin/env python3


import json 


try:
    with open('proxy.json') as f:
        data=f.read()
        data=json.load(data)
except:
    print("Eror, Not found data base")

try:
    print(data['proxy_game'])

except :
    print('Server no  ejecutado')
