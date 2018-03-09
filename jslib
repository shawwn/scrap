#!/usr/bin/env python

#==============================================================================
# Functionality
#==============================================================================
import pdb
import sys
import os
import re
import scrap

# utility funcs, classes, etc go here.

def asserting(cond):
    if not cond:
        pdb.set_trace()
    assert(cond)

def has_stdin():
    return not sys.stdin.isatty()

def reg(pat, flags=0):
    return re.compile(pat, re.VERBOSE | flags)

#==============================================================================
# Cmdline
#==============================================================================
import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
    description="""
TODO
""")
     
parser.add_argument('-v', '--verbose',
    action="store_true",
    help="verbose output" )
     
parser.add_argument('-t', '--no-unescape-tabs',
    action="store_true",
    help="don't unescape tabs." )
     
parser.add_argument('-r', '--requires',
    action="append",
    default=[],
    help="specify a dependency." )
     
parser.add_argument('name')
parser.add_argument('projectname')
parser.add_argument('projectsite')

args = None

#==============================================================================
# Main
#==============================================================================

def cmd(name, args):
    out, err = scrap._system(name, args)
    if err:
        sys.stderr.write(err)
    else:
        return out

def run():
    if args.verbose:
        print args

    if args.verbose:
        print "; $ jslib %s" % ' '.join(sys.argv[1:])
    print """;
; %s
; %s
; 
(jslib %s""" % (args.projectname, args.projectsite, args.name)

    for req in args.requires:
        print "  (requires %s)" % req

    # for each arg on cmdline...
    for path in args.args:
        body = cmd('curlquote', [path] + (['-t'] if args.no_unescape_tabs else []))
        if body:
            if body.startswith('"') and not body.startswith('"\n'):
                body = body[:1] + '\n' + body[1:]
            if body.endswith('"') and not body.endswith('\n"'):
                body = body[:-1] + '\n' + body[-1:]
            ext = os.path.splitext(path)[1].lower()
            print ""
            print "  ; %s" % os.path.basename(path)
            print "  (%s %s)" % (ext[1:], body)

    print ")"
    print ""

def main():
    global args
    if not args:
        args, leftovers = parser.parse_known_args()
        args.args = leftovers
    return run()

if __name__ == "__main__":
    main()

