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
    parser.add_argument('--interface')
    parser.add_argument('--full', action='store_true')

    choices = virpy.utils.strsInterfaceAddressesSource()
    parser.add_argument('--source', default='lease', choices=choices)

    return DomifaddrCommand()


class DomifaddrCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        addrs = obj.interfaceAddresses(
            virpy.utils.idInterfaceAddressesSource(args.source))

        def mod(kv):
            for addr in kv['addrs']:
                addr['type'] = virpy.utils.strIPAddrType(addr['type'])

            return kv

        if args.interface is not None:
            if args.interface not in addrs:
                raise virpy.classes.ObjectNotFoundError(f"failed to get interface '{args.interface}'")

            data = {'name': args.interface, } | mod(addrs[args.interface])

        else:
            data = tuple(map(lambda x: {'name': x[0], **mod(x[1]), }, addrs.items()))

        return data

# EOF
