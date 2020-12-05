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
except ValueError:
    print('Command arguments: {} <user> <password> <proxy>'.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)

_COMMAND_ = './Server.py "%(proxy)s" --Ice.Config=server.config'

final_command = _COMMAND_ % {
    'proxy': proxy
}

os.system(final_command)