#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib
import getpass


class ClientAuth(Ice.Application):
    def run(self,argv):
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.AuthenticationPrx.checkedCast(proxy)


        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 3:
            raise RuntimeError('Error. Parametros insuficientes')

        user= argv[2]
        p = getpass.getpass()



        if len(sys.argv)==4:
            option = argv[3]
        else:
            option='d'

        if option == 'c':

            try:
                print("Nueva contraseña: ")
                np = getpass.getpass()
            except Exception as err:
                print('ERROR:', err)
    
    
            passHash = hashlib.sha256(p.encode()).hexdigest()
            newpassHash = hashlib.sha256(np.encode()).hexdigest()
            server.changePassword(user,passHash,newpassHash)
        elif option == 't' :
            passHash = hashlib.sha256(p.encode()).hexdigest()
            print(server.getNewToken(user,passHash))

        elif option == 'd':
            print('Opcion por defecto')


ClientAuth().main(sys.argv)

        