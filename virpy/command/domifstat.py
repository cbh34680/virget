import sys
import argparse
import importlib
import libvirt
import pprint

import virpy
import virpy.classes
import virpy.utils

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-domain.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('domain')
    parser.add_argument('interface')

    return DomifstatCommand()


class DomifstatCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        stats = obj.interfaceStats(args.interface)

        names = (
            'rx_bytes',
            'rx_packets',
            'rx_errs',
            'rx_drop',
            'tx_bytes',
            'tx_packets',
            'tx_errs',
            'tx_drop',
        )

        return dict(zip(names, stats))

# EOF
