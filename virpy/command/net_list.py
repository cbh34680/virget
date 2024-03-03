import sys
import argparse
import importlib
import libvirt
import virpy
import virpy.utils

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-network.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--inactive', action='store_true')
    group1.add_argument('--all', action='store_true')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--persistent', action='store_true')
    group2.add_argument('--transient', action='store_true')

    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument('--autostart', action='store_true')
    group3.add_argument('--no-autostart', action='store_true')

    return NetListCommand()


class NetListCommand(virpy.Command):
    def run(self, conn, args):

        data = []

        # https://libvirt.org/html/libvirt-libvirt-network.html#virConnectListAllNetworks

        flags_db = {
            # 1
            'all':      libvirt.VIR_CONNECT_LIST_NETWORKS_ACTIVE |
                        libvirt.VIR_CONNECT_LIST_NETWORKS_INACTIVE,
            'inactive': libvirt.VIR_CONNECT_LIST_NETWORKS_INACTIVE,

            # 2
            'persistent':   libvirt.VIR_CONNECT_LIST_NETWORKS_PERSISTENT,
            'transient':    libvirt.VIR_CONNECT_LIST_NETWORKS_TRANSIENT,

            # 3
            'autostart':    libvirt.VIR_CONNECT_LIST_NETWORKS_AUTOSTART,
            'no_autostart': libvirt.VIR_CONNECT_LIST_NETWORKS_NO_AUTOSTART,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        # default) active
        if not (flags & libvirt.VIR_CONNECT_LIST_NETWORKS_INACTIVE):
            flags |= libvirt.VIR_CONNECT_LIST_NETWORKS_ACTIVE

        for obj in conn.listAllNetworks(flags):
            rec = {
                'name': obj.name(),
                'state': 'active' if obj.isActive() else 'inactive',
                'autostart': bool(obj.autostart()),
                'persistent': bool(obj.isPersistent()),
            }

            data.append(rec)

        return data

