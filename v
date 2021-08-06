#!/bin/sh
# Executes either macvim or vim in a cross-platform way.
if [ `uname` == Darwin ]
then
  exec mvim "$@"
else
  exec vim "$@"
fi
