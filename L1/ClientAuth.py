#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys 
import Ice 
Ice.loadSlice('icegauntlet.ice')
import IceGauntlet

class ClientAuth(Ice._Application):
    def run(self,argv):
        proxy=self.communicator().stringToProxy(argv[1])