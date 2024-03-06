import sys
import argparse
import datetime
import importlib
import libvirt
import pprint
import xml.etree.ElementTree as ET

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
    parser.add_argument('snapshotname')
    parser.add_argument('--security-info', action='store_true')
    #parser.add_argument('--xpath')
    #parser.add_argument('--wrap', action='store_true')

    return SnapshotDumpjsonCommand()


class SnapshotDumpjsonCommand(virpy.classes.Command):
    def run(self, conn, args):

        dom = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(dom))

        obj = virpy.utils.lookupSnapshot(dom, args.snapshotname)

        flags_db = {
            'security_info': libvirt.VIR_DOMAIN_SNAPSHOT_XML_SECURE,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        xml = obj.getXMLDesc(flags)

        data = virpy.utils.xmlToDict(xml, args)

        return data

# EOF
