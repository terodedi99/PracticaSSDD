#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

class ClientAuth(Ice.Application):
    def run(self,argv):
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.AuthenticationPrx.checkedCast(proxy)

        if not server:
            raise RuntimeError('Invalid Proxy')

        
        print(server.isValid("pedro"))


        

ClientAuth().main(sys.argv)

        