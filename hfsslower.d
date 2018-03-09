#!/usr/sbin/dtrace -s

#pragma D option quiet
#pragma D option defaultargs
#pragma D option switchrate=10hz

dtrace:::BEGIN
{
	printf("%-20s %-16s %1s %4s %6s %s\n", "TIME", "PROCESS",
	    "D", "KB", "ms", "FILE");
	min_ns = $1 * 1000000;
}

/* see bsd/hfs/hfs_vnops.c */

fbt::hfs_vnop_read:entry
{
	this->read = (struct vnop_read_args *)arg0;
	self->path = this->read->a_vp->v_name;
	self->kb = this->read->a_uio->uio_resid_64 / 1024;
	self->start = timestamp;
}

fbt::hfs_vnop_write:entry
{
	this->write = (struct vnop_write_args *)arg0;
	self->path = this->write->a_vp->v_name;
	self->kb = this->write->a_uio->uio_resid_64 / 1024;
	self->start = timestamp;
}

fbt::hfs_vnop_read:return,
fbt::hfs_vnop_write:return
/self->start && (timestamp - self->start) >= min_ns/
{
	this->iotime = (timestamp - self->start) / 1000000;
	this->dir = probefunc == "hfs_vnop_read" ? "R" : "W";
	printf("%-20Y %-16s %1s %4d %6d %s\n", walltimestamp,
	    execname, this->dir, self->kb, this->iotime,
	self->path != NULL ? stringof(self->path) : "<null>");
}

fbt::hfs_vnop_read:return,
fbt::hfs_vnop_write:return
{
	self->path = 0; self->kb = 0; self->start = 0;
}
