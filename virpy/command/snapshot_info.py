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

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--snapshotname')
    group.add_argument('--current', action='store_true')

    return SnapshotInfoCommand()


class SnapshotInfoCommand(virpy.classes.Command):
    def run(self, conn, args):

        dom = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(dom))

        obj = virpy.utils.lookupSnapshot(dom, args.snapshotname)

        try:
            parent = obj.getParent().getName()
        except libvirt.libvirtError:
            parent = None

        xmlRoot = ET.fromstring(obj.getXMLDesc())

        memory = xmlRoot.find('memory')

        data = {
            'name': obj.getName(),
            'domain': dom.name(),
            'current': bool(obj.isCurrent()),
            'state': xmlRoot.findtext('state'),
            'location': memory.attrib['snapshot'],
            'parent': parent,
            'children': obj.numChildren(),
            'descendants': -1,
            'metadata': bool(obj.hasMetadata()),
        }

        return data

# EOF
