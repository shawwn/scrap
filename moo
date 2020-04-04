#!/bin/sh

dir="${1}"
shift 1

if [ -z "${dir}" ]
then
    1>&2 echo "usage:"
    1>&2 echo "  ${0} <cow> [<option>]"
    exit 1
fi


set -x
exec cowsay -f "${HOME}/cowsay-files/cows/${dir}.cow" "$@"

