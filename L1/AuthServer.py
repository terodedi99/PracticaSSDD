import sys
import os
import Ice

Ice.loadSlice("icegauntlet.ice")
import IceGauntlet 


class AuthServer(Ice.Application):
    def run():


class AuthServerI(IceGauntlet.AuthServer):
    def isValid(self,token,current=None):
        try:
            
        except Exception as err:
            print('Error.Invalid token {}'.format(err)) #lanzamos excepcion, haciendo referencia a la del slice
            raise IceGauntlet.Unauthorized(str(err))

    def getNewToken(self,user,passHash, current=None):
        try:
            
        except Exception as err:
            print('Error.Invalid token {}'.format(err)) #lanzamos excepcion, haciendo referencia a la del slice
            raise IceGauntlet.Unauthorized(str(err))
    
    def changePassword(self,user,currentPassHash,newPassHash,current=None):
        try:
            
        except Exception as err:
            print('Error.Invalid token {}'.format(err)) #lanzamos excepcion, haciendo referencia a la del slice
            raise IceGauntlet.Unauthorized(str(err))