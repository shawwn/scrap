#!/bin/sh
export PYTHONSTARTUP="${PYTHONSTARTUP:-$(bindir)/etc/tfrepl.py}"
export PYTHON_HOST="${PYTHON_HOST:-python3}"
exec "${PYTHON_HOST}" "$@"
