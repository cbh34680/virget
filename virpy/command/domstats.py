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
    parser.add_argument('--state', action='store_true')
    parser.add_argument('--cpu-total', action='store_true')
    parser.add_argument('--balloon', action='store_true')
    parser.add_argument('--vcpu', action='store_true')
    parser.add_argument('--interface', action='store_true')
    parser.add_argument('--block', action='store_true')
    parser.add_argument('--perf', action='store_true')
    parser.add_argument('--iothread', action='store_true')
    parser.add_argument('--memory', action='store_true')
    parser.add_argument('--dirtyrate', action='store_true')
    parser.add_argument('--vm', action='store_true')

    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument('--list-active', action='store_true')
    group1.add_argument('--list-inactive', action='store_true')

    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument('--list-persistent', action='store_true')
    group2.add_argument('--list-transient', action='store_true')

    group3 = parser.add_mutually_exclusive_group()
    group3.add_argument('--list-running', action='store_true')
    group3.add_argument('--list-paused', action='store_true')
    group3.add_argument('--list-shutoff', action='store_true')
    group3.add_argument('--list-other', action='store_true')

    #parser.add_argument('--raw', action='store_true')
    parser.add_argument('--enforce', action='store_true')
    parser.add_argument('--backing', action='store_true')
    parser.add_argument('--nowait', action='store_true')

    parser.add_argument('domain', nargs='?')

    return DomstatsCommand()


class DomstatsCommand(virpy.classes.Command):
    def run(self, conn, args):

        stats_db = {
            'state': libvirt.VIR_DOMAIN_STATS_STATE,
            'cpu_total': libvirt.VIR_DOMAIN_STATS_CPU_TOTAL,
            'balloon': libvirt.VIR_DOMAIN_STATS_BALLOON,
            'vcpu': libvirt.VIR_DOMAIN_STATS_VCPU,
            'interface': libvirt.VIR_DOMAIN_STATS_INTERFACE,
            'block': libvirt.VIR_DOMAIN_STATS_BLOCK,
            'perf': libvirt.VIR_DOMAIN_STATS_PERF,
            'iothread': libvirt.VIR_DOMAIN_STATS_IOTHREAD,
            'memory': libvirt.VIR_DOMAIN_STATS_MEMORY,
            'dirtyrate': libvirt.VIR_DOMAIN_STATS_DIRTYRATE,
            'vm': libvirt.VIR_DOMAIN_STATS_VM,
        }

        flags_db = {
            'list_active': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_ACTIVE,
            'list_inactive': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_INACTIVE,
            'list_persistent': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_PERSISTENT,
            'list_transient': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_TRANSIENT,
            'list_running': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_RUNNING,
            'list_paused': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_PAUSED,
            'list_shutoff': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_SHUTOFF,
            'list_other': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_OTHER,
            'nowait': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_NOWAIT,
            'backing': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_BACKING,
            'enforce': libvirt.VIR_CONNECT_GET_ALL_DOMAINS_STATS_ENFORCE_STATS,
        }

        stats = virpy.utils.setBitsByArgs(args, stats_db)
        flags = virpy.utils.setBitsByArgs(args, flags_db)

        data = None

        for dom, stats in conn.getAllDomainStats(stats, flags):
            rec = {'name': dom.name(), } | formatStats(stats)

            if args.domain is not None:
                if virpy.utils.isIndicateDomain(args.domain, dom):
                    data = rec
                    break

                continue

            if data is None:
                data = []

            data.append(rec)

        else:
            if args.domain is not None:
                raise virpy.classes.ObjectNotFoundError(f"failed to get domain '{args.domain}'")

        return data


def formatStats(stats):
    ret = {}

    for k, v in stats.items():
        key0 = k.split('.')[0]
        sub = ret.setdefault(key0, {})

        match key0:
            case 'block' | 'net':
                pass

            case _:
                sub[k[len(key0) + 1:]] = v

    for k in ('block', 'net', ):
        if f'{k}.count' in stats:
            ret[k] = tuple(virpy.utils.eachOrderedStats(stats, k))

    return ret

# EOF
