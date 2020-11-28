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
        
        

        try:
            p = getpass.getpass()
        except Exception as err:
            print('ERROR:', err)
        passHash = hashlib.sha256(p.encode()).hexdigest()
        print(m)
        #server.changePassword("pedro.millan",None, m)

        #print(server.isValid("fTEDqMMqrDE1JY3IkrW3shbEm57iB8InYttOi9Xd"))
        print(server.getNewToken("pedro.millan","f86b776078cd49867e70c387164c81adefa91350f56d948991ec852419e1ec19"))

        ##server.changePassword("pedro.millan",None, "puta")

        

ClientAuth().main(sys.argv)

        