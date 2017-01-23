###########################################################
#
# Copyright (c) 2005, Southpaw Technology
#                     All Rights Reserved
#
# PROPRIETARY INFORMATION.  This software is proprietary to
# Southpaw Technology, and is not to be reproduced, transmitted,
# or disclosed in any way without written permission.
#
#
#

import sys, os, getpass

try:
    import tacticenv
except ImportError:
    pass

from tactic_client_lib import TacticServerStub


def main(args):

    server = TacticServerStub(setup=False)
    server.get_info_from_user(force=True)
    return


def cli():
    executable = sys.argv[0]
    args = sys.argv[1:]
    main(args)
