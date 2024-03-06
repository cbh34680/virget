import sys
import argparse
import getpass
import importlib
import libvirt
import pprint
import virpy
import virpy.classes


'''
https://libvirt.org/html/

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):

    return VersionCommand()


class VersionCommand(virpy.classes.Command):
    def run(self, conn, args):

        modroot = __name__.split('.')[0]

        lvvi = libvirt.getVersion()
        lvma = int(lvvi / 1000000)
        lvmi = int((lvvi - lvma * 1000000) / 1000)
        lvre = (lvvi - lvma * 1000000 - lvmi * 1000)
        lvver = f'{lvma}.{lvmi}.{lvre}'

        out = [
            f'Using library: libvirt {lvver}',
            f'Using library: {modroot} {virpy.__version__}',
            f'Current user: {getpass.getuser()}',
        ]

        print('\n'.join(out))

