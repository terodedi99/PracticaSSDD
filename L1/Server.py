import sys
import os 
import Ice
import logging
Ice.loadSlice("icegauntlet.ice")
import IceGauntlet
import json
import yaml

class ServerI(IceGauntlet.RoomManager):
    def __init__(self, auth):
        self.auth_server = auth
        self.room = ''


    
    def Publish(self,token,roomData,current=None):
        datos=''
        roomData=yaml.load(roomData)
               
        if self.auth_server.isValid(token):
            print('el token es valido')
            room=roomData["room"]
            print(' la room es',room)
            ruta='client-distrib-icegauntlet/assets/'+room+'.json'
            if not os.path.isfile(ruta):            
                with open(ruta,'w') as f:
                    json.dump(roomData, f, indent=4)
                print('El token es valido')

                try:
                    with open('maps.json') as f:
                        maps=f.read()
                    maps=json.loads(maps)
                except:
                    print("Eror, Not found data base")

                maps[room]={'token' : token}
                with open('maps.json','w') as f:
                    json.dump(maps, f, indent=4)
            else:
                raise IceGauntlet.RoomAlreadyExists()
        else: 
            raise IceGauntlet.Unauthorized()
            
    def Remove(self,token,roomName,current=None):


        if self.auth_server.isValid(token):

            print(token)
            if(os.path.exists('client-distrib-icegauntlet/assets/'+roomName+'.json')):
            
                try:
                    with open('maps.json') as f:
                        maps=f.read()
                    maps=json.loads(maps)
                except:
                    print("Eror, Not found data base")

                if (maps[roomName]['token']!= token):
                    raise IceGauntlet.Unauthorized()
                else:
                    os.remove('client-distrib-icegauntlet/assets/'+roomName+'.json')
                    maps[roomName]={}
                    
                    with open('maps.json','w') as f:
                        json.dump(maps, f, indent=4)


                
            else:
                raise IceGauntlet.RoomNotExists()     
        else: 
            raise IceGauntlet.Unauthorized()
     
class DungeonI(IceGauntlet.Dungeon):
    def getRoom(self,current=None):
        try:
            return self.room
        except Exception as err:
            print('Error.RoomAlreadyExists {}'.format(err)) 
            raise IceGauntlet.RoomAlreadyExists(str(err))
class Server(Ice.Application):
    '''
    Server
    '''
    def run(self, args):
        '''
        Server loop
        '''
        with Ice.initialize(sys.argv, "server.config") as communicator:
            auth_proxy=self.communicator().stringToProxy(sys.argv[1])
            auth_server= IceGauntlet.AuthenticationPrx.checkedCast(auth_proxy)
            



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
        