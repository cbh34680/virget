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

    return NetInfoCommand()


class NetInfoCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupNetwork(conn, args.network)
        #pprint.pprint(dir(obj))

        data = {
            'name': obj.name(),
            'uuid': obj.UUIDString(),
            'active': bool(obj.isActive()),
            'persistent': bool(obj.isPersistent()),
            'autostart': bool(obj.autostart()),
            'bridge': obj.bridgeName(),
        }

        return data

