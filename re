#!/usr/bin/env python

#==============================================================================
# Functionality
#==============================================================================
import pdb

# utility funcs, classes, etc go here.

def asserting(cond):
    if not cond:
        pdb.set_trace()
    assert(cond)

#==============================================================================
# Cmdline
#==============================================================================
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
    description="""
TODO
""")
     
parser.add_argument('--re-verbose',
    dest='verbose',
    action="store_true",
    help="verbose output" )
     
# parser.add_argument('--re-escape',
#     dest='escape',
#     action="append",
#     help="interpret the next param as a literal (by using re.escape() on it)" )
     
# parser.add_argument('--re-pattern',
#     dest='pattern',
#     action="append",
#     help="interpret the next param as a regex pattern" )
     
parser.add_argument('--ignorecase',
    action="store_true",
    help="re.IGNORECASE" )
     
parser.add_argument('--multiline',
    action="store_true",
    help="re.MULTILINE" )
     
parser.add_argument('--dotall',
    action="store_true",
    help="re.DOTALL" )

args = None

def _startup():
    global args
    if not args:
        args, leftovers = parser.parse_known_args()
        args.args = leftovers
    return args

#==============================================================================
# Main
#==============================================================================
import sys
import os
import re

def terms():
    x = []
    x += args.args or []
    #x += args.pattern or []
    #x += [re.escape(x) for x in (args.escape or [])]
    return x

def reflags():
    x = re.VERBOSE
    if args.ignorecase:
        x |= re.IGNORECASE
    if args.multiline:
        x |= re.MULTILINE
    if args.dotall:
        x |= re.DOTALL
    return x

def process(patterns, data):
    #data = data.replace('\r', '').replace('\t', ' ').replace('\n', ' ')
    if not data.startswith(' '):
        data = ' ' + data
    for pat in patterns:
        pat = r' [\s]+ (%s) \b' % pat
        if args.verbose:
            print 'pat:', pat
        for m in re.compile(pat, flags=reflags()).finditer(data):
            yield m.group(1)

def run():
    if args.verbose:
        print args
    found = set()
    wrote = False
    data = sys.stdin.read()
    if args.verbose:
        print 'stdin:', data.rstrip()
    pats = terms()
    # if no terms provided, just print everything.
    if len(pats) <= 0:
        if args.verbose:
            print 're: no patterns provided, printing everything'
        sys.stdout.write(data)
        sys.stdout.flush()
    else:
        for flag in process(pats, data):
            lflag = flag.strip()
            if args.ignorecase:
                lflag = lflag.lower()
            if lflag in found:
                continue
            found.add(lflag)
            wrote = True
            sys.stdout.write(' ' + flag)
            if args.verbose:
                print ''
        if wrote:
            sys.stdout.write('\n')
        

def main():
    _startup()
    return run()

if __name__ == "__main__":
    main()

