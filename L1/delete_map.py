#!/usr/bin/env python3


import os
import sys

try:
    import pexpect
except ImportError:
    print('Required library "pexpect" not exists. Install with pip and try again')
    sys.exit(1)


try:
    proxy = sys.argv[1]
    token= sys.argv[2]
    roomName= sys.argv[3]
except ValueError:
    print('Command arguments: {} <user> <password> <proxy>'.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)

_COMMAND_ = './ClientServer.py "%(proxy)s" %(token)s r "%(nombre_mapa)s" '

final_command = _COMMAND_ % {
    'nombre_mapa': roomName,
    'proxy': proxy,
    'token': token
}

os.system(final_command)
