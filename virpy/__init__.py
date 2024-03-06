import os
import sys
import argparse
import contextlib
import importlib
import jmespath
import json
import libvirt
import pathlib
import pprint
import re
import virpy.classes
import virpy.utils

__version__ = '1.0.0'

DUMP_XML_ATTR_PREFIX = '@'
DUMP_XML_CDATA_KEY = '#CDATA'


# https://stackoverflow.com/questions/45541725/avoiding-console-prints-by-libvirt-qemu-python-apis
# https://github.com/libvirt/libvirt-python/blob/master/examples/consolecallback.py

def libvirt_callback(_, error):

    # The console stream errors on VM shutdown; we don't care
    if error[0] == libvirt.VIR_ERR_RPC and error[1] == libvirt.VIR_FROM_STREAMS:
        return

    #logging.warn(error)
    #print(f'!!! {error}')


def main():
    try:
        parser = argparse.ArgumentParser(prog=__name__.split('.')[0])
        parser.add_argument('-c', '--connect', dest='url')
        parser.add_argument('-r', '--readonly', action='store_true')
        parser.add_argument('--query')
        parser.add_argument('--pretty', action='store_true')
        parser.add_argument('--version', action='store_true')

        return run_command(parser)

    except (virpy.classes.ObjectNotFoundError, libvirt.libvirtError) as ex:
        print(f'error: {ex}', file=sys.stderr)

        return 1

    except Exception as ex:
        raise ex


def run_command(parser):
    # add_subparsers()
    # https://qiita.com/oohira/items/308bbd33a77200a35a3d

    sub_parsers = parser.add_subparsers()
    sub_parsers.add_parser('help', help=f'output this help')

    thisdir = pathlib.Path(__file__).parent
    cmdpaths = thisdir.glob('command/*.py')

    cmdpat = re.compile(r'\A[a-zA-Z]\w*\Z')
    cmds = set(x.stem for x in cmdpaths if cmdpat.match(str(x.stem)))
    #print(cmds)

    for cmd in cmds:
        modname = f'{__name__}.command.{cmd}'

        with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
            mod = importlib.import_module(modname)

        if hasattr(mod, 'create_handler'):
            argname = cmd.replace('_', '-')

            cmd_parser = sub_parsers.add_parser(argname, help=f'see: {argname} -h')

            handler = mod.create_handler(cmd_parser)
            cmd_parser.set_defaults(handler=handler)

        else:
            print(f"warning: {mod.__file__} does not provide function 'create_handler'", file=sys.stderr)

            del sys.modules[modname]
            del mod

    args = parser.parse_args()

    if args.version:
        print(virpy.__version__)
        return 0

    libvirt.registerErrorHandler(f=libvirt_callback, ctx=None)

    handler = getattr(args, 'handler', None)

    if handler is None:
        parser.print_help(file=sys.stderr)

    else:
        conn = libvirt.openReadOnly(args.url) if args.readonly else libvirt.open(args.url)
        rslt = handler(conn, args)

        if rslt is None:
            return 0

        if virpy.utils.isScalar(rslt):
            print(rslt)
            return 0

        resp = {'data': rslt, }

        if args.query:
            # execute JMESPath query 
            resp = jmespath.search(args.query, resp)

        if virpy.utils.isScalar(resp):
            print(resp)
            return 0

        dumpopts = {
            'ensure_ascii': False,
            'indent': 2,
            #'sort_keys': True,
            #'separators': (',', ': ', ),
        } if args.pretty else {}

        #pprint.pprint(resp, width=180)
        print(json.dumps(resp, **dumpopts))

    return 0

# EOF
