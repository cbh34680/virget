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
    parser.add_argument('--source', default='lease', choices=('lease', 'agent', 'arp', ))

    return DomifaddrCommand()


class DomifaddrCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        src_db = {
            'lease': libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE,
            'agent': libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT,
            'arp':   libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_ARP,
        }

        # https://libvirt.org/html/libvirt-libvirt-network.html#virIPAddrType
        atype_db = {
            libvirt.VIR_IP_ADDR_TYPE_IPV4: 'ipv4',
            libvirt.VIR_IP_ADDR_TYPE_IPV6: 'ipv6',
        }

        addrs = obj.interfaceAddresses(src_db[args.source])

        def mod(kv):
            for addr in kv['addrs']:
                addr['type'] = atype_db[addr['type']]

            return kv

        if args.interface is not None:
            data = {'name': args.interface} | mod(addrs[args.interface])

        else:
            data = tuple(map(lambda x: {'name': x[0], **mod(x[1]), }, addrs.items()))

        return data

# EOF
