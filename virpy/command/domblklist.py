import sys
import argparse
import importlib
import libvirt
import pprint
import xml.etree.ElementTree as ET

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
    #parser.add_argument('--inactive', action='store_true')
    parser.add_argument('--details', action='store_true')

    return DomblklistCommand()


class DomblklistCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        details = None

        if args.details:
            details = {}

            xmlRoot = ET.fromstring(obj.XMLDesc())

            for disk in xmlRoot.findall('devices/disk'):
                #print(disk.attrib['type'])
                #print(disk.attrib['device'])

                for src in disk.findall('target'):
                    details[src.attrib['dev']] = {
                        'type': disk.attrib['type'],
                        'device': disk.attrib['device']
                    }

        data = []

        for block in virpy.utils.eachDomainStatsBlocks(conn, obj):
            target = block['name']

            rec = {
                'target': target,
                'source': block['path'],
            }

            if details is not None:
                rec |= details[target]

            data.append(rec)

        return data

# EOF
