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
https://libvirt.org/html/libvirt-libvirt-interface.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('domain')
    #parser.add_argument('--inactive')

    return DomiflistCommand()


class DomiflistCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        xmlRoot = ET.fromstring(obj.XMLDesc())

        def attrval(xmlObj, tag, key):
            tagObj = xmlObj.find(tag)
            if tagObj is None:
                return None

            return tagObj.attrib.get(key)

        data = []

        for iface in xmlRoot.findall('devices/interface'):
            rec = {
                'interface': attrval(iface, 'target', 'dev'),
                'type': iface.attrib['type'],
                'source': attrval(iface, 'source', 'network'),
                'model': attrval(iface, 'model', 'type'),
                'mac': attrval(iface, 'mac', 'address'),
            }

            if rec['source'] is None:
                rec['source_bridge'] = attrval(iface, 'source', 'bridge')

            rec['vlan_trunk'] = attrval(iface, 'vlan', 'trunk')
            if rec['vlan_trunk'] is None:
                rec['vlan_trunk'] = 'no'
            else:
                rec['vlans'] = []
                for vlan in iface.iter('vlan'):
                    for tag in vlan.iter('tag'):
                        vlan_rec = {}
                        vlan_rec['id'] = tag.attrib['id']
                        if tag.attrib.get('nativeMode') is not None:
                            vlan_rec['nativeMode'] = tag.attrib.get('nativeMode')
                        rec['vlans'].append(vlan_rec)
            for virtualport in iface.iter('virtualport'):
                rec['virtualport'] = attrval(virtualport, 'parameters', 'interfaceid')

            data.append(rec)

        return data


# EOF
