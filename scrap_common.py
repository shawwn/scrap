import pdb
import os

def isverbose(x):
    return False

#===============================================================================
# Basic Utilities
#===============================================================================

def panic(msg, exitcode=1):
    for line in listify(msg):
        if not line.endswith('\n'):
            line += '\n'
        sys.stderr.write(line)
    sys.exit(exitcode)

def asserting(val):
    if not val:
        pdb.set_trace()
    assert(val)

def reverse(seq):
    return seq[::-1]

def contains(xs, elem):
    return xs.find(elem) >= 0

def no(xs):
    return (not xs) or (len(xs) <= 0)
empty=no

def is_str(x):
    return (type(x) is str) or (type(x) is unicode)

def is_iterable(x):
    try:
        if is_str(x):
            return False
        xit = iter(x)
        return True
    except TypeError, te:
        return False

def listify(x):
    if is_iterable(x):
        return list(x)
    if not x:
        return list()
    return [x]

def flatten_once(xs):
    return [item for sublist in xs for item in listify(sublist)]

def flatten(xs, recursive=True):
    ys = flatten_once(xs)
    if recursive:
        for y in ys:
            if is_iterable(y):
                return flatten(ys, recursive=True)
    return ys

#===============================================================================
# Other Utilities
#===============================================================================

import platform
def iswindows():
    return platform.system().lower().find('windows') >= 0

def wait_any_key():
    if iswindows():
        print "Press any key to continue..."
        import msvcrt as m
        return m.getch()
    else:
        return raw_input("Press enter to continue...")
        

def increase_stackoverflow_limit(limit=10**6):
    import resource, sys
    #resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
    sys.setrecursionlimit(limit)

#===============================================================================
# Filesystem Utilities
#===============================================================================

class Path(object):
    def __init__(self, path):
        assert(isinstance(path, str) or isinstance(path, unicode))
        self._path = path

    @property
    def path(self):
        val = self._path
        val = os.path.normpath(val)
        val = os.path.normcase(val)
        return val

    @property
    def abspath(self):
        return os.path.abspath(self.path)

    @property
    def isfile(self):
        return os.path.isfile(self.path)

    @property
    def isdir(self):
        return os.path.isdir(self.path)

    @property
    def exists(self):
        return os.path.exists(self.path)

    def __eq__(self, other):
        return self.abspath == mkpath(other).abspath

    def __hash__(self):
        return hash(self.abspath)

    def __str__(self):
        return self.path

    def __repr__(self):
        return repr(self.path)

def mkpath(filepath):
    asserting(filepath)
    if isinstance(filepath, Path):
        return filepath
    return Path(filepath)

def getpath(filepath):
    if isinstance(filepath, Path):
        return str(filepath)
    return filepath


class FileSet(object):
    def __init__(self, filepaths=[]):
        self.added = set()
        self.files = []
        self.add(filepaths)

    def add(self, x):
        if not x:
            return
        if isinstance(x, FileSet):
            return self.add(x.files)
        for filepath in listify(x):
            path = mkpath(filepath)
            if not path.exists:
                print "Path doesn't exist: %s" % path
                return
            if not path.isfile:
                pdb.set_trace()
                print "Path isn't a file: %s" % path
                return
            # if it was already added, ignore it.
            if path in self.added:
                return
            self.added.add(path)
            self.files.append(path)

    def __contains__(self, filepath):
        path = mkpath(filepath)
        return path in self.added

    def __repr__(self):
        return repr(self.files)

    def __str__(self):
        return repr(self.files)

import fnmatch
def patmatch(name, patterns, ignorecase=False):
    name = name.lower() if ignorecase else name
    for pattern in listify(patterns):
        pattern = pattern.lower() if ignorecase else pattern
        if fnmatch.fnmatch(name, pattern):
            return True
    return False


#
# adapted from http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
#
import os
def find_files_in(directory, patterns=[], ignore_patterns=[], ignorecase=True, verbose=False):
    patterns = listify(patterns)
    ignore_patterns = listify(ignore_patterns)
    # if no patterns, then match everything.
    if len(patterns) <= 0:
        patterns += ['*']
    if os.path.isfile(directory):
        # if the 'directory' is actually a file, then allow it if it
        # matches.
        if patmatch(directory, patterns, ignorecase=ignorecase):
            if not patmatch(directory, ignore_patterns, ignorecase=ignorecase):
                yield directory
    else:
        for root, dirs, files in os.walk(directory):
            if isverbose(verbose):
                print 'find_files_in(%s): trying %d files' % (repr(root), len(files))
            for basename in files:
                if patmatch(basename, patterns, ignorecase=ignorecase):
                    if not patmatch(basename, ignore_patterns, ignorecase=ignorecase):
                        filename = os.path.join(root, basename)
                        yield filename

def find_files(paths_or_patterns, patterns=['*'], ignore_patterns=[], ignorecase=True, verbose=False):
    paths_or_patterns = listify(paths_or_patterns)
    patterns = list(listify(patterns))
    ignore_patterns = list(listify(ignore_patterns))
    paths = []
    for arg in paths_or_patterns:
        if arg.find('*') >= 0:
            # get all patterns that were passed into the first param.
            patterns.append(arg)
        else:
            # get all paths that were passed into the first param.
            paths.append(arg)
    # search for matching files under each path.
    found = FileSet()
    for path in paths:
        path = mkpath(path)
        # skip bogus dirs.
        if not path.exists:
            print "find_files(): Doesn't exist: %s" % path
            continue
        if isverbose(verbose):
            print 'find_files(%s)' % repr(str(path))
        for filepath in find_files_in(str(path), patterns=patterns, ignore_patterns=ignore_patterns, ignorecase=ignorecase, verbose=verbose):
            if filepath not in found:
                found.add(filepath)
                yield filepath




