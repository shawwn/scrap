#!/usr/bin/env python3

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

def rx(pat, flags=0):
    return re.compile(pat, re.VERBOSE | flags)

# http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

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
     
parser.add_argument('-d', '--dirs-only',
    action="store_true",
    help="only print directories." )

parser.add_argument('-n', '--no-color',
    action="store_true",
    help="disable color." )

parser.add_argument('-r', '--reverse',
    action="store_true",
    help="reverse the sorting." )
     
parser.add_argument('-L', '-l', '--level',
    type=int,
    default=0,
    help="maximum dir nesting to descend into." )

parser.add_argument('--only-paths',
    action="store_true",
    dest='only_paths',
    help="print out only the paths.  (Equivalent to ls -1).  Can use -1 instead of --only-paths" )

parser.add_argument('--path',
    default=[],
    action="append",
    help="a path to be searched." )
     
llprogs = [
        "lltree",
        "lltime",
        "lltype",
        "llsize",
        "llsortlast",
        "llpaths",
        "llpathst",
        "llunpaths"
        ]

parser.add_argument('-p', '--prog',
    default=[],
    action="append",
    help="ll variants to be successively applied:\n%s" % '\n'.join(llprogs) )

args = None

#==============================================================================
# Main
#==============================================================================

def errcheck(out, err):
    # # if err or (out.find('error opening') >= 0):
    # #     sys.stderr.write(err or out)
    # #     sys.exit(1)
    # if out.find(b'error opening') >= 0:
    #   print(out, file=sys.stderr.buffer, flush=True)
    #   out = b''
    # if err:
    #   print(err, file=sys.stderr.buffer, flush=True)
    return out

def cmd(progs, paths, baseprog="lltree"):
    progs = list(progs)
    paths = list(paths)
    if len(paths) <= 0:
      paths += ['.']
    #paths = ['"%s"' % x for x in paths]
    if args.verbose:
        print('progs=%s, paths=%s, baseprog=%s' % (repr(progs), repr(paths), repr(baseprog)))
    flags = []
    progflags = []
    if args.reverse:
        progflags += ['-r']
    if args.level > 0:
        flags += ['-L']
        flags += ['%d' % args.level]
    if args.no_color:
        flags += ['-n']
    if args.dirs_only:
        flags += ['-d']
    if args.verbose:
        print('scrap.system(%s, %s) | %s' % (repr(baseprog), repr(flags + progflags + paths), ' | '.join(progs)))
    input = b''
    for path in paths:
        out, err = scrap._system(baseprog, flags + progflags + [path], check=False, text=None)
        out = errcheck(out, err)
        input += out
    for prog in progs:
        out, err = scrap._system(prog, progflags, stdin=input, check=False, text=None)
        out = errcheck(out, err)
        input = out
    if args.only_paths:
        #out, err = scrap._system('cols', [',3:'], stdin=input, check=False)
        out, err = scrap._system('l-1', [], stdin=input, check=False, text=None)
        out = errcheck(out, err)
        input = out
    out = input
    if out:
        sys.stdout.buffer.write(out)
    return input


def run():
    if args.verbose:
        print(args)
    cmd(args.prog, args.args + args.path)

def remove_all_in(lst, x):
    in_ = False
    while x in lst:
        lst.remove(x)
        in_ = True
    return in_

def isfunc(x):
    return hasattr(x, '__call__')

def testify(x):
    if isfunc(x):
        return x
    def fn(item):
        return item == x
    return fn

def testify_any(lst):
    if not isinstance(lst, list):
        return testify(lst)
    def fn(item):
        return item in lst
    return fn


def remove_all_matching(lst, predicate):
    predicate = testify_any(predicate)
    gather = []
    i = 0
    while i < len(lst):
        if predicate(lst[i]):
            gather.append(lst[i])
            del lst[i]
        else:
            i += 1
    return gather

def main():
    global args
    if not args:
        args, leftovers = parser.parse_known_args()
        if not args.prog:
            args.prog = []
        if not args.path:
            args.path = []
        #
        # hack to differentiate passing -1 vs 1
        #
        args.only_paths |= remove_all_in(leftovers, '-1')
        #
        # if we're doing `l -1` then disable color, since the stdout
        # is likely going to be piped to other scripts.
        #
        args.no_color |= args.only_paths
        #
        args.prog += remove_all_matching(leftovers, llprogs)
        levels = remove_all_matching(leftovers, lambda x: RepresentsInt(x))
        if len(levels) > 0:
            args.level = int(levels[-1])
        args.args = leftovers
    return run()

if __name__ == "__main__":
    main()

