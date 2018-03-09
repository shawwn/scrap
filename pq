#!/usr/bin/env python

import sys
import re

args = sys.argv[1:]

out = ''

for arg in args:
    if len(arg) == 1:
        arg = re.escape(arg)
    out += arg

bs = "\\"

#out = out.replace(bs, bs * 2)
sys.stdout.write(out)

