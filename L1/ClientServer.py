#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib
import getpass


class ClientServer(Ice.Application):
    def run(self,argv):
        # serverprx argv[1] name_user argv[2] token argv[3] op argv[4] name_json argv[5]
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.ServerPrx.checkedCast(proxy)

        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 6:
            raise RuntimeError('Error')

        user= argv[2]

        if argv[4] == 'p':
            # publish
            try:
                server.Publish(argv[3], argv[5])
            except Exception as err:
                print('ERROR:', err)
        elif argv[4] == 'r':
            # remove
            try:
                server.Remove(argv[3], argv[5])
            except Exception as err:
                print('ERROR:', err)
        

ClientServer().main(sys.argv)

        