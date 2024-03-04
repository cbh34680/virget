import sys
import argparse
import importlib
import libvirt
import virpy
import virpy.classes
import virpy.utils
import xmltodict

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-domain.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):

    parser.add_argument('domain')
    parser.add_argument('--security-info', action='store_true')
    parser.add_argument('--inactive', action='store_true')
    parser.add_argument('--update-cpu', action='store_true')
    parser.add_argument('--migratable', action='store_true')

    return DumpjsonCommand()


class DumpjsonCommand(virpy.classes.Command):
    def run(self, conn, args):
        obj = virpy.utils.lookupDomain(conn, args.domain)

        flags_db = {
            'security_info': libvirt.VIR_DOMAIN_XML_SECURE,
            'inactive':      libvirt.VIR_DOMAIN_XML_INACTIVE,
            'update_cpu':    libvirt.VIR_DOMAIN_XML_UPDATE_CPU,
            'migratable':    libvirt.VIR_DOMAIN_XML_MIGRATABLE,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        # https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainGetXMLDesc
        xml = obj.XMLDesc(flags)

        data = xmltodict.parse(xml, attr_prefix='', cdata_key=virpy.DUMP_XML_CDATA_KEY)

        return data

# EOF
