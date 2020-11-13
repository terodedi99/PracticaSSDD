import sys
import os 
import Ice

Ice.loadSlice("icegauntlet.ice")
import icegauntlet

class Server(Ice.Application):
    def run():

class ServerI(icegauntlet.Server):
    def getRoom(self,current=None):
        try:
            
        except Exception as err:
            print('Error.RoomAlreadyExists {}'.format(err)) 
            raise IceGauntlet.RoomAlreadyExists(str(err))
    
    def Publish(self,toke,roomData,current=None):ç
        try:
            
        except Exception as err:
            print('Error.Invalid token {}'.format(err)) 
            raise IceGauntlet.Unauthorized(str(err))
    
    def Remove(self,token,roomName,current=None):
        try:
            
        except Exception as err:
            print('Error.RoomNotExists {}'.format(err)) 
            raise IceGauntlet.RoomNotExists(str(err))
        