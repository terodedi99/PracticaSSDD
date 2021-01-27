#!/usr/bin/env python3

# pylint: disable=C0114
import os
import sys

try:
    # pylint: disable=W0632
    proxy, token, roomName = sys.argv[1:]
except ValueError:
    print('Command arguments: {} <user> <token> <nombre>'.format(
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
