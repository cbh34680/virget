import sys
import argparse
import importlib
import libvirt
import pprint
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
    #parser.add_argument('--period', type=int)
    #parser.add_argument('--config', type=int)
    #parser.add_argument('--live', type=int)
    #parser.add_argument('--current', type=int)

    return DommemstatCommand()


class DommemstatCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        return obj.memoryStats()

# EOF
