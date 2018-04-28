# scrap

Various scripts I've written over the years.

## installation 

```
git clone https://github.com/shawwn/scrap ~/scrap

# add scrap to PATH
echo 'export PATH="${HOME}/scrap:${PATH}"' >> ~/.bashrc
echo 'export PATH="${HOME}/scrap:${PATH}"' >> ~/.zshrc
```

## examples

## `mkbin <name>`
Make a new scrap script with a predefined bash template.
If `<name>` already exists, the script is edited instead.
If you save an empty file, the script is deleted.

## `mkpy <name>`
Make a new scrap script with a predefined python template.
If `<name>` already exists, the script is edited instead.
If you save an empty file, the script is deleted.

### `math <expr>`

Evaluate math.
```
$ math 60*60
3600
$ math 2^64/2^60
16.0000
$ math '2^64/2^(60+1)'
8.0000
```

### `narrow [filter1] [filter2] ....`

Filter lines by each filter.

A filter is a python regex. NOTE: You must explicitly put whitespace within `[ ]`.

For each line, the line is discarded unless it matches the filter.

If a filter starts with `!`, all lines are kept except those matching the filter.

The general idea is that you can do `<some command> | narrow foo` to see all lines containing foo,
and `<some command> | narrow foo bar` to see all lines containing foo and bar, and so on.

This is a very easy way of trimming down output to exactly what you care about.

```
$ ls -1 /
bin
boot
dev
etc
home
init
lib
lib64
media
mnt
opt
proc
root
run
sbin
snap
srv
sys
tmp
usr
var
$ ls -1 / | narrow lib
lib
lib64
$ ls -1 / | narrow '^[bdl]'
bin
boot
dev
lib
lib64
$ ls -1 / | narrow 'bin|lib|tmp'
bin
lib
lib64
sbin
tmp
$ ls -1 / | narrow 'bin|lib|tmp' 'ib|bi'
bin
lib
lib64
$ ls -1 / | narrow 'bin|lib|tmp' 'ib|bi' "\!lib"
bin
```

### llbin [filter1] [filter2] ...
List all scrap scripts.

```
$ llbin
1st
2nd
3rd
ack2
ag-filenames-only
agc
agcolor
...
$ llbin mk
mkalias
mkalias2
mkbash
mkbin
mkbranch
mkbranch-local
mkcd
mkmod
mkpy
mkpy-basic
$ llbin git
git-3way
git-3way-rm
git-alldiff
git-branch-current
git-branch-rm
git-branch-rm-remote
git-checkout
git-clone-from-commit
git-commit
git-commit-message-last
git-commit-undo
git-diff-show-all
git-diff-show-all-single-commit
git-discard
git-keep-ours
git-keep-theirs
git-key
git-list-files
git-list-objects
git-log
git-log2
git-merge
git-merge-to
git-merge-to-master
git-nuke
git-nuke-commits
git-patch-apply
git-patch-from-commit
git-patch-from-last-commit
git-pr-fetch
git-pr-fetchall
git-repush
git-revert
git-review-all-changes-just-merged
git-status
git-stdout
git-unpush-last-commit
git-unstage
github-branch-create
github-branch-create-local
github-clone-and-add-remote
github-image-host
github-image-hostall
github-shorten-url
github-subtree-create
github-subtree-pull
```


