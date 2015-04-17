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
#from sys import argv
from commands import getstatusoutput
from os import mkdir

parser = OptionParser()
parser.add_option('-d', '--drive', dest='drive', help='this is the name of the drive like sda, hdd etc..')
parser.add_option('-f', '--folder', dest='folder', help='this is the name of the directory')
(opts, args) = parser.parse_args()

def fdisk():
    '''This is a definition to perform fdisk the drive in the argument'''
    before_pipe_cmd = 'echo -e "n\np\n1\n\n\nt\\n8e\nw"'
    before_pipe_args = split(before_pipe_cmd)
    after_pipe_cmd = "fdisk /dev/%s" %opts.drive
    after_pipe_args = split(after_pipe_cmd)
    p1 = Popen(before_pipe_args, stdout=PIPE)
    p2 = call(after_pipe_args, stdin=p1.stdout)

def partprobe():
    '''This function performs the partprobe'''
    pprobe = "partprobe /dev/%s" %opts.drive
    pprobe1 = split(pprobe)
    part = call(pprobe1)

def volgroup():
    '''This function creates the physical volume and also created the volume group'''
    pvcreate = call(["pvcreate", "/dev/%s1" %opts.drive])
    vgcreate = 'vgcreate -v vg_%s /dev/%s1' % (opts.folder, opts.drive)
    status,output = getstatusoutput(vgcreate)
    
def lvm():
    '''This function creates the logical volume'''
    lvcreate = 'lvcreate -v -l "100%FREE" -n lv_{0} vg_{1}' .format(opts.folder, opts.folder)
    status,output = getstatusoutput(lvcreate)

def makefs():
    '''This functions creates the ext4 filesystem on the /dev/mapper LVM device'''
    mkfs = call(["mkfs.ext4", "/dev/mapper/vg_%s-lv_%s" %(opts.folder, opts.folder)])

def makedir():
    '''This function makes directory inthe /root level'''
    path = "/%s" %opts.folder
    mkdir( path, 0755 )
    print '%s is created' %path

def write_to_fstab():
    '''This function appends the filesystem info to the /etc/fstab'''
    string = '/dev/mapper/vg_%s-lv_%s     /%s           ext4    defaults        1 1' %(opts.folder,opts.folder,opts.folder)
    f = open("/etc/fstab",'a')
    f.write(string + "\n")
    f.close()

def filesystem_mount():
    '''This is a simple function to mount all the drive'''
    fsmount = 'mount -a'
    status,output = getstatusoutput(fsmount)

if __name__ == '__main__':

   if opts.drive == None or opts.folder == None:
      parser.print_help()
      exit(-1)
   print 'The root folder is /%s' %opts.folder
   print 'the drive is %s' %opts.drive
   #fdisk()
   #partprobe()
   #volgroup()
   #lvm()
   #makefs()
   #makedir()
   #write_to_fstab()
   #filesystem_mount()
