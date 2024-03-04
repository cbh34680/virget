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
    parser.add_argument('--output-dir', '-o', required=True)

    return BackupNewxmlCommand()


class BackupNewxmlCommand(virpy.classes.Command):
    def run(self, conn, args):
        output_dir = pathlib.Path(args.output_dir)

        if not output_dir.is_dir():
            raise virpy.classes.ObjectNotFoundError(f"error: directory not exist '{args.output_dir}'")

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

            file_path = str((output_dir / pathlib.Path(obj['path']).name).resolve())

            ET.SubElement(xmlDisk, 'driver', type='qcow2')
            ET.SubElement(xmlDisk, 'target', file=file_path)

        data = ET.tostring(xmlRoot, encoding='utf-8').decode('utf-8')

        return data

# EOF
