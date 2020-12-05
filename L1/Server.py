#!/usr/bin/env python3

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0103
# pylint: disable=W0702
# pylint: disable=R0903

import sys
import os
import json
from random import shuffle, sample
from glob import glob
import string
import yaml
import Ice
Ice.loadSlice("icegauntlet.ice")
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

class ServerI(IceGauntlet.RoomManager):
    def __init__(self, auth):
        self.auth_server = auth
        self.room = ''

    def RoomExists(self, roomData):
        '''
        roomAlreadyExists method
        '''
        ficheros = glob('client-distrib-icegauntlet/assets/maps/*.json')
        try:
            for i in ficheros:
                with open(i, 'r') as f:
                    d = f.read()
                d = json.loads(d)
                if d['data'] == roomData:
                    return False
            return True
        except:
            print("Error, not found data base")

    def Publish(self, token, roomData, current=None):
        datos = ''
        roomData = yaml.load(roomData)
        room_name = roomData['room']
        if self.auth_server.isValid(token):
            print('El token es valido')
            room = ''.join(sample(string.ascii_letters, 8))
            ruta = 'client-distrib-icegauntlet/assets/maps/'+room+'.json'
            if self.RoomExists(roomData['data']):
                with open(ruta, 'w') as f:
                    json.dump(roomData, f, indent=4)
                try:
                    with open('client-distrib-icegauntlet/publicmaps.json') as f:
                        maps = f.read()
                        maps = json.loads(maps)
                except:
                    print("Eror, Not found data base")

                maps[room] = {'token' : token,
                            'name' : room_name}
                with open('client-distrib-icegauntlet/publicmaps.json', 'w') as f:
                    json.dump(maps, f, indent=4)
            else:
                raise IceGauntlet.RoomAlreadyExists()
        else:
            raise IceGauntlet.Unauthorized()

    # pylint: disable=W0613
    def Remove(self, token, roomName, current=None):

        ficheros = glob('client-distrib-icegauntlet/assets/maps/*.json')
        fichero_room = ''
        nombrefichero = ''
        try:
            for i in ficheros:
                with open(i, 'r') as f:
                    d = f.read()
                d = json.loads(d)
                if d['room'] == roomName:
                    fichero_room = i
                    nombrefichero = i.split('/')[3].split('.')[0]
        except:
            raise IceGauntlet.RoomNotExists
        if self.auth_server.isValid(token):
            print(token)
            if os.path.exists(fichero_room):
                try:
                    with open('client-distrib-icegauntlet/publicmaps.json') as f:
                        maps = f.read()
                    maps = json.loads(maps)
                except FileNotFoundError:
                    print("Eror, Not found data base")

                if maps[nombrefichero]['token'] != token:
                    # pylint: disable=R1720
                    raise IceGauntlet.Unauthorized()
                else:
                    os.remove(fichero_room)
                    maps[nombrefichero] = {}
                    with open('client-distrib-icegauntlet/publicmaps.json', 'w') as f:
                        json.dump(maps, f, indent=4)
            else:
                raise IceGauntlet.RoomNotExists()
        else:
            raise IceGauntlet.Unauthorized()
class DungeonI(IceGauntlet.Dungeon):
    def getRoom(self, current=None):
        '''
        getRoom method, return a map.json
        '''
        keys = []
        mapa = ''
        try:
            with open('client-distrib-icegauntlet/publicmaps.json') as f:
                maps = f.read()
                maps = json.loads(maps)
        except FileNotFoundError:
            print("Eror, Not found data base")
        for key in maps:
            keys.append(key)

        shuffle(keys)
        mapa = keys[0]

        print('assets/maps/'+mapa+'.json')
        return 'assets/maps/'+mapa+'.json'
class Server(Ice.Application):
    '''
    Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        with Ice.initialize(sys.argv, "server.config") as communicator:
            auth_proxy = self.communicator().stringToProxy(sys.argv[1])
            auth_server = IceGauntlet.AuthenticationPrx.checkedCast(auth_proxy)
            if not auth_server:
                raise RuntimeError('Invalid Proxy')
            adapter = communicator.createObjectAdapter("ServerAdapter")
            server = ServerI(auth_server)
            proxy = adapter.add(server, Ice.stringToIdentity("server"))
            print('"{}"'.format(proxy), flush=True)
            adapter.activate()


            adapter_dungeon = communicator.createObjectAdapter("DungeonAdapter")
            server_dungeon = DungeonI()
            proxy_dungeon = adapter.add(server_dungeon, Ice.stringToIdentity("server_dungeon"))
            print('"{}"'.format(proxy_dungeon), flush=True)
            adapter_dungeon.activate()
            communicator.waitForShutdown()
            return 0
if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
        