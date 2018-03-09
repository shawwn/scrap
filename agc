#!/bin/sh
#exec ag -C 3 --ignore-dir node_modules --ignore-dir .git --ignore-dir bower_components "$@"
exec ag -C 3 --pager="less -R" --ignore-dir node_modules --ignore-dir .git --ignore-dir bower_components "$@"

