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

class RoomManager(IceGauntlet.RoomManager):
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
class ServerII(IceGauntlet.RoomManagerSync):
    def hello(self,manager,managerid,current=None):

        if not manager in self.server_3.lista:

            print('HOLA')
            self.server_3.lista.append(manager)
        else:
            self.announce(IceGauntlet.RoomManagerPrx.uncheckedCast(self.server_3.servant_subscriber),"hola")

    
    def announce(self,manager,managerid,current=None):
        print("[ANNOUNCE] Previous orchestrator: %s" % manager)
        self.server_3.lista.append(manager)
    
    def newRoom(self,roomName,managerid,current=None):
        print('HOla')

    def removedRoom(self,roomName,current=None):
        print('Hola')

class Server(Ice.Application):
    '''
    Server
    '''
    lista = []
    servant_subscriber=None

    def get_topic_manager(self):
        key = 'IceStorm.TopicManager.Proxy'
        proxy = self.communicator().propertyToProxy(key)
        if proxy is None:
            print("property {} not set".format(key))
            return None
        
        print("Using IceStorm in: '%s'" % key)
        return IceStorm.TopicManagerPrx.checkedCast(proxy)
    
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
            server = RoomManager(auth_server)
            proxy = adapter.add(server, Ice.stringToIdentity("proxy_maps"))
            #print('"{}"'.format(proxy), flush=True)
            adapter.activate()


            adapter_dungeon = communicator.createObjectAdapter("DungeonAdapter")
            server_dungeon = DungeonI()
            proxy_dungeon = adapter.add(server_dungeon, Ice.stringToIdentity("proxy_dungeon"))
            #print('"{}"'.format(proxy_dungeon), flush=True)
            adapter_dungeon.activate()
            proxy_game='"{}"'.format(proxy_dungeon)
            proxy_maps='"{}"'.format(proxy)
            

            ###### Canal de eventos 
            topic_mgr = self.get_topic_manager()
            if not topic_mgr:
                print('Invalid proxy')
                return 2
            

            ####### Subscriptor 
            ic = self.communicator()
            servant_roomManager = ServerII()
            servant_roomManager.server_3 = self
            adapter_instance = ic.createObjectAdapter("RoomManagerSyncAdapter")
            subscriber_instance = adapter_instance.addWithUUID(servant_roomManager)
            print(subscriber_instance)
            topic_name = "RoomManagerTopic"
            qos = {}

            try:
                topic = topic_mgr.retrieve(topic_name)
            except IceStorm.NoSuchTopic:
                print("no such topic found, creating")
                topic = topic_mgr.create(topic_name)
            
            topic.subscribeAndGetPublisher(qos, subscriber_instance)

            ## #### Publicador 
            publisher_instance = topic.getPublisher()
            server_instance = IceGauntlet.RoomManagerSyncPrx.uncheckedCast(publisher_instance)


            
           
            server_instance.hello(IceGauntlet.RoomManagerPrx.uncheckedCast(publisher_instance),str(subscriber_instance))
            
    
            ## Empezar 
            adapter_instance.activate()
            self.shutdownOnInterrupt()
            ic.waitForShutdown()
            ## Acabar 
            topic.unsubscribe(subscriber_instance)



            try: 
                if sys.argv[2]=='proxy-maps':
                    print(proxy_maps)
                elif sys.argv[2]=='proxy-game':
                    print(proxy_game)
                else :
                    print('Tipo de proxyy incorrecto. proxy-maps or proxy-game')
            except :
                print('No se ha especificado proxy, los argumentos tienen que ser: <proxy> , <tipo de proxy>')
            communicator.waitForShutdown()
            return 0

        


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
        