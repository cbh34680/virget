import sys
import argparse
import importlib
import libvirt
import pathlib
import pprint
import virpy
import virpy.classes
import virpy.utils
import xml.etree.ElementTree as ET

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-domain.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('domain')
    parser.add_argument('outdir')

    return BackupNewxmlCommand()


class BackupNewxmlCommand(virpy.classes.Command):
    def run(self, conn, args):
        outdir = pathlib.Path(args.outdir)

        if not outdir.is_dir():
            raise virpy.classes.ObjectNotFoundError(f"directory not exist '{args.outdir}'")

        dom = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(dom))

        blocks = virpy.utils.eachDomainStatsBlocks(conn, dom)

        xmlRoot = ET.Element('domainbackup', mode='push')
        xmlDisks = ET.SubElement(xmlRoot, 'disks')

        for obj in (x for x in blocks if x.get('path')):
            #pprint.pprint(obj)

            params = {
                'name': obj['name'],
                'backup': 'yes',
                'type': 'file',
                'backupmode': 'full',
            }

            #pprint.pprint(params)
            xmlDisk = ET.SubElement(xmlDisks, 'disk', **params)

            file_path = str((outdir / pathlib.Path(obj['path']).name).resolve())

            ET.SubElement(xmlDisk, 'driver', type='qcow2')
            ET.SubElement(xmlDisk, 'target', file=file_path)

        data = ET.tostring(xmlRoot, encoding='utf-8').decode('utf-8')

        return data

# EOF
