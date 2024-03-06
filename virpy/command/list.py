import sys
import argparse
import importlib
import libvirt
import virpy
import virpy.classes
import virpy.utils

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-domain.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--inactive', action='store_true')
    group1.add_argument('--all', action='store_true')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--transient', action='store_true')
    group2.add_argument('--persistent', action='store_true')

    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument('--state-running', action='store_true')
    group3.add_argument('--state-paused', action='store_true')
    group3.add_argument('--state-shutoff', action='store_true')
    group3.add_argument('--state-other', action='store_true')

    group4 = parser.add_mutually_exclusive_group()
    group4.add_argument('--autostart', action='store_true')
    group4.add_argument('--no-autostart', action='store_true')

    group5 = parser.add_mutually_exclusive_group()
    group5.add_argument('--with-snapshot', action='store_true')
    group5.add_argument('--without-snapshot', action='store_true')

    group6 = parser.add_mutually_exclusive_group()
    group6.add_argument('--with-checkpoint', action='store_true')
    group6.add_argument('--without-checkpoint', action='store_true')

    #parser.add_argument('--uuid', action='store_true')
    #parser.add_argument('--name', action='store_true')
    #parser.add_argument('--id', action='store_true')
    #parser.add_argument('--table', action='store_true')

    group7 = parser.add_mutually_exclusive_group()
    group7.add_argument('--with-managed-save', action='store_true')
    group7.add_argument('--without-managed-save', action='store_true')

    parser.add_argument('--title', action='store_true')

    return ListCommand()


class ListCommand(virpy.classes.Command):
    def run(self, conn, args):

        data = []

        # https://libvirt.org/html/libvirt-libvirt-domain.html#virConnectListAllDomains

        flags_db = {
            # 1
            'all':           libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE |
                             libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE,
            'inactive':      libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE,

            # 2
            'transient':     libvirt.VIR_CONNECT_LIST_DOMAINS_TRANSIENT,
            'persistent':    libvirt.VIR_CONNECT_LIST_DOMAINS_PERSISTENT,

            # 3
            'state_running': libvirt.VIR_CONNECT_LIST_DOMAINS_RUNNING,
            'state_paused':  libvirt.VIR_CONNECT_LIST_DOMAINS_PAUSED,
            'state_shutoff': libvirt.VIR_CONNECT_LIST_DOMAINS_SHUTOFF,
            'state_other':   libvirt.VIR_CONNECT_LIST_DOMAINS_OTHER,

            # 4
            'autostart':     libvirt.VIR_CONNECT_LIST_DOMAINS_AUTOSTART,
            'no_autostart':  libvirt.VIR_CONNECT_LIST_DOMAINS_NO_AUTOSTART,

            # 5
            'with_snapshot':        libvirt.VIR_CONNECT_LIST_DOMAINS_HAS_SNAPSHOT,
            'without_snapshot':     libvirt.VIR_CONNECT_LIST_DOMAINS_NO_SNAPSHOT,

            # 6
            'with_checkpoint':      libvirt.VIR_CONNECT_LIST_DOMAINS_HAS_CHECKPOINT,
            'without_checkpoint':   libvirt.VIR_CONNECT_LIST_DOMAINS_NO_CHECKPOINT,

            # 7
            'with_managed_save':    libvirt.VIR_CONNECT_LIST_DOMAINS_MANAGEDSAVE,
            'without_managed_save': libvirt.VIR_CONNECT_LIST_DOMAINS_NO_MANAGEDSAVE,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        # default) active
        if not (flags & libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE):
            flags |= libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE

        for obj in conn.listAllDomains(flags):
            state = obj.state()[0]

            rec = {
                'id': None if obj.ID() < 0 else obj.ID(),
                'name': obj.name(),
                'state': virpy.utils.strDomainState(state),
            }

            if args.title:
                try:
                    title = obj.metadata(libvirt.VIR_DOMAIN_METADATA_TITLE, None)

                except libvirt.libvirtError:
                    title = None

                rec['title'] = title

            data.append(rec)

        return data

