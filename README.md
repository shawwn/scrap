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
# all the scrap scripts containing `mk`
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
```

```
# all the scrap scripts containing `git`
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

# Complete listing of all scripts
```
$ llbin
1st
2nd
3rd
ack2
agc
agcolor
ag-filenames-only
apps
args
b64dec
b64enc
backupbin
backupdir
beautify
beautify-portscan
beyond-compare
beyond-compare-wait
bin-bin
bindir
bindirs
bin-edit
bin-find
bin-find1
bin-find-exact
binlink
bin-path
bin-paths
bins
branch
brewpath
brews
brewurl
bytes2human
cant-eject
ccode
cdbin
cdbranch
cdmvim
changedir
cleardns
cls
cmd
cmd2
codefiles-c
codegrep
coff
collapse-blanks
cols
columnize
comparefiles
contains
cpbin
cpcmd
cpp-classes
cputemp
ctrlc
ctrlctrim
ctrlv
cuMSP
curl-get-with-headers
curlquote
cut-before
ddgui
ddpv
decrypt
dlls
duh
eachline
eachnull
echoargs
echo-stdin
edbin
edit
edit2
editft
encrypt
enum-hashes
exist
exists
extract-urls
exts
fileext
fileexts
fileinfo-check-arch
files
filesize
findf
first
firstlast
first
flags
foo
foreach-line
fromhex
fromhex2
ft
ga
gac
gacm
gc
gca
gcgh
gcm
gco
gcu
gd
gd1
gdn
gdns
gh
ghc
ghclone
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
github-branch-create
github-branch-create-local
github-clone-and-add-remote
github-image-host
github-image-hostall
github-shorten-url
github-subtree-create
github-subtree-pull
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
gl
gl1
gm
gp
gpul
greps
gs
gs2
gsa
gu
gzip-size
hasbang
hashing
hex2ip
hfsslower.d
hs
http-beautify
http-body
http-headers
human2bytes
humansizesort
icgrep
igrep
infopystdin
initialtext
install-homebrew
iosnoop-show-full-paths_but-only-shows-calls-to-open
ip2cidr
ips
irgrep
isort
iterm
joinlines
jslib
json-beautify
key2rsa
keygen
keys
kill-chrome-helpers
kill-tunnelblick
l
l1
l-1
l2
l3
l4
l5
lall
last
lastfirst
lib-changename
linecount
ll
llapp
llbin
llbranch
llcommit1
lld
llpaths
llpathst
llps
llrecent
llsize
llsortlast
lltar
lltime
lltree
lltype
llunpaths
locate-update
log-grep
lowercase
ls
ls1
lsdisk
lsn
lsusb
ltrim
lwrap
macbook-config-sleep-hibernate
macbook-config-sleep-normal
maclife.d
make-with
match
matchfiles
math
mdtool
merge
mergefiles
mergepython
mergeruby
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
month2num
mvbin
mvbranch
mvim
mvimc
mvimft
mvims
mysql-start
mysql-stop
narrow
natsort
nbytes
netinfo-arp
netinfo-arp-scan
netinfo-daemons
netinfo-netdiscover
netinfo-netstat
netinfo-netstat-tulpn
netinfo-nmap-scan-localnet
netinfo-pingsweep
netinfo-routes
netpen-fetch
netpen-find-interesting-files
netpen-getinfo
netpen-getinfo2
netpen-getinfo3
netpen-outdir
netpen-path
netscan
netview
newl
nlines
nocolor
normpath
npm-download-all-packages
nthcol
nthline
null
oauth
opencl-linklib
open-editor
openfirst
openvpn-fetch-client-files
osx-bouncing-icons-disable
osx-bouncing-icons-enable
osx-cpu-features
p'
packhex
parse-c
pastebin
patch-apply
patch-create
patch-integrate
pdfcat
phoenix-db-setup
phoenix-deps
phoenix-new
phoenix-start
pingsweep
pip-install-test
plistcat
plt-racket
portscan
portscan2
portscan3
portscan-quick
pos
postgres-initialize-database
postgres-start
postgres-stop
pq
print0
prjson
psfind
ps-find
psfocus
pskill
ps-offspring
psqlgetfield
psqlsetfield
ptyfix
pubkey
pwgen
pws
py-example-watchdog
pyinst
pypitest-register
pypitest-upload
python-build-ext
pyval
quote
quoten
quotent
ramdisk-create
rand-bday
randint
ratio
re
re[
re[]+
readvar
recgrep
recvchars
recvfile
recvsh
recvtar
redis-start
reminder
rename
replace
replace2
replace-in-files
replace_n_rn
report-gen
resub
revbytes
reverse
revlines
revstr
rgrep
rll
rls
rmblanks
rmbranch
rmbranch-remote
rmrf
routeof
routes
rpi-default-led
rpi-deploy
rtrim
run
sack
sackvim
sag
scrap-setup-ubuntu
screenshot-firefox
sdcard-dd
sdcard-detect-disk
sdcard-write-freebsd
sdcard-write-kali
sendbackup
sendchars
sendfile
sendsh
sendsh2
sendtar
sendweb
sha1sum-recursive
sha256sums
simulavr_preprocess
skip-first-n-lines
skip-last-n-lines
skip-n-lines
sleepnow
snippet-array-loop-with-spaces
snippet-receive-and-repass-quoted-args
snippet-receive-and-repass-quoted-args2
snippet-special-params
socatchk
sort-cppfiles
sortuniq
splitby
splitext
sp-notes
spotlight-rebuild
sqlmap
srm1
srm1z
srmz
sshfwd
sshproxy
ssh-rpi
ssh-sync
sshtar
strace-osx
sub
sub1
suball
sub-all
tcpview
td
tmpbin
tohex
trim
trimlines
tsnap
ttyMSP
tweets
udisk
unbuffer
unescape
unix2dos
unquote
urlavail
urldecode
urlencode
urlquote
urlunquote
utcnow
utcstamp
utcstamp2time
utctime2stamp
viewbytes
viewchars
viewfile
vimterm
vim-tokenize
vinoinfo
vs
watcher
wgetfiles
where
wheredir
whichapp
xbuild-both
xbuild-debug
xbuild-release
zopped
```

