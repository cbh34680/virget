import collections.abc
import functools
import libvirt

# https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainState

_db_strDomainState = 'nostate', 'running', 'blocked', 'paused', 'shutdown', 'shutoff', 'crashed', 'pmsuspended', 'last',

def strDomainState(x):
    return _db_strDomainState[x]


def isIndicateDomain(key, dom):
    try:
        id = int(key)
        return id == dom.ID()

    except ValueError:
        if key == dom.UUID():
            return True

        return key == dom.name()


def lookupDomain(conn, key):
    try:
        return conn.lookupByID(int(key))

    except ValueError:
        try:
            return conn.lookupByName(key)

        except libvirt.libvirtError:
            return conn.lookupByUUIDString(key)


def lookupNetwork(conn, key):
    try:
        return conn.networkLookupByName(key)

    except libvirt.libvirtError:
        return conn.networkLookupByUUIDString(key)


def isScalar(v):
    if v is None:
        return True

    if isinstance(v, str):
        return True

    if isinstance(v, collections.abc.Iterable):
        return False

    return True


def eachDomainStatsBlocks(conn, dom):

    stats_types = libvirt.VIR_DOMAIN_STATS_BLOCK
    stats = conn.domainListGetStats([dom], stats_types)[0][1]
    #pprint.pprint(stats)

    yield from eachOrderedStats(stats, 'block')


def eachOrderedStats(stats, key, count_key='count'):

    for i in range(stats[f'{key}.{count_key}']):
        pfx = f'{key}.{i}.'
        yield dict((k[len(pfx):], v) for k, v in stats.items() if k.startswith(pfx))


def setBitsByArgs(args, db, initval=0):
    return functools.reduce(lambda a, b: a | b, (v for k, v in db.items() if getattr(args, k)), initval)

# EOF
