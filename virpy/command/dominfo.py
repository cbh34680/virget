import sys
import argparse
import importlib
import libvirt
import pprint
import virpy
import virpy.utils

'''
https://libvirt.org/html/
https://libvirt.org/html/libvirt-libvirt-domain.html

python -c 'import libvirt; help(libvirt)'
'''

def create_handler(parser):
    parser.add_argument('domain')

    return DominfoCommand()


class DominfoCommand(virpy.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        state = obj.state()[0]
        running = state == libvirt.VIR_DOMAIN_RUNNING

        stats_types = (libvirt.VIR_DOMAIN_STATS_CPU_TOTAL |
                       libvirt.VIR_DOMAIN_STATS_VCPU |
                       libvirt.VIR_DOMAIN_STATS_BALLOON)

        stats = conn.domainListGetStats([obj], stats_types)
        stats = stats[0][1]
        #pprint.pprint(stats)

        secModel, secDOI = conn.getSecurityModel()

        data = {
            'id': None if obj.ID() < 0 else obj.ID(),
            'name': obj.name(),
            'uuid': obj.UUIDString(),
            'osType': obj.OSType(),
            'state': virpy.utils.strDomainState(state),
            'cpu': {
                'count': stats['vcpu.maximum'],
                'time': stats['cpu.time'] if running else None,
            },
            'memory': {
                'maximum': stats['balloon.maximum'],
                'current': stats['balloon.current'],
            },
            'persistent': bool(obj.isPersistent()),
            'autostart': bool(obj.autostart()),
            'managedSave': bool(obj.hasManagedSaveImage()),
            'security': {
                'model': secModel,
                'DOI': secDOI,
                'label': obj.securityLabel()[0] if running else None,
                'enforcing': obj.securityLabel()[1] if running else None,
            },
        }

        return data

# EOF
