#!/usr/sbin/dtrace -s

#pragma D option quiet
#pragma D option switchrate=10hz

dtrace:::BEGIN
{
	printf("%-12s %6s %6s %-12.12s %-12s %s\n", "TIME(ms)", "UID",
	    "PID", "PROCESS", "CALL", "DIR/FILE");
}

/* see sys/bsd/sys/vnode_if.h */

fbt::VNOP_CREATE:entry,
fbt::VNOP_REMOVE:entry
{
	this->path = ((struct vnode *)arg0)->v_name;
	this->name = ((struct componentname *)arg2)->cn_nameptr;
	printf("%-12d %6d %6d %-12.12s %-12s %s/%s\n",
	    timestamp / 1000000, uid, pid, execname, probefunc,
	    this->path != NULL ? stringof(this->path) : "<null>",
	    stringof(this->name));
}
