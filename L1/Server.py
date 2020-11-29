import sys
import os 
import Ice
import logging
Ice.loadSlice("icegauntlet.ice")
import IceGauntlet

class ServerI(IceGauntlet.Server):
    def __init__(self, auth):
        self.auth_server = auth
        self.room = ''

    def getRoom(self,current=None):
        try:
            return self.room
        except Exception as err:
            print('Error.RoomAlreadyExists {}'.format(err)) 
            raise IceGauntlet.RoomAlreadyExists(str(err))
    
    def Publish(self,token,roomData,current=None):
        if self.auth_server.isValid(token):
            print('El token es valido')
            print('Datos: ')
            print(token)
            print(roomData)
        else: 
            raise IceGauntlet.Unauthorized('Error.Invalid token')
            
    def Remove(self,token,roomName,current=None):
        if self.auth_server.isValid(token):
            print('El token es valido')
            print('Datos: ')
            print(token)
            print(roomData)
        else: 
            raise IceGauntlet.RoomNotExists('Error.RoomNotExists')
     

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
            communicator.waitForShutdown()
    

            return 0


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
        