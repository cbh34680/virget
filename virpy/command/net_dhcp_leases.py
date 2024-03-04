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
https://libvirt.org/html/libvirt-libvirt-network.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('network')
    parser.add_argument('--mac')

    return NetDhcpLeasesCommand()


class NetDhcpLeasesCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupNetwork(conn, args.network)
        #pprint.pprint(dir(obj))

        data = obj.DHCPLeases()
        #pprint.pprint(data)

        def mod(x):
            x['type'] = virpy.utils.strIPAddrType(x['type'])
            return x

        if args.mac is not None:
            data = tuple(filter(lambda x: x['mac'] == args.mac, data))
            if not data:
                raise virpy.classes.ObjectNotFoundError(f"failed to get mac '{args.mac}'")

            assert len(data) == 1
            data = mod(data[0])

        else:
            #data = tuple(
            #        map(lambda x: { **x,
            #            'type': virpy.utils.strIPAddrType(x['type']), }, data))

            data = tuple(map(lambda x: mod(x), data))

        return data

