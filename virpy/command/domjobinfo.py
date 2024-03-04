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
    parser.add_argument('--completed', action='store_true')
    parser.add_argument('--keep-completed', action='store_true')

    return DomjobinfoCommand()


class DomjobinfoCommand(virpy.classes.Command):
    def run(self, conn, args):

        obj = virpy.utils.lookupDomain(conn, args.domain)
        #pprint.pprint(dir(obj))

        '''
        names = (
            'type',
            'timeElapsed',
            'timeRemaining',
            'dataTotal',
            'dataProcessed',
            'dataRemaining',
            'memTotal',
            'memProcessed',
            'memRemaining',
            'fileTotal',
            'fileProcessed',
            'fileRemaining',
        )

        info = obj.jobInfo()

        data = dict(zip(names, info))
        data['type'] = virpy.utils.strDomainJobType(data['type'])
        '''

        flags_db = {
            'completed':      libvirt.VIR_DOMAIN_JOB_STATS_COMPLETED,
            'keep_completed': libvirt.VIR_DOMAIN_JOB_STATS_KEEP_COMPLETED,
        }

        flags = virpy.utils.setBitsByArgs(args, flags_db)

        data = obj.jobStats(flags)
        #pprint.pprint(data)
        data['type'] = virpy.utils.strDomainJobType(data['type'])

        return data

# EOF
