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

    parser.add_argument('--parent', action='store_true')

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--roots', action='store_true')
    group1.add_argument('--from', dest='from_name')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--leaves', action='store_true')
    group2.add_argument('--no-leaves', action='store_true')

    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument('--metadata', action='store_true')
    group3.add_argument('--no-metadata', action='store_true')

    group4 = parser.add_mutually_exclusive_group()
    group4.add_argument('--inactive', action='store_true')
    group4.add_argument('--active', action='store_true')
    group4.add_argument('--disk-only', action='store_true')

    group5 = parser.add_mutually_exclusive_group()
    group5.add_argument('--internal', action='store_true')
    group5.add_argument('--external', action='store_true')

    # tree
    # current

    #parser.add_argument('--descendants', action='store_true')
    parser.add_argument('--name', action='store_true')
    parser.add_argument('--topological', action='store_true')

    return SnapshotListCommand()


class SnapshotListCommand(virpy.classes.Command):
    def run(self, conn, args):

        dom = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(dom))

        flags_db = {
            'roots':        libvirt.VIR_DOMAIN_SNAPSHOT_LIST_ROOTS,
            'leaves':       libvirt.VIR_DOMAIN_SNAPSHOT_LIST_LEAVES,
            'no_leaves':    libvirt.VIR_DOMAIN_SNAPSHOT_LIST_NO_LEAVES,
            'metadata':     libvirt.VIR_DOMAIN_SNAPSHOT_LIST_METADATA,
            'no_metadata':  libvirt.VIR_DOMAIN_SNAPSHOT_LIST_NO_METADATA,
            'inactive':     libvirt.VIR_DOMAIN_SNAPSHOT_LIST_INACTIVE,
            'active':       libvirt.VIR_DOMAIN_SNAPSHOT_LIST_ACTIVE,
            'disk_only':    libvirt.VIR_DOMAIN_SNAPSHOT_LIST_DISK_ONLY,
            'internal':     libvirt.VIR_DOMAIN_SNAPSHOT_LIST_INTERNAL,
            'external':     libvirt.VIR_DOMAIN_SNAPSHOT_LIST_EXTERNAL,
            #'descendants':  libvirt.VIR_DOMAIN_SNAPSHOT_LIST_DESCENDANTS,
            'topological':  libvirt.VIR_DOMAIN_SNAPSHOT_LIST_TOPOLOGICAL,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        data = None

        for obj in dom.listAllSnapshots(flags):
            #pprint.pprint(dir(obj))

            name = obj.getName()
            xmlRoot = ET.fromstring(obj.getXMLDesc())

            #try:
            #    parent = obj.getParent().getName()
            #except libvirt.libvirtError:
            #    parent = None
    
            parent = xmlRoot.findtext('parent/name')
            #print(parent)


            if args.name:
                rec = name

            else:
                # creationTime -> datetime -> string
                ts = int(xmlRoot.findtext('creationTime'))
                dt = datetime.datetime.fromtimestamp(ts)
                ct = dt.strftime('%Y-%m-%d %H:%M:%S')
    
                rec = {
                    'name': name,
                    'creationTime': ct,
                    'state': xmlRoot.findtext('state'),
                }

                rec |= {'parent': parent, } if args.parent else {}

                # bool(obj.isCurrent())

            if args.roots:
                if parent is None:
                    data = rec
                    break

                continue

            if args.from_name is not None:
                if args.from_name == parent:
                    data = rec
                    break

                continue
                    
            if data is None:
                data = []

            data.append(rec)

        return data

# EOF
