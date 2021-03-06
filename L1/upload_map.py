#!/usr/bin/env python3

# pylint: disable=C0114

import os
import sys

# pylint: disable=W0632
try:
    proxy, token, mapa = sys.argv[1:]
except ValueError:
    print('Command arguments: {} <proxy> <token> <fichero>'.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)

_COMMAND_ = './ClientServer.py "%(proxy)s" %(token)s p %(fichero)s'

final_command = _COMMAND_ % {
    'fichero': mapa,
    'proxy': proxy,
    'token': token
}

os.system(final_command)
