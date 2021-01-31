#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0103
# pylint: disable=W0702

import sys
import json
import os.path
import hashlib
import getpass

import Ice
Ice.loadSlice('icegauntlet.ice')
# pylint: disable=E0401
# pylint: disable=C0413
import IceGauntlet

class ClientAuth(Ice.Application):
    def leer_json(self, fichero, user):
        '''
        method to read a json file
        '''

        try:
            with open(fichero) as f:
                usuario = f.read()
            usuario = json.loads(usuario)
        except:
            print("Error, Not found data base")
        try:
            password = usuario[user]['password_hash']
            return password
        except:
            return None

    def run(self, argv):
        proxy = self.communicator().stringToProxy(argv[1])
        server = IceGauntlet.AuthenticationPrx.checkedCast(proxy)


        if not server:
            raise RuntimeError('Invalid Proxy')


        if  len(sys.argv) < 3:
            raise RuntimeError('Error. Parametros insuficientes')

        user = argv[2]
        password_hash = self.leer_json('users.json', user)
        print('Enter password: ')
        p = getpass.getpass()
        if password_hash is None:
            print('Creando nueva contraseña...')
            passHash = hashlib.sha256(p.encode()).hexdigest()
            print(password_hash)
            server.changePassword(user, None, passHash)
        if len(sys.argv) == 4:
            option = argv[3]
        else:
            option = 'd'

        if option == 'c':
            p = getpass.getpass()
            passHash = hashlib.sha256(p.encode()).hexdigest()
            try:
                print("--- Introducir nueva contraseña ---")
                np = getpass.getpass()
            except Exception as err:
                print('ERROR:', err)
            #passHash = hashlib.sha256(p.encode()).hexdigest()
            newpassHash = hashlib.sha256(np.encode()).hexdigest()
            server.changePassword(user, passHash, newpassHash)
        elif option == 't':
            passHash = hashlib.sha256(p.encode()).hexdigest()
            print(server.getNewToken(user, passHash))
        elif option == 'd':
            print(server.getOwner("izZA404ytFwp9h7dIcYazah0BaTchSYZIuvwu7lT"))
            
ClientAuth().main(sys.argv)
