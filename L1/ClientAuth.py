#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet
import hashlib
import getpass
import argparse
import json
import os

class ClientAuth(Ice.Application):
    def leer_json(self,fichero,user):
        try:
            with open(fichero) as f:
                usuario=f.read()
            usuario=json.loads(usuario)
        except:
            print("Eror, Not found data base")
        
        try :
            password=usuario[user]['password_hash']
            return password
        except:
            return None


    def run(self,argv):
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.AuthenticationPrx.checkedCast(proxy)


        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 3:
            raise RuntimeError('Error. Parametros insuficientes')

        user= argv[2]
        password_hash=self.leer_json('users.json',user)
        print('Enter password: ')
        p = getpass.getpass()
       
        if password_hash == None:
            print('creando nueva contraseña...')
            p = getpass.getpass()
            passHash = hashlib.sha256(p.encode()).hexdigest()
            print(password_hash)
            server.changePassword(user,None,passHash)
        
        if len(sys.argv)==4:
            option = argv[3]
        else:
            option='d'

        if option == 'c':
            p = getpass.getpass()
            passHash = hashlib.sha256(p.encode()).hexdigest()

            try:
                print("---Introducir nueva contraseña---")
                np = getpass.getpass()
            except Exception as err:
                print('ERROR:', err)
    

            #passHash = hashlib.sha256(p.encode()).hexdigest()
            newpassHash = hashlib.sha256(np.encode()).hexdigest()
            server.changePassword(user,passHash,newpassHash)
        elif option == 't' :
            passHash = hashlib.sha256(p.encode()).hexdigest()
            print(server.getNewToken(user,passHash))
            

        elif option == 'd':
            os.system('python3 ClientServer.py "server -t -e 1.1:tcp -h 192.168.0.15 -p 8700 -t 60000" jesus.gamero "bSOlGteFhvjxLEZQF4nTs7LM0KHcMI1qVEbgEkod" r mi_mapa')


ClientAuth().main(sys.argv)

        