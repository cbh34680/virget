import collections.abc
import functools
import libvirt
import virpy.classes

# https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainState

_db_strDomainState = 'nostate', 'running', 'blocked', 'paused', 'shutdown', 'shutoff', 'crashed', 'pmsuspended', 'last',

def strDomainState(x):
    return _db_strDomainState[x]


# https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainJobType

_db_strDomainJobType = 'none', 'bounded', 'unbounded', 'completed', 'failed', 'cancelled', 'last',

def strDomainJobType(x):
    return _db_strDomainJobType[x]


# https://libvirt.org/html/libvirt-libvirt-network.html#virIPAddrType

_db_strIPAddrType = {
    libvirt.VIR_IP_ADDR_TYPE_IPV4: 'ipv4',
    libvirt.VIR_IP_ADDR_TYPE_IPV6: 'ipv6',
    #libvirt.VIR_IP_ADDR_TYPE_LAST: 'last',
}

def strIPAddrType(x):
    return _db_strIPAddrType[x]


# https://libvirt.org/html/libvirt-libvirt-domain.html#virDomainInterfaceAddressesSource

_db_idInterfaceAddressesSource = {
    'lease': libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_LEASE,
    'agent': libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT,
    'arp':   libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_ARP,
}

def idInterfaceAddressesSource(x):
    return _db_idInterfaceAddressesSource[x]

def strsInterfaceAddressesSource():
    return _db_idInterfaceAddressesSource.keys()


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

    except (ValueError, libvirt.libvirtError):
        try:
            return conn.lookupByName(key)

        except libvirt.libvirtError:
            try:
                return conn.lookupByUUIDString(key)

            except libvirt.libvirtError:
                raise virpy.classes.ObjectNotFoundError(f"failed to get domain '{key}'")


def lookupNetwork(conn, key):
    try:
        return conn.networkLookupByName(key)

    except libvirt.libvirtError:
        try:
            return conn.networkLookupByUUIDString(key)

        except libvirt.libvirtError:
            raise virpy.classes.ObjectNotFoundError(f"failed to get network '{key}'")


def lookupSnapshot(dom, key=None):
    try:
        if key is None:
            return dom.snapshotCurrent()

        return dom.snapshotLookupByName(key)

    except libvirt.libvirtError:
        raise virpy.classes.ObjectNotFoundError(f"failed to get snapshot '{key}'")


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
