#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib
import getpass
import json 


class ClientServer(Ice.Application):
    def run(self,argv):
        # serverprx argv[1] token argv[2] op argv[3] name_json argv[4]
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.RoomManagerPrx.checkedCast(proxy)
        print(server)
        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 5:
            raise RuntimeError('Error')

        ##user= argv[2]

        if argv[3] == 'p':
            # publish
            ruta='Mapas-creados/'+argv[4]
            print(ruta)
            try:
                with open(ruta,'r') as f:
                    datos=f.read()
                    datos=json.loads(datos)
            except:
                print("No se ha podido leer el fichero json de busqueda")
                
            try:
                #server.getRoom()
                server.Publish(argv[2],str(datos))
            except Exception as err:
                print('ERROR:', err)
        elif argv[3] == 'r':
            # remove
            print('hola')
            try:
                server.Remove(argv[2], argv[4])
            except Exception as err:
                print('ERROR:', err)
        

ClientServer().main(sys.argv)

        