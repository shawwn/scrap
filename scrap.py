import sys
import subprocess
import os
import pdb
import re
import pipes
import errno
try:
  from cStringIO import StringIO
except:
  from io import StringIO

def asserting(cond):
    if not cond:
        pdb.set_trace()
    assert(cond)

def scriptpath():
    # if which("sosbin"):
    #     path = shell("sosbin").strip()
    # else:
    #     path = "~/bin"
    """
    path = os.path.expanduser("~/bin")
    asserting(len(path) >= 0)
    return path
    """
    return os.path.dirname(os.path.abspath(__file__))

def trace():
    pdb.set_trace()

_args=sys.argv[1:]
def args():
    return list(_args)
scrap_args = args

def needargs(i, required):
    assert(i >= 0)
    sys.stderr.write('not enough args, need at least %d\n' % (i + 1))
    assert(not required)
    if required:
        sys.exit(1)
    return None

def nargs():
    return len(_arg)

def arg(i, required=True):
    xs = _args
    if len(xs) <= 0:
        return needargs(-1, required)

    if i >= len(xs):
        return needargs(i, required)
    if i < -len(xs):
        return needags(-i - 1, required)
    arg = xs[i]
    assert(arg)
    return arg

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def path():
    return getenv('PATH')

def home():
    path = getenv('HOME')
    path = os.path.normpath(path).strip()
    assert(path.startswith(os.path.sep))
    assert(len(path) > 0)
    return path

def normpath(path):
    opath = os.path.normpath(path)
    while opath.find('~' + os.path.sep) >= 0:
        opath = opath.replace('~' + os.path.sep, home() + os.path.sep, 1)
    return os.path.normpath(opath)

def joinpath(*args):
    path = os.path.join(*args)
    return os.path.normpath(path)

def isext(fname, ext):
    root, xt = os.path.splitext(fname)
    if no(ext) and no(xt):
        return True
    return fname.endswith(ext.lower())

def getenv(key=None):
    if key:
        return os.environ[key]
    else:
        return os.environ

def chmod_x(fname):
    os.system('chmod +x "%s"' % fname)

# set either fname or stdin
def edit(fname=None, filetype=None, stdin=None):
    if not fname and stdin:
        fname = '-'
    """
    args = ['mvim']
    if filetype:
        args += ['-c "set filetype=%s"' % filetype]
    args += ['"%s"' % fname]
    """
    """
    args = ['mvimft']
    if filetype:
        args += [filetype]

    fname = fname.strip()
    if fname.find(' ') >= 0:
        args += ['"%s"' % fname]
    else:
        args += ['%s' % fname]

    cmd = ' '.join(args)
    #print(cmd)
    return _system(args[0], args[1:], stdin=stdin)
    """
    import spawn_editor
    output = spawn_editor.edit_file(fname, filetype=filetype)
    return output
    # if output is None or output == '':
    #     print("Deleting empty file %s" % fname)
    #     if os.path.isfile(fname):
    #         os.unlink(fname)
    # else:
    #     return output

def mkscriptpath(scriptdir, fname=None):
    fname = fname or arg(0)
    scriptdir = scriptdir or scriptpath()

    mkdir_p(scriptdir)

    fpath = joinpath(scriptdir, fname)
    fpath = normpath(fpath)
    
    if os.path.exists(fpath):
        if not os.path.isfile(fpath):
            sys.stderr.write("filename exists but isn't a file\n")
            sys.exit(2)
    return fpath


def mkscript(is_exec, gen, name=None, scriptdir=None, verbose=True):
    fname = mkscriptpath(scriptdir, name)
    x = is_exec(fname)

    if not os.path.exists(fname):
        with open(fname, 'w') as f:
            body = gen(is_exec=x)
            if body:
                f.write(body)
        if verbose:
            print('created "%s"' % fname)
    else:
        if not os.path.isfile(fname):
            sys.stderr.write('destination is a directory\n')
            sys.exit(2)
        if verbose:
            print('%s exists, editing' % fname)

    if x:
        chmod_x(fname)

    assert(not no(fname) and os.path.isfile(fname))
    return fname

#===============================================================================
# Tee: http://stackoverflow.com/questions/616645/how-do-i-duplicate-sys-stdout-to-a-log-file-in-python
#===============================================================================
import subprocess, os, sys

def tee(logfile_name):
    # Unbuffer output
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    #
    tee = subprocess.Popen(["tee", logfile_name], stdin=subprocess.PIPE)
    os.dup2(tee.stdin.fileno(), sys.stdout.fileno())
    os.dup2(tee.stdin.fileno(), sys.stderr.fileno())
    #
    # print("\nstdout")
    # print("stderr", file=sys.stderr)
    #os.spawnve("P_WAIT", "/bin/ls", ["/bin/ls"], {})
    #os.execve("/bin/ls", ["/bin/ls"], os.environ)


#===============================================================================
# other shell utils.
#===============================================================================
from distutils.spawn import find_executable

# see http://stackoverflow.com/questions/6856119/can-i-use-an-alias-to-execute-a-program-from-a-python-script
# import subprocess
# scrap = subprocess.Popen(["/bin/bash", "-i", "-c", "nuke -x scriptpath"])
# scrap.communicate()

def which(prog):
    result = find_executable(prog)
    # if is_str(result) and not os.path.exists(result) and not result.startswith('/'):
    #     result = which(result)
    return result

def exe(cmd, *args):
    params = list(args or [])
    binpath = which(cmd)
    if not binpath:
        raise ValueError("No such exe: %s" % cmd)
    os.execve(binpath, [binpath] + params, os.environ)

def bash(cmdline, interactive=False, login=False):
    flags = "-O expand_aliases"
    if interactive:
        flags += " -i"
    if login:
        flags += " -l"
    flags += " -c"
    cmd = flatten_once(["/bin/bash", flags.split(), "-c",
        #"source ~/.bash_profile; %s" % cmdline
        cmdline
        ])
    exe(*cmd)


#===============================================================================
# load a binary python script file from ~/bin as a module, such as ~/bin/hex2ip
#===============================================================================

import imp
import sys

def load(name):
    scriptpath = os.path.dirname(sys.argv[0])
    modname = os.path.basename(name)
    pathname = os.path.normpath(os.path.join(scriptpath, modname))
    #modname, ext = os.path.splitext(basename)
    return imp.load_source(modname, pathname)

#===============================================================================
# utilities.
#===============================================================================

def reverse(seq):
    return seq[::-1]

def contains(xs, elem):
    return xs.find(elem) >= 0

def no(xs):
    return (not xs) or (len(xs) <= 0)
empty=no

def is_str(x):
    return type(x) is str

def is_iterable(x):
    try:
        if is_str(x):
            return False
        xit = iter(x)
        return True
    except TypeError as te:
        return False

def iterable(x):
    return x if is_iterable(x) else [x]

def flatten_once(xs):
    return [item for sublist in xs for item in iterable(sublist)]

def flatten(xs, recursive=True):
    ys = flatten_once(xs)
    if recursive:
        for y in ys:
            if is_iterable(y):
                return flatten(ys, recursive=True)
    return ys

def anone(x):
    return x is None

def denil(x):
    return list() if anone(x) else x

def astr(x):
    return isinstance(x, str) or isinstance(x, unicode)

def ablank(x):
    if astr(x):
        return len(x.strip()) <= 0

def nostr(x):
    return anone(x) or ablank(x)

# http://stackoverflow.com/questions/1624883/alternative-way-to-split-a-list-into-groups-of-n
import itertools
def group(n, iterable, fillvalue=None):
    "group(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(*args, fillvalue=fillvalue)

# nice stack overflow, bro
#def tuples(l, n=2):
#  return [] if len(l) <= 0 else [l[0:n], *tuples(l[n:], n)]

def tuples(l, n=2):
  r = []
  for i in range(0, len(l), n):
    r.append(l[i:i+n])
  return r

#===============================================================================

def cmd(cmd, stdin=None, stdout=subprocess.PIPE, stderr=None, shell=False):

    inputdata=stdin
    stdin=None

    if inputdata:
        if isinstance(inputdata, str):
            stdin = subprocess.PIPE
        elif hasattr(inputdata, 'read'):
            stdin = subprocess.PIPE
            inputdata = inputdata.read()
        else:
            raise Exception("stdin must be str or file-like")

    #inputdata = pipes.quote(inputdata)
    if is_str(cmd):
        cmd = cmd.replace('"""', "'")
    #print(cmd)

    p = subprocess.Popen(cmd, stdout=stdout, stderr=stderr, stdin=stdin, shell=shell, env=getenv())
    return p.communicate(input=inputdata)
command=cmd

_unset = object()

def _stdin(stdin, text=_unset):
    if isinstance(stdin, str):
        return subprocess.PIPE, stdin, 'utf-8' if text is _unset else text
    elif isinstance(stdin, bytes):
        return subprocess.PIPE, stdin, None if text is _unset else text
    elif stdin is None:
        return None, None, 'utf-8' if text is _unset else text
    else:
        raise NotImplementedError()

def _popen(cmd, stdout, stdin, shell, check=False, text=_unset):
    stdin, input, text = _stdin(stdin, text)
    #sys.stderr.write('_popen() %s\n' % repr(cmd))
    p = subprocess.Popen(cmd, stdout=stdout, stdin=stdin, shell=shell, env=getenv(), text=text)
    out, err = p.communicate(input=input)
    if check:
      if p.returncode != 0:
        raise subprocess.CalledProcessError(p.returncode, cmd, out, err)
    return out, err

# call system function.
def _system(cmd, args, stdin=None, stdout=subprocess.PIPE, check=False, text=_unset):
    out, err = _popen([cmd] + flatten(args), stdout=stdout, stdin=stdin, shell=False, check=check, text=text)
    return out, err

def system(cmd, args, stdin=None, stdout=subprocess.PIPE, check=False, text=_unset):
    out, err = _system(cmd, args, stdin=stdin, stdout=stdout, check=check, text=text)
    return out

#
# Careful with _shell() and shell().
#
def _shell(cmd, stdin=None, stdout=subprocess.PIPE, check=False, text=_unset):
    out, err = _popen(cmd, stdout=stdout, stdin=stdin, shell=True, check=check, text=text)
    return out, err

def shell(cmd, stdin=None, stdout=subprocess.PIPE, check=False, text=_unset):
    out, err = _shell(cmd, stdin=stdin, stdout=stdout, check=check, text=text)
    return out

def verbose():
    try:
        return args and args.verbose
    except NameError:
        return False
    except AttributeError:
        return False

def ppcmd(cmd):
    assert(not nostr(cmd))
    # cmd = [] if anone(cmd) else cmd
    cmd = [cmd] if astr(cmd) else cmd
    if verbose():
        prcmd(cmd)
    return cmd

def prcmd(cmd):
    print('system(%s)' % ', '.join(['"%s"' % x for x in cmd]))

def syscmd(cmd, exitcode=1):
    if nostr(cmd):
        return ''
    out, err = command(ppcmd(cmd))
    if astr(err) and not no(err):
        sys.stderr.write(err)
        sys.exit(exitcode)
    return out

def pipecmds(lhs, rhs):
    if nostr(lhs):
        return syscmd(rhs)
    if nostr(rhs):
        return syscmd(lhs)
    p1 = subprocess.Popen(ppcmd(lhs), stdout=subprocess.PIPE)
    p2 = subprocess.Popen(ppcmd(rhs), stdin=p1.stdout, stdout=subprocess.PIPE)
    out, err = p2.communicate()
    if astr(err) and not no(err):
        sys.stderr.write(err)
        sys.exit(p2.returncode)
    return out

# http://stackoverflow.com/questions/35817/how-to-escape-os-system-calls-in-python
def shellquote(s):
    #return "'" + s.replace("'", "'\\''") + "'"
    #
    # use Python 3's shlex solution instead:
    #
    return "'" + s.replace("'", '"' + "'" + '"') + "'"

#===============================================================================
# quote.
#===============================================================================

try:
    from shlex import quote 
except ImportError:
    from pipes import quote 


#===============================================================================
# UTC.
#===============================================================================


# return current UTC timestamp.
def utc():
    from datetime import datetime
    d = datetime.utcnow()
    import calendar
    return calendar.timegm(d.utctimetuple())

#===============================================================================
# hexstr.
#===============================================================================

# hexstr examples:
#  >>> hexstr(0)
#  '00'
#  >>> hexstr(255)
#  'ff'
#  >>> hexstr(256)
#  '0100'
def hexstr(n):
    s = hex(n)[2:]
    return s.zfill(len(s) + len(s) % 2)


