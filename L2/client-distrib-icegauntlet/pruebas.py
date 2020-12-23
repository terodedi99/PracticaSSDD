import json
from random import shuffle

try:
    with open('maps.json') as f:
        maps=f.read()
        maps=json.loads(maps)
except:
    print("Eror, Not found data base")

keys=[]



for key in maps :
    keys.append(key)

shuffle(keys)

print(keys[0])