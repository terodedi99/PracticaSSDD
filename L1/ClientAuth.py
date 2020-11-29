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

class ClientAuth(Ice.Application):
    def run(self,argv):
        proxy=self.communicator().stringToProxy(argv[1])
        server= IceGauntlet.AuthenticationPrx.checkedCast(proxy)


        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 3:
            raise RuntimeError('No user')

        user= argv[2]
        password_hash=self.leer_json("users.json",user)
       
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

            try:
                np = getpass.getpass()
            except Exception as err:
                print('ERROR:', err)
    

            #passHash = hashlib.sha256(p.encode()).hexdigest()
            newpassHash = hashlib.sha256(np.encode()).hexdigest()
            server.changePassword(user,password_hash,newpassHash)
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
    def leer_json(self,fichero,user):
        password_hash=0
        try:
            with open(fichero) as f:
                datos=f.read()
            datos=json.loads(datos)
        except:
            print("No se ha podido leer el fichero json")
        else:
            try:
                user=datos[user]
            except:
                raise IceGauntlet.Unauthorized()
            else:   
                try:                 
                    password_hash=user["password_hash"] 
                except:
                    return None
        
        return password_hash
  
    def argumentos():
        parser = argparse.ArgumentParser(description='default option, user, change password,new token)
        parser.add_argument("-d","--default",default=True, help='default option')
        parser.add_argument("-u","--user",required=True,help='user',type=str)
        parser.add_argument("-c","--ChangePassword",required=False,help='change password',type=str)
        parser.add_argument("-t","--token",required=False,help='new token',type=str)
        
        args=parser.parse_args()
        return args





ClientAuth().main(sys.argv)

        