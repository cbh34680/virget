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

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--device')
    group.add_argument('--all', action='store_true')

    return DomblkinfoCommand()


class DomblkinfoCommand(virpy.classes.Command):
    def run(self, conn, args):

        dom = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(dom))

        blocks = virpy.utils.eachDomainStatsBlocks(conn, dom)

        data = None

        for obj in blocks:
            #pprint.pprint(obj)

            if args.device is not None:
                if args.device == obj['name']:
                    data = obj
                    break

                continue

            if data is None:
                data = []

            data.append(obj)

        return data

# EOF
