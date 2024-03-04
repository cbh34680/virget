import sys
import argparse
import datetime
import importlib
import libvirt
import pprint
import xml.etree.ElementTree as ET
import xmltodict

import virpy
import virpy.classes
import virpy.utils

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-domain-snapshot.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('domain')

    return SnapshotCurrentCommand()


class SnapshotCurrentCommand(virpy.classes.Command):
    def run(self, conn, args):

        dom = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(dom))

        obj = virpy.utils.lookupSnapshot(dom)

        xml = obj.getXMLDesc()
        data = xmltodict.parse(xml, attr_prefix='', cdata_key=virpy.DUMP_XML_CDATA_KEY)

        return data

# EOF