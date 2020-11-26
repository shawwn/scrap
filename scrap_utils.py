import socket
import struct
import re
import pdb

#==============================================================================
# Regex Utils
#==============================================================================

class Pat:
    hex = r'[0-9a-fA-F]+'
    ip = r'[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}'

class Re:
    @staticmethod
    def compile(pat, flags=0):
        pat = pat.replace('[:hex:]', Pat.hex)
        pat = pat.replace('[:ip:]', Pat.ip)
        return re.compile(pat, Re.useflags(flags))

    @staticmethod
    def match(pat, string, flags=0):
        return re.match(pat, string, Re.useflags(flags))

    @staticmethod
    def useflags(x=0):
        return (x | re.VERBOSE);

#==============================================================================
# Network Utils
#==============================================================================

def str2endian(endian):
    if endian == "big":
        endian = "<"
    elif endian == "little":
        endian = ">"
    if endian not in ['>', '<']:
        raise Exception("str2endian(): unknown endian spec: %s" % endian)
    return endian

def int2ip(i, endian="big"):
    ip = i
    if type(ip) is int:
        ip = socket.inet_ntoa(struct.pack("%sL" % str2endian(endian), i))
    assert(type(ip) is str)
    return ip

def ip2int(ip, endian="big"):
    if type(ip) is str:
        ip = struct.unpack("%sL" % str2endian(endian), socket.inet_aton(ip))[0]
    assert(type(ip) is int)
    return ip

def ipAND(ip1, ip2):
    assert(type(ip1) == type(ip2))
    if type(ip1) is str:
        return int2ip( ipAND( ip2int(ip1), ip2int(ip2) ) )
    elif type(ip1) is int:
        return ip1 & ip2
    raise Exception("ipAND(): bad type for ip: %s" % type(ip1))


rxhex2ip = Re.compile(r'0[xX] ( [:hex:] )' )

def hex2ip(line):
    outstr = ''
    pos = 0
    if not rxhex2ip.search(line):
        outstr += line
    else:
        for m in rxhex2ip.finditer(line):
            outp = line[pos:m.start(0)]
            outstr += outp

            h = line[m.start(1):m.end(1)]
            h = int(h, 16)
            
            ip = socket.inet_ntoa(struct.pack(">L", h))
            outstr += ip
            pos = m.end(1) 
        outstr += line[pos:]
    return outstr


rxips = Re.compile(r'(?P<addr> [:ip:]) \b .*? (?P<netmask> [:ip:])' )

def parse_ifconfig(ifconfig):
    ifaces = []
    env = {}
    g = None

    def it_new():
        env['g'] = {}
        return env['g']

    def it_ensure():
        if 'g' not in env:
            it_new()
        return env['g']

    def it_finish():
        if 'g' in env and len(env['g']['lines']) > 0:
            info = ' '.join(env['g']['lines'])
            del env['g']['lines']
            ifaces.append(info)
        it_new()

    def it_set(key, val):
        g = it_ensure()
        g[key] = val
        return g

    def it_getarr(key):
        g = it_ensure()
        if key not in g:
            g[key] = []
        arr = g[key]
        assert(type(arr) is type([]))
        return arr

    for line in ifconfig.splitlines():
        if Re.match(r'^ [\s]', line):
            it_getarr('lines').append(line)
        elif Re.match(r'^ [\w\d]+ \b', line):
            it_finish()
            it_getarr('lines').append(line)
    it_finish()
    return ifaces


def ipinfo(ifconfig):
    for iface in parse_ifconfig(ifconfig):
        print(iface)


import sys

def pipeline(thunk, *args, stdout=sys.stdout, stderr=sys.stderr):
    try:
        return thunk(*args)
    except IOError:
        # http://stackoverflow.com/questions/15793886/how-to-avoid-a-broken-pipe-error-when-printing-a-large-amount-of-formatted-data
        try:
            sys.stdout.close()
        except IOError:
            pass
        try:
            sys.stderr.close()
        except IOError:
            pass
