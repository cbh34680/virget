import sys
import argparse
import importlib
import libvirt
import pprint
import virpy
import virpy.utils
import xmltodict

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-network.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('network')
    parser.add_argument('--inactive', action='store_true')
    #parser.add_argument('--xpath')
    #parser.add_argument('--wrap', action='store_true')

    return NetDumpjsonCommand()


class NetDumpjsonCommand(virpy.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupNetwork(conn, args.network)
        #pprint.pprint(dir(obj))

        flags_db = {
            'inactive': libvirt.VIR_NETWORK_XML_INACTIVE,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        # https://libvirt.org/html/libvirt-libvirt-network.html#virNetworkGetXMLDesc
        xml = obj.XMLDesc(flags)

        data = xmltodict.parse(xml, attr_prefix='', cdata_key='Value')

        return data

