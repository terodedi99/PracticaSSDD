#!/usr/bin/env python3

# pylint: disable=C0114

import os
import sys

try:
    proxy = sys.argv[1]
except IndexError:
    print('Command arguments: {} <proxy>'.format(
        os.path.basename(sys.argv[0]))
    )
    sys.exit(1)

_COMMAND_ = './dungeon_distrib "%(proxy)s"'

final_command = _COMMAND_ % {

    'proxy': proxy
}

os.chdir('client-distrib-icegauntlet')
os.system(final_command)
