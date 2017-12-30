#!/usr/bin/python

__author__ = "Anirudh Srinivasan "
__copyright__ = "Copyright 2015"
__version__ = "1.0"
__maintainer__ = "Anirudh Srinivasan"
__email__ = "srianirudh@gmail.com"
__status__ = "Production"

from optparse import OptionParser
from subprocess import Popen, call, PIPE
from shlex import split
from commands import getstatusoutput
from os import mkdir
from os.path import basename , normpath
import time

parser = OptionParser()
parser.add_option('-d', '--drive', dest='drive', help='this is the name of the drive like sda, hdd etc..')
parser.add_option('-f', '--folder', dest='folder', help='this is the name of the directory like /data or /var/log')
parser.add_option('-t', '--fstype', dest='fstype', help='this is the type of filesystem you need like ext4 or xfs')
(opts, args) = parser.parse_args()

class FormatDrive(object):
	'''This is a class that does end to end create partition, deal with lvm, make filesystem, extend filesystem, write to fstab and resize filesystem'''

	def __init__(self, drive, folder, fstype):
	    self.drive = str(drive)
	    self.folder =str (folder)
	    self.fstype = str(fstype)

	def fdisk(self):
	    '''This is a definition to perform fdisk the drive in the argument'''
	    before_pipe_cmd = 'echo -e "n\np\n1\n\n\nt\\n8e\nw"'
	    before_pipe_args = split(before_pipe_cmd)
	    after_pipe_cmd = "fdisk /dev/%s" %self.drive
	    after_pipe_args = split(after_pipe_cmd)
	    p1 = Popen(before_pipe_args, stdout=PIPE)
	    p2 = call(after_pipe_args, stdin=p1.stdout)

	def partprobe(self):
	    '''This function performs the partprobe'''
	    #pprobe = "partprobe /dev/%s" %self.drive
	    pprobe = "partprobe"
	    pprobe1 = split(pprobe)
	    part = call(pprobe1)

	def pvcreate(self):
	    '''This function creates the physical volume '''
	    pvcreate = call(["pvcreate", "/dev/%s1" %self.drive])

	def volgroup(self):
	    '''This function creates the physical volume and also created the volume group'''
	    vgcreate = 'vgcreate -v vg_%s /dev/%s1' % (basename(normpath(self.folder)), self.drive)
	    status,output = getstatusoutput(vgcreate)

	def lvm(self):
	    '''This function creates the logical volume'''
	    lvcreate ='lvcreate -v -l "100%FREE" -n lv_{0} vg_{1}' .format(basename(normpath(self.folder)), basename(normpath(self.folder)))
	    #lvcreate = 'lvcreate -v -l "100%FREE" -n lv_{0} vg_{1}' .format(self.folder, self.folder)
	    status,output = getstatusoutput(lvcreate)
	    print status
	    print output

	def makefs(self):
	    '''This functions creates the filesystem on the /dev/mapper LVM device'''
	    if self.fstype == 'ext4':
	    	mkfs = call(["mkfs.ext4", "/dev/mapper/vg_%s-lv_%s" % (basename(normpath(self.folder)),basename(normpath(self.folder)))])
	    elif self.fstype == 'xfs':
	    	mkfs = call(["mkfs.xfs", "/dev/mapper/vg_%s-lv_%s" % (basename(normpath(self.folder)),basename(normpath(self.folder)))])

	def makedir(self):
	    '''This function makes directory inthe /root level'''
	    path = "%s" %self.folder
	    mkdir( path, 0755 )
	    print '%s is created' %path

	def write_to_fstab(self):
	    '''This function appends the filesystem info to the /etc/fstab'''
	    if self.fstype == 'ext4':
		string = '/dev/mapper/vg_%s-lv_%s     %s           ext4    defaults        1 1' % (basename(normpath(self.folder)), basename(normpath(self.folder)), self.folder)
	    	f = open("/etc/fstab",'a')
	    	f.write(string + "\n")
	    	f.close()
	    elif self.fstype == 'xfs':
	    	string = '/dev/mapper/vg_%s-lv_%s     %s           xfs    defaults        1 1' % (basename(normpath(self.folder)), basename(normpath(self.folder)), self.folder)
	    	f = open("/etc/fstab",'a')
	    	f.write(string + "\n")
	    	f.close()

	def filesystem_mount(self):
	    '''This is a simple function to mount all the drive'''
	    fsmount = 'mount -a'
	    status,output = getstatusoutput(fsmount)

	def resizefs(self):
	    ''' This method is to resize an existing filesystem'''
	    if self.fstype == 'ext4':
		rs = 'resize2fs /dev/vg_%s/lv_%s' % (basename(normpath(self.folder)),basename(normpath(self.folder)))
		status,output = getstatusoutput(rs)
	    elif self.fstype == 'xfs':
		rs = 'xfs_growfs /dev/vg_%s/lv_%s' % (basename(normpath(self.folder)),basename(normpath(self.folder)))
		status,output = getstatusoutput(rs)

	def extend_vg(self):
	   '''Extending volume group'''
	   vgextend = 'vgextend vg_%s /dev/%s1'	% (basename(normpath(self.folder)), self.drive)
	   status,output = getstatusoutput(vgextend)

	def extend_lv(self):
	   '''Extending logical volume'''
	   lvextend = call(["lvextend", "-l", "+100%FREE", "/dev/vg_%s/lv_%s" % (basename(normpath(self.folder)),basename(normpath(self.folder)))])

def main():
	x = FormatDrive(opts.drive, opts.folder, opts.fstype)
	intake = raw_input("Do you want to extend of create a new filesystem ?")
	if intake == 'create':
	    print "a new drive has been created"
	    x.fdisk()
	    x.partprobe()
	    x.pvcreate()
	    time.sleep(5)
	    x.volgroup()
	    time.sleep(5)
	    x.lvm()
	    x.makefs()
	    x.makedir()
	    x.write_to_fstab()
	    x.filesystem_mount()
	if intake == 'extend':
	    print "a drive has been extended"
	    x.fdisk()
	    x.partprobe()
	    x.pvcreate()
	    x.extend_vg()
	    x.extend_lv()
	    x.resizefs()

if __name__ == '__main__':
	if opts.drive == None or opts.folder == None or opts.fstype == None:
		parser.print_help()
    		exit(-1)
	main()
  	print 'The root folder is %s' %opts.folder
  	print 'the drive is %s' %opts.drive
	print 'The fstype is %s' %opts.fstype
