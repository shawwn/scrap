import re

def reg(pat, flags=0):
    return re.compile(pat, re.VERBOSE | flags)

def matches(s, pat, *, case='smart', verbose=False):
    inverted = True
    if len(pat) > 0 and pat[0] == "!":
        inverted = False
        pat = pat[1:]
    flags = 0
    if case == 'off':
        if verbose: print('case==of')
        flags = re.IGNORECASE
    elif case == 'on':
        if verbose: print('case==on')
        pass
    elif case == 'smart': # smart case
        if verbose: print('case==smart')
        if not any(x.isupper() for x in pat):
            if verbose: print('smartcase-ignore')
            flags = re.IGNORECASE
    else:
        raise ValueError('unknown case specification %s' % case)
    x = reg('(?:.*)' + pat, flags).match(s)
    return inverted == (not (not x))

def narrow(strings, searches, **kws):
  if isinstance(strings, str):
    return len(narrow([strings], searches, **kws)) > 0
  if isinstance(searches, str):
    searches = [searches]
  for search in searches:
    strings = [s for s in strings if matches(s, search, **kws)]
  return strings

