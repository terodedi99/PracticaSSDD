#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib



class ClientAuth(Ice.Application):
    def run(self,argv):
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not server:
            raise RuntimeError('Invalid Proxy')

        
        print(server.isValid("fTEDqMMqrDE1JY3IkrW3shbEm57iB8InYttOi9Xd"))


        ##server.changePassword("pedro.millan",None, "puta")

        

ClientAuth().main(sys.argv)

        