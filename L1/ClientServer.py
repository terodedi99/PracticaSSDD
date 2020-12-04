#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0103
# pylint: disable=E0401
# pylint: disable=W0703
# pylint: disable=C0413

import sys
import json
import Ice
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

class ClientServer(Ice.Application):
    def run(self,argv):
        # serverprx argv[1] name_user argv[2] token argv[3] op argv[4] name_json argv[5]
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.RoomManagerPrx.checkedCast(proxy)
        print(server)
        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 6:
            raise RuntimeError('Error')
        if argv[4] == 'p':
            # publish
            ruta='Mapas-creados/'+argv[5]
            print(ruta)
            try:
                with open(ruta,'r') as f:
                    datos=f.read()
                    datos=json.loads(datos)
            except:
                print("No se ha podido leer el fichero json de busqueda")
            try:
                #server.getRoom()
                server.Publish(argv[3],str(datos))
            except Exception as err:
                print('ERROR:', err)
        elif argv[4] == 'r':
            # remove
            try:
                server.Remove(argv[3], argv[5])
            except Exception as err:
                print('ERROR:', err)
ClientServer().main(sys.argv)
        