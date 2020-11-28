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
            raise RuntimeError('No user')

        user= argv[2]
        p = getpass.getpass()



        if len(sys.argv)==4:
            option = argv[3]
        else:
            option='d'

        if option == 'c':

            try:
                print("Nueva Contraseña: ")
                np = getpass.getpass()
            except Exception as err:
                print('ERROR:', err)
    
    
            passHash = hashlib.sha256(p.encode()).hexdigest()
            newpassHash = hashlib.sha256(np.encode()).hexdigest()
            server.changePassword(user,passHash,newpassHash)
        elif option == 'p' :
            passHash = hashlib.sha256(p.encode()).hexdigest()
            print(server.getNewToken("pedro.millan",passHash))

        elif option == 'd':
            print('Opcion por defecto')


            

        ##print(token)
        ##print(server.isValid(token))
        #print(server.isValid("fTEDqMMqrDE1JY3IkrW3shbEm57iB8InYttOi9Xd"))
        ##print(server.getNewToken("pedro.millan","f86b776078cd49867e70c387164c81adefa91350f56d948991ec852419e1ec19"))

        ##print(server.isValid('FbilB401HoxBilz4BJUbFJs51WgyoCtf8TfwK4qh'))


        ##token= server.getNewToken(u , passHash)

ClientAuth().main(sys.argv)

        