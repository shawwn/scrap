#!/usr/bin/env python3
'''
Idea got from here:
http://stackoverflow.com/questions/10103359/vim-editor-in-python-script-tempfile
'''
import sys, tempfile, os
from subprocess import call
import shlex

scrap_home = os.path.dirname(__file__)
edit_bin = os.path.join(scrap_home, 'edit')
#default_editor = 'vim'
default_editor = edit_bin

def get_editor_output(initial_message="", filetype=None):
    EDITOR = os.environ.get('EDITOR',edit_bin)
    output = ""
    with tempfile.NamedTemporaryFile(suffix=".tmp") as f:
        f.write(initial_message)
        f.flush()
        call([EDITOR, f.name])
        k = open(f.name, "r")
        output = k.read()
        k.close()
    return output

def edit_file(name, filetype=None):
    EDITOR = os.environ.get('EDITOR',edit_bin)
    call(EDITOR + ' ' + shlex.quote(name), shell=True)
    if os.path.isfile(name):
        with open(name) as f:
            return f.read()

