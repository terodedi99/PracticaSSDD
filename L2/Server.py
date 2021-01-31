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
import IceStorm
Ice.loadSlice("icegauntlet.ice")
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet
import uuid

PROPERTY_AUTH = "property_authorization"
ADAPTER = "ServerAdapter"
DUNGEONADAPTER = "DungeonAdapter"
ICESTORM_MANAGER = 'SSDD-GameroMillanRodriguez.IceStorm/TopicManager'
SYNCCHANGEL = "RoomManagerSyncChannel"
lista=[]

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

    def publish(self, token, roomData, current=None):
        datos = ''
        roomData = yaml.load(roomData)
        room_name = roomData['room']
       
        user= self.auth_server.getOwner(token)
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

            maps[room] = {'user' : user,
                        'name' : room_name}
            with open('client-distrib-icegauntlet/publicmaps.json', 'w') as f:
                json.dump(maps, f, indent=4)
        else:
            raise IceGauntlet.RoomAlreadyExists()
    # pylint: disable=W0613
    def remove(self, token, roomName, current=None):

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

            
        if os.path.exists(fichero_room):
            try:
                with open('client-distrib-icegauntlet/publicmaps.json') as f:
                    maps = f.read()
                maps = json.loads(maps)
            except FileNotFoundError:
                print("Eror, Not found data base")

            if maps[nombrefichero]['user'] != self.auth_server.getOwner(token):
                # pylint: disable=R1720
                raise IceGauntlet.Unauthorized()
            else:
                os.remove(fichero_room)
                del maps[nombrefichero]
                with open('client-distrib-icegauntlet/publicmaps.json', 'w') as f:
                    json.dump(maps, f, indent=4)
        else:
            raise IceGauntlet.RoomNotExists()
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

class ServerSyncI(IceGauntlet.RoomManagerSync):

    def __init__(self, id_server, room_manager_sync_channel_prx, room_manager_prx):
        self.id_server = id_server
        self.room_manager_sync_channel_prx = room_manager_sync_channel_prx
        self.room_manager_prx = room_manager_prx


    def hello(self, room_manager_prx, id_server, current=None):
        print('HELLO    '+id_server+' conoce a ' + self.id_server)
       
        
        servers_sync_prx = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(self.room_manager_sync_channel_prx.getPublisher()) 
        if self.id_server != id_server and self.id_server not in lista:
            lista.append(id_server)
            servers_sync_prx.announce(self.room_manager_prx, self.id_server)  
         


    def announce(self, room_manager_prx, id_server, current=None):
        lista.append(id_server)
        
        if self.id_server != id_server:
            print('ANNOUNCE '+id_server+' conoce a ' + self.id_server)
        
    def hello_client(self, current=None):
        servers_sync_prx = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(self.room_manager_sync_channel_prx.getPublisher()) 
        servers_sync_prx.hello(self.room_manager_prx, self.id_server)  
    
    def newRoom(self, roomName, managerId, current=None):
        '''room_manager_prx.publish
        a = [room_manager_prx, room_manager_prx, room_manager_prx]
        a[0].publish'''
        
        print('newRoom')
    
    def removedRoom(self, roomName, current=None):
        print('removedRoom')



class Server(Ice.Application):
    '''
    Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        
        '''nombre=''.join(sample(string.ascii_letters, 4))
        os.mkdir('servidor_'+nombre)'''
       
        auth_proxy = self.communicator().propertyToProxy(PROPERTY_AUTH)
        auth_server = IceGauntlet.AuthenticationPrx.checkedCast(auth_proxy)
        if not auth_server:
            raise RuntimeError('Invalid Proxy')

        id_server = uuid.uuid4().hex
        adapter = self.communicator().createObjectAdapter(ADAPTER)
        server = ServerI(auth_server)
        proxy = adapter.add(server, Ice.stringToIdentity("proxy_maps_"+id_server))

        icestorm_proxy = self.communicator().stringToProxy(ICESTORM_MANAGER)
        if icestorm_proxy is None:
        	print("property '{}' not set".format(ICESTORM_MANAGER))
        	return None

        icestorm_topic_manager = IceStorm.TopicManagerPrx.checkedCast(icestorm_proxy)
        if not icestorm_topic_manager:
            print("Invalid topic manager")
            return 1

        try:
            room_manager_sync_channel_prx = icestorm_topic_manager.retrieve(SYNCCHANGEL)
        except IceStorm.NoSuchTopic:
            room_manager_sync_channel_prx = icestorm_topic_manager.create(SYNCCHANGEL)

        room_manager_prx = IceGauntlet.RoomManagerPrx.checkedCast(proxy)
        server_sync = ServerSyncI(id_server, room_manager_sync_channel_prx, room_manager_prx)
        server_sync_prx = adapter.addWithUUID(server_sync)
        room_manager_sync_channel_prx.subscribeAndGetPublisher(dict(), server_sync_prx)

        adapter.activate()
        #print('"{}"'.format(proxy), flush=True)

        '''
        hello
        '''
        server_sync.hello_client()
        
        
        # Dungeon Server


        adapter_dungeon = self.communicator().createObjectAdapter(DUNGEONADAPTER)
        server_dungeon = DungeonI()
        proxy_dungeon = adapter.add(server_dungeon, Ice.stringToIdentity("proxy_dungeon_"+id_server))
        #print('"{}"'.format(proxy_dungeon), flush=True)
        adapter_dungeon.activate()
        proxy_game='"{}"'.format(proxy_dungeon)
        
        '''
        try: 
            if sys.argv[2]=='proxy-maps':
                print(proxy_maps)
            elif sys.argv[2]=='proxy-game':
                print(proxy_game)
            else :
                print('Tipo de proxyy incorrecto. proxy-maps or proxy-game')
        except :
            print('No se ha especificado proxy, los argumentos tienen que ser: <proxy> , <tipo de proxy>')
        '''
        self.communicator().waitForShutdown()
        return 0
if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
        