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

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        blocks = virpy.utils.eachDomainStatsBlocks(conn, obj)

        data = None

        for block in blocks:
            #pprint.pprint(block)

            target = block['name']

            rec = {
                'target': target,
                'capacity': block['capacity'],
                'allocation': block['allocation'],
                'physical': block['physical'],
            }

            if args.device is not None:
                if args.device == target:
                    data = rec
                    break

                continue

            if data is None:
                data = []

            data.append(rec)

        return data

# EOF
