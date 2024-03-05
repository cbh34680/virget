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

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):

    return VersionCommand()


class VersionCommand(virpy.classes.Command):
    def run(self, conn, args):

        modroot = __name__.split('.')[0]
        return f'Using library: {modroot} {virpy.__version__}'

